#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
from collections import Counter

def git(cmd):
    try:
        return subprocess.check_output(["git"] + cmd, stderr=subprocess.DEVNULL, text=True)
    except subprocess.CalledProcessError:
        return ""

def cmd_stats(args):
    commits = git(["rev-list", "--count", "HEAD"]).strip()
    branches = git(["branch", "-a"]).strip().splitlines()
    tags = git(["tag"]).strip().splitlines()
    files = git(["ls-files"]).strip().splitlines()
    print(f"commits:   {commits}")
    print(f"branches:  {len(branches)}")
    print(f"tags:      {len(tags)}")
    print(f"files:     {len(files)}")

def cmd_contributors(args):
    out = git(["shortlog", "-sn", "HEAD"])
    for line in out.strip().splitlines():
        parts = line.strip().split("\t", 1)
        if len(parts) == 2:
            print(f"{parts[0]:>6}  {parts[1]}")

def cmd_hotspots(args):
    out = git(["log", "--name-only", "--pretty=format:", "HEAD"])
    files = [f for f in out.splitlines() if f.strip()]
    counts = Counter(files)
    for f, n in counts.most_common(args.limit):
        print(f"{n:>6}  {f}")

def cmd_branches(args):
    out = git(["branch", "-a", "--format=%(refname:short) %(objectname:short)"])
    for line in out.strip().splitlines():
        print(line)

def cmd_tags(args):
    out = git(["tag", "--sort=-creatordate"])
    for line in out.strip().splitlines():
        print(line)

def cmd_recent(args):
    out = git(["log", f"-{args.n}", "--pretty=format:%h %an %s", "--date=short"])
    for line in out.strip().splitlines():
        print(line)

def main():
    parser = argparse.ArgumentParser(prog="gitstat", description="Analyze git repositories from your terminal. Zero dependencies.")
    sub = parser.add_subparsers(dest="command")

    p_stats = sub.add_parser("stats", help="repository statistics")
    p_stats.set_defaults(func=cmd_stats)

    p_contrib = sub.add_parser("contributors", help="contributor statistics")
    p_contrib.set_defaults(func=cmd_contributors)

    p_hot = sub.add_parser("hotspots", help="most changed files")
    p_hot.add_argument("-n", "--limit", type=int, default=10, help="number of files")
    p_hot.set_defaults(func=cmd_hotspots)

    p_branch = sub.add_parser("branches", help="list branches")
    p_branch.set_defaults(func=cmd_branches)

    p_tags = sub.add_parser("tags", help="list tags")
    p_tags.set_defaults(func=cmd_tags)

    p_recent = sub.add_parser("recent", help="recent commits")
    p_recent.add_argument("-n", type=int, default=10, help="number of commits")
    p_recent.set_defaults(func=cmd_recent)

    args = parser.parse_args()
    if not args.command:
        args.command = "stats"
        cmd_stats(args)
        return
    args.func(args)

if __name__ == "__main__":
    main()
