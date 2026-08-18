from typing import Any


def build_log_analysis_prompt(
    logs: list[dict[str, Any]],
) -> str:

    log_lines = []

    for log in logs:
        timestamp = log["timestamp"]
        level = log["level"]
        message = log["message"]

        log_lines.append(
            f"[{timestamp}] {level}: {message}"
        )

    formatted_logs = "\n".join(log_lines)

    prompt = f"""
You are an expert DevOps incident analysis assistant.

Analyze the following application logs.

Your task is to identify:
1. The overall problem
2. Severity
3. Likely root cause
4. Evidence from the logs
5. Recommended remediation steps
6. Potential risks if the issue is not fixed

Rules:
- Base your analysis only on the provided logs.
- Do not invent facts that are not supported by the logs.
- Clearly distinguish evidence from assumptions.
- Focus on actionable recommendations.
- If the logs do not provide enough information to determine the root cause, say so.

Logs:
--------------------
{formatted_logs}
--------------------

Provide a concise DevOps-focused analysis.
"""

    return prompt.strip()

def filter_relevant_logs(
    logs: list[dict[str, Any]],
) -> list[dict[str, Any]]:

    relevant_levels = {
        "ERROR",
        "WARN",
        "WARNING",
        "CRITICAL",
    }

    return [
        log
        for log in logs
        if log["level"] in relevant_levels
    ]


def build_analysis_prompt(
    logs: list[dict[str, Any]],
) -> str:

    relevant_logs = filter_relevant_logs(logs)

    if not relevant_logs:
        return (
            "No ERROR, WARN, WARNING, or CRITICAL "
            "events were found in the provided logs."
        )

    return build_log_analysis_prompt(
        relevant_logs
    )