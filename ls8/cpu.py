"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0]* 10
        self.ram = [0] * 256
        self.cmds = {
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b00000001: "HLT"
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    def ram_read(self, pc):
        return self.ram[pc]
    def ram_write(self, address, value):
        self.ram[address] = value
        return self.ram[address]
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
        """Run the CPU."""
        self.load()
        running = True
        while running:
            cmd = self.ram[self.pc]
            op_size = (cmd >> 6) + 1
            if self.cmds[cmd]== "LDI":
                reg_index = self.ram[self.pc + 1]
                num = self.ram[self.pc + 2]
                self.reg[reg_index] = num
            elif self.cmds[cmd]== "PRN":
                reg_index = self.ram[self.pc + 1]
                num = self.reg[reg_index]
                print(num)
            
            elif self.cmds[cmd]== "HLT":
                running = False
            self.pc += op_size
cpu = CPU()
cpu.run()
