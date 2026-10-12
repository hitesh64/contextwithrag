"""Generate realistic demo banking records (customers, accounts, transactions, loans, cards).

Self-contained synthetic data only -- nothing here touches a real bank or payment network.
Safe to re-run: skips seeding if customers already exist, unless --force is passed.

Usage:
    python -m backend.seed_banking_data --count 50
    python -m backend.seed_banking_data --count 50 --force
"""
import argparse
import random
from datetime import datetime, timedelta, timezone

from faker import Faker

from .config import settings
from .database import accounts, cards, customers, init_db, loans, transactions
from .routes_banking import emi, new_account_number, new_card_number, next_customer_code

fake = Faker("en_IN")


def _random_past(days_back: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(
        days=random.randint(0, days_back), seconds=random.randint(0, 86_399),
    )


def seed(count: int) -> None:
    for _ in range(count):
        branch = random.choice(settings.BRANCHES)
        customer = {
            "customer_code": next_customer_code(),
            "full_name": fake.name(),
            "email": fake.unique.email(),
            "phone": fake.msisdn()[:10],
            "address": fake.address().replace("\n", ", "),
            "branch_code": branch["code"],
            "kyc_status": random.choice(["verified", "verified", "verified", "pending"]),
            "created_at": _random_past(365),
        }
        customer["_id"] = customers.insert_one(customer).inserted_id

        for _ in range(random.randint(1, 2)):
            account_type = random.choice(settings.ACCOUNT_TYPES)
            opening_balance = round(random.uniform(5_000, 500_000), 2)
            account = {
                "account_number": new_account_number(),
                "customer_id": customer["_id"],
                "account_type": account_type,
                "balance": opening_balance,
                "currency": settings.CURRENCY,
                "status": "active",
                "branch_code": branch["code"],
                "created_at": customer["created_at"],
            }
            account["_id"] = accounts.insert_one(account).inserted_id

            balance = opening_balance
            for _ in range(random.randint(3, 20)):
                kind = random.choice(["deposit", "withdrawal"])
                amount = round(random.uniform(500, 20_000), 2)
                if kind == "withdrawal":
                    amount = min(amount, balance)
                    if amount <= 0:
                        continue
                    balance -= amount
                else:
                    balance += amount
                transactions.insert_one({
                    "account_id": account["_id"], "type": kind,
                    "direction": "credit" if kind == "deposit" else "debit",
                    "amount": amount, "to_account_id": None,
                    "balance_after": round(balance, 2), "description": fake.bs().capitalize(),
                    "created_at": _random_past(180), "created_by": "seed-script",
                })
            accounts.update_one({"_id": account["_id"]}, {"$set": {"balance": round(balance, 2)}})

            if random.random() < 0.3:
                now = datetime.now(timezone.utc)
                cards.insert_one({
                    "account_id": account["_id"], "card_type": random.choice(settings.CARD_TYPES),
                    "card_number": new_card_number(), "expiry": f"{now.month:02d}/{(now.year + 4) % 100:02d}",
                    "status": "active", "created_at": customer["created_at"],
                })

        if random.random() < 0.4:
            principal = round(random.uniform(50_000, 2_000_000), 2)
            rate = round(random.uniform(7.5, 14.5), 2)
            tenure = random.choice([12, 24, 36, 60, 84, 120, 180])
            loans.insert_one({
                "customer_id": customer["_id"], "loan_type": random.choice(settings.LOAN_TYPES),
                "principal": principal, "interest_rate": rate, "tenure_months": tenure,
                "emi": emi(principal, rate, tenure),
                "status": random.choice(["pending", "approved", "approved", "rejected", "closed"]),
                "created_at": customer["created_at"],
            })


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=50, help="Number of customers to generate")
    parser.add_argument("--force", action="store_true", help="Seed even if customers already exist")
    args = parser.parse_args()

    init_db()
    if customers.count_documents({}) > 0 and not args.force:
        print("Customers already exist -- skipping (pass --force to add more anyway).")
        return

    seed(args.count)
    print(f"Seeded {args.count} customers with accounts, transactions, loans and cards.")


if __name__ == "__main__":
    main()
