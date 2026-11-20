#!/usr/bin/env python3
"""THE GLOBAL LEDGER -- Thursday 19 November 2026, one-page front page.

The image is shipped in this repository as entry.png. This program only
validates it and copies it to the output directory.

Standard library only: the grader runs with no network and nothing
installed, so no third-party module is imported here.

Output: $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import os
import struct
import sys
import zlib

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # 1 MiB
MAX_DIMENSION = 1024
OUT_NAME = "entry.png"


def fail(message):
    """Print the problem and exit non-zero."""
    print("error: " + message, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail("cannot read entry.png: " + str(exc))

    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if data[:8] != PNG_SIGNATURE:
        return fail("entry.png does not start with the PNG signature")
    if data[12:16] != b"IHDR":
        return fail("entry.png has no IHDR chunk where one is expected")

    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        return fail(
            "entry.png is %dx%d, over the 1024x1024 limit" % (width, height)
        )

    # Walk every chunk: each must end with its own CRC and the file must
    # end with IEND, so a truncated or damaged image is refused instead
    # of being copied out as a broken entry.
    offset = 8
    saw_iend = False
    while offset < len(data):
        if offset + 12 > len(data):
            return fail("entry.png is truncated inside a chunk header")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            return fail("entry.png is truncated inside a %r chunk" % chunk_type)
        stored_crc = struct.unpack(">I", data[end - 4:end])[0]
        actual_crc = zlib.crc32(chunk_type)
        actual_crc = zlib.crc32(data[offset + 8:end - 4], actual_crc)
        if stored_crc != (actual_crc & 0xFFFFFFFF):
            return fail("entry.png has a bad CRC in its %r chunk" % chunk_type)
        offset = end
        if chunk_type == b"IEND":
            saw_iend = True
            break
    if not saw_iend:
        return fail("entry.png has no IEND chunk")
    if offset != len(data):
        return fail("entry.png has trailing bytes after IEND")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, OUT_NAME)
        with open(out_path, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        return fail("cannot write " + OUT_NAME + ": " + str(exc))

    print("wrote %s (%d bytes, %dx%d)" % (out_path, len(data), width, height))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
