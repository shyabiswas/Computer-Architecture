"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.sp = 7
        self.reg = [0]* 10
        self.ram = [0] * 256
        self.cmds = {
            0b10000010: "LDI",
            0b01000111: "PRN",
            0b00000001: "HLT",
            0b10100010: "MUL",
            0b01000101: "PUSH",
            0b01000110: "POP"
        }

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

                    value = int(n, 2)

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

        running = True

        while running:

            # FETCH
            cmd = self.ram_read(self.pc)
            op_size = (cmd >> 6) + 1

            # DECODE
            if self.cmds[cmd] == 'LDI':
                # EXECUTE
                reg_index = self.ram_read(self.pc + 1)
                num = self.ram_read(self.pc + 2)
                self.reg[reg_index] = num

            elif self.cmds[cmd] == 'PRN':
                reg_index = self.ram_read(self.pc + 1)
                num = self.reg[reg_index]
                print(num)

            elif self.cmds[cmd] == 'MUL':
                num1_index = self.ram_read(self.pc + 1)
                num2_index = self.ram_read(self.pc + 2)
                self.alu('MUL', num1_index, num2_index)
            elif self.cmds[cmd] == 'PUSH':
                reg_index = self.ram_read(self.pc + 1)
                value = self.reg[reg_index]

                self.reg[self.sp] -= 1

                self.ram_write(self.reg[self.sp], value)

            elif self.cmds[cmd] == 'POP':
                reg_index = self.ram_read(self.pc + 1)
                value = self.ram_read(self.reg[self.sp])

                self.reg[reg_index] = value

                self.reg[self.sp] += 1

            elif self.cmds[cmd] == 'HLT':
                running = False

            self.pc += op_size
cpu = CPU()
cpu.run()
