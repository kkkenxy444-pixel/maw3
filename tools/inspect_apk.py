#!/usr/bin/env python3
"""Inspect a user-provided MAW3 APK using Python standard library only.

Termux example:
    python inspect_apk.py "/sdcard/Download/Machines-War-3-RTS.apk"

This displays metadata only. No game code is executed or extracted.
"""
import argparse
import collections
import re
import struct
import zipfile
import xml.etree.ElementTree as ET
from pathlib import PureWindowsPath


def pak_summary(blob):
    if len(blob) < 5:
        raise ValueError("PAK file too short")
    count = struct.unpack_from("<I", blob, 0)[0]
    if not 0 < count < 200000:
        raise ValueError("PAK entry count outside safety limit")
    pos = 5
    names = []
    for i in range(count):
        end = blob.find(b"\x00", pos)
        if end == -1 or end + 9 > len(blob):
            raise ValueError("PAK index truncated")
        name = bytes(byte ^ 255 for byte in blob[pos:end]).decode("latin-1")
        length, offset = struct.unpack_from("<II", blob, end + 1)
        length ^= 0xFFFFFFFF
        offset ^= 0xFFFFFFFF
        pos = end + 9
        if offset + length > len(blob):
            raise ValueError("PAK entry outside archive: " + name)
        names.append(name)
    counts = collections.Counter(PureWindowsPath(n).suffix.lower() for n in names)
    print("PAK entries:", len(names))
    print("PAK file types:", ", ".join(f"{typ or '(none)'}={num}" for typ,num in counts.most_common()))
    print("PAK sample entries:", ", ".join(names[:8]))


def analyze(apk):
    with zipfile.ZipFile(apk) as z:
        print("ZIP members:", len(z.namelist()))
        name_set = set(z.namelist())
        for item in ("assets/schema.xml", "assets/data.pak", "assets/terrain.xml", "assets/gui.xml"):
            print(item, "found" if item in name_set else "missing")
        if "assets/schema.xml" in name_set:
            xml = z.read("assets/schema.xml")
            section = re.search(rb"<schema\b[^>]*>.*?</schema>", xml, re.DOTALL)
            if section:
                root = ET.fromstring(section.group())
                units = root.findall("unit")
                print("Top-level schema unit definitions:", len(units))
                print("Sample names:", ", ".join(x.get("Name", "?") for x in units[:12]))
        if "assets/data.pak" in name_set:
            pak_summary(z.read("assets/data.pak"))


if __name__ == "__main__":
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("apk", help="Path to APK on your device")
    analyze(argp.parse_args().apk)
