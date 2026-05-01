"""Banker's Algorithm with safe-state and deadlock details."""

import sys
from pathlib import Path


def compute_need_matrix(allocation, maximum):
    """Return Max - Allocation for each process/resource cell."""
    return [
        [maximum[row][col] - allocation[row][col] for col in range(len(maximum[row]))]
        for row in range(len(maximum))
    ]


def bankers_algorithm(allocation, maximum, available, process_ids=None):
    """Evaluate whether a system is in a safe state.

    Args:
        allocation: matrix of allocated resources.
        maximum: matrix of maximum declared resource need.
        available: vector of currently available resources.
        process_ids: optional labels matching matrix rows.
    """
    process_count = len(allocation)
    resource_count = len(available)
    process_ids = process_ids or [f"P{index + 1}" for index in range(process_count)]
    need = compute_need_matrix(allocation, maximum)

    work = available[:]
    finish = [False] * process_count
    safe_sequence = []
    trace = []

    # Mirrors the JS simulator's safe-state loop: repeatedly find an unfinished
    # process whose Need row can be satisfied by the current Work vector.
    progress = True
    while progress:
        progress = False
        for index in range(process_count):
            if finish[index]:
                continue

            can_finish = all(need[index][res] <= work[res] for res in range(resource_count))
            if can_finish:
                before = work[:]
                work = [work[res] + allocation[index][res] for res in range(resource_count)]
                finish[index] = True
                safe_sequence.append(process_ids[index])
                trace.append(
                    {
                        "process": process_ids[index],
                        "work_before": before,
                        "released": allocation[index][:],
                        "work_after": work[:],
                    }
                )
                progress = True

    unfinished = [process_ids[index] for index, done in enumerate(finish) if not done]
    deadlock_details = []

    if unfinished:
        for index, done in enumerate(finish):
            if done:
                continue

            shortages = []
            for res in range(resource_count):
                shortage = max(0, need[index][res] - work[res])
                if shortage > 0:
                    shortages.append(
                        {
                            "resource": f"R{res + 1}",
                            "needed": need[index][res],
                            "available": work[res],
                            "shortage": shortage,
                        }
                    )

            deadlock_details.append(
                {
                    "process": process_ids[index],
                    "need": need[index][:],
                    "shortages": shortages,
                    "clues_to_fix": [
                        "Increase available resources for the short resources.",
                        "Terminate or roll back a blocked process to release allocation.",
                        "Reduce the process maximum claim if the declared max need is too high.",
                    ],
                }
            )

    return {
        "safe": not unfinished,
        "need": need,
        "safe_sequence": safe_sequence,
        "unfinished": unfinished,
        "final_work": work,
        "trace": trace,
        "deadlock_details": deadlock_details,
    }


def main():
    """Display Banker's Algorithm results when this file is run directly."""
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))

    from run_all import INPUT_FILE, format_bankers, parse_input

    data = parse_input(INPUT_FILE)
    process_ids = [f"P{process['pid']}" for process in data["processes"]]
    result = bankers_algorithm(
        data["allocation"],
        data["maximum"],
        data["available"],
        process_ids=process_ids,
    )
    print(format_bankers(result))


if __name__ == "__main__":
    main()
