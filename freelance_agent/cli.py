from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .pipeline import process_orders


def main() -> None:
    parser = argparse.ArgumentParser(description="Run freelance order analysis pipeline.")
    parser.add_argument("--input", required=True, help="Path to JSON file with sample orders.")
    args = parser.parse_args()

    input_path = Path(args.input)
    raw_orders = json.loads(input_path.read_text(encoding="utf-8"))
    results = process_orders(raw_orders)

    print(json.dumps([asdict(result) for result in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
