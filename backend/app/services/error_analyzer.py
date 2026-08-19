from collections import Counter


ERROR_LEVELS = {
    "ERROR",
    "CRITICAL",
    "FATAL",
}


ERROR_KEYWORDS = [
    "exception",
    "timeout",
    "timed out",
    "connection refused",
    "connection failed",
    "database error",
    "out of memory",
    "oom",
    "failed",
    "failure",
    "http 500",
    "http 502",
    "http 503",
    "http 504",
]


def analyze_errors(logs: list[dict]) -> dict:
    error_logs = []
    warning_logs = []

    for log in logs:
        level = str(log.get("level", "")).upper()
        message = str(log.get("message", "")).lower()

        if level in ERROR_LEVELS:
            error_logs.append(log)

        elif level == "WARN":
            warning_logs.append(log)

        elif any(
            keyword in message
            for keyword in ERROR_KEYWORDS
        ):
            error_logs.append(log)

    error_messages = [
        log.get("message", "")
        for log in error_logs
    ]

    message_counts = Counter(error_messages)

    return {
        "total_logs": len(logs),
        "error_count": len(error_logs),
        "warning_count": len(warning_logs),
        "error_logs": error_logs,
        "warning_logs": warning_logs,
        "top_errors": [
            {
                "message": message,
                "count": count,
            }
            for message, count in message_counts.most_common(10)
        ],
    }