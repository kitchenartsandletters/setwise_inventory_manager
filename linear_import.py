import csv
import os
import requests

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
LINEAR_API_URL = "https://api.linear.app/graphql"

HEADERS = {
    "Authorization": LINEAR_API_KEY,
    "Content-Type": "application/json"
}

def get_team_id():
    query = {
        "query": """
        query {
          teams {
            nodes {
              id
              name
            }
          }
        }
        """
    }
    response = requests.post(LINEAR_API_URL, json=query, headers=HEADERS)
    response.raise_for_status()
    teams = response.json()["data"]["teams"]["nodes"]
    for team in teams:
        print(f"Team Name: {team['name']}, ID: {team['id']}")
    return teams

def create_issue(team_id, title, description):
    mutation = {
        "query": """
        mutation CreateIssue($input: IssueCreateInput!) {
          issueCreate(input: $input) {
            success
            issue {
              id
              title
            }
          }
        }
        """,
        "variables": {
            "input": {
                "teamId": team_id,
                "title": title,
                "description": description
            }
        }
    }
    response = requests.post(LINEAR_API_URL, json=mutation, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    print(f"Issue created: {data['data']['issueCreate']['issue']['title']}")

def load_issues_from_csv(csv_path, team_id):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            create_issue(team_id, row['title'], row.get('description', ''))

if __name__ == "__main__":
    if not LINEAR_API_KEY:
        print("Missing LINEAR_API_KEY environment variable.")
        exit(1)

    print("Fetching team IDs...")
    teams = get_team_id()
    print("\nUse one of the IDs above when calling `load_issues_from_csv()` in future runs.\n")