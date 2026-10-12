"""The evaluation's own scoring and merging: a report is only worth something if these are right."""
import pytest

from backend.eval.run_eval import combine, has_fact, summarize

E204 = ["overheat", "exceeded 70", "exceeds 70", "above 70", "over 70", "more than 70", "higher than 70"]


def test_a_fact_may_be_worded_differently_but_a_different_value_is_not_the_fact():
    assert has_fact("Alarm E-204: spindle overheating.", E204)
    assert has_fact("It means the spindle temperature has exceeded 70 degrees C [1].", E204)
    # The wrong temperature, or the right number meaning something else, does not pass
    assert not has_fact("It means the spindle temperature has exceeded 80 degrees C [1].", E204)
    assert not has_fact("It means the spindle temperature has exceeded 170 degrees C [1].", E204)
    assert not has_fact("Do not restart until the temperature is below 70 degrees C.", E204)


def test_a_number_must_stand_alone():
    assert has_fact("Wait 5 minutes.", "5") and has_fact("between 22-28 bar", "28") and has_fact("It is 2000.", "2000")
    assert not has_fact("Wait 15 minutes.", "5")
    assert not has_fact("Every 12000 hours.", "2000")
    assert not has_fact("Set it to 2.5 bar.", "5") and not has_fact("Set it to 5.5 bar.", "5")
    assert has_fact("Use iso vg 32 oil.", "ISO VG 32") and not has_fact("Use ISO VG 320 oil.", "ISO VG 32")


def run(model, rows, embedding="gemini-embedding-001", k=6):
    return {"summary": {"generation_model": model, "embedding_model": embedding, "retrieval_k": k}, "rows": rows}


def answered(qid, answer="Wait 10 minutes [1].", **extra):
    return {"id": qid, "kind": "direct", "question": "?", "latency_s": 1.0, "answer": answer, "abstention_ok": True, **extra}


def failed(qid):
    return {"id": qid, "kind": "direct", "question": "?", "latency_s": 0.2, "error": "429: quota"}


def test_merging_keeps_every_question_once_and_an_error_never_replaces_an_answer():
    first = run("gemini-2.5-flash", [answered("q01", "first"), failed("q02"), failed("q03")])
    second = run("gemini-2.5-flash", [failed("q01"), answered("q02", "second"), failed("q03"), answered("q04", "second")])

    rows = combine([first, second], [])
    assert [r["id"] for r in rows] == ["q01", "q02", "q03", "q04"]
    by_id = {r["id"]: r for r in rows}
    # q01 was answered in the first run: the later quota error does not overwrite it
    assert by_id["q01"]["answer"] == "first" and "error" not in by_id["q01"]
    assert by_id["q02"]["answer"] == "second"
    # Still unanswered after both runs: it stays an error and is counted as one
    assert "error" in by_id["q03"]
    summary = summarize(rows, "gemini-embedding-001", 6, "gemini-2.5-flash")
    assert summary["questions"] == 4 and summary["model_errors"] == 1

    # An answer is not replaced by a later answer either: the order of the files decides
    again = combine([first, run("gemini-2.5-flash", [answered("q01", "later")])], [])
    assert {r["id"]: r for r in again}["q01"]["answer"] == "first"
    # The inputs are left as they were
    assert first["rows"][0]["answer"] == "first" and "facts_ok" not in first["rows"][0]


def test_runs_of_different_models_or_settings_are_not_one_benchmark():
    flash = run("gemini-2.5-flash", [answered("q01")])
    with pytest.raises(SystemExit, match="generation_model"):
        combine([flash, run("gemini-2.5-flash-lite", [answered("q02")])], [])
    with pytest.raises(SystemExit, match="retrieval_k"):
        combine([flash, run("gemini-2.5-flash", [answered("q02")], k=3)], [])
    with pytest.raises(SystemExit, match="embedding_model"):
        combine([flash, run("gemini-2.5-flash", [answered("q02")], embedding="other")], [])


def test_merging_scores_facts_again_with_the_current_labels():
    labels = [{"id": "q05", "must_include": [E204]}]
    old = run("gemini-2.5-flash", [answered("q05", "The spindle temperature has exceeded 70 degrees C [1].", facts_ok=False)])
    assert combine([old], labels)[0]["facts_ok"] is True
    wrong = run("gemini-2.5-flash", [answered("q05", "The spindle temperature has exceeded 90 degrees C [1].", facts_ok=True)])
    assert combine([wrong], labels)[0]["facts_ok"] is False
