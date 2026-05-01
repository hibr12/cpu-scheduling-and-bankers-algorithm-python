"""Round Robin CPU scheduling."""

import sys
from collections import deque
from pathlib import Path


def round_robin(processes, quantum=2):
    """Return Round Robin scheduling results."""
    if quantum <= 0:
        raise ValueError("Quantum must be greater than zero.")

    ordered = sorted(processes, key=lambda item: (item["arrival_time"], item["pid"]))
    remaining_time = {process["pid"]: process["burst_time"] for process in ordered}
    completion_times = {}
    start_times = {}
    current_time = 0
    index = 0
    queue = deque()

    while len(completion_times) < len(ordered):
        while index < len(ordered) and ordered[index]["arrival_time"] <= current_time:
            queue.append(ordered[index])
            index += 1

        if not queue:
            current_time = ordered[index]["arrival_time"]
            continue

        process = queue.popleft()
        pid = process["pid"]
        if pid not in start_times:
            start_times[pid] = current_time

        slice_time = min(quantum, remaining_time[pid])
        remaining_time[pid] -= slice_time
        current_time += slice_time

        while index < len(ordered) and ordered[index]["arrival_time"] <= current_time:
            queue.append(ordered[index])
            index += 1

        if remaining_time[pid] > 0:
            queue.append(process)
        else:
            completion_times[pid] = current_time

    process_map = {process["pid"]: process for process in ordered}
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
    """Display Round Robin results when this file is run directly."""
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    from run_all import INPUT_FILE, format_table, parse_input

    data = parse_input(INPUT_FILE)
    print(format_table("Round Robin (Quantum = 2)", round_robin(data["processes"], quantum=2)))


if __name__ == "__main__":
    main()
