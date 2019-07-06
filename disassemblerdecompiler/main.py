import argparse
import sys
from vm.pitou import VM

bytecodepath = "./bytecode/dga.data"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", choices=['nasm', 'disassembly', 'debug', 'debugwithstack'])
    parser.add_argument("-o", "--out")
    args = parser.parse_args()
    if args.type in ['nasm', 'disassembly']:
        if not args.out:
            raise ValueError("output file missing")
    vm = VM(bytecodepath)
    vm.run(args.out, args.type)


