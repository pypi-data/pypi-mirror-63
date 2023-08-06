import argparse
import sys

from emeki.project_setup import setup_project_UI


def emeki_main():
    """The main function.

    It may be called directly from the command line when
    typing `emeki`."""

    print("Hoi! This is my personal python library.")

    parser = argparse.ArgumentParser()
    parser.add_argument("--init_pro", help="initialize project", action="store_true")
    args = parser.parse_args(sys.argv[1:])
    if args.init_pro:
        setup_project_UI()


if __name__ == "__main__":
    emeki_main()
