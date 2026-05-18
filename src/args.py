import argparse


def parse_args(args_list: list[str]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", required=True)
    parser.add_argument("--task", required=True)
    parser.add_argument("--agent-dir", required=True)
    parser.add_argument("--keep", action="store_true")
    return parser.parse_args(args_list)
