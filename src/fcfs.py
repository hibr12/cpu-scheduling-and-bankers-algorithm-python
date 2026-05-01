"""First Come First Served CPU scheduling."""

import sys
from pathlib import Path


def first_come_first_served(processes):
    """Return FCFS scheduling results.

    Args:
        processes: list of dicts with pid, arrival_time, and burst_time.
    """
    ordered = sorted(processes, key=lambda item: (item["arrival_time"], item["pid"]))
    current_time = 0
    results = []

    for process in ordered:
        start_time = max(current_time, process["arrival_time"])
        completion_time = start_time + process["burst_time"]
        turnaround_time = completion_time - process["arrival_time"]
        waiting_time = turnaround_time - process["burst_time"]

        results.append(
            {
                "pid": process["pid"],
                "arrival_time": process["arrival_time"],
                "burst_time": process["burst_time"],
                "start_time": start_time,
                "completion_time": completion_time,
                "turnaround_time": turnaround_time,
                "waiting_time": waiting_time,
            }
        )
        current_time = completion_time

    return sorted(results, key=lambda item: item["pid"])


def main():
    """Display FCFS results when this file is run directly."""
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    from run_all import INPUT_FILE, format_table, parse_input

    data = parse_input(INPUT_FILE)
    print(format_table("First Come First Served (FCFS)", first_come_first_served(data["processes"])))


if __name__ == "__main__":
    main()
