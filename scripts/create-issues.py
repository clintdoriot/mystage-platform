#!/usr/bin/env python3
"""
Create GitHub issues from issues.json file across multiple repositories.

Usage:
    python scripts/create-issues.py initiatives/[initiative-name]/issues.json

This script will:
1. Create the milestone in each affected repository (if it doesn't exist)
2. Create each issue in its designated repository with the milestone assigned
3. Add each issue to the common GitHub Project (default: #3)
4. Print a summary of created issues

The script runs with a single confirmation at the start, then creates all issues
in batch without prompting for each one.

Multi-repo support:
- Each issue specifies which repository it belongs to
- The same milestone name is created in all affected repositories
- All issues are added to a single GitHub Project for unified tracking
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


def milestone_exists(repo, milestone_name):
    """Check if milestone exists in repo."""
    try:
        cmd = f'gh api repos/{repo}/milestones --jq \'.[] | select(.title=="{milestone_name}") | .number\''
        result = run_command(cmd)
        return bool(result)
    except:
        return False


def create_milestone(repo, milestone_name, description):
    """Create milestone in repo."""
    print(f"📌 Creating milestone '{milestone_name}' in {repo}...")
    cmd = f'gh milestone create "{milestone_name}" --repo {repo} --description "{description}"'
    run_command(cmd, capture=False)
    print(f"✅ Milestone created\n")


def create_issue(repo, title, body, milestone):
    """Create issue and return issue URL."""
    # Escape double quotes and newlines for shell command
    title_escaped = title.replace('"', '\\"')
    body_escaped = body.replace('"', '\\"').replace('\n', '\\n')

    cmd = f'gh issue create --repo {repo} --title "{title_escaped}" --body "{body_escaped}" --milestone "{milestone}" --json url --jq .url'

    return run_command(cmd)


def add_to_project(project_number, project_owner, issue_url):
    """Add issue to GitHub project."""
    cmd = f'gh project item-add {project_number} --owner {project_owner} --url "{issue_url}"'
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
    required_fields = ["initiative", "milestone", "project_number", "project_owner", "issues"]
    for field in required_fields:
        if field not in data:
            print(f"❌ Error: Missing required field '{field}' in JSON")
            sys.exit(1)

    initiative = data["initiative"]
    milestone = data["milestone"]
    project_number = data["project_number"]
    project_owner = data["project_owner"]
    issues = data["issues"]

    # Validate each issue has a repository field
    for i, issue in enumerate(issues, 1):
        if "repository" not in issue:
            print(f"❌ Error: Issue {i} missing 'repository' field")
            sys.exit(1)

    # Get list of unique repositories
    repositories = sorted(set(issue["repository"] for issue in issues))

    # Count issues per repository
    repo_counts = {}
    for repo in repositories:
        repo_counts[repo] = sum(1 for issue in issues if issue["repository"] == repo)

    # Print summary
    print(f"\n{'='*70}")
    print(f"🚀 Creating GitHub Issues")
    print(f"{'='*70}")
    print(f"Initiative:       {initiative}")
    print(f"Milestone:        {milestone}")
    print(f"Project:          #{project_number} (@{project_owner})")
    print(f"Total Issues:     {len(issues)}")
    print(f"\nRepositories:")
    for repo in repositories:
        print(f"  • {repo}: {repo_counts[repo]} issue(s)")
    print(f"{'='*70}\n")

    # Confirmation
    response = input("Create these issues? [y/N]: ").strip().lower()
    if response != 'y':
        print("❌ Aborted")
        sys.exit(0)

    print()

    # Create milestones in each repository (if they don't exist)
    print(f"📌 Setting up milestones...\n")
    for repo in repositories:
        if not milestone_exists(repo, milestone):
            create_milestone(repo, milestone, f"Issues for {initiative} initiative")
        else:
            print(f"✅ Milestone '{milestone}' already exists in {repo}\n")

    # Create issues
    created_issues = []
    failed_issues = []

    print(f"📝 Creating issues...\n")

    for i, issue in enumerate(issues, 1):
        repo = issue.get("repository", "")
        title = issue.get("title", "")
        body = issue.get("body", "")

        if not title:
            print(f"⚠️  Skipping issue {i}: Missing title")
            continue

        if not repo:
            print(f"⚠️  Skipping issue {i}: Missing repository")
            failed_issues.append(title)
            continue

        print(f"[{i}/{len(issues)}] {repo}")
        print(f"  Creating: {title}")

        try:
            # Create issue
            issue_url = create_issue(repo, title, body, milestone)
            print(f"  ✅ Created: {issue_url}")

            # Add to project
            print(f"  📋 Adding to project #{project_number}...")
            add_to_project(project_number, project_owner, issue_url)
            print(f"  ✅ Added to project\n")

            created_issues.append({
                "repository": repo,
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
            print(f"  • [{issue['repository'].split('/')[-1]}] {issue['title']}")
            print(f"    {issue['url']}")
        print()

    if failed_issues:
        print("Failed issues:")
        for title in failed_issues:
            print(f"  • {title}")
        print()

    print(f"📍 View milestones:")
    for repo in repositories:
        print(f"  • {repo}: https://github.com/{repo}/milestone")
    print(f"\n📋 View all issues in project: https://github.com/users/{project_owner}/projects/{project_number}\n")

    if failed_issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
