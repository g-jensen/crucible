import argparse


def parse_args(args_list: list[str] | None = None):
    parser = argparse.ArgumentParser()
    dir_group = parser.add_mutually_exclusive_group(required=True)
    dir_group.add_argument("--results-dir")
    dir_group.add_argument("--run-dir")
    parser.add_argument("--task", required=True)
    parser.add_argument("--agent-dir", required=True)
    parser.add_argument("--keep", action="store_true")
    return parser.parse_args(args_list)
