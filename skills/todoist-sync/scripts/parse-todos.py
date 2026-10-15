#!/usr/bin/env python3
"""
Parse TODO items from markdown files.

Usage:
    python parse-todos.py [markdown-file]

Output: JSON array of TODO items to stdout
"""

import re
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class TodoItem:
    """Represents a TODO item extracted from markdown."""

    def __init__(
        self,
        item_type: str,
        content: str,
        due_date: Optional[str] = None,
        due_string: Optional[str] = None,
        priority: int = 4,
        labels: List[str] = None,
        source_file: str = "",
        source_line: int = 0
    ):
        self.item_type = item_type
        self.content = content
        self.due_date = due_date
        self.due_string = due_string
        self.priority = priority
        self.labels = labels or []
        self.source_file = source_file
        self.source_line = source_line

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.item_type,
            "content": self.content,
            "due_date": self.due_date,
            "due_string": self.due_string,
            "priority": self.priority,
            "labels": self.labels,
            "source_file": self.source_file,
            "source_line": self.source_line
        }


class TodoParser:
    """Extract TODO items from markdown text."""

    # Regex patterns for different item types
    PATTERNS = {
        # Hard deadlines with explicit DUE/Deadline markers
        "deadline_iso": re.compile(
            r'\*?\*?\s*(?:DUE|Deadline|Due):\s*(\d{4}-\d{2}-\d{2})(?:\s+(\d{1,2}:\d{2}))?\s*\*?\*?\s*(?:—|–|-)?\s*(.+?)(?:\n|$)',
            re.IGNORECASE
        ),
        "deadline_written": re.compile(
            r'\*?\*?\s*(?:DUE|Deadline|Due):\s*([A-Z][a-z]+\s+\d{1,2},\s+\d{4})(?:\s+at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?))?\s*\*?\*?\s*(?:—|–|-)?\s*(.+?)(?:\n|$)',
            re.IGNORECASE
        ),

        # TODO markers
        "todo_explicit": re.compile(
            r'-\s*\[\s*\]\s*(?:TODO:?\s*)(.+?)(?:\n|$)',
            re.IGNORECASE
        ),

        # Generic checkbox tasks (unchecked)
        "checkbox_task": re.compile(
            r'-\s*\[\s*\]\s*(.+?)(?:\n|$)'
        ),

        # Tasks with dates in parentheses
        "task_with_date_iso": re.compile(
            r'-\s*\[\s*\]\s*(.+?)\s*\((?:by\s+)?(\d{4}-\d{2}-\d{2})\)',
            re.IGNORECASE
        ),
        "task_with_date_written": re.compile(
            r'-\s*\[\s*\]\s*(.+?)\s*\((?:by\s+)?([A-Z][a-z]+\s+\d{1,2},?\s+\d{4})\)',
            re.IGNORECASE
        ),

        # Questions/issues to address (must have substantial content)
        "question_marker": re.compile(
            r'(?:\*\*)?(?:Question|Issue|Open Issue):?\s*(?:\*\*)?\s*(.{10,})(?:\n|$)',
            re.IGNORECASE
        ),
    }

    @staticmethod
    def parse_file(file_path: str) -> List[TodoItem]:
        """Parse a markdown file and extract all TODO items."""
        items = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            return items

        # Extract source file label
        file_label = TodoParser._file_to_label(file_path)

        # Track seen items to avoid duplicates
        seen_content = set()

        for line_num, line in enumerate(lines, start=1):
            # Skip empty lines and frontmatter
            if not line.strip() or line.strip() == '---':
                continue

            # Try each pattern
            new_items = []
            new_items.extend(TodoParser._parse_deadlines(line, file_path, line_num, file_label))
            new_items.extend(TodoParser._parse_todos(line, file_path, line_num, file_label))
            new_items.extend(TodoParser._parse_tasks_with_dates(line, file_path, line_num, file_label))
            new_items.extend(TodoParser._parse_checkbox_tasks(line, file_path, line_num, file_label))
            new_items.extend(TodoParser._parse_questions(line, file_path, line_num, file_label))

            # Add unique items only
            for item in new_items:
                key = (item.content.lower().strip(), item.due_date)
                if key not in seen_content:
                    seen_content.add(key)
                    items.append(item)

        return items

    @staticmethod
    def _parse_deadlines(line: str, source_file: str, line_num: int, file_label: str) -> List[TodoItem]:
        """Extract deadline items from a line."""
        items = []

        # ISO format deadlines
        match = TodoParser.PATTERNS["deadline_iso"].search(line)
        if match:
            date, time, content = match.groups()
            due_string = f"{date}"
            if time:
                due_string += f" {time}"

            items.append(TodoItem(
                item_type="deadline",
                content=content.strip(),
                due_date=date,
                due_string=due_string,
                priority=1,  # P1 for explicit deadlines
                labels=[file_label],
                source_file=source_file,
                source_line=line_num
            ))
            return items

        # Written format deadlines
        match = TodoParser.PATTERNS["deadline_written"].search(line)
        if match:
            date_str, time, content = match.groups()
            date_iso = TodoParser._parse_written_date(date_str)
            due_string = date_str
            if time:
                due_string += f" at {time}"

            items.append(TodoItem(
                item_type="deadline",
                content=content.strip(),
                due_date=date_iso if date_iso != date_str else None,
                due_string=due_string,
                priority=1,  # P1 for explicit deadlines
                labels=[file_label],
                source_file=source_file,
                source_line=line_num
            ))

        return items

    @staticmethod
    def _parse_todos(line: str, source_file: str, line_num: int, file_label: str) -> List[TodoItem]:
        """Extract explicit TODO items from a line."""
        items = []

        match = TodoParser.PATTERNS["todo_explicit"].search(line)
        if match:
            content = match.group(1).strip()

            items.append(TodoItem(
                item_type="todo",
                content=content,
                priority=4,  # P4 for regular TODOs
                labels=[file_label],
                source_file=source_file,
                source_line=line_num
            ))

        return items

    @staticmethod
    def _parse_tasks_with_dates(line: str, source_file: str, line_num: int, file_label: str) -> List[TodoItem]:
        """Extract tasks with dates in parentheses."""
        items = []

        # ISO format date
        match = TodoParser.PATTERNS["task_with_date_iso"].search(line)
        if match:
            content, date = match.groups()

            items.append(TodoItem(
                item_type="milestone",
                content=content.strip(),
                due_date=date,
                due_string=date,
                priority=4,  # P4 for milestones
                labels=[file_label],
                source_file=source_file,
                source_line=line_num
            ))
            return items

        # Written format date
        match = TodoParser.PATTERNS["task_with_date_written"].search(line)
        if match:
            content, date_str = match.groups()
            date_iso = TodoParser._parse_written_date(date_str)

            items.append(TodoItem(
                item_type="milestone",
                content=content.strip(),
                due_date=date_iso if date_iso != date_str else None,
                due_string=date_str,
                priority=4,  # P4 for milestones
                labels=[file_label],
                source_file=source_file,
                source_line=line_num
            ))

        return items

    @staticmethod
    def _parse_checkbox_tasks(line: str, source_file: str, line_num: int, file_label: str) -> List[TodoItem]:
        """Extract generic checkbox tasks (only if not already matched by other patterns)."""
        items = []

        # Skip if already matched by more specific patterns
        if any(pattern.search(line) for name, pattern in TodoParser.PATTERNS.items()
               if name not in ['checkbox_task']):
            return items

        match = TodoParser.PATTERNS["checkbox_task"].search(line)
        if match:
            content = match.group(1).strip()

            # Skip common false positives and TODO placeholders
            if (content.lower().startswith(('milestone', 'contribution', 'advantage', 'limitation')) or
                '[TODO' in content or
                content.startswith('[') or
                len(content) < 5):
                return items

            items.append(TodoItem(
                item_type="task",
                content=content,
                priority=4,  # P4 for regular tasks
                labels=[file_label],
                source_file=source_file,
                source_line=line_num
            ))

        return items

    @staticmethod
    def _parse_questions(line: str, source_file: str, line_num: int, file_label: str) -> List[TodoItem]:
        """Extract questions and open issues."""
        items = []

        # Skip markdown headers
        if line.strip().startswith('#'):
            return items

        match = TodoParser.PATTERNS["question_marker"].search(line)
        if match:
            content = match.group(1).strip()

            # Skip if content looks like a header anchor
            if content.startswith('{#') or content.endswith('}'):
                return items

            items.append(TodoItem(
                item_type="question",
                content=f"Question: {content}",
                priority=4,  # P4 for questions
                labels=[file_label, "question"],
                source_file=source_file,
                source_line=line_num
            ))

        return items

    @staticmethod
    def _parse_written_date(date_str: str) -> str:
        """Convert written date to ISO format."""
        try:
            # Try parsing common formats
            for fmt in ["%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%d %b %Y"]:
                try:
                    dt = datetime.strptime(date_str.strip(), fmt)
                    return dt.strftime("%Y-%m-%d")
                except ValueError:
                    continue

            # If all parsing fails, return as-is
            return date_str.strip()
        except Exception:
            return date_str.strip()

    @staticmethod
    def _file_to_label(file_path: str) -> str:
        """Convert file path to a label name."""
        # Get base filename without extension
        name = Path(file_path).stem

        # Remove common suffixes
        name = re.sub(r'_plan$', '', name)
        name = re.sub(r'_notes$', '', name)

        # Replace underscores with hyphens
        name = name.replace('_', '-')

        return name


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python parse-todos.py [markdown-file]", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Parse the file
    parser = TodoParser()
    items = parser.parse_file(file_path)

    # Convert to JSON and output
    items_dict = [item.to_dict() for item in items]
    print(json.dumps(items_dict, indent=2))


if __name__ == "__main__":
    main()
