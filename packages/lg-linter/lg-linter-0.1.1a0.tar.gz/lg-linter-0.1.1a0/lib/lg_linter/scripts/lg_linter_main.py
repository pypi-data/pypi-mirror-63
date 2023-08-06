#!/usr/bin/env python3
import argparse
import pathlib
import sys
sys.path.append('../src')

from lg_linter import LgLinter


def main():
    parser = argparse.ArgumentParser(description='Lint all staged files')
    parser.add_argument('repo_path')
    args = parser.parse_args()

    linter = LgLinter(pathlib.Path(args.repo_path))
    linter.lint()


if __name__ == '__main__':
    main()
