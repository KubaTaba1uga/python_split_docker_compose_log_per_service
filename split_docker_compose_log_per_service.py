#!/usr/bin/env python3
import re
import os
import argparse
from collections import defaultdict

def split_logs(input_file: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    service_logs = defaultdict(list)

    log_pattern = re.compile(r"^(?P<container>[^\s|]+)\s+\|\s+(?P<line>.*)$")

    with open(input_file, "r", encoding="utf-8", errors="replace") as f:
        for raw_line in f:
            line = raw_line.strip()
            match = log_pattern.match(line)
            if match:
                container = match.group("container")
                service = re.sub(r"-\d+$", "", container.split("/")[-1])
                service_logs[service].append(f"{match.group('line')}\n")

    for service, logs in service_logs.items():
        with open(os.path.join(output_dir, f"{service}.log"), "w", encoding="utf-8") as out:
            out.writelines(logs)

    print(f"Logs split into '{output_dir}/'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split docker-compose logs by service name.")
    parser.add_argument("logfile", help="Path to docker-compose log file")
    parser.add_argument("-o", "--output-dir", default="split_logs", help="Output directory for split logs (default: split_logs)")
    args = parser.parse_args()

    split_logs(args.logfile, args.output_dir)

