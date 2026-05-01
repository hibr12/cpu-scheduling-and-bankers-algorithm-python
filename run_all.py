"""Run every algorithm and write a combined output report.

This script is the Python equivalent of a JavaScript simulator's runAll()
function: parse inputs, validate values, run each algorithm, and build one
structured output.
"""

from pathlib import Path

from src.bankers import bankers_algorithm
from src.fcfs import first_come_first_served
from src.round_robin import round_robin
from src.sjf import shortest_job_first
from src.srtf import shortest_remaining_time_first


ROOT = Path(__file__).resolve().parent
INPUT_FILE = ROOT / "input" / "sample_input.txt"
OUTPUT_FILE = ROOT / "output" / "sample_output.txt"


def parse_non_negative_int(value, label):
    """Validate one numeric cell, like JS form validation for each input box."""
    stripped = value.strip()
    if stripped == "":
        raise ValueError(f"{label} cannot be empty.")
    try:
        number = int(stripped)
    except ValueError as exc:
        raise ValueError(f"{label} must be a whole number, not NaN.") from exc
    if number < 0:
        raise ValueError(f"{label} cannot be negative.")
    return number


def read_sections(path):
    sections = {}
    current = None

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current = line[1:-1].strip().upper()
            sections[current] = []
            continue
        if current is None:
            raise ValueError(f"Line {line_number}: data appears before a section header.")
        sections[current].append((line_number, line))

    return sections


def parse_processes(lines):
    processes = []
    seen_pids = set()

    for line_number, line in lines:
        parts = [part.strip() for part in line.split(",")]
        if len(parts) != 3:
            raise ValueError(f"Line {line_number}: process row must be PID, Arrival, Burst.")

        pid = parse_non_negative_int(parts[0], f"PID on line {line_number}")
        arrival = parse_non_negative_int(parts[1], f"Arrival Time for P{pid}")
        burst = parse_non_negative_int(parts[2], f"Burst Time for P{pid}")
        if burst == 0:
            raise ValueError(f"Burst Time for P{pid} must be greater than zero.")
        if pid in seen_pids:
            raise ValueError(f"PID {pid} is duplicated.")

        seen_pids.add(pid)
        processes.append({"pid": pid, "arrival_time": arrival, "burst_time": burst})

    if not processes:
        raise ValueError("At least one process is required.")
    return sorted(processes, key=lambda item: item["pid"])


def parse_matrix(lines, name, resource_count=None):
    matrix = []

    for row_index, (line_number, line) in enumerate(lines, 1):
        parts = [part.strip() for part in line.split(",")]
        if resource_count is not None and len(parts) != resource_count:
            raise ValueError(
                f"Line {line_number}: {name} row must contain {resource_count} values."
            )
        row = [
            parse_non_negative_int(value, f"{name} P{row_index} R{col_index + 1}")
            for col_index, value in enumerate(parts)
        ]
        matrix.append(row)

    if not matrix:
        raise ValueError(f"{name} matrix cannot be empty.")
    return matrix


def parse_vector(lines):
    if len(lines) != 1:
        raise ValueError("Available vector must be exactly one row.")
    line_number, line = lines[0]
    parts = [part.strip() for part in line.split(",")]
    return [
        parse_non_negative_int(value, f"Avail R{index + 1}")
        for index, value in enumerate(parts)
    ]


def parse_input(path):
    sections = read_sections(path)
    required = {"PROCESSES", "ALLOCATION", "MAX", "AVAILABLE"}
    missing = sorted(required - set(sections))
    if missing:
        raise ValueError(f"Missing required section(s): {', '.join(missing)}.")

    processes = parse_processes(sections["PROCESSES"])
    available = parse_vector(sections["AVAILABLE"])
    allocation = parse_matrix(sections["ALLOCATION"], "Alloc", len(available))
    maximum = parse_matrix(sections["MAX"], "Max", len(available))

    if len(allocation) != len(maximum):
        raise ValueError("Allocation and Max matrices must have the same row count.")
    if len(allocation) != len(processes):
        raise ValueError("Banker's matrix row count must match the number of processes.")

    for row_index, row in enumerate(allocation):
        for col_index, allocated in enumerate(row):
            max_claim = maximum[row_index][col_index]
            if allocated > max_claim:
                raise ValueError(
                    f"Alloc P{row_index + 1} R{col_index + 1} cannot exceed "
                    f"Max P{row_index + 1} R{col_index + 1}."
                )

    return {
        "processes": processes,
        "allocation": allocation,
        "maximum": maximum,
        "available": available,
    }


def format_table(title, rows):
    headers = ["PID", "AT", "BT", "ST", "CT", "TAT", "WT"]
    output = [title, "-" * len(title), " | ".join(f"{header:>3}" for header in headers)]
    output.append("-" * 41)

    for row in rows:
        output.append(
            " | ".join(
                [
                    f"{row['pid']:>3}",
                    f"{row['arrival_time']:>3}",
                    f"{row['burst_time']:>3}",
                    f"{row['start_time']:>3}",
                    f"{row['completion_time']:>3}",
                    f"{row['turnaround_time']:>3}",
                    f"{row['waiting_time']:>3}",
                ]
            )
        )

    average_tat = sum(row["turnaround_time"] for row in rows) / len(rows)
    average_wt = sum(row["waiting_time"] for row in rows) / len(rows)
    output.append(f"Average Turnaround Time: {average_tat:.2f}")
    output.append(f"Average Waiting Time: {average_wt:.2f}")
    return "\n".join(output)


def format_matrix(title, matrix):
    lines = [title]
    for index, row in enumerate(matrix, 1):
        lines.append(f"P{index}: " + " ".join(f"R{col + 1}={value}" for col, value in enumerate(row)))
    return "\n".join(lines)


def format_bankers(result):
    lines = ["Banker's Algorithm", "------------------"]
    lines.append(format_matrix("Need Matrix", result["need"]))

    if result["safe"]:
        lines.append("Status: SAFE")
        lines.append("Safe Sequence: " + " -> ".join(result["safe_sequence"]))
        lines.append("Safety Trace:")
        for step in result["trace"]:
            lines.append(
                f"{step['process']}: Work {step['work_before']} + "
                f"Allocation {step['released']} = {step['work_after']}"
            )
    else:
        lines.append("Status: UNSAFE / POSSIBLE DEADLOCK")
        lines.append("Unfinished Processes: " + ", ".join(result["unfinished"]))
        lines.append("Deadlock Details:")
        for detail in result["deadlock_details"]:
            lines.append(f"{detail['process']} Need: {detail['need']}")
            if detail["shortages"]:
                shortage_text = ", ".join(
                    f"{item['resource']} shortage={item['shortage']} "
                    f"(needed {item['needed']}, available {item['available']})"
                    for item in detail["shortages"]
                )
                lines.append(f"Shortages: {shortage_text}")
            else:
                lines.append("Shortages: none at final work vector, but no safe order remains.")
            lines.append("Clues to fix:")
            for clue in detail["clues_to_fix"]:
                lines.append(f"- {clue}")

    return "\n".join(lines)


def build_output(data):
    processes = data["processes"]
    process_ids = [f"P{process['pid']}" for process in processes]

    sections = [
        "CPU Scheduling and Banker's Algorithm Results",
        "=============================================",
        format_table("First Come First Served (FCFS)", first_come_first_served(processes)),
        format_table("Shortest Job First (Non-Preemptive)", shortest_job_first(processes)),
        format_table("Shortest Remaining Time First (Preemptive)", shortest_remaining_time_first(processes)),
        format_table("Round Robin (Quantum = 2)", round_robin(processes, quantum=2)),
        format_bankers(
            bankers_algorithm(
                data["allocation"],
                data["maximum"],
                data["available"],
                process_ids=process_ids,
            )
        ),
    ]
    return "\n\n".join(sections) + "\n"


def main():
    data = parse_input(INPUT_FILE)
    report = build_output(data)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(report)
    print(f"Wrote combined results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
