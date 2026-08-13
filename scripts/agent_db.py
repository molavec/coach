import sys
import os
import argparse
import json

# Add project root to sys.path to allow importing from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core.db as db

def main():
    parser = argparse.ArgumentParser(description="CLI adapter for the agent to interact with coach.db")
    parser.add_argument("--action", required=True, help="The action to perform")
    
    # Arguments for add_transaction / update_transaction
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
    
    # Argument for load_transactions limit
    parser.add_argument("--limit", type=int, default=500)
    # Argument for budgets vs actual
    parser.add_argument("--period", type=str)
    # Argument for generic sql query execution
    parser.add_argument("--sql", type=str, help="Raw SQL query string for generic execution")
    
    args = parser.parse_args()
    
    if args.action == "load_accounts":
        df = db.load_accounts()
        print(df.to_json(orient="records"))
        
    elif args.action == "load_categories":
        df = db.load_categories()
        print(df.to_json(orient="records"))
        
    elif args.action == "load_transactions":
        df = db.load_transactions(limit=args.limit)
        print(df.to_json(orient="records"))
        
    elif args.action == "load_pending_payments":
        df = db.load_pending_payments()
        print(df.to_json(orient="records"))
        
    elif args.action == "load_savings_goals":
        df = db.load_savings_goals()
        print(df.to_json(orient="records"))
        
    elif args.action == "load_budgets_vs_actual":
        df = db.load_budgets_vs_actual(period=args.period)
        print(df.to_json(orient="records"))
        
    elif args.action == "load_cash_flow_monthly":
        df = db.load_cash_flow_monthly()
        print(df.to_json(orient="records"))
        
    elif args.action == "load_projects_and_tasks":
        projects_df, tasks_df = db.load_projects_and_tasks()
        result = {
            "projects": json.loads(projects_df.to_json(orient="records")),
            "tasks": json.loads(tasks_df.to_json(orient="records"))
        }
        print(json.dumps(result))
        
    elif args.action == "add_transaction":
        success, msg = db.add_transaction(
            args.date, args.type, args.amount, args.currency, 
            args.account_id, args.destination_account_id, 
            args.category_id, args.description, args.status, args.is_recurring
        )
        print(json.dumps({"success": success, "message": msg}))
        
    elif args.action == "delete_transaction":
        success, msg = db.delete_transaction(args.transaction_id)
        print(json.dumps({"success": success, "message": msg}))
        
    elif args.action == "update_transaction":
        success, msg = db.update_transaction(
            args.transaction_id, args.date, args.type, args.amount, args.currency, 
            args.account_id, args.destination_account_id, 
            args.category_id, args.description, args.status, args.is_recurring
        )
        print(json.dumps({"success": success, "message": msg}))
        
    elif args.action == "query":
        if not args.sql:
            print(json.dumps({"error": "--sql argument is required for query action"}))
            sys.exit(1)
        df = db.execute_read_query(args.sql)
        print(df.to_json(orient="records"))
        
    elif args.action == "execute":
        if not args.sql:
            print(json.dumps({"error": "--sql argument is required for execute action"}))
            sys.exit(1)
        success, msg = db.execute_write_query(args.sql)
        print(json.dumps({"success": success, "message": msg}))
        
    else:
        print(json.dumps({"error": f"Unknown action: {args.action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
