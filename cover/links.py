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
    def __init__(self) -> "ChoiceNode":
        super().__init__()
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
    def __init__(self) -> "ConstraintNode":
        super().__init__()
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

        return res

    def push(self, node: Node = None):
        if not node:
            node: Node = self.stack.pop()

        node.attach_left()
        node.attach_right()
        node.attach_above()
        node.attach_below()

        return node

    def pop(self, node: Node):
        node.cut_left()
        node.cut_right()
        node.cut_above()
        node.cut_below()

        self.stack.append(node)

    def insert(self, node: Node, left, above):
        node_choice = self.choices[left]
        node_constraint = self.constraints[above]

        node.left = node_choice
        node.right = node_choice.right
        node.above = node_constraint
        node.below = node_constraint.below

        node.choice = left
        node.constraint = above

        self.push(node)

    def choose_choices(self, col) -> Iterable:
        node = self.constraints[col]
        res = []

        node_it = node.below
        while not isinstance(node_it, ConstraintNode):
            res.append(node_it.choice)
            node_it = node_it.below

        return res

    def choose_constraints(self, row) -> Iterable:
        node = self.choices[row]
        res = []

        node_it = node.right
        while not isinstance(node_it, ChoiceNode):
            res.append(node_it.constraint)
            node_it = node_it.right

        return res

    def delete_choices(self, rows: Iterable):
        for row_it in rows:
            node_it: ChoiceNode = self.choices.pop(row_it)
            while node_it is not node_it.right:
                self.pop(node_it)
                node_it = node_it.right
            self.pop(node_it)

    def delete_constraints(self, cols: Iterable):
        for col_it in cols:
            node_it: ConstraintNode = self.constraints.pop(col_it)
            while node_it is not node_it.below:
                self.pop(node_it)
                node_it = node_it.below
            self.pop(node_it)

    def restore_choices(self, rows: Iterable):
        for row_it in rows:
            node_it: Node = self.push()
            while not isinstance(node_it, ChoiceNode):
                node_it = self.push()
            self.choices[row_it] = node_it

    def restore_constraints(self, cols: Iterable):
        for col_it in cols:
            node_it: Node = self.push()
            while not isinstance(node_it, ConstraintNode):
                node_it = self.push()
            self.constraints[col_it] = node_it

    def next_col(self):
        try:
            return min(self.constraints)
        except ValueError:
            raise StopIteration
