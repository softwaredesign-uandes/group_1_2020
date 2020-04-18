import sys
import block_model_proccesor

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    query_console.main_menu()
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do.
if __name__ == "__main__":
    main()