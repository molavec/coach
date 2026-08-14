import sys
import os
import argparse
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core.repositories.goals_repo as goals_repo

def main():
    parser = argparse.ArgumentParser(description="CLI adapter for goals interactions")
    parser.add_argument("--action", required=True, help="The action to perform")
    
    args = parser.parse_args()
    
    if args.action == "load_savings_goals":
        df = goals_repo.load_savings_goals()
        print(df.to_json(orient="records"))
    else:
        print(json.dumps({"error": f"Unknown action: {args.action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
