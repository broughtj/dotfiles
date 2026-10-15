#!/usr/bin/env python3
"""
Sync TODO items to Todoist via REST API v1.

Usage:
    python sync-todoist.py [json-file] [--dry-run]

The json-file should contain an array of TODO items from parse-todos.py.
Use --dry-run to preview changes without creating/updating tasks.
"""

import json
import sys
import os
import hashlib
from pathlib import Path
from typing import List, Dict, Optional
import urllib.request
import urllib.error


class TodoistClient:
    """Client for Todoist REST API v1."""

    API_BASE = "https://api.todoist.com/rest/v2"

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

    def create_task(
        self,
        content: str,
        due_string: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: int = 1,
        labels: Optional[List[str]] = None,
        description: Optional[str] = None
    ) -> Dict:
        """Create a new task in Todoist."""
        url = f"{self.API_BASE}/tasks"

        # Build task data
        task_data = {
            "content": content,
            "priority": priority,
        }

        if due_string:
            task_data["due_string"] = due_string
        elif due_date:
            task_data["due_date"] = due_date

        if labels:
            task_data["labels"] = labels

        if description:
            task_data["description"] = description

        # Make request
        request = urllib.request.Request(
            url,
            data=json.dumps(task_data).encode('utf-8'),
            headers=self.headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code}: {error_body}")

    def update_task(
        self,
        task_id: str,
        content: Optional[str] = None,
        due_string: Optional[str] = None,
        due_date: Optional[str] = None,
        priority: Optional[int] = None,
        labels: Optional[List[str]] = None,
        description: Optional[str] = None
    ) -> Dict:
        """Update an existing task in Todoist."""
        url = f"{self.API_BASE}/tasks/{task_id}"

        # Build update data (only include fields that are provided)
        task_data = {}

        if content is not None:
            task_data["content"] = content
        if priority is not None:
            task_data["priority"] = priority
        if labels is not None:
            task_data["labels"] = labels
        if description is not None:
            task_data["description"] = description

        # Handle due dates
        if due_string is not None:
            task_data["due_string"] = due_string
        elif due_date is not None:
            task_data["due_date"] = due_date

        # Make request
        request = urllib.request.Request(
            url,
            data=json.dumps(task_data).encode('utf-8'),
            headers=self.headers,
            method='POST'
        )

        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code}: {error_body}")

    def get_task(self, task_id: str) -> Optional[Dict]:
        """Get a task by ID."""
        url = f"{self.API_BASE}/tasks/{task_id}"

        request = urllib.request.Request(
            url,
            headers=self.headers,
            method='GET'
        )

        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            error_body = e.read().decode('utf-8')
            raise Exception(f"HTTP {e.code}: {error_body}")


class SyncState:
    """Manages sync state to track created/updated tasks."""

    def __init__(self, state_file: str = ".todoist-sync-state.json"):
        self.state_file = state_file
        self.state = self._load_state()

    def _load_state(self) -> Dict:
        """Load sync state from file."""
        if not Path(self.state_file).exists():
            return {"tasks": {}}

        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load sync state: {e}", file=sys.stderr)
            return {"tasks": {}}

    def _save_state(self):
        """Save sync state to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save sync state: {e}", file=sys.stderr)

    def get_task_id(self, todo_hash: str) -> Optional[str]:
        """Get Todoist task ID for a given TODO hash."""
        return self.state.get("tasks", {}).get(todo_hash)

    def set_task_id(self, todo_hash: str, task_id: str):
        """Record a TODO to Todoist task mapping."""
        if "tasks" not in self.state:
            self.state["tasks"] = {}
        self.state["tasks"][todo_hash] = task_id
        self._save_state()

    @staticmethod
    def hash_todo(todo: Dict) -> str:
        """Generate a stable hash for a TODO item."""
        # Use source file and line number as unique identifier
        key = f"{todo['source_file']}:{todo['source_line']}:{todo['content']}"
        return hashlib.md5(key.encode('utf-8')).hexdigest()


class TodoistSyncer:
    """Syncs TODO items to Todoist."""

    def __init__(self, api_token: str, state_file: str = ".todoist-sync-state.json"):
        self.client = TodoistClient(api_token)
        self.state = SyncState(state_file)

    def sync_todos(self, todos: List[Dict], dry_run: bool = False) -> Dict:
        """Sync a list of TODO items to Todoist."""
        results = {
            "created": [],
            "updated": [],
            "skipped": [],
            "errors": []
        }

        for todo in todos:
            try:
                result = self._sync_single_todo(todo, dry_run)
                results[result["action"]].append({
                    "content": todo["content"],
                    "details": result.get("details", "")
                })
            except Exception as e:
                results["errors"].append({
                    "content": todo["content"],
                    "error": str(e)
                })

        return results

    def _sync_single_todo(self, todo: Dict, dry_run: bool) -> Dict:
        """Sync a single TODO item."""
        todo_hash = SyncState.hash_todo(todo)
        existing_task_id = self.state.get_task_id(todo_hash)

        # Build description with source location
        description = f"Source: {todo['source_file']}:{todo['source_line']}"

        if existing_task_id:
            # Check if task still exists
            if not dry_run:
                existing_task = self.client.get_task(existing_task_id)
                if not existing_task:
                    # Task was deleted, create new one
                    return self._create_task(todo, todo_hash, dry_run, description)

            # Update existing task
            if dry_run:
                return {
                    "action": "updated",
                    "details": f"Would update task {existing_task_id}"
                }

            self.client.update_task(
                task_id=existing_task_id,
                content=todo["content"],
                due_string=todo.get("due_string"),
                due_date=todo.get("due_date"),
                priority=todo["priority"],
                labels=todo.get("labels", []),
                description=description
            )

            return {
                "action": "updated",
                "details": f"Updated task {existing_task_id}"
            }
        else:
            # Create new task
            return self._create_task(todo, todo_hash, dry_run, description)

    def _create_task(self, todo: Dict, todo_hash: str, dry_run: bool, description: str) -> Dict:
        """Create a new Todoist task."""
        if dry_run:
            return {
                "action": "created",
                "details": "Would create new task"
            }

        result = self.client.create_task(
            content=todo["content"],
            due_string=todo.get("due_string"),
            due_date=todo.get("due_date"),
            priority=todo["priority"],
            labels=todo.get("labels", []),
            description=description
        )

        # Record the task ID in state
        self.state.set_task_id(todo_hash, result["id"])

        return {
            "action": "created",
            "details": f"Created task {result['id']}"
        }


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python sync-todoist.py [json-file] [--dry-run]", file=sys.stderr)
        sys.exit(1)

    json_file = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    # Load TODO items
    try:
        with open(json_file, 'r') as f:
            todos = json.load(f)
    except Exception as e:
        print(f"Error loading TODO items: {e}", file=sys.stderr)
        sys.exit(1)

    # Get API token from environment
    api_token = os.environ.get("TODOIST_API_TOKEN")
    if not api_token:
        # Try loading from .env file
        env_file = Path(__file__).parent.parent / ".env"
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("TODOIST_API_TOKEN="):
                            api_token = line.split("=", 1)[1].strip()
                            break
            except Exception as e:
                print(f"Error reading .env file: {e}", file=sys.stderr)

    if not api_token:
        print("Error: TODOIST_API_TOKEN not found", file=sys.stderr)
        print("Set it in ~/.claude/skills/todoist-sync/.env or as an environment variable", file=sys.stderr)
        sys.exit(1)

    # Perform sync
    syncer = TodoistSyncer(api_token)

    if dry_run:
        print("DRY RUN - No changes will be made", file=sys.stderr)

    results = syncer.sync_todos(todos, dry_run=dry_run)

    # Output results as JSON
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
