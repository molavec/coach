import sys
import os
import argparse
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core.repositories.base_repo as base_repo

def main():
    parser = argparse.ArgumentParser(description="CLI adapter for generic database query/execute operations")
    parser.add_argument("--action", required=True, help="The action to perform (query, execute)")
    parser.add_argument("--sql", type=str, help="Raw SQL query string for generic execution")
    
    args = parser.parse_args()
    
    if args.action == "query":
        if not args.sql:
            print(json.dumps({"error": "--sql argument is required for query action"}))
            sys.exit(1)
        df = base_repo.execute_read_query(args.sql)
        print(df.to_json(orient="records"))
        
    elif args.action == "execute":
        if not args.sql:
            print(json.dumps({"error": "--sql argument is required for execute action"}))
            sys.exit(1)
        success, msg = base_repo.execute_write_query(args.sql)
        print(json.dumps({"success": success, "message": msg}))
        
    else:
        print(json.dumps({"error": f"Unknown or deprecated action in agent_db.py: {args.action}. Check if it was moved to agent_finance.py, agent_productivity.py or agent_goals.py"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
