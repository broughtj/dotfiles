#!/usr/bin/env python3
"""
Parse calendar items from markdown files.

Usage:
    python parse-dates.py [markdown-file]

Output: JSON array of calendar items to stdout
"""

import re
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class CalendarItem:
    """Represents a calendar item extracted from markdown."""

    def __init__(
        self,
        item_type: str,
        title: str,
        date: str,
        time: Optional[str] = None,
        end_date: Optional[str] = None,
        alert: Optional[str] = None,
        recurrence: Optional[str] = None,
        location: Optional[str] = None,
        source_file: str = "",
        source_line: int = 0
    ):
        self.item_type = item_type
        self.title = title
        self.date = date
        self.time = time
        self.end_date = end_date
        self.alert = alert
        self.recurrence = recurrence
        self.location = location
        self.source_file = source_file
        self.source_line = source_line

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.item_type,
            "title": self.title,
            "date": self.date,
            "time": self.time,
            "end_date": self.end_date,
            "alert": self.alert,
            "recurrence": self.recurrence,
            "location": self.location,
            "source_file": self.source_file,
            "source_line": self.source_line
        }


class DateParser:
    """Extract calendar items from markdown text."""

    # Regex patterns for different item types
    PATTERNS = {
        # Hard deadlines
        "deadline_iso": re.compile(
            r'\*?\*?\s*(?:DUE|Deadline|Due):\s*(\d{4}-\d{2}-\d{2})(?:\s+(\d{1,2}:\d{2}))?\s*\*?\*?\s*(?:—|–|-)?\s*(.+?)(?:\n|$)',
            re.IGNORECASE
        ),
        "deadline_written": re.compile(
            r'\*?\*?\s*(?:DUE|Deadline|Due):\s*([A-Z][a-z]+\s+\d{1,2},\s+\d{4})(?:\s+at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?))?\s*\*?\*?\s*(?:—|–|-)?\s*(.+?)(?:\n|$)',
            re.IGNORECASE
        ),
        "submit_by": re.compile(
            r'\*?\*?\s*(?:Complete\s+by|Finish\s+by):\s*([A-Z][a-z]+\s+\d{1,2},?\s+\d{4}|\d{4}-\d{2}-\d{2})(?:\s+at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?))?\s*\*?\*?\s*(?:—|–|-)?\s*(.+?)(?:\n|$)',
            re.IGNORECASE
        ),

        # Milestones in task lists
        "milestone_checkbox": re.compile(
            r'-\s*\[\s*\]\s*(.+?)\s*\((?:by\s+)?(\d{4}-\d{2}-\d{2}|[A-Z][a-z]+\s+\d{1,2},?\s+\d{4})\)',
            re.IGNORECASE
        ),

        # Meetings
        "meeting_explicit": re.compile(
            r'\*?\*?\s*(?:Meeting|Call):\s*(.+?)\s+(\d{4}-\d{2}-\d{2}|[A-Z][a-z]+\s+\d{1,2},?\s+\d{4})\s+(?:at\s+)?(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)',
            re.IGNORECASE
        ),
        "meeting_recurring": re.compile(
            r'\*?\*?\s*(?:Weekly|Recurring\s+Meeting|Every):\s*(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s+(\d{1,2}:\d{2})\s*\*?\*?\s*(?:—|–|-)?\s*(.+?)(?:\n|$)',
            re.IGNORECASE
        ),

        # Conferences (date ranges)
        "conference_range": re.compile(
            r'(?:Conference|Event):\s*(.+?)\s*\((\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})\)',
            re.IGNORECASE
        ),
        "conference_written": re.compile(
            r'(?:Conference|Event):\s*(.+?)\s*\(([A-Z][a-z]+\s+\d{1,2})-(\d{1,2}),?\s+(\d{4})\)',
            re.IGNORECASE
        ),
    }

    @staticmethod
    def parse_file(file_path: str) -> List[CalendarItem]:
        """Parse a markdown file and extract all calendar items."""
        items = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}", file=sys.stderr)
            return items

        for line_num, line in enumerate(lines, start=1):
            # Try each pattern
            items.extend(DateParser._parse_deadlines(line, file_path, line_num))
            items.extend(DateParser._parse_milestones(line, file_path, line_num))
            items.extend(DateParser._parse_meetings(line, file_path, line_num))
            items.extend(DateParser._parse_conferences(line, file_path, line_num))

        return items

    @staticmethod
    def _parse_deadlines(line: str, source_file: str, line_num: int) -> List[CalendarItem]:
        """Extract deadline items from a line."""
        items = []

        # ISO format deadlines
        match = DateParser.PATTERNS["deadline_iso"].search(line)
        if match:
            date, time, title = match.groups()
            items.append(CalendarItem(
                item_type="deadline",
                title=title.strip(),
                date=date,
                time=time if time else "17:00",  # Default to 5pm
                alert="1 week before",
                source_file=source_file,
                source_line=line_num
            ))
            return items

        # Written format deadlines
        match = DateParser.PATTERNS["deadline_written"].search(line)
        if match:
            date_str, time, title = match.groups()
            date = DateParser._parse_written_date(date_str)
            items.append(CalendarItem(
                item_type="deadline",
                title=title.strip(),
                date=date,
                time=time if time else "17:00",
                alert="1 week before",
                source_file=source_file,
                source_line=line_num
            ))
            return items

        # "Complete by" / "Finish by" format
        match = DateParser.PATTERNS["submit_by"].search(line)
        if match:
            date_str, time, title = match.groups()
            if "-" in date_str:
                date = date_str
            else:
                date = DateParser._parse_written_date(date_str)

            items.append(CalendarItem(
                item_type="deadline",
                title=title.strip() if title else "Complete task",
                date=date,
                time=time if time else "17:00",
                alert="1 week before",
                source_file=source_file,
                source_line=line_num
            ))

        return items

    @staticmethod
    def _parse_milestones(line: str, source_file: str, line_num: int) -> List[CalendarItem]:
        """Extract milestone items from a line."""
        items = []

        match = DateParser.PATTERNS["milestone_checkbox"].search(line)
        if match:
            title, date_str = match.groups()

            if "-" in date_str:
                date = date_str
            else:
                date = DateParser._parse_written_date(date_str)

            items.append(CalendarItem(
                item_type="milestone",
                title=title.strip(),
                date=date,
                time="09:00",  # Default to 9am for milestones
                alert="1 day before",
                source_file=source_file,
                source_line=line_num
            ))

        return items

    @staticmethod
    def _parse_meetings(line: str, source_file: str, line_num: int) -> List[CalendarItem]:
        """Extract meeting items from a line."""
        items = []

        # Explicit meeting with date
        match = DateParser.PATTERNS["meeting_explicit"].search(line)
        if match:
            title, date_str, time = match.groups()

            if "-" in date_str:
                date = date_str
            else:
                date = DateParser._parse_written_date(date_str)

            # Clean time format
            time = DateParser._normalize_time(time)

            items.append(CalendarItem(
                item_type="meeting",
                title=title.strip(),
                date=date,
                time=time,
                alert="30 minutes before",
                source_file=source_file,
                source_line=line_num
            ))
            return items

        # Recurring meeting
        match = DateParser.PATTERNS["meeting_recurring"].search(line)
        if match:
            day, time, title = match.groups()
            time = DateParser._normalize_time(time)

            items.append(CalendarItem(
                item_type="meeting",
                title=title.strip(),
                date=day,  # Will be processed as "every Thursday"
                time=time,
                alert="30 minutes before",
                recurrence="weekly",
                source_file=source_file,
                source_line=line_num
            ))

        return items

    @staticmethod
    def _parse_conferences(line: str, source_file: str, line_num: int) -> List[CalendarItem]:
        """Extract conference items from a line."""
        items = []

        # ISO date range
        match = DateParser.PATTERNS["conference_range"].search(line)
        if match:
            title, start_date, end_date = match.groups()

            # Extract location if present
            location = None
            if "in " in title.lower():
                parts = title.rsplit(" in ", 1)
                if len(parts) == 2:
                    title, location = parts

            items.append(CalendarItem(
                item_type="conference",
                title=title.strip(),
                date=start_date,
                end_date=end_date,
                alert="1 month before",
                location=location,
                source_file=source_file,
                source_line=line_num
            ))
            return items

        # Written date range (e.g., "August 2-7, 2025")
        match = DateParser.PATTERNS["conference_written"].search(line)
        if match:
            title, month, end_day, year = match.groups()

            # This is approximate - Fantastical will handle it
            # We just need to provide something reasonable
            start_date = f"{year}-{DateParser._month_to_num(month):02d}-01"

            items.append(CalendarItem(
                item_type="conference",
                title=title.strip(),
                date=start_date,
                alert="1 month before",
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

            # If all parsing fails, return as-is (let Fantastical handle it)
            return date_str.strip()
        except Exception:
            return date_str.strip()

    @staticmethod
    def _normalize_time(time_str: str) -> str:
        """Convert time to 24-hour format."""
        try:
            time_str = time_str.strip().lower()

            # Already in HH:MM format
            if re.match(r'^\d{1,2}:\d{2}$', time_str):
                return time_str

            # Parse various formats
            for fmt in ["%I:%M%p", "%I:%M %p", "%I%p", "%I %p"]:
                try:
                    dt = datetime.strptime(time_str, fmt)
                    return dt.strftime("%H:%M")
                except ValueError:
                    continue

            # If parsing fails, return as-is
            return time_str
        except Exception:
            return time_str

    @staticmethod
    def _month_to_num(month_str: str) -> int:
        """Convert month name to number."""
        months = {
            "january": 1, "jan": 1,
            "february": 2, "feb": 2,
            "march": 3, "mar": 3,
            "april": 4, "apr": 4,
            "may": 5,
            "june": 6, "jun": 6,
            "july": 7, "jul": 7,
            "august": 8, "aug": 8,
            "september": 9, "sep": 9, "sept": 9,
            "october": 10, "oct": 10,
            "november": 11, "nov": 11,
            "december": 12, "dec": 12
        }
        return months.get(month_str.lower(), 1)


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python parse-dates.py [markdown-file]", file=sys.stderr)
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Parse the file
    parser = DateParser()
    items = parser.parse_file(file_path)

    # Convert to JSON and output
    items_dict = [item.to_dict() for item in items]
    print(json.dumps(items_dict, indent=2))


if __name__ == "__main__":
    main()
