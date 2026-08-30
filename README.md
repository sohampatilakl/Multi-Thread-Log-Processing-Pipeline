# Multi-Thread-Log-Processing-Pipeline
Problem Statement: Build a producer-consumer system for processing large log files. A file reader adds data to a queue, worker threads parse and analyze records, and an aggregator generates statistics. Implement synchronization, error handling, safe statistics aggregation, and graceful shutdown.
[README.md](https://github.com/user-attachments/files/31617504/README.md)
# Multi-Threaded Log Processing Pipeline

A simple Python program that reads a log file and processes it using multiple
threads at the same time, so large files get processed faster.

## What it does

1. **Producer (Reader)** – Opens the log file and reads it line by line. Each
   line is put into a shared queue.
2. **Workers** – Several threads pick up lines from the queue, check if the
   line looks like a valid log entry, and count what kind of log it is
   (INFO, WARNING, ERROR, DEBUG).
3. **Aggregator** – Once everyone is done, the program prints a summary:
   how many lines were read, how many were valid, how many failed, and a
   count for each log level.

Think of it like a small factory line:
- One person reads pages out of a book and drops them in a basket (producer).
- A few people pick pages from the basket and sort them (workers).
- At the end, someone counts up all the sorted piles (aggregator).

## Why use threads here?

Reading a file is usually fast, but *parsing and analyzing* every line can
take time if the file is huge. By splitting that work across several worker
threads, the program can process many lines in parallel instead of one at a
time.

## Requirements

- Python 3.7 or newer
- No external libraries needed — everything used (`threading`, `queue`,
  `re`, `argparse`) comes built into Python.

## How to run it

```bash
python log_pipeline.py yourfile.log --workers 4
```

- `yourfile.log` — path to the log file you want to process
- `--workers 4` — how many worker threads to use (optional, default is 4)

## Example

Given a log file like this:

```
2026-08-30 10:00:01 INFO Server started
2026-08-30 10:00:02 DEBUG Loaded config
2026-08-30 10:00:03 ERROR Failed to connect to DB
this is a garbage line
2026-08-30 10:00:05 WARNING High memory usage
```

Running the program prints:

```
=== Log Processing Summary ===
Total lines read : 5
Successfully parsed: 4
Failed to parse    : 1
Counts by level:
  DEBUG   : 1
  ERROR   : 1
  INFO    : 1
  WARNING : 1
Elapsed time: 0.00s
```

## What happens with bad or broken lines?

If a line doesn't match the expected log format, it's not skipped silently
or allowed to crash the program — it's counted as a "failed to parse" line,
and the worker moves on to the next line.

## How does it shut down cleanly?

Once the reader finishes the file, it sends a special "stop" signal into the
queue — one for each worker. When a worker receives that signal, it knows
there's no more work coming and exits on its own. This way, no thread gets
stuck waiting forever, and no work is lost.

## Files in this project

- `log_pipeline.py` — the main program
- `README.md` — this file

## Possible improvements (not included, but easy to add later)

- Support JSON-formatted log lines instead of plain text
- Save the summary to a file instead of just printing it
- Process lines in small batches instead of one at a time, for extra speed
