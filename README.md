# Pitou 
Accompanying material for the blog post on Pitou's DGA

## disassemblerdecompiler
Disassembler and decompiler for the bytecode of Pitou's virtual machine. Run the script in ``./disassemblerdecompiler/``. To disassemble the bytecode, run

    python3 main.py disassembly -o pitou.dis

To decompile the bytecode, run:

    python3 main.py nasm -o pitou.nasm

Folder ``./disassemblerdecompiler/output`` contains the output of the disassembler ``pitou.dis``, the output of the decompiler ``pitou.nasm`` and the compiled ELF binary ``pitou.elf``.

## instructionvisualizer
Python script to visualize the virtual instruction encodings. Run the script from the directory ``./instructionvisualizer/src`` as follow:

    python3 do.py ../data/data.json

The script writes one SVG image per virtual instruction, and prints a markdown table with the fields to stdout. Warning: the underlying data is not up to date, I fixed some encodings and renamed fields while writing the blog posts. I did not put these changes back into ``data.json``. 

