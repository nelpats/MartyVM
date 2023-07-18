import sys
import os
from Core.Encoder import VM, process_bytecode

def main(argc : int, argv : list[str]):

    vm : VM

    if argc < 2:
        print("PATH to the script expected.")
        print("usage: marty.py PATH.pyc")
        exit(1)

    path = argv[1]

    if not os.path.isfile(path):
        print(f"The file '{path}' does not exist")
        exit(1)
    
    match path[-3:].replace('.', ''):
        case "pyc":
            vm = VM(
                process_bytecode(
                    path=path
                )
            )
        case _:
            print("This kind of file is not supported.")
            exit(1)


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)