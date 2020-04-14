import sys
import block_model_proccesor
import tests

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    tests.test_answer()
    print("tests done")
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
if __name__ == "__main__":
    main()