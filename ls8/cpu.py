"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.running = False
        self.op_size = 0
        self.pc = 0
        self.sp = 7
        self.reg = [0]* 10
        self.ram = [0] * 256
        self.cmds = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100000: self.ADD
        }
    def LDI(self, op1, op2):
        self.reg[op1]= op2
    def PRN(self, op1, op2):
        print(self.reg[op1])
    def HLT(self, op1, op2):
        self.running = False
    def ADD(self, op1, op2):
        self.alu('ADD', op1, op2)
    def MULT(self, op1, op2):
        self.alu('MUL', op1, op2)
    def PUSH(self, op1, op2):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.reg[op1])
    def POP(self, op1, op2):
        self.reg[op1]= self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1
    def CALL(self, op1, op2):
        self.reg[self.sp] -= 1
        self.ram_write(self.reg[self.sp], self.pc + 2)
        self.pc = self.reg[op1]
        self.op_size = 0
    def RET(self, op1, op2):
        self.pc = self.ram_read(self.reg[self.sp])
        self.reg[self.sp] += 1

        self.op_size = 0



    def load(self, filename):
        """Load a program into memory."""

        MAR = 0

        try:
            with open(filename) as f:
                for line in f:
                    line = line.split('#')
                    n = line[0].strip()

                    if n == '':
                        continue

                    MDR = int(n, 2)

                    self.ram_write(MAR, MDR)
                    MAR += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")
    def ram_read(self, MAR):
        return self.ram[MAR]
    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR
        return self.ram[MAR]
    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        self.load(sys.argv[1])

        self.running = True

        while self.running:

            cmd = self.ram_read(self.pc)

            op1 = self.ram_read(self.pc + 1)
            op2 = self.ram_read(self.pc + 2)

            self.op_size = (cmd >> 6) + 1

            # DECODE
            if cmd in self.cmds:

                # EXECUTE
                self.cmds[cmd](op1, op2)

            else:
                print(f"Invalid Instruction: {cmd:b}")
                self.running = False

            self.pc += self.op_size
cpu = CPU()
cpu.run()
