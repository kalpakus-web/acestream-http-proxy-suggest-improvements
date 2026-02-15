#!/usr/bin/env python3
"""Build an M3U playlist for acestream-http-proxy with grouped channels.

Input CSV columns:
- name (required)
- id (required)
- group (optional, default: Other)
- logo (optional)

Example:
name,id,group,logo
Channel 1,dd1e67078381739d14beca697356ab76d49d1a2d,News,https://example/logo.png
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.parse import quote


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Path to channels CSV")
    parser.add_argument("-o", "--output", type=Path, default=Path("playlist.m3u"))
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:6878",
        help="Base URL of acestream-http-proxy (default: %(default)s)",
    )
    parser.add_argument(
        "--path",
        default="/ace/getstream",
        choices=["/ace/getstream", "/ace/manifest.m3u8"],
        help="Stream endpoint to use (default: %(default)s)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    rows: list[dict[str, str]] = []
    with args.input.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        required = {"name", "id"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            missing_s = ", ".join(sorted(missing))
            raise SystemExit(f"CSV must contain columns: {missing_s}")

        for row in reader:
            name = (row.get("name") or "").strip()
            stream_id = (row.get("id") or "").strip()
            if not name or not stream_id:
                continue
            rows.append(
                {
                    "name": name,
                    "id": stream_id,
                    "group": (row.get("group") or "Other").strip() or "Other",
                    "logo": (row.get("logo") or "").strip(),
                }
            )

    rows.sort(key=lambda r: (r["group"].lower(), r["name"].lower()))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as out:
        out.write("#EXTM3U\n")
        for row in rows:
            logo_attr = f' tvg-logo="{row["logo"]}"' if row["logo"] else ""
            out.write(
                f'#EXTINF:-1 group-title="{row["group"]}"{logo_attr},{row["name"]}\n'
            )
            stream_id = quote(row["id"], safe="")
            out.write(f'{args.base_url}{args.path}?id={stream_id}\n')


if __name__ == "__main__":
    main()

