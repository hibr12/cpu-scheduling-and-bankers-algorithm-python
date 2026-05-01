"""Shortest Remaining Time First preemptive CPU scheduling."""

import sys
from pathlib import Path


def shortest_remaining_time_first(processes):
    """Return preemptive SJF/SRTF scheduling results.

    The simulation advances one time unit at a time so the preemption logic is
    easy to compare with an interactive JavaScript simulator.
    """
    remaining_time = {process["pid"]: process["burst_time"] for process in processes}
    process_map = {process["pid"]: process for process in processes}
    completion_times = {}
    start_times = {}
    current_time = 0

    while len(completion_times) < len(processes):
        ready = [
            process
            for process in processes
            if process["arrival_time"] <= current_time
            and remaining_time[process["pid"]] > 0
        ]

        if not ready:
            current_time = min(
                process["arrival_time"]
                for process in processes
                if remaining_time[process["pid"]] > 0
            )
            continue

        selected = min(
            ready,
            key=lambda item: (
                remaining_time[item["pid"]],
                item["arrival_time"],
                item["pid"],
            ),
        )

        if selected["pid"] not in start_times:
            start_times[selected["pid"]] = current_time

        remaining_time[selected["pid"]] -= 1
        current_time += 1

        if remaining_time[selected["pid"]] == 0:
            completion_times[selected["pid"]] = current_time

    results = []
    for pid in sorted(process_map):
        process = process_map[pid]
        completion_time = completion_times[pid]
        turnaround_time = completion_time - process["arrival_time"]
        waiting_time = turnaround_time - process["burst_time"]
        results.append(
            {
                "pid": pid,
                "arrival_time": process["arrival_time"],
                "burst_time": process["burst_time"],
                "start_time": start_times[pid],
                "completion_time": completion_time,
                "turnaround_time": turnaround_time,
                "waiting_time": waiting_time,
            }
        )

    return results


def main():
    """Display SRTF results when this file is run directly."""
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    from run_all import INPUT_FILE, format_table, parse_input

    data = parse_input(INPUT_FILE)
    print(
        format_table(
            "Shortest Remaining Time First (Preemptive)",
            shortest_remaining_time_first(data["processes"]),
        )
    )


if __name__ == "__main__":
    main()
