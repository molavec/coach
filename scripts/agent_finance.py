import sys
import os
import argparse
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core.repositories.finance_repo as finance_repo

def main():
    parser = argparse.ArgumentParser(description="CLI adapter for finance interactions")
    parser.add_argument("--action", required=True, help="The action to perform")
    
    parser.add_argument("--transaction_id", type=int)
    parser.add_argument("--date", type=str)
    parser.add_argument("--type", type=str)
    parser.add_argument("--amount", type=float)
    parser.add_argument("--currency", type=str, default="CLP")
    parser.add_argument("--account_id", type=int)
    parser.add_argument("--destination_account_id", type=int)
    parser.add_argument("--category_id", type=int)
    parser.add_argument("--description", type=str)
    parser.add_argument("--status", type=str, default="Completado")
    parser.add_argument("--is_recurring", type=int, default=0)
    
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--period", type=str)
    
    args = parser.parse_args()
    
    if args.action == "load_accounts":
        df = finance_repo.load_accounts()
        print(df.to_json(orient="records"))
    elif args.action == "load_categories":
        df = finance_repo.load_categories()
        print(df.to_json(orient="records"))
    elif args.action == "load_transactions":
        df = finance_repo.load_transactions(limit=args.limit)
        print(df.to_json(orient="records"))
    elif args.action == "load_pending_payments":
        df = finance_repo.load_pending_payments()
        print(df.to_json(orient="records"))
    elif args.action == "load_budgets_vs_actual":
        df = finance_repo.load_budgets_vs_actual(period=args.period)
        print(df.to_json(orient="records"))
    elif args.action == "load_cash_flow_monthly":
        df = finance_repo.load_cash_flow_monthly()
        print(df.to_json(orient="records"))
    elif args.action == "add_transaction":
        success, msg = finance_repo.add_transaction(
            args.date, args.type, args.amount, args.currency, 
            args.account_id, args.destination_account_id, 
            args.category_id, args.description, args.status, args.is_recurring
        )
        print(json.dumps({"success": success, "message": msg}))
    elif args.action == "delete_transaction":
        success, msg = finance_repo.delete_transaction(args.transaction_id)
        print(json.dumps({"success": success, "message": msg}))
    elif args.action == "update_transaction":
        success, msg = finance_repo.update_transaction(
            args.transaction_id, args.date, args.type, args.amount, args.currency, 
            args.account_id, args.destination_account_id, 
            args.category_id, args.description, args.status, args.is_recurring
        )
        print(json.dumps({"success": success, "message": msg}))
    else:
        print(json.dumps({"error": f"Unknown action: {args.action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
