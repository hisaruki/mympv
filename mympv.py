#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import argparse
import re
import sys
from magic import Magic
from mimetypes import guess_type
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("paths", nargs="*")
parser.add_argument("--order", default="default")
parser.add_argument("--reverse", action="store_true")
args = parser.parse_args()


td = tempfile.TemporaryDirectory()
magic = Magic(mime=True)
paths = []

if len(args.paths) == 0:
    inputs = sys.stdin
else:
    inputs = args.paths

def checkmime(p, ln):
    if p.is_dir():
        return None
    mime, e = guess_type(p.name)
    if not mime:
        mime = magic.from_buffer(p.open("rb").read(1024))
    if mime:
        if re.match(r'(image|video)', mime):
            if ln:
                ln = Path(td.name) / Path(ln)
                ln.symlink_to(p)
                p = ln
            return p
    return None

if len(args.paths) != 1:
    for line in inputs:
        line = line.strip()
        line = line.split("\t")
        l = line[0]
        ln = None
        if len(line) == 2:
            ln = line[1]
        l = Path(re.sub(r'^file://', '', l))
        if l.exists():
            l = checkmime(l, ln)
            if l:
                paths.append(l)
else:
    line = inputs[0]
    line = line.strip()
    line = line.split("\t")
    l = Path(line[0])
    if l.is_dir():
        cur = l.iterdir()
    else:
        cur = l.parent.iterdir()
    for p in cur:
        p = checkmime(p, None)
        if p:
            paths.append(p)

paths = list(set(paths))

proc = ["mpv"]
if len(paths):
    if args.order == "default":
        args.order = "filename"
        ils = list(filter(lambda x: re.search(r'[0-9a-z]{32}$', x.stem), paths))
        if len(ils) / len(paths) >= 0.33:
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
proc = Popen(proc)
for p in paths:
    p.open("rb").read(1024*1024*8)
