#!/usr/bin/python3.7

from Formulas import *
from SyntaxTrees import *

def solve_expr(expr):
    formula = LogicFormula(expr)
    treeGen = LogicalSyntaxTreeGenerator(formula)
    print("Formel: " + expr)
    print()
    print("Wahrheitstabelle:\n")
    print(formula.generate_table())
    print()
    print("KV-Diagramm:\n")
    print(formula.generate_KVDiagram())
    print()
    print("Syntaxbaum:\n")
    print(treeGen.draw_tree())
    print()
    print("-"*64)
    print()

Task91 = [
    "(p ∧ ((q ∧ (r ∨ (¬r ∧ x ∧ ¬z))) ∨ (¬q ∧ ((r ∧ x ∧ z) ∨ (¬r ∧ (x ∨ (¬x ∧ ¬y ∧ ¬z)))))))∨(¬p ∧ ((q ∧ ((r ∧ x) ∨ (¬r ∧ z))) ∨ (¬q ∧ ((r ∧ (x ∨ (¬x ∧ (y ∨ (¬y ∧ z))))) ∨ (¬r ∧ x ∧ z)))))",
    "(p ∧ ((q ∧ ((r ∧ ((x ∧ y ∧ z) ∨ (¬x ∧ (¬y ∨ (y ∧ ¬z)))))∨(¬r ∧ ((x ∧ ((y ∧ ¬z) ∨ (¬y ∧ z))) ∨ (¬x ∧ ¬y ∧ ¬z))))) ∨ (¬q ∧ ¬r ∧ x ∧ y)))∨(¬p ∧ ((q ∧ ((r ∧ ((x ∧ ¬y ∧ ¬z) ∨ (¬x ∧ y))) ∨ (¬r ∧ x ∧ ¬y ∧ ¬z)))∨(¬q ∧ ((r ∧ ¬x ∧ ¬y ∧ z) ∨ (¬r ∧ x ∧ ¬y)))))"
]
Task92 = [
    "((p ∨ p) → (t ⊕ t)) ∨ (p ⊕ (t → s))",
    "((q ∨ t) → (p ∨ t)) ∨ (q ∧ (t ↔ p))",
    "¬(s ↔ t) ⊕ ((q ↔ t) → ¬s)",
    "(q ∧ r) → ((q ⊕ s) ↔ (r → p))",
    "(((q ∨ t) → (p ∨ t)) ∨ (q ∧ (t ↔ p))) ∧ (s ∨ ¬s)",
    "(((¬q ∧ ¬t) ∨ (p ∨ t)) ∨ (q ∧ ((¬t ∨ p) ∧ (¬p ∨ t)))) ∨ (((q ∨ t) ∧ (¬p ∧ ¬t)) ∧ (¬q ∨ ((t ∧ ¬p) ∨ (p ∧ ¬t))))"
]



solve_expr(input())
