#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import argparse
import re
import sys
import mimetypes
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("paths", nargs="*")
parser.add_argument("--order", default="default")
parser.add_argument("--reverse", action="store_true")
args = parser.parse_args()


td = tempfile.TemporaryDirectory()
paths = []

if len(args.paths) == 0:
    inputs = sys.stdin
else:
    inputs = args.paths

if len(args.paths) != 1:
    for line in inputs:
        line = line.strip()
        line = line.split("\t")
        l = line[0]
        ln = None
        if len(line) == 2:
            ln = line[1]
        l = Path(re.sub(r'^file://', '', l))
        if l.exists() and not l.is_dir():
            mime, enc = mimetypes.guess_type(str(l))
            if mime:
                if re.match(r'(image|video)', mime):
                    if ln:
                        ln = Path(td.name) / Path(ln)
                        ln.symlink_to(l)
                        l = ln
                    paths.append(l)
else:
    line = inputs[0]
    line = line.strip()
    line = line.split("\t")
    l = Path(line[0])
    if l.is_dir():
        for p in l.iterdir():
            paths.append(p)
    else:
        for p in l.parent.iterdir():
            paths.append(p)

paths = list(set(paths))

proc = ["mpv"]
if len(paths):
    if args.order == "default":
        args.order = "filename"
        ils = list(filter(lambda x: re.match(
            r'^[0-9a-z]{32}$', x.stem), paths))
        if len(ils) / len(paths) >= 0.5:
            args.order = "mtime"

    if args.order == "filename":
        paths = sorted(paths, key=lambda x: x.name, reverse=args.reverse)

    if args.order == "mtime":
        paths = sorted(paths, key=lambda x: x.stat().st_mtime,
                       reverse=args.reverse)

    playlist_start = 0

    if len(args.paths):
        first = Path(args.paths[0])
        if not first.is_dir():
            playlist_start = [x.name for x in paths].index(first.name)
        proc.append("--playlist-start=" + str(playlist_start))

proc += [str(x) for x in paths]
Popen(proc).communicate()
