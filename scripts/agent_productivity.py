import sys
import os
import argparse
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import core.repositories.projects_repo as projects_repo

def main():
    parser = argparse.ArgumentParser(description="CLI adapter for productivity interactions")
    parser.add_argument("--action", required=True, help="The action to perform")
    
    args = parser.parse_args()
    
    if args.action == "load_projects_and_tasks":
        projects_df, tasks_df = projects_repo.load_projects_and_tasks()
        result = {
            "projects": json.loads(projects_df.to_json(orient="records")),
            "tasks": json.loads(tasks_df.to_json(orient="records"))
        }
        print(json.dumps(result))
    else:
        print(json.dumps({"error": f"Unknown action: {args.action}"}))
        sys.exit(1)

if __name__ == "__main__":
    main()
