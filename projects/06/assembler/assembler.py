class Parser():
    def __init__(self, file):
        with open(file) as f:
            self.commands = f.readlines()
            for i in range(len(self.commands)):

                comment = self.commands[i].find("//")
                if comment != -1:
                    self.commands[i] = self.commands[i][:comment]
                self.commands[i] = self.commands[i].replace(" ", "")
                self.commands[i] = self.commands[i].replace("\n", "")

            self.commands = [i for i in self.commands if i != ""]
            self.current = self.commands[0]
            self.num_com = len(self.commands)
            self.count = 0
            self.eq_pos = self.current.find("=")
            self.sc_pos = self.current.find(";")
            self.rom_num = 0

    def hasMoreCommands(self):
        if self.count + 1 >= self.num_com:
            return False
        else:
            return True

    def advance(self):
        if self.hasMoreCommands():
            self.count += 1
            self.current = self.commands[self.count]
            self.eq_pos = self.current.find("=")
            self.sc_pos = self.current.find(";")

    def commandType(self):
        if self.current[0] == "(":
            return "L"
        elif self.current[0] == "@":
            return "C"
        else:
            return "A"

    def dest(self):
        if self.eq_pos != -1:
            return self.current[:self.eq_pos]
        else:
            return None

    def comp(self):
        if self.eq_pos == -1:
            return self.current[:self.sc_pos]
        elif self.sc_pos == -1:
            return self.current[self.eq_pos + 1:]
        else:
            return self.current[self.eq_pos + 1:self.sc_pos]

    def jump(self):

        if self.sc_pos != -1:
            return self.current[self.sc_pos + 1:]
        else:
            return None

    def c_symbol(self):
        try:
            return int(self.current[1:])
        except  ValueError:
            return self.current[1:]

    def l_symbol(self):
        return self.current[1:-1]


class Code():
    def dest(self, p):
        d = p.dest()
        if d == None:
            return "000"
        elif d == "M":
            return "001"
        elif d == "D":
            return "010"
        elif d == "MD" or d == "DM":
            return "011"
        elif d == "A":
            return "100"
        elif d == "AM" or d == "MA":
            return "101"
        elif d == "AD" or d == "DA":
            return "110"
        elif d == "ADM" or d == "AMD" or d == "DAM" or d == "DMA" or d == "MDA" or d == "MAD":
            return "111"

    def comp(self, p):
        c = p.comp()

        if c == "0":
            return "0101010"
        elif c == "1":
            return "0111111"
        elif c == "-1":
            return "0111010"
        elif c == "D":
            return "0001100"
        elif c == "A":
            return "0110000"
        elif c == "!D":
            return "0001101"
        elif c == "!A":
            return "0110001"
        elif c == "-D":
            return "0001111"
        elif c == "-A":
            return "0110011"
        elif c == "D+1":
            return "0011111"
        elif c == "A+1":
            return "0110111"
        elif c == "D-1":
            return "0001110"
        elif c == "A-1":
            return "0110010"
        elif c == "D+A":
            return "0000010"
        elif c == "D-A":
            return "0010011"
        elif c == "A-D":
            return "0000111"
        elif c == "D&A":
            return "0000000"
        elif c == "D|A":
            return "0010101"
        elif c == "M":
            return "1110000"
        elif c == "!M":
            return "1110001"
        elif c == "-M":
            return "1110011"
        elif c == "M+1":
            return "1110111"
        elif c == "M-1":
            return "1110010"
        elif c == "D+M":
            return "1000010"
        elif c == "D-M":
            return "1010011"
        elif c == "M-D":
            return "1000111"
        elif c == "D&M":
            return "1000000"
        elif c == "D|M":
            return "1010101"

    def jump(self, p):
        j = p.jump()
        if j == None:
            return "000"
        elif j == "JGT":
            return "001"
        elif j == "JEQ":
            return "010"
        elif j == "JGE":
            return "011"
        elif j == "JLT":
            return "100"
        elif j == "JNE":
            return "101"
        elif j == "JLE":
            return "110"
        elif j == "JMP":
            return "111"

    def c_bin(self, p, st):
        if type(p.c_symbol()) is int:
            return format(p.c_symbol(), "015b")
        else:
            return format(st.s_table[p.c_symbol()], "015b")


class STable():
    def __init__(self):
        self.s_table = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
                        "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4, "R5": 5, "R6": 6,
                        "R7": 7, "R8": 8, "R9": 9, "R10": 10, "R11": 11, "R12": 12,
                        "R13": 13, "R14": 14, "R15": 15, "SCREEN": 16384, "KBD": 24576}
        self.c_num = 16
        self.l_num = 0

    def contains(self, symbol):
        if list(self.s_table.keys()).count(symbol) == 1:
            return True
        else:
            return False

    def addEntry(self, symbol, order):
        if not self.contains(symbol):
            if order == "C":
                self.s_table[symbol] = self.c_num
                self.c_num += 1
            elif order == "L":

                self.s_table[symbol] = self.l_num

    def getAddress(self, symbol):
        return self.s_table[symbol]


def assembler(asm_file, hack_file):
    p = Parser(asm_file)
    c = Code()
    st = STable()

    ## labeling & symbol translation
    while True:
        if p.commandType() == "A":
            st.l_num += 1

        elif p.commandType() == "L":
            st.addEntry(p.l_symbol(), "L")

        elif p.commandType() == "C":
            st.l_num += 1

        if not p.hasMoreCommands():
            p.count = 0
            p.current = p.commands[0]
            break
        p.advance()

    while True:
        if p.commandType() == "A":
            pass

        elif p.commandType() == "L":
            pass

        elif p.commandType() == "C":
            if type(p.c_symbol()) is int:
                pass
            else:
                if not st.contains(p.c_symbol()):
                    st.addEntry(p.c_symbol(), "C")

        if not p.hasMoreCommands():
            p.count = 0
            p.current = p.commands[0]
            break
        p.advance()
    print(st.s_table)
    ## encoding
    binary_codes = []
    while True:
        print(p.current)
        if p.commandType() == "A":

            s = "111" + c.comp(p) + c.dest(p) + c.jump(p)
            binary_codes.append(s)
        elif p.commandType() == "C":
            s = "0" + c.c_bin(p, st)
            binary_codes.append(s)

        if not p.hasMoreCommands():
            p.count = 0
            p.current = p.commands[0]
            break

        p.advance()

    with open(hack_file, mode='w') as f:
        f.write('\n'.join(binary_codes))

assembler("/Users/manako/nand2tetris/projects/06/add/Add.asm", "/Users/manako/nand2tetris/projects/06/add/Add2.hack")
assembler("/Users/manako/nand2tetris/projects/06/max/Max.asm", "/Users/manako/nand2tetris/projects/06/max/Max2.hack")
assembler("/Users/manako/nand2tetris/projects/06/max/MaxL.asm", "/Users/manako/nand2tetris/projects/06/max/MaxL2.hack")
assembler("/Users/manako/nand2tetris/projects/06/rect/Rect.asm", "/Users/manako/nand2tetris/projects/06/rect/Rect2.hack")
assembler("/Users/manako/nand2tetris/projects/06/rect/RectL.asm", "/Users/manako/nand2tetris/projects/06/rect/RectL2.hack")
assembler("/Users/manako/nand2tetris/projects/06/pong/Pong.asm", "/Users/manako/nand2tetris/projects/06/pong/Pong2.hack")
assembler("/Users/manako/nand2tetris/projects/06/pong/PongL.asm", "/Users/manako/nand2tetris/projects/06/pong/PongL2.hack")
