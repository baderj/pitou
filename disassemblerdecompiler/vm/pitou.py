from collections import OrderedDict
import random
import string
from datetime import datetime
import colorama
import re
import struct
import operator

class Context:

    def __init__(self):
        self.context = OrderedDict([
            ("rax", None),
            ("rcx", None),
            ("rdx", None),
            ("rbx", None),
            ("rsp", None),
            ("rbp", None),
            ("rsi", None),
            ("rdi", None),
            ("r8", None),
            ("r9", None),
            ("r10", None),
            ("r11", None),
            ("r12", None),
            ("r13", None),
            ("r14", None),
            ("r15", None),
            ("eflags", None),
            ("field_88", None),
            ("vminstruction_pointer", None),
            ("vm_stack_base", None),
            ("vm_stack_pointer", None),
            ("vm_stack_pointer2", None),
            ("what_is_this", None),
            ("field_B8", None),
            ("flag_C0", None),
            ("state2", None),
            ("state1", None)
        ])
        self.memory = {}
        self.addstr = None

    @property
    def eip(self):
        return self.context["v_vminstruction_pointer"]

    @eip.setter
    def eip(self, eip):
        self.context["v_vminstruction_pointer"] = eip

    def increase_eip(self, nr):
        self.context["v_vminstruction_pointer"] += nr

    @property
    def state1(self):
        return self.context["v_state1"]

    @property
    def state2(self):
        return self.context["v_state2"]

    def get_register_name(self, flag, index, flag2):
        if flag or (index <= 3 or index >= 8 or flag2):
            return list(self.context.items())[index][0]
        else:
            raise NotImplementedError("")

    def write_to_memory(self, address, value, size):
        for i in range(2**size):
            self.memory[address + i] = value & 0xFF
            value >>= 8

class Stack:

    def __init__(self):
        self.elements = []

    def listify(self, value):
        if type(value) not in (list, tuple):
            return value, []
        else:
            return value

    @property
    def size(self):
        return len(self.elements)

    def check(self, v):
        if not type(v) in [list, tuple] or len(v) != 2:
            raise ValueError("can only push/set 2-tuples to stack")
        if type(v[0]) in [list, tuple]:
            raise ValueError("first element can't be list/tuple")
        if type(v[1]) not in [list, tuple]:
            raise ValueError("second element needs to be list/tuple")
        for vv in v[1]:
            if not re.search("\s+", vv):
                raise ValueError("not an assembly instr: {}".format(vv))

    def push(self, upper, lower=None):
        if lower is None:
            lower = upper
        lower = self.listify(lower)
        upper = self.listify(upper)

        self.check(lower)
        self.check(upper)

        self.elements.append([upper, lower])

    def pop(self, both=False):
        if both:
            return self.elements.pop()
        else:
            return self.elements.pop()[0]

    def set(self, v, low=False, index=0):
        self.check(v)
        if low:
            self.elements[-(1+index)][1] = v
        else:
            self.elements[-(1+index)][0] = v

    def get(self, low=False, both=False, index=0):
        if both:
            return self.elements[-(1+index)]
        elif low:
            return self.elements[-(1+index)][1]
        else:
            return self.elements[-(1+index)][0]


    def __str__(self):
        res = ""
        for s in self.elements[::-1]:
            us, ls = s
            uss = "/".join(us[1])
            lss = "/".join(ls[1])
            res += "| {:<14}{:<30} | {:<14}{:<30} |\n".format(us[0], uss, ls[0], lss)
        return res

    @property
    def printmarkdown(self):
        res = ""
        res += "| {:<14} | {:<30} | {:<14} | {:<30} |\n".format("value","value instructions","extra","extra instructions")
        res += "| {:<14} | {:<30} | {:<14} | {:<30} |\n".format("---","---","---","---")
        for s in self.elements[::-1]:
            us, ls = s
            uss = "<br>".join(us[1])
            lss = "<br>".join(ls[1])
            res += "| {:<14} | {:<30} | {:<14} | {:<30} |\n".format(us[0], uss, ls[0], lss)
        return res


class Assembly:

    def __init__(self, stack):
        self.stack = stack
        self.VALID_REGISTERNAMES = {
            "rax": ["rax", "eax", "ax", "al", "ah"],
            "rbx": ["rbx", "ebx", "bx", "bl", "bh"],
            "rcx": ["rcx", "ecx", "cx", "cl", "ch"],
            "rdx": ["rdx", "edx", "dx", "dl", "dh"],
            "rsi": ["rsi", "esi", "si", "sil"],
            "rdi": ["rdi", "edi", "di", "dil"],
            "rbp": ["rbp", "ebp", "bp", "bpl"],
            "rsp": ["rsp", "esp", "sp", "spl"],
            "r8": ["r8", "r8d", "r8w", "r8b"],
            "r9": ["r9", "r9d", "r9w", "r9b"],
            "r10": ["r10", "r10d", "r10w", "r10b"],
            "r11": ["r11", "r11d", "r11w", "r11b"],
            "r12": ["r12", "r12d", "r12w", "r12b"],
            "r13": ["r13", "r13d", "r13w", "r13b"],
            "r14": ["r14", "r14d", "r14w", "r14b"],
            "r15": ["r15", "r15d", "r15w", "r15b"]
        }

    def isvalue(self, v):
        return type(v) == int

    def isoffset(self, v):
        if not type(v) == str:
            return
        return v.startswith("data_")

    def isregister(self, v):
        m = re.match("[re]?([abcdsdbsi])([xpil])$", v)
        if m:
            return True

        m = re.match("(r\d{1,2})[dwb]?$", v)

        if m:
            return True

    def removecasts(self, line):
        for cast in ["WORD", "DWORD", "BYTE", "QWORD"]:
            line = line.replace(" " + cast + " ", " ")
        return line

    def dref(self, instr):
        reg, assembly = instr
        """ if no assembly"""
        if not assembly:
            if self.isregister(reg) or self.isvalue(reg) or self.isoffset(reg):
                return "[{}]".format(reg), []
            m = re.match("addr\((.*)\)$", reg, re.I)
            if m:
                return m.group(1), []
            else:
                raise ValueError("cannot dereference {}".format(instr))

        lastline = assembly[-1]
        lastline = self.removecasts(lastline)


        if len(assembly) >= 2:
            prelastline = assembly[-2]
            prelastline = self.removecasts(prelastline)
            m = re.match("ADD ([^,]*), ([^,]*)", lastline)
            if m:
                reg1 = m.group(1)
                off = m.group(2)
                m = re.match("ADD ([^,]*), ([^,]*)", prelastline)
                if m:
                    reg2 = m.group(1)
                    regx = m.group(2)
                    if self.sameregister(reg, reg2):
                        nn =  "[{} + {} + {}]".format(regx, reg1, off), assembly[:-2]
                        return nn



        m = re.match("ADD ([^,]*), ([^,]*)", lastline)
        if m:
            return "[{} + {}]".format(*m.groups()), assembly[:-1]

        m = re.search("SUB ([^,]*), (\d+)", lastline)
        if m:
            return "[{} - {}]".format(*m.groups()), assembly[:-1]

        raise NotImplementedError()

    def reg64(self, regname):

        for fullname, cands in self.VALID_REGISTERNAMES.items():
            if regname in cands:
                return fullname

        raise ValueError("invalid register name %s", regname)

    def cast(self, v, size):
        assert(size in [0,1,2,3])
        if v is None:
            return v
        if type(v) == int:
            mod = 2 ** (2 ** (3 + size))
            v =  v & (mod - 1)
            if v > mod//2:
                return v - mod
            else:
                return v
        else:
            if not re.match("^[a-z0-9]+$",  v):
                return v
            fullreg = self.reg64(v)
            return self.VALID_REGISTERNAMES[fullreg][3-size]


    def sizename(self, v):
        return {0: "BYTE", 1: "WORD", 2: "DWORD", 3: "QWORD"}[v]

    def extractregister(self, raw):
        m = set()
        for k,v in self.VALID_REGISTERNAMES.items():
            for vv in v:
                if vv in raw:
                    m.add(vv)
        if not m:
            raise ValueError("no register in {}".format(raw))
        x = sorted(m, key=lambda x: len(x))
        best = x[-1]
        return best


    def replaceregister(self, instr, from_reg, to_reg, target=True):
        if not "," in instr:
            raise ValueError("cannot parse: {}".format(instr))

        before, after = instr.split(",")
        if target:
            reg = self.extractregister(before)
            if self.sameregister(reg, from_reg):
                size = self.sizefromregname(reg)
                to_reg_casted = self.cast(to_reg, size)
                before = before.replace(reg, to_reg_casted)
                x = ",".join([before, after])
                return x
        else:
            reg = self.extractregister(after)
            if self.sameregister(reg, from_reg):
                size = self.sizefromregname(reg)
                to_reg_casted = self.cast(to_reg, size)
                after = after.replace(reg, to_reg_casted)
                x = ",".join([before, after])
                return x

        return instr

    def replacesource(self, instr, from_reg, to_reg):
        m = re.match("([^,]+\s+)([^,\s]+)(,[^,]+$)", instr)
        if m:
            target = m.group(2)
            if self.sameregister(target, from_reg):
                size = self.sizefromregname(target)
                to_reg_casted = self.cast(to_reg, size)
                x = "{}{}{}".format(m.group(1), to_reg_casted, m.group(3))
                return x
        return instr

    def sameregister(self, reg_a, reg_b):
        assert(type(reg_a) == str)
        assert(type(reg_b) == str)

        reg_a_full = self.cast(reg_a, 3)
        reg_b_full = self.cast(reg_b, 3)
        return reg_a_full == reg_b_full

    def sizefromregname(self, regname):

        for fullname, cands in self.VALID_REGISTERNAMES.items():
            if regname in cands:
                return 3 - cands.index(regname)

        raise ValueError("invalid register name %s", regname)

    def isempty(self, instr):
        m = re.match("MOV\s+(QWORD|DWORD|WORD|BYTE)?\s+([^,]+),\s*(.*)$", instr)
        if m:
            reg1 = m.group(2).strip()
            reg2 = m.group(3).strip()
            if reg1 == reg2:
                return True
        return False

    def arithmetic(self, sym, size, nr=2, onstack=True, keep=False):
        """
        Perform a binary or unary instruction

        :param sym: mnemonic of the instruction, e.g., XOR
        :param size: size of the instruction (0=byte, ..., 3=qword)
        :param nr: number of operands (2=binary, 1=unary
        :param onstack:
        :return:
        """
        if nr not in [1,2]:
            raise ValueError("{} operands not supported".format(nr))

        if nr == 2:
            if keep:
                a = self.stack.get()
                b = self.stack.get(1)
            elif onstack:
                a = self.stack.pop()
                b = self.stack.get()
            else:
                a = self.stack.pop()
                b = self.stack.pop()
        else:
            b = self.stack.get() if (onstack or keep) else self.stack.pop()
            a = None

        dst, assembly = self.buildinstruction(sym, size, b, a)
        if onstack:
            self.stack.set((dst, assembly))
        else:
            return assembly

    def castedreg(self, v, size):
        return self.cast(v[0], size)

    def mergedassembly(self, a, b):
        res = []
        if a:
            res += a[1]
        if b:
            res += b[1]
        return res

    def buildinstruction(self, op, size, dst, src=None):

        sizename_pad = self.sizename(size) + " "

        if src:
            src_reg = self.castedreg(src, size)
        else:
            src_reg = None

        dst_reg = self.castedreg(dst, size)

        assembly = self.mergedassembly(src, dst)

        if op == "MOV" and src_reg == dst_reg:
            """ emtpy move """
            pass
        elif src_reg is not None:
            """ binary operation """
            a = "{} {}{}, {}".format(op, sizename_pad, dst_reg, src_reg)
            assembly.append(a)
        else:
            """ unary operation """
            a = "{} {}{}".format(op, sizename_pad, dst_reg)
            assembly.append(a)
        return dst_reg, assembly

class VM:

    def __init__(self, path):
        self.code = self.load_code(path)
        self.imagebase = 0xFFFFF880058517D8
        self.entrypoint_dga = 112797
        self.entrypoint = 112797
        self.lastaddr = self.imagebase + len(self.code)
        self.highest_address = 0xFFFFF8800589CFBB
        self.context = Context()
        self.state1 = None
        self.state2 = None
        self.mz = 0xFFFFF8800582C000
        self.offset = 0xFFFFF87EC582C000
        self.stack = Stack()
        self.assembly = Assembly(self.stack)
        self.jump_targets = set()
        self.data = {
            0xFFFFF8800589E540: ("dd", [31,28,31,30,31,30,31,31,30,31,30,31] ),
            0xFFFFF8800589E570: ("dd", [31,29,31,30,31,30,31,31,30,31,30,31] ),
            0xFFFFF880058A81F0: ("db", 100*[0]),
            0xFFFFF880058A3170: ("db", "RtlInitString"),
            0xFFFFF8800584C2B7: ("db", "return"),
            0xFFFFF8800584C230: ("db", "?,biz,net,info,mobi,us,name,me"),
            0xFFFFF880058A8238: ("db", "bcdfghjklmnpqrstvwxyz"),
            0xFFFFF880058A8240: ("db", "aeiou"),
            0xFFFFF880058A3010: ("db", "ExAllocatePool"),
            0xFFFFF880058A3018: ("db", "ExFreePool"),
            0xFFFFF880058A2228: ("db", [0xE9]),
            0xFFFFF880058A222D: ("db", [0x24]),
            0xFFFFF880058A222E: ("db", [0]),
            0xFFFFF880058A2245: ("db", [0xe6]),
            0xFFFFF880058A2246: ("db", [0]),
            0xFFFFF880058A8230: ("dq", [0]),
            0xFFFFF880058A226C: ("db", [0xA])
        }

        self.instructions = {
            0x00: self.instruction_00,
            0x01: self.instruction_01,
            0x02: self.instruction_02,
            0x03: self.instruction_03,
            0x04: self.instruction_04,
            0x05: self.instruction_05,
            0x06: self.instruction_06,
            0x07: self.instruction_07,
            0x08: self.instruction_08,
            0x09: self.instruction_09,
            0x0A: self.instruction_0A,
            0x0B: self.instruction_0B,
            0x0C: self.instruction_0C,
            0x0D: self.instruction_0D,
            0x0E: self.instruction_0E,
            0x0F: self.instruction_0F,
            0x10: self.instruction_10,
            0x11: self.instruction_11,
            0x12: self.instruction_12,
            0x13: self.instruction_13,
            0x14: self.instruction_14,
            0x15: self.instruction_15,
            0x16: self.instruction_16,
            0x17: self.instruction_17,
            0x18: self.instruction_18,
            0x19: self.instruction_19,
            0x1A: self.instruction_1A,
            0x1B: self.instruction_1B,
            0x1C: self.instruction_1C,
            0x28: self.instruction_28
        }

        self.current_opcode = None
        self.variant = None
        self.subvariant = None
        self.current_instr = None
        self.current_chain = None
        self.chains = []
        self.lastpushed = None

        self.mapping = {
            0x1D: 0x03,
            0x1E: 0x04,
            0x1F: 0x1A,
            0x20: 0x0B,
            0x21: 0x10,
            0x22: 0x08,
            0x23: 0x04,
            0x24: 0x02,
            0x25: 0x02,
            0x26: 0x10,
            0x27: 0x12,
            0x29: 0x0C,
            0x2A: 0x03,
            0x2B: 0x12,
            0x2C: 0x16,
            0x2D: 0x08,
            0x2E: 0x05,
            0x2F: 0x00,
            0x30: 0x10,
            0x31: 0x18,
            0x32: 0x05,
            0x33: 0x04,
            0x34: 0x0F,
            0x35: 0x00,
            0x36: 0x0B,
            0x37: 0x07,
            0x38: 0x11,
            0x39: 0x0F,
            0x3A: 0x03,
            0x3B: 0x13,
            0x3C: 0x0A,
            0x3D: 0x14,
            0x3E: 0x0D
        }

    def load_code(self, path):
        with open(path, 'rb') as r:
            data = r.read()
        return [int(_) for _ in data]

    def map_to_offset(self, address):
        return (address - self.imagebase)

    def map_to_addr(self, offset):
        return (offset + self.imagebase)

    def add_chain(self, addr, label=None):
        if type(addr) != int:
            return

        if not label:
            label = self.current_chain['label']


        self.lastpushed = addr
        if not self.imagebase <= addr <= self.imagebase + self.lastaddr:
            raise ValueError("address {:016X} outside range")
        done = False
        addr = self.map_to_offset(addr)
        self.jump_targets.add(self.map_to_addr(addr))
        for chain in self.chains:
            if addr == chain['eip']:
                done = True
            for c in chain['instr']:
                a = c['offset']
                if addr == a:
                    done = True
                    break
            if done:
                break
        if done:
            return
        self.chains.append(self.new_chain(addr, label))

    def new_chain(self, addr, label=None):
        self.jump_targets.add(self.map_to_addr(addr))
        c = {"start": addr, "eip": addr, "done": False, "instr": [], "label": label}
        return c

    def parse_opcode(self):
        self.current_opcode = self.get_opcode()
        self.variant = (self.current_opcode & 0x80) >> 7
        self.subvariant = (self.current_opcode & 0x40) >> 6

    def run(self, outpath, type_):
        self.chains.append(self.new_chain(self.entrypoint, "main"))
        print("[+] disassembling pitou")
        steps_taken = 0

        while True:
            """
                get first chain which is not yet done, or finished
            """
            for chain in self.chains:
                if not chain["done"]:
                    self.current_chain = chain
                    break
            else:
                print("[-] no more chains left")
                break

            """
                reset the states
            """
            if self.state1 == 1:
                self.state1 = 2
            elif self.state1 == 2:
                self.state1 = 0
                self.state2 = 0
            self.context.eip = chain["eip"]

            """
                get the opcode
            """
            self.parse_opcode()
            self.current_instr = self.get_current_instruction()

            routine = self.get_routine(self.current_opcode)

            self.context.addrstr = hex(self.map_to_addr(self.context.eip))


            res = routine()
            addr = self.map_to_addr(self.context.eip)

            if type_.startswith("debug"):
                print(colorama.Style.RESET_ALL, end="")
                print(colorama.Fore.MAGENTA + "{:16X} {}".format(addr, res[1]))
                print(colorama.Style.DIM, end="") 
                print(colorama.Fore.WHITE, end="") 
                if type_ == "debugwithstack":
                    print(self.stack, end="")

            if len(res) == 2: 
                assembly = None
                length, code = res
            else:
                length, code, assembly = res
                if type_.startswith("debug"):
                    if assembly:
                        for a in assembly:
                            print(colorama.Fore.GREEN + "{:>16} {}".format("▶", a))
                print(colorama.Style.RESET_ALL, end="")

            self.current_chain['instr'].append(
                {
                    'disassembly': code,
                    'nasm': assembly,
                    'entrypoint': self.context.eip == self.entrypoint,
                    'offset': self.context.eip,
                    'length': length
                }
            )
            self.context.increase_eip(length)
            self.current_chain["eip"] = self.context.eip

        if type_ not in ["debug", "debugwithstack"]:
            self._writecode(type_=type_, path=outpath)

    def label(self, addr):
        return "_addr_{:016X}".format(addr)

    def _writecode(self, type_, path):
        ALLOWED_TYPES = ['disassembly', 'nasm', 'both']
        if type_ not in ALLOWED_TYPES:
            self._write_assembly(path)
            raise ValueError("type needs to be in {}, is {}".format(ALLOWED_TYPES, type_))

        with open(path, 'w') as w:
            """ data """
            if type_ == "nasm":
                w.write("section .data\n")
                for addr, info in self.data.items():
                    if type(info[1]) == str:
                        llabel = '"{}"'.format(info[1]) + ",0"
                    else:
                        llabel = ",".join(str(i) for i in info[1])
                    w.write("{}    {}    {}\n".format(self.addr2datalabel(addr), info[0], llabel))
                """ labels """
                jump_targets = self.jump_targets
                w.write("section .text\nglobal _start\n")

            """ merge chains """
            merged_code = {}
            labels = set()
            for i, chain in enumerate(self.chains):
                label = chain['label']
                labels.add(label)
                for c in chain['instr']:
                    offset = c['offset']
                    merged_code[offset] = {'chainindex': i, 'instr': c, 'label': label}

            """ merge empty lines """
            for key, mc in sorted(merged_code.items()):
                instr = mc['instr']
                code = instr[type_]
                length = instr['length']
                offset = instr['offset']
                if not code:
                    next_code = merged_code.get(offset + length, None)
                    if next_code:
                        next_instr = next_code['instr']
                        next_instr['length'] += length
                        next_instr['offset'] = offset
                        next_instr['entrypoint'] |= instr['entrypoint']
                        del merged_code[key]

            last_index = None
            last_offset = None
            for label in labels:
                for _, mc in sorted(merged_code.items()):
                    instr = mc['instr']
                    offset = instr['offset']
                    if label != mc['label']:
                        continue
                    index = mc['chainindex']
                    length = instr['length']
                    code = instr[type_]
                    ep = instr['entrypoint']
                    addr = self.map_to_addr(offset)

                    if type_ in ["disassembly"]:
                        if last_index is not None and last_index != index:
                            w.write(100*"-" + "\n")
                            opcodebuffer = []
                        elif last_offset is not None and last_offset != offset:
                            w.write(100*"?" + "\n")
                            opcodebuffer = []
                    if type_ in ["nasm"]:
                        if addr == self.map_to_addr(self.entrypoint):
                            w.write("""_start:\n    PUSH rbp\n    MOV rbp, rsp\n""")
                            jump_targets.remove(addr)
                        elif addr in jump_targets:
                            w.write("{}:\n".format(self.label(addr)))
                            jump_targets.remove(addr)
                        codestr = self.instr2ass(code, ep)
                        w.write(codestr)
                    if type_ in ["disassembly"]:
                        codestr = self._instr2str(offset, length, code, ep, breakafter=5)
                        codestr = codestr.replace("\n", "")
                        code = instr["nasm"]
                        codestr += self.instr2ass(code, None).replace("\n", " / ")
                        codestr += "\n"
                        w.write(codestr)

                    last_offset = offset + length
                    last_index = index

        print("[+] written {} to {}".format(type_, path))

    def patch(self, code):
        rep = {
            "MUL DWORD eax, [rsp + 48]": "MUL DWORD [rsp + 48]",
            "SHR DWORD edx, ecx": "SHR DWORD edx, cl",
            "MUL DWORD eax, r11d": "MUL DWORD r11d"
        }
        for k,v in rep.items():
            if code == k:
                return v
        return code

    def instr2ass(self, code, ep, indent=4):
        if not code:
            return ""
        res = ""
        for c in code:
            res += "{}{}\n".format(indent*" ", self.patch(c))
        return res

    def _instr2str(self, address, nr, code, ep=False, breakafter=0, hidecasts=False):
        if not code:
            code = ["???"]
        s = ""
        line = code
        linenr = 0
        while True:
            addr = "{:X}".format(self.map_to_addr(address))
            astr = addr
            istr = "{:02X}".format(self.get_instruction_nr(self.code[address]))
            cstr = self._get_opcodes(address, linenr, breakafter, nr)
            if not cstr:
                break
            estr = ">" if ep else ""
            if hidecasts:
                for cast in ["WORD", "DWORD", "BYTE", "QWORD"]:
                    line = line.replace(" " + cast + " ", " ")
            if linenr:
                estr, astr, line, istr = "", "", "", ""
            res = 3*[""]
            for i, l in enumerate(line.split(" ", 2)):
                res[i] = l
            res = ";".join(res)
            fmt = "{:<1} {:<19} {:<" + str(breakafter*3 + 2) + "} {}\n"
            s += fmt.format(estr, astr, cstr, res)
            linenr += 1

        return s

    def _get_opcodes(self, offset, linenr, breakafter, nr):
        if not breakafter:
            lines = self.code[offset:offset + nr]
        else:
            xl = min(nr, (linenr+1)*breakafter)
            lines = self.code[offset + linenr*breakafter:offset + xl]
        code = " ".join(["{:02X}".format(_) for _ in lines])
        return code

    def get_opcode(self):
        instr = self.get_current_instruction()
        if not instr:
            raise RuntimeError("ran out of code")
        return instr[0]

    def get_current_instruction(self):
        eip = self.context.eip
        return self.code[eip:eip+20]

    def get_instruction_nr(self, opcode):
        opcode = opcode % 64
        nr = self.mapping.get(opcode, opcode)
        if nr not in self.instructions:
            raise NotImplementedError("can't handle instruction {:02X}".format(nr))
        return nr

    def get_routine(self, opcode):
        nr = self.get_instruction_nr(opcode)
        return self.instructions[nr]

    def get_arg(self, nr, size=0, decrypt=True):
        v = 0
        for i in range(2**size):
            v += (self.current_instr[nr+i] << (8*i))
        if decrypt:
            v = self.decrypt(v, size)
        return v

    def _ror(self, value, shift):
        return (value & (2**shift - 1)) << (64-shift) | (value >> shift)

    def extract_sub(self, value, f, t=None):
        if t:
            return (value >> f) & (2**(t-f) - 1)
        else:
            return (value >> f)

    def sizename(self, v):
        return {0: "byte", 1: "word", 2: "dword", 3: "qword"}[v]

    def addr(self, reg):
        return "addr({})".format(reg)

    def _op(self, v, opr, sym):
        if len(v) == 2:
            a,b = v
            if type(a) == int and type(b) == int:
                return opr(a,b)
            else:
                if len(sym) == 1:
                    return "{0}{1}{2}".format(self._h(a), sym, self._h(b))
                else:
                    return "{1} {0}, {2}".format(self._h(a), sym, self._h(b))
        else:
            a = v
            if type(a) == int:
                return opr(a)
            else:
                return "{} {}".format(sym, self._h(a))

    def pseudoinstrwithsize(self, instr, size=None, arg=""):
        assert(size is None or type(size) == int)
        sizename = self.sizename(size) if size is not None else ""
        return "{} {} {}".format(instr, sizename.lower(), arg)

    def targetregister(self, assemblyline):
        m = re.search("[^,]+\s+([^,\s]+),[^,]+$", assemblyline)
        if m:
            return m.group(1)
        m = re.search("\s*([^\s]+)$", assemblyline)
        if m:
            return m.group(1)

    def sourceregister(self, assemblyline):
        m = re.search("[^,]+\s+[^,\s]+,\s*([^,]+)$", assemblyline)
        if m:
            return m.group(1)
        m = re.search("\s*([^\s]+)$", assemblyline)
        if m:
            return m.group(1)

    def supercast(self, v):
        m = re.search("(r\d+)", v)
        if m:
            return m.group(1)

        m = re.match("[re]?([abcdsdbsi])([xpil])$", v)
        if m:
            return "r{}{}".format(m.group(1), m.group(2))

    def checktainted(self, assembly):
        tainted = set()
        for a in assembly:
            src = self.sourceregister(a)
            dst = self.targetregister(a)
            if src in tainted:
                return True
            tainted.add(dst)
        return False


    def dontrealize(self, target, assembly):
        if len(assembly) == 1:
            return assembly

        targets = set()
        for a in assembly[:-1]:
            targets.add(self.targetregister(a))

        if len(targets) == 0:
            return assembly

        prevtarget = targets.pop()

        newassembly = []
        target = self.supercast(target)
        prevtarget = self.supercast(prevtarget)
        fixed = False
        if target != prevtarget:
            newassembly.append("MOV {}, {}".format(target, prevtarget))
            for a in assembly[:-1]:
                newassembly.append(self.assembly.replaceregister(a, prevtarget, target))
            a = assembly[-1]
            newassembly.append(self.assembly.replaceregister(a, prevtarget, target, target=False))
            if self.assembly.isempty(newassembly[-1]):
                newassembly = newassembly[:-1]

            if self.checktainted(newassembly):
                pass
            else:
                fixed = True
        if not fixed:
            newassembly = []
            tmp = "r15"
            newassembly.append("MOV [rsp-1000], {}".format(tmp))
            newassembly.append("MOV {}, {}".format(tmp, prevtarget))
            for a in assembly:
                newassembly.append(self.assembly.replaceregister(a, prevtarget, tmp))
            newassembly.append("MOV {}, {}".format(target, tmp))
            newassembly.append("MOV r15, [rsp-1000]")

        return newassembly

    def signed(self, v, size):
        if type(v) != int:
            return v
        ra = (1 << (2**size)*8)
        assert(0 <= v < ra)
        if v >= ra//2:
            return v - ra
        else:
            return v

    def addr2datalabel(self, v):
        return "data_{:016X}".format(v)

    def datalabel(self, v, create=True):
        v += self.mz
        if v not in self.data:
            if not create:
                raise RuntimeError("Got unnamed data offset: {:016X}".format(v))
            else:
                self.data[v] = ("db", "?")
        return self.addr2datalabel(v)

    def randomlabel(self):
        letters = string.ascii_lowercase
        return ''.join([random.choice(letters) for _ in range(10)])

    def decrypt(self, v, size):
        if size == 0:
            return v ^ 0x57
        elif size == 1:
            return v ^ 0x13F1
        elif size == 2:
            return v ^ 0x69B00B7A
        elif size == 3:
            return v ^ 0x7EF5142A570C5298

    def offsetted_value(self, value):
        if self.state1 == 2:
            if self.state2 == 1:
                value = self.decrypt(value, 3)
                value += self.offset
        else:
            value = self.decrypt(value, 3)
        return value

    def check_flags(self, arg):
        flag_selection = arg & 63
        flags = {0: "CF", 1: "PF", 2: "AF", 3: "ZF", 4: "SF", 5: "OF"}

        selected = []
        for k,v in flags.items():
            if flag_selection & (2**k):
                selected.append(v)

        if not arg & 0x40:
            if arg & 0x80:
                return " & ".join(selected)
            else:
                return "NOT " + " | ".join(selected)
        if arg & 0x80:
            return "({}) OR NOT ({})".format(" & ".join(selected), " | ".join(selected))
        else:
            return "NOT ({}) AND ({})".format(" & ".join(selected), " | ".join(selected))

    def instruction_00(self):
        if self.variant:
            size = self.get_arg(1)
            if size not in [0, 2, 3]:
                raise NotImplementedError("not implemented by VM")
            length = 2
        else:
            size = 2
            length = 1
        dis = self.pseudoinstrwithsize("XOR", size)
        self.assembly.arithmetic("XOR", size=size)
        return (length, dis)

    def instruction_01(self, pop=1):
        if self.subvariant:
            if self.variant:
                arg1 = self.get_arg(1)
                size = self.extract_sub(arg2, 0, 2)
                b = self.extract_sub(arg1, 2)
                if b not in [0, 6]:
                    raise RuntimeError("cant write to gs or fs segments")
                argnr = 2
            else:
                argnr = 1
                size = 3

            value = self.get_arg(argnr, size=3, decrypt=False)
            value = self.offsetted_value(value)

            if self.variant:
                length = 6
            else:
                length = 5

            if b:
                raise NotImplementedError("writing to segment %d", b)

            if pop:
                mnemonic = "P2V"
            else:
                mnemonic = "M2V"
        else:
            if self.variant:
                arg1 = self.get_arg(1)
                size = self.extract_sub(arg1, 0, 2)
                b = self.extract_sub(arg1, 2)
                if size == 2:
                    pass
                length = 2
                if b not in [0, 6]:
                    raise RuntimeError("cant write to gs or fs segments")
            else:
                size = 2
                length = 1

            if pop:
                mnemonic = "P2E"
            else:
                mnemonic = "M2E"


        if pop:
            h, l = self.stack.pop(both=True)
        else:
            h, l = self.stack.get(both=True)

        if self.subvariant:
            dst = value
        else:
            dst = self.assembly.dref(l)
        dis = self.pseudoinstrwithsize(mnemonic, size, dst[0])
        _, assembly = self.assembly.buildinstruction("MOV", size, dst, h)
        if not pop:
            h = (h[0], [])
            self.stack.set(h)

        return (length, dis, assembly)

    def instruction_02(self):
        assembly = []
        length = 1
        if self.variant:
            reg = self.context.get_register_name(1, 4, 0)    # r_rsp
            reg2 = self.context.get_register_name(1, 18, 0)  # vm_ip

        pp  = self.stack.pop()
        a = pp[0]
        assembly.extend(pp[1])

        if self.variant:
            self.add_chain(a, label=self.randomlabel())
        else:
            self.add_chain(a)

        if a == "[rsp]":
            assembly.extend(["RET"])
            dis = "RET"
            self.current_chain["done"] = True
            return (1, dis, assembly)

        if not self.subvariant and type(a) == int and self.imagebase <= a <= self.imagebase + self.lastaddr: 
            # means leave the VM
            pass

        if self.variant:
            dis = "CALL"
        else:
            dis = "JMP"
            self.current_chain["done"] = True
            length = 0

        if type(a) == int:
            assembly.extend(["{} {}".format(dis, self.label(a))])
        else:
            assembly.extend(["{} {}".format(dis, a)])
        return (length, dis, assembly)

    def instruction_03(self):
        if not self.variant:
            dis = "POPD"
            v = self.stack.pop()
            if v[1]:
                return (1, dis, v[1])
            else:
                return (1, dis)
        else:
            nr = self.get_arg(1)
            dis = self.pseudoinstrwithsize("POP", arg=nr)
            extras = []
            for i in range(nr):
                v = self.stack.pop()
                if v[1]:
                    extras.extend(v[1])
            if extras:
                return (2, dis, extras)
            else:
                return (2, dis)

    def instruction_04(self):
        if self.subvariant:
            """ DEREF from VALUE """
            size = 3
            if not self.variant:
                value = self.get_arg(1, size=size, decrypt=False)
                signed = False
            else:
                arg1 = self.get_arg(1)
                size = self.extract_sub(arg1, 0, 2)
                signed = self.extract_sub(arg1, 2, 3)
                if size == 3:
                    value = self.get_arg(2, size=3, decrypt=False)
                else:
                    value = self.get_arg(2, size=3, decrypt=True)

            if size == 3:
                value = self.offsetted_value(value)

            length = 1 + 2**size
            if self.variant:
                length += 1
        else:
            """ DEREF From stack """
            if self.variant:
                arg1 = self.get_arg(1)
                size = self.extract_sub(arg1, 0, 2)
                signed = self.extract_sub(arg1, 2, 3)
                segment = self.extract_sub(arg1, 3, 6) # the segment

                if not segment in [0]:
                    raise NotImplementedError("cannot handle segments")

                length = 2
            else:
                size = 2
                length = 1
                signed = False

        if self.subvariant:
            dis = self.pseudoinstrwithsize("DREFH", size, value)
        else:
            dis = self.pseudoinstrwithsize("DREFH", size)

        if not self.subvariant:
            t = self.stack.get()
        else:
            t = value
        self.stack.set(t, low=True)
        dr = self.assembly.dref(t)
        self.stack.set(dr)
        return (length, dis)

    def instruction_05(self):
        if self.variant:
            size = self.get_arg(1)
            length = 2
        else:
            size = 2
            length = 1

        dis = self.pseudoinstrwithsize("SBB", size)
        assembly = self.assembly.arithmetic("SBB", size=size, op=operator.sub, inlinesym="-")
        return (length, dis, assembly)

    def instruction_06(self):
        arg1 = self.get_arg(1)
        cond1 = self.check_flags(arg1)

        if self.variant:
            arg2 = self.get_arg(2, decrypt=True)
            cond2 = self.check_flags(arg2)
            if self.subvariant:
                cond = "IF {} AND {}".format(cond1, cond2)
            else:
                cond = "IF {} OR {}".format(cond1, cond2)
            length = 3
            argnr = 3
        else:
            argnr = 2
            cond = cond1
            length = 2

        value = self.get_arg(argnr, size=3, decrypt=False)
        length += 8

        if cond == "NOT SF":
            ins = "JNS"
        elif cond == "SF":
            ins = "JS"
        elif cond == "(SF & OF) OR NOT (SF | OF)": # SF == OF
            ins = "JGE"
        elif cond == "NOT ZF":
            ins = "JNZ"
        elif cond == "NOT (SF & OF) AND (SF | OF)":
            ins = "JL"
        elif cond == "IF ZF OR NOT (SF & OF) AND (SF | OF)":
            ins = "JLE"
        elif cond == "ZF":
            ins = "JZ"
        elif cond == "CF":
            ins = "JB"
        else:
            raise ValueError("unknown condition: {}".format(cond))

        target = self.offsetted_value(value)

        assembly = ["{} {}".format(ins, self.label(target))]
        dis = "IF {} -> {}".format(cond, "JMP 0x{:016X}".format(target))
        self.add_chain(target)
        return (length, dis, assembly)

    def instruction_07(self):
        dis = "NOP"
        return (1, dis)

    def instruction_08(self):
        if self.variant:
            size = self.get_arg(1)
            if size not in [2,3]:
                raise NotImplementedError("0, 1 will just NOP")
            length = 2
        else:
            length = 1
            size = 2

        dis = self.pseudoinstrwithsize("MUL", size)
        assembly = self.assembly.arithmetic("MUL", size=size, onstack=False, keep=False, nr=1)
        return (length, dis, assembly)

    def instruction_09(self):
        value = self.stack.pop()
        if self.variant:
            size = self.get_arg(1)
            if size not in [2,3]:
                raise NotImplementedError("0, 1 will just NOP")
            length = 2
        else:
            length = 1
            size = 2

        dis = self.pseudoinstrwithsize("DIV", size)
        assembly = self.assembly.arithmetic("DIV", size=size, onstack=False, keep=False, nr=1)
        return (length, dis, assembly)

    def instruction_0A(self):
        value1 = self.stack.get(low=True, index=0)
        value2 = self.stack.get(low=True, index=1)

        self.stack.set(value2, low=True, index=0)
        self.stack.set(value1, low=True, index=1)

        dis = "STACKSWP"
        return (1, dis)

    def instruction_0B(self):
        length = 1

        arg = 2
        if self.variant:
            arg = self.get_arg(1)
            length += 1

        if self.subvariant:
            if arg == 1:
                dis = "CWD"
            elif arg == 2:
                dis = "CDQ"
            elif arg == 3:
                dis = "CQO"
        else:
            if arg == 1:
                dis = "CBW"
            elif arg == 2:
                dis = "CWDE"
            elif arg == 3:
                dis = "CDQE"

        assembly = [dis]
        return (length, dis, assembly)

    def instruction_0C(self):
        arg1 = self.get_arg(1)
        a = self.extract_sub(arg1, 0, 2)
        b = self.extract_sub(arg1, 2, 5)
        c = self.extract_sub(arg1, 5, 8)
        return (2, "TRIPLE")

    def instruction_0D(self):
        if self.variant:
            size = self.get_arg(1)
            length = 2
        else:
            size = 2
            length = 1

        assembly = []
        a = self.stack.get(index=1)
        b = self.stack.get(index=0)

        if a[0] != "rdx":
            if a[1]:
                assembly.append(a[1])
            assembly.append("MOV rdx, {}".format(a[0]))
        if b[0] != "rax":
            if b[1]:
                assembly.append(b[1])
            assembly.append("MOV rax, {}".format(b[0]))

        self.stack.set(["rdx",[]], index=0)
        self.stack.set(["rax",[]], index=1)
        #a = ('rdx', [])
        dst, assembly2 = self.assembly.buildinstruction("IMUL", size, a)
        assembly = assembly + assembly2
        dis = self.pseudoinstrwithsize("IMUL", size)
        if assembly:
            return (length, dis, assembly)
        else:
            return (length, dis)

    def instruction_0E(self):
        if not self.variant:
            size = 2
            length = 1
            self.assembly.arithmetic("NEG", size=2, nr=1)
        else:
            size = self.get_arg(1)
            length = 2
            self.assembly.arithmetic("NEG", size=size, nr=1)

        dis = self.pseudoinstrwithsize("NEG", size)
        return (length, dis)

    def instruction_0F(self):
        if self.variant:
            size = self.get_arg(1)
            length = 2
        else:
            size = 2
            length = 1
        dis = self.pseudoinstrwithsize("SUB", size)
        self.assembly.arithmetic("SUB", size=size)
        return (length, dis)

    def instruction_10(self):
        if not self.variant:
            size = 2
            length =1
        else:
            size = self.get_arg(1)
            length = 2
        dis = self.pseudoinstrwithsize("OR", size)
        self.assembly.arithmetic("OR", size=size)
        return(length, dis)

    def instruction_11(self):
        size = 2
        opcodes = 1
        if self.variant:
            size = self.get_arg(1)
            opcodes += 1
        if not self.subvariant:
            dis = self.pseudoinstrwithsize("DEC", size)
            self.assembly.arithmetic("DEC", size=size, nr=1)
        else:
            dis = self.pseudoinstrwithsize("INC", size)
            self.assembly.arithmetic("INC", size=size, nr=1)
        return (opcodes, dis)

    def instruction_12(self):
        arg1 = self.get_arg(1)
        regidx = self.extract_sub(arg1, 0, 5)
        size = self.extract_sub(arg1, 5, 7)
        c = self.extract_sub(arg1, 7)
        reg = self.context.get_register_name(size, regidx, c)

        if self.variant:
            """ PUSH """
            if self.subvariant:
                """ push address of register """
                arg = "(addr({0}), addr({0}))".format(reg)
                self.stack.push(self.addr(reg), self.addr(reg))
            else:
                """ push register """
                arg = "({0}, addr({0}))".format(reg)
                self.stack.push(reg, self.addr(reg))
            dis = self.pseudoinstrwithsize("PUSH", size, arg)
            return (2, dis)
        else:
            length = 2
            """ POP """
            dis = self.pseudoinstrwithsize("POP", size, reg)
            src = self.stack.pop()
            dst = reg, []
            target, assembly = self.assembly.buildinstruction("MOV", size, dst, src)
            assembly = self.dontrealize(target, assembly)
            return (length, dis, assembly)

    def instruction_13(self):
        if not self.variant:
            size = 2
            opcodes = 1
        else:
            arg1 = self.get_arg(1)
            size = arg1
            opcodes = 2

        dis = self.pseudoinstrwithsize("CMP", size)
        assembly = self.assembly.arithmetic("CMP", size=size, onstack=True, keep=False)
        return (opcodes, dis, assembly)

    def instruction_14(self):
        reg = self.context.get_register_name(1, 24, 0)
        dis = self.pseudoinstrwithsize("SET1", arg=reg)
        return (1, dis)

    def instruction_15(self):
        if self.subvariant:
            if self.variant:
                dis = "MDIAGA"
            else:
                dis = "MDIAG"
            x = self.stack.get()
        else:
            if self.variant:
                dis = "PDIAGA"
            else:
                dis = "PDIAG"
            x = self.stack.pop()
        if self.variant:
            x = self.addr(x)
        self.stack.set(x, low=True)
        return (1, dis)

    def instruction_16(self):
        self.state1 = 1
        self.state2 = self.variant
        dis = self.pseudoinstrwithsize("STATE", arg=self.variant)
        return (1, dis)

    def instruction_17(self):
        if self.variant:
            size = self.get_arg(1)
            length = 2
        else:
            length = 1
            size = 2
        dis = self.pseudoinstrwithsize("ADD", size)
        self.assembly.arithmetic("ADD", size=size)
        return (length, dis)

    def instruction_18(self):
        if self.variant:
            arg1 = self.get_arg(1)
            size = self.extract_sub(arg1, 0, 2)
            signed = self.extract_sub(arg1, 2, 3)
            if size == 3:
                value = self.get_arg(2, size=size, decrypt=False)
                value = self.offsetted_value(value)
            else:
                value = self.get_arg(2, size=size, decrypt=True)


            if not signed and size == 2 and self.state1 == 2:
                value = self.datalabel(value)
        else:
            signed = False
            size = 2
            value = self.get_arg(1, size=size)
            if self.state1 == 2:
                value = self.datalabel(value)

        if signed:
            value = self.signed(value, size)
        if type(value) == int:
            arg = "({0:X}h, {0:X}h)".format(value)
        else:
            arg = "({0}, {0})".format(value)
        dis = self.pseudoinstrwithsize("PUSH", size, arg)
        self.stack.push(value)
        return (1 + self.variant + 2**size, dis)

    def instruction_19(self):
        """ see instruction 01 """
        return self.instruction_01(pop=0)

    def instruction_1A(self):
        """ DC """
        if not self.variant:
            length = 1
            size = 2
        else:
            length = 2
            size = self.get_arg(1)

        dis = self.pseudoinstrwithsize("NOT", size)
        assembly = self.assembly.arithmetic("NOT", size=size, nr=1)
        return (length, dis, assembly)

    def instruction_1B(self):
        if not self.variant:
            length = 1
            size = 2
        else:
            length = 2
            size = self.get_arg(1)

        dis = self.pseudoinstrwithsize("AND", size)
        self.assembly.arithmetic("AND", size=size)
        return (length, dis)

    def instruction_1C(self):
        if self.subvariant:
            direction = "L"
        else:
            direction = "R"

        if not self.variant:
            size = 2
            b = 0
            length = 1
        else:
            arg1 = self.get_arg(1)
            size = self.extract_sub(arg1, 0, 2)
            b = self.extract_sub(arg1, 2)
            length = 2

        if b == 0:
            line = "SH"
        elif b == 2:
            line = "RO"
        elif b == 3:
            line = "SA"
        else:
            raise ValueError()

        line += direction
        self.assembly.arithmetic(line, size=size)
        dis = self.pseudoinstrwithsize(line, size)
        return (length, dis)

    def instruction_28(self):
        return (5, "NOP")

    def _set_eflags_from_vm(self):
        reg1 = self.context.get_register_name(1, 16, 0)
        return "EFLAGS = {}".format(reg1)

    def _set_eflags_to_vm(self):
        reg = self.context.get_register_name(1, 24, 0)
        reg1 = self.context.get_register_name(1, 16, 0)
        return "IF {0} == 1 THEN {0} = 0 ELSE {1} = EFLAGS".format(reg, reg1)

    def _addr_range(self):
        return [self.imagebase, self.imagebase + len(self.code)]




