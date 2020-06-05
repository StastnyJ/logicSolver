from Formulas import *

class SyntaxTreeNode:
    def __init__(self, text):
        self.text = text
        self.left = None
        self.right = None
        self.size = 1
        self.height = 1
        self.width = 1
        self.x_pos = -1
        self.deep = -1

    def count_proportions(self):
        self.size = 1
        self.height = 1
        self.width = 1
        if self.left is not None:
            self.size += self.left.size
            self.height += self.left.height
            if self.right is None:
                self.width = self.left.width
            else:
                self.width = self.right.width + self.left.width + 1
        if self.right is not None:
            self.size += self.right.size
            self.height = max(self.height, self.right.height + 1)
            if self.left is None:
                self.width = self.right.width
            else:
                self.width = self.right.width + self.left.width + 1

    def get_children_count(self):
        res = 0
        if self.left is not None:
            res += 1
        if self.right is not None:
            res += 1
        return res

class SyntaxTreeGenerator:
    def __init__(self, formula: Formula, operands_counts):
        self.formula = formula
        self.operands_counts = operands_counts
        self.tree = self._generate_tree()
        self._calculate_tree_pos()

    def _generate_tree(self):
        stack = []
        for act in self.formula.formula:
            if act.isalpha():
                stack.append(SyntaxTreeNode(act))
            else:
                new = SyntaxTreeNode(act)
                if self.operands_counts[act] == 1:
                    new.left = stack.pop()
                else:
                    new.right = stack.pop()
                    new.left = stack.pop()
                new.count_proportions()
                stack.append(new)
        return stack.pop()

    def _calculate_tree_pos(self, offset = 0, deep = 0, act:SyntaxTreeNode = None):
        if act is None:
            act = self.tree
        if act.left is not None:
            self._calculate_tree_pos(offset, deep + 1, act.left)
        act.deep = deep
        if act.get_children_count() == 0:
            act.x_pos = offset
        elif act.get_children_count() == 1:
            act.x_pos = act.left.x_pos
        else:
            act.x_pos = offset + act.left.width
        if act.right is not None:
            self._calculate_tree_pos(act.x_pos + 1, deep + 1, act.right)
        
    def _fill_plane(self, plane, act:SyntaxTreeNode):
        plane[act.deep * 2][act.x_pos] = act.text
        if act.get_children_count() == 1:
            plane[act.deep * 2 + 1][act.x_pos] = "|"
        if act.get_children_count() == 2:
            for i in range(act.left.x_pos + 1, act.right.x_pos):
                plane[act.deep * 2 + 1][i] = "─"
            plane[act.deep * 2 + 1][act.left.x_pos] = "┌"
            plane[act.deep * 2 + 1][act.right.x_pos] = "┐"
            plane[act.deep * 2 + 1][act.x_pos] = "┴"
        if act.left is not None:
            plane = self._fill_plane(plane, act.left)
        if act.right is not None:
            plane = self._fill_plane(plane, act.right)
        return plane

    def draw_tree(self):
        plane = [[" "] * self.tree.width for _ in range(self.tree.height * 2)]
        plane = self._fill_plane(plane, self.tree)
        return "\n".join(["".join(x) for x in plane])
        
class LogicalSyntaxTreeGenerator(SyntaxTreeGenerator):
    def __init__(self, formula: Formula):
        super(LogicalSyntaxTreeGenerator, self).__init__(formula, {'↔': 2, '→': 2, '⊕': 2, '∨': 2, '∧': 2, '¬': 1})