#!/usr/bin/env python3


from . import Cover


class Node:
    def __init__(self, val: bool = False) -> "Node":
        self.val = val
        self.left = self
        self.right = self
        self.above = self
        self.below = self

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
        super().__init__(left=self, right=self)
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
        super().__init__(above=self, below=self)
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
    def __init__(self) -> "DancingLinks":
        self.choices: dict[str, ChoiceNode] = {}
        self.constraints: dict[str, ConstraintNode] = {}

    def push(self, node: Node):
        node.attach_left()
        node.attach_right()
        node.attach_above()
        node.attach_below()

    def pop(self, node: Node) -> Node:
        node.cut_left()
        node.cut_right()
        node.cut_above()
        node.cut_below()
        return node

    def insert(self, node: Node, left: ChoiceNode, above: ConstraintNode):
        node.left = left
        node.right = left.right
        node.above = above
        node.below = above.below
        self.push(node)
