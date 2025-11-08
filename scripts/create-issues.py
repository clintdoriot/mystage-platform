#!/usr/bin/env python3
"""
Create GitHub issues from issues.json file across multiple repositories.

Usage:
    python scripts/create-issues.py initiatives/[initiative-name]/issues.json

This script will:
1. Create each issue in its designated repository
2. Add each issue to the common GitHub Project (default: #3)
3. Set custom fields: Initiative, Team, Priority, Size
4. Print a summary of created issues

The script runs with a single confirmation at the start, then creates all issues
in batch without prompting for each one.

Multi-repo support:
- Each issue specifies which repository it belongs to
- All issues are added to a single GitHub Project for unified tracking
- Custom fields are set automatically from issues.json
"""

import json
import subprocess
import sys
from pathlib import Path


def run_command(cmd, capture=True):
    """Run shell command and return output."""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {cmd}")
        if capture and e.stderr:
            print(f"Error output: {e.stderr}")
        sys.exit(1)


def create_issue(repo, title, body):
    """Create issue and return issue URL and node ID."""
    # Escape double quotes and newlines for shell command
    title_escaped = title.replace('"', '\\"')
    body_escaped = body.replace('"', '\\"').replace('\n', '\\n')

    cmd = f'gh issue create --repo {repo} --title "{title_escaped}" --body "{body_escaped}" --json url,id --jq "{{url: .url, id: .id}}"'

    result = run_command(cmd)
    data = json.loads(result)
    return data['url'], data['id']


def add_to_project(project_number, project_owner, issue_url):
    """Add issue to GitHub project and return the project item ID."""
    cmd = f'gh project item-add {project_number} --owner {project_owner} --url "{issue_url}" --format json --jq .id'
    return run_command(cmd)


def get_project_id(project_number, project_owner):
    """Get the project node ID."""
    cmd = f'gh project view {project_number} --owner {project_owner} --format json --jq .id'
    return run_command(cmd)


def get_project_fields(project_id):
    """Get project field information including IDs and options."""
    query = """
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          fields(first: 20) {
            nodes {
              ... on ProjectV2Field {
                id
                name
              }
              ... on ProjectV2SingleSelectField {
                id
                name
                options {
                  id
                  name
                }
              }
            }
          }
        }
      }
    }
    """

    # Escape the query for shell
    query_escaped = query.replace('"', '\\"').replace('\n', ' ')
    cmd = f'gh api graphql -f query="{query_escaped}" -f projectId="{project_id}"'

    result = run_command(cmd)
    data = json.loads(result)

    fields = {}
    for field in data['data']['node']['fields']['nodes']:
        field_name = field['name']
        field_id = field['id']

        # Store field info
        fields[field_name] = {
            'id': field_id
        }

        # If it's a single select field, store the options
        if 'options' in field:
            fields[field_name]['options'] = {
                opt['name']: opt['id'] for opt in field['options']
            }

    return fields


def create_field_option(project_id, field_id, option_name):
    """Create a new option for a single select field."""
    mutation = """
    mutation($projectId: ID!, $fieldId: ID!, $optionName: String!) {
      addProjectV2SingleSelectFieldValue(input: {
        projectId: $projectId
        fieldId: $fieldId
        value: {name: $optionName}
      }) {
        option {
          id
          name
        }
      }
    }
    """

    mutation_escaped = mutation.replace('"', '\\"').replace('\n', ' ')
    cmd = f'gh api graphql -f query="{mutation_escaped}" -f projectId="{project_id}" -f fieldId="{field_id}" -f optionName="{option_name}"'

    result = run_command(cmd)
    data = json.loads(result)
    return data['data']['addProjectV2SingleSelectFieldValue']['option']['id']


def set_project_field(project_id, item_id, field_id, value_id):
    """Set a single select field value on a project item."""
    mutation = """
    mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $valueId: String!) {
      updateProjectV2ItemFieldValue(input: {
        projectId: $projectId
        itemId: $itemId
        fieldId: $fieldId
        value: {singleSelectOptionId: $valueId}
      }) {
        projectV2Item {
          id
        }
      }
    }
    """

    mutation_escaped = mutation.replace('"', '\\"').replace('\n', ' ')
    cmd = f'gh api graphql -f query="{mutation_escaped}" -f projectId="{project_id}" -f itemId="{item_id}" -f fieldId="{field_id}" -f valueId="{value_id}"'

    run_command(cmd, capture=False)


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/create-issues.py initiatives/[initiative-name]/issues.json")
        sys.exit(1)

    json_file = Path(sys.argv[1])

    if not json_file.exists():
        print(f"❌ Error: {json_file} not found")
        sys.exit(1)

    # Load issues.json
    try:
        with open(json_file) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON: {e}")
        sys.exit(1)

    # Validate required fields
    required_fields = ["initiative", "project_number", "project_owner", "issues"]
    for field in required_fields:
        if field not in data:
            print(f"❌ Error: Missing required field '{field}' in JSON")
            sys.exit(1)

    initiative = data["initiative"]
    project_number = data["project_number"]
    project_owner = data["project_owner"]
    issues = data["issues"]

    # Validate each issue has required fields
    for i, issue in enumerate(issues, 1):
        if "repository" not in issue:
            print(f"❌ Error: Issue {i} missing 'repository' field")
            sys.exit(1)
        if "team" not in issue:
            print(f"❌ Error: Issue {i} missing 'team' field")
            sys.exit(1)

    # Get list of unique repositories
    repositories = sorted(set(issue["repository"] for issue in issues))

    # Count issues per repository and team
    repo_counts = {}
    team_counts = {}
    for repo in repositories:
        repo_counts[repo] = sum(1 for issue in issues if issue["repository"] == repo)
    for issue in issues:
        team = issue.get("team", "Unknown")
        team_counts[team] = team_counts.get(team, 0) + 1

    # Print summary
    print(f"\n{'='*70}")
    print(f"🚀 Creating GitHub Issues")
    print(f"{'='*70}")
    print(f"Initiative:       {initiative}")
    print(f"Project:          #{project_number} (@{project_owner})")
    print(f"Total Issues:     {len(issues)}")
    print(f"\nRepositories:")
    for repo in repositories:
        print(f"  • {repo}: {repo_counts[repo]} issue(s)")
    print(f"\nTeams:")
    for team in sorted(team_counts.keys()):
        print(f"  • {team}: {team_counts[team]} issue(s)")
    print(f"{'='*70}\n")

    # Confirmation
    response = input("Create these issues? [y/N]: ").strip().lower()
    if response != 'y':
        print("❌ Aborted")
        sys.exit(0)

    print()

    # Get project ID and fields
    print(f"📋 Fetching project configuration...\n")
    project_id = get_project_id(project_number, project_owner)
    project_fields = get_project_fields(project_id)

    print(f"✅ Project fields configured:")
    for field_name in ['Initiative', 'Team', 'Priority', 'Size']:
        if field_name in project_fields:
            print(f"  • {field_name}: {len(project_fields[field_name].get('options', {}))} options")
        else:
            print(f"  ⚠️  {field_name}: Not found in project")
    print()

    # Create issues
    created_issues = []
    failed_issues = []

    print(f"📝 Creating issues...\n")

    for i, issue in enumerate(issues, 1):
        repo = issue.get("repository", "")
        team = issue.get("team", "")
        title = issue.get("title", "")
        body = issue.get("body", "")
        priority = issue.get("priority", "")
        size = issue.get("size", "")

        if not title:
            print(f"⚠️  Skipping issue {i}: Missing title")
            continue

        if not repo:
            print(f"⚠️  Skipping issue {i}: Missing repository")
            failed_issues.append(title)
            continue

        print(f"[{i}/{len(issues)}] {repo} - {team}")
        print(f"  Creating: {title}")

        try:
            # Create issue
            issue_url, issue_id = create_issue(repo, title, body)
            print(f"  ✅ Created: {issue_url}")

            # Add to project
            print(f"  📋 Adding to project #{project_number}...")
            item_id = add_to_project(project_number, project_owner, issue_url)
            print(f"  ✅ Added to project")

            # Set custom fields
            fields_set = []

            # Set Initiative field
            if 'Initiative' in project_fields:
                initiative_field = project_fields['Initiative']
                # Check if initiative value exists in options, if not create it
                if initiative in initiative_field.get('options', {}):
                    initiative_option_id = initiative_field['options'][initiative]
                else:
                    # Create the initiative option
                    initiative_option_id = create_field_option(project_id, initiative_field['id'], initiative)
                    # Update our local cache
                    if 'options' not in initiative_field:
                        initiative_field['options'] = {}
                    initiative_field['options'][initiative] = initiative_option_id

                set_project_field(project_id, item_id, initiative_field['id'], initiative_option_id)
                fields_set.append("Initiative")

            # Set Team field
            if 'Team' in project_fields and team:
                team_field = project_fields['Team']
                if team in team_field.get('options', {}):
                    team_option_id = team_field['options'][team]
                    set_project_field(project_id, item_id, team_field['id'], team_option_id)
                    fields_set.append("Team")

            # Set Priority field
            if 'Priority' in project_fields and priority:
                priority_field = project_fields['Priority']
                if priority in priority_field.get('options', {}):
                    priority_option_id = priority_field['options'][priority]
                    set_project_field(project_id, item_id, priority_field['id'], priority_option_id)
                    fields_set.append("Priority")

            # Set Size field
            if 'Size' in project_fields and size:
                size_field = project_fields['Size']
                if size in size_field.get('options', {}):
                    size_option_id = size_field['options'][size]
                    set_project_field(project_id, item_id, size_field['id'], size_option_id)
                    fields_set.append("Size")

            if fields_set:
                print(f"  ✅ Set fields: {', '.join(fields_set)}")
            print()

            created_issues.append({
                "repository": repo,
                "team": team,
                "title": title,
                "url": issue_url
            })

        except Exception as e:
            print(f"  ❌ Failed: {str(e)}\n")
            failed_issues.append(f"{title} ({repo})")

    # Print final summary
    print(f"\n{'='*70}")
    print(f"📊 Summary")
    print(f"{'='*70}")
    print(f"✅ Successfully created: {len(created_issues)} issues")
    if failed_issues:
        print(f"❌ Failed: {len(failed_issues)} issues")
    print(f"{'='*70}\n")

    if created_issues:
        print("Created issues:")
        for issue in created_issues:
            print(f"  • [{issue['team']}] [{issue['repository'].split('/')[-1]}] {issue['title']}")
            print(f"    {issue['url']}")
        print()

    if failed_issues:
        print("Failed issues:")
        for title in failed_issues:
            print(f"  • {title}")
        print()

    print(f"📋 View all issues in project: https://github.com/users/{project_owner}/projects/{project_number}")
    print(f"   Filter by: Initiative = \"{initiative}\"")
    print(f"   Group by: Team, Status, Priority, etc.\n")

    if failed_issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
