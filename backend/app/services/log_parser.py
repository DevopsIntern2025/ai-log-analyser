import re
from datetime import datetime


LOG_PATTERN = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} "
    r"\d{2}:\d{2}:\d{2})\s+"
    r"(?P<level>INFO|WARN|WARNING|ERROR|DEBUG|CRITICAL)"
    r"\s+(?P<message>.*)$"
)


def parse_log_line(line: str) -> dict | None:
    line = line.strip()

    if not line:
        return None

    match = LOG_PATTERN.match(line)

    if not match:
        return None

    timestamp_text = match.group("timestamp")

    try:
        timestamp = datetime.strptime(
            timestamp_text,
            "%Y-%m-%d %H:%M:%S",
        )
    except ValueError:
        return None

    return {
        "timestamp": timestamp,
        "level": match.group("level"),
        "message": match.group("message"),
    }
def parse_log_content(content: str) -> list[dict]:
    parsed_logs = []

    for line in content.splitlines():
        parsed_line = parse_log_line(line)

        if parsed_line:
            parsed_logs.append(parsed_line)

    return parsed_logs