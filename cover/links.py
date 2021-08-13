#!/usr/bin/env python3

from collections.abc import Iterable, Sequence

from . import Cover


class Node:
    def __init__(self) -> "Node":
        self.left: Node = self
        self.right: Node = self
        self.above: Node = self
        self.below: Node = self

        self.choice = None
        self.constraint = None

    def cut_left(self):
        self.left.right = self.right

    def cut_right(self):
        self.right.left = self.left

    def cut_above(self):
        self.above.below = self.below

    def cut_below(self):
        self.below.above = self.above

    def attach_left(self):
        self.left.right = self

    def attach_right(self):
        self.right.left = self

    def attach_above(self):
        self.above.below = self

    def attach_below(self):
        self.below.above = self


class ChoiceNode(Node):
    def __init__(self, name) -> "ChoiceNode":
        super().__init__(left=self, right=self)
        self.choice = name
        self.no_constraints: int = 0

    def cut_above(self):
        pass

    def cut_below(self):
        pass

    def attach_above(self):
        pass

    def attach_below(self):
        pass


class ConstraintNode(Node):
    def __init__(self, name) -> "ConstraintNode":
        super().__init__(above=self, below=self)
        self.constraint = name
        self.no_choices: int = 0

    def cut_left(self):
        pass

    def cut_right(self):
        pass

    def attach_left(self):
        pass

    def attach_right(self):
        pass


class DancingLinks(Cover):
    def __init__(self, rows: Iterable, cols: Iterable) -> "DancingLinks":
        self.choices: dict[object, ChoiceNode] = {
            row_it: ChoiceNode() for row_it in rows
        }
        self.constraints: dict[object, ConstraintNode] = {
            col_it: ConstraintNode() for col_it in cols
        }
        self.stack: list = []

    @staticmethod
    def read_json(data: dict[object, Sequence]) -> "DancingLinks":
        rows = list(data.keys())
        cols = set()
        cols = list(cols.union(*data.values()))

        res = DancingLinks(rows, cols)
        for row_it in data:
            for col_it in data[row_it]:
                res.insert(Node(), row_it, col_it)

    def push(self):
        node: Node = self.stack.pop()

        node.attach_left()
        node.attach_right()
        node.attach_above()
        node.attach_below()

    def pop(self, node: Node):
        node.cut_left()
        node.cut_right()
        node.cut_above()
        node.cut_below()

        self.stack.append(node)

    def insert(self, node: Node, left: ChoiceNode, above: ConstraintNode):
        node.left = left
        node.right = left.right
        node.above = above
        node.below = above.below

        self.stack.append(node)
        self.push(node)

    def choose_rows(self, col) -> Iterable:
        node = self.constraints[col]
        res = []

        node_it = node.below
        while not isinstance(node_it, ConstraintNode):
            res.append(node.choice)
            node_it = node_it.below

        return res

    def choose_cols(self, row) -> Iterable:
        node = self.choices[row]
        res = []

        node_it = node.right
        while not isinstance(node_it, ChoiceNode):
            res.append(node.constraint)
            node_it = node_it.right

        return res

    def delete_rows(self, rows: Iterable):
        for row_it in rows:
            node: ChoiceNode = self.choices.pop(row_it)
            while not isinstance(node.right, ChoiceNode):
                self.pop(node.right)

    def delete_cols(self, cols: Iterable):
        for col_it in cols:
            node: ConstraintNode = self.constraints.pop(col_it)
            while not isinstance(node.below, ConstraintNode):
                self.pop(node.below)

    def restore_rows(self, rows: Iterable):
        for row_it in rows:
            node: ChoiceNode = self.stack.pop()
            self.choices[row_it] = node

            while not isinstance(self.stack[-1], ChoiceNode):
                self.insert(self.stack.pop())

    def restore_cols(self, cols: Iterable):
        for col_it in rows:
            node: ConstraintNode = self.stack.pop()
            self.constraints[col_it] = node

            while not isinstance(self.stack[-1], ConstraintNode):
                self.insert(self.stack.pop())

    def next_col(self):
        return self.constraints[0]
