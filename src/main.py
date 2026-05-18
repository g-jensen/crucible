import args
import crucible


def main():
    parsed_args = args.parse_args()
    crucible.run(parsed_args)


if __name__ == "__main__":
    main()
