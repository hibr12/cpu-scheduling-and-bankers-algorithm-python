       
       BAHIR DAR UNIVERSITY  

     BAHIR DAR INSTITUTE OF TECHNOLOGY                                                              
         FACULTY OF COMPUTING         

  Course:          operattingsystem

             Group Assignment 
             
Group members                     ID                                                              
GETANEW TILAHUN          .................BDU1601593
HABTAMU GENET            .................BDU1601645
HAYMANOT YABIBAL         .................BDU1601729 
HELEN KINDU              .................BDU1601736 
HIBRU YITAYEW            .................BDU1601769
GEBREKIDAN ABAY          .................BDU1601545
GEBREMESKEL KEFLEMESKEL   ................BDU1601548
GETACHER KIFILIE          ................BDU1601567
               
                                       Submitted to   Lec.  alemitu                     
                                       Submission Date: 24/08/18 EC 

Bairdar, ethiopia
         




# CPU Scheduling Assignment

This project implements classic CPU scheduling algorithms and Banker's Algorithm in Python. it generated process fields, matrix-style resource inputs, validation before running, one `runAll()`-style execution path, and structured output.

## Features

- First Come First Served (FCFS)
- Shortest Job First, non-preemptive (SJF)
- Shortest Remaining Time First, preemptive SJF (SRTF)
- Round Robin with default quantum `2`
- Banker's Algorithm with:
  - Allocation Matrix
  - Max Need Matrix
  - Available Vector
  - computed Need Matrix
  - safe sequence detection
  - deadlock details, unfinished processes, shortages, and fix clues

## Project Structure

text
cpu-scheduling-assignment/
├── README.md
├── run_all.py
├── src/
│   ├── __init__.py
│   ├── fcfs.py
│   ├── sjf.py
│   ├── srtf.py
│   ├── round_robin.py
│   └── bankers.py
├── input/
│   └── sample_input.txt
└── output/
    └── sample_output.txt


## Setup

Python 3.9 or newer is recommended. No third-party packages are required.

bash
cd cpu-scheduling-assignment
python run_all.py


The combined report is written to:

text
output/sample_output.txt


Each Python file can also be run directly to display its own result in the terminal:

bash
python src/fcfs.py
python src/sjf.py
python src/srtf.py
python src/round_robin.py
python src/bankers.py
python run_all.py


## Input Format

input/sample_input.txt` uses simple sections:

text
[PROCESSES]
1,0,5
2,1,3

[ALLOCATION]
0,1,0
2,0,0

[MAX]
7,5,3
3,2,2

[AVAILABLE]
3,3,2


Process rows are:

text
PID, Arrival Time, Burst Time


Banker's Algorithm rows use the same matrix layout as a browser form. Comments document placeholder names such as:

- `Alloc P1 R1`
- `Alloc P1 R2`
- `Max P2 R3`
- `Avail R2`

## Validation Rules

The parser rejects:

- empty values
- negative numbers
- non-numeric or NaN-like values
- duplicate process IDs
- zero burst times
- mismatched matrix sizes
- allocation values greater than max claims

These checks correspond to the JavaScript simulator's per-field validation before running any algorithm.

## Output

`run_all.py` produces one structured report containing all scheduling tables and the Banker's Algorithm result. Scheduling rows include:

- PID
- Arrival Time
- Burst Time
- Start Time
- Completion Time
- Turnaround Time
- Waiting Time

Banker's Algorithm output includes the Need Matrix, safe sequence if one exists, and a safety trace. If unsafe, it reports unfinished processes, shortages, and clues to fix the state by increasing resources, terminating a blocked process, or reducing maximum claims.

## Python and JavaScript Simulator Mapping

The Python implementation mirrors the earlier JavaScript simulator in these ways:

- Dynamic input generation becomes section-based text input with documented placeholders.
- Matrix layout is preserved through Allocation, Max, and Available sections.
- Field validation happens before algorithms run, like form validation in JavaScript.
- `run_all.py` acts like `runAll()`: it parses, validates, runs FCFS, SJF, SRTF, Round Robin, and Banker's Algorithm, then builds one output.
- Errors are raised with field-specific messages such as `Alloc P1 R1`, `Max P2 R3`, and `Avail R2`.
- Results are formatted in tables and structured text similar to simulator output panels.

## Educational Value

This project is useful for comparing how CPU scheduling policies affect completion, turnaround, and waiting time. It also shows how Banker's Algorithm avoids unsafe resource allocation states by checking whether all processes can finish in some sequence.

## Responsiveness

The original JS version likely updated a responsive page layout. This Python version keeps that spirit by producing compact, readable text tables that work in terminals, editors, and assignment submissions without requiring a browser.

## Example Output

After running:

bash
python run_all.py


open `output/sample_output.txt` to see FCFS, SJF, SRTF, Round Robin, and Banker's Algorithm results generated from the sample input.

## conclusion

This project successfully demonstrates how fundamental CPU scheduling algorithms and the Banker's Algorithm can be implemented in Python in a structured, educational way.  it preserves validation rigor, matrix-style resource handling, and unified execution path, while producing clear, text-based outputs suitable for study.

The combination of FCFS, SJF, SRTF, Round Robin, and Banker's Algorithm provides a comprehensive toolkit for analyzing both process scheduling and resource allocation safety. The design emphasizes correctness, readability, and comparability, making it a valuable resource for students learning operating system concepts.

In essence, the project bridges theory and practice: it shows how scheduling policies affect performance metrics, and how Banker's Algorithm ensures system safety, all within a compact, accessible Python framework.


