"""Shortest Job First non-preemptive CPU scheduling."""

import sys
from pathlib import Path


def shortest_job_first(processes):
    """Return non-preemptive SJF scheduling results."""
    remaining = [dict(process) for process in processes]
    current_time = 0
    completed = []

    while remaining:
        ready = [
            process for process in remaining if process["arrival_time"] <= current_time
        ]

        if not ready:
            current_time = min(process["arrival_time"] for process in remaining)
            ready = [
                process for process in remaining if process["arrival_time"] <= current_time
            ]

        selected = min(
            ready,
            key=lambda item: (item["burst_time"], item["arrival_time"], item["pid"]),
        )
        start_time = current_time
        completion_time = start_time + selected["burst_time"]
        turnaround_time = completion_time - selected["arrival_time"]
        waiting_time = turnaround_time - selected["burst_time"]

        completed.append(
            {
                "pid": selected["pid"],
                "arrival_time": selected["arrival_time"],
                "burst_time": selected["burst_time"],
                "start_time": start_time,
                "completion_time": completion_time,
                "turnaround_time": turnaround_time,
                "waiting_time": waiting_time,
            }
        )

        current_time = completion_time
        remaining.remove(selected)

    return sorted(completed, key=lambda item: item["pid"])


def main():
    """Display SJF results when this file is run directly."""
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    from run_all import INPUT_FILE, format_table, parse_input

    data = parse_input(INPUT_FILE)
    print(format_table("Shortest Job First (Non-Preemptive)", shortest_job_first(data["processes"])))


if __name__ == "__main__":
    main()
