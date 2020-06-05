class Formula: 
    def __init__(self, expression, precedence): 
        self.top = -1 
        self.stack = [] 
        self.precedence = precedence
        self.original_expression = expression
        self.operator_positions_in_original_expression = []
        self.formula = [] 
        self.operands = set()
        self._generatePostfixFormula(expression)
        self._tmp_results = []

    def _isOperand(self, ch): 
        return ch.isalpha() 
  
    def _notGreater(self, i): 
        try: 
            a = self.precedence[i] 
            b = self.precedence[self.stack[-1][0]]
            return True if a  <= b else False
        except KeyError:  
            return False
              
    def _generatePostfixFormula(self, exp):
        act_pos = -1
        for i in exp:
            act_pos += 1 
            if i == " ":
                continue
            if self._isOperand(i): 
                self.operands.add(i)
                self.formula.append(i) 
            elif i  == '(': 
                self.stack.append((i, act_pos)) 
            elif i == ')': 
                while(len(self.stack) > 0 and self.stack[-1][0] != '('): 
                    a, pos = self.stack.pop() 
                    self.formula.append(a) 
                    self.operator_positions_in_original_expression.append(pos)
                if (len(self.stack) > 0 and self.stack[-1][0] != '('): 
                    return -1
                else: 
                    self.stack.pop()
            else: 
                while(len(self.stack) > 0 and self._notGreater(i)): 
                    a, pos = self.stack.pop()
                    self.formula.append(a) 
                    self.operator_positions_in_original_expression.append(pos)
                self.stack.append((i, act_pos)) 
        while len(self.stack) > 0: 
            a, pos = self.stack.pop()
            self.formula.append(a) 
            self.operator_positions_in_original_expression.append(pos)
        self.operands = sorted(list(self.operands))

    def _solve_operator(self, operator):
        pass

    def solve(self, operands_values):
        self._tmp_results = []
        for act in self.formula:
            if self._isOperand(act):
                self.stack.append(operands_values[act])
            else:
                self.stack.append(self._solve_operator(act))
                self._tmp_results.append(self.stack[-1])
        return self.stack.pop()

    def _generate_table_header(self):
        res = ""
        for op in self.operands:
            res += op + " "
        res = res[:len(res) - 1]
        res += " | " + self.original_expression + " | Ergebniss"
        res += "\n" + "─" * len(self.operands) * 2 + "┼" + "─" * (len(self.original_expression) + 2) + "┼" + "─" * 10 + "\n"
        return res

    def _generate_table_row(self, operands_values, result):
        res = ""
        for op in self.operands:
            res += str(operands_values[op]) + " "
        res = res[:len(res) - 1]
        res += " | " + self._generate_tmp_result_string() + " | " + str(result) + "\n"
        return res

    def _generate_tmp_result_string(self):
        res = [" "] * len(self.original_expression)
        for i in range(len(self._tmp_results)):
            res[self.operator_positions_in_original_expression[i]] = str(self._tmp_results[i])
        return "".join(res)

    def _generate_operands_values(self):
        pass

    def generate_table(self):
        table = self._generate_table_header()
        for values in self._generate_operands_values():
            result = self.solve(values)
            table += self._generate_table_row(values, result)
        return table

class LogicFormula(Formula):
    def __init__(self, expression):
        super(LogicFormula, self).__init__(expression, {'↔': 1, '→': 2, '⊕': 3, '∨': 4, '∧': 5, '¬': 6})

    def _solve_operator(self, operator):
        if operator == "¬":
            return (self.stack.pop() + 1) % 2
        if operator == "∧":
            return self.stack.pop() * self.stack.pop()
        if operator == "∨":
            op2 = self.stack.pop()
            op1 = self.stack.pop()
            return op1 + op2 - (op1 * op2)
        if operator == "⊕":
            return (self.stack.pop() + self.stack.pop()) % 2
        if operator == "→":
            op2 = self.stack.pop()
            op1 = self.stack.pop()
            return 0 if op1 == 1 and op2 == 0 else 1
        if operator == "↔":
            return (self.stack.pop() + self.stack.pop() + 1) % 2
    
    def _generate_operand_values(self, binString):
        res = {}
        for i in range(len(self.operands)):
            res[self.operands[i]] = int(binString[i])
        return res

    def _generate_operands_values(self):
        res = []
        for i in range(2**len(self.operands)):
            binString = bin(i).replace("0b", "").zfill(len(self.operands))
            res.append(self._generate_operand_values(binString))
        return res

    def generate_KVDiagram(self):
        muster = self._generate_KVMuster()
        row_prefs = self._generate_KVDiagram_colheader()
        res = self._generate_KVDiagram_header(len(row_prefs[0]))
        res += row_prefs[0] + "┌" + "──┬" * (len(muster[0]) - 1) + "──┐\n"
        for i in range(len(muster)):
            res += row_prefs[2*i + 1] + "|"
            for cell in muster[i]:
                values = self._generate_KV_operands_values(cell)
                res += "██|" if self.solve(values) == 1 else "  |"
            if muster[i] != muster[-1]:
                res +=  "\n" + row_prefs[2*i + 2] + "├" + "──┼" * (len(muster[0]) - 1) + "──┤\n"
        res += "\n" + row_prefs[-1] + "└" + "──┴" * (len(muster[0]) - 1) + "──┘\n"
        return res
                
    def _generate_KVDiagram_header(self, offset):
        width = 3 * 2**(round(len(self.operands) / 2, 0))
        res = []
        for i in range(int(round(len(self.operands) / 2, 0))):
            base = "   " * 2**i + "───" * 2**i
            while len(base) < width:
                base = base + "".join(reversed(base))
            res.append(" " * offset + str(self.operands[2*i]) + base)
        return "\n".join(reversed(res)) + "\n"
    
    def _generate_KVDiagram_colheader(self):
        height = 2 * 2**(len(self.operands) // 2)
        res = [[] for _ in range(height + 1)]
        for i in range(len(self.operands) // 2):
            base = "  " * 2**i + "||" * 2**i
            while len(base) < height:
                base = base + "".join(reversed(base))
            base = str(self.operands[2*i + 1]) + base
            for row in range(len(base)):
                res[row].append(base[row])
        return ["".join(reversed(x)) for x in res]

    def _generate_KV_operands_values(self, cell):
        res = {}
        for key in self.operands:
            res[key] = 0
        for i in cell:
            res[self.operands[i]] = 1
        return res

    def _generate_KVMuster(self, base = None, level=0):
        if base is None:
            base = [[set()]]
        if level == len(self.operands):
            return base
        if len(base) == len(base[0]):
            return self._generate_KVMuster(self._mirror_KV_vertical(base, level), level + 1)
        else:
            return self._generate_KVMuster(self._mirror_KV_horizontal(base, level), level + 1)

    def _mirror_KV_vertical(self, base, level):
        for i in range(len(base)):
            new = list(reversed([x.union(set([level])) for x in base[i]]))
            base[i] = base[i] + new
        return base

    def _mirror_KV_horizontal(self, base, level):
        new = list(reversed([[a.union(set([level])) for a in x] for x in base]))
        base = base + new
        return base
