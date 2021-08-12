#!/usr/bin/env python3


from . import Cover


class Node:
    def __init__(
        self,
        val = False,
        left: Node = None,
        right: Node = None,
        above: Node = None,
        below: Node = None,
    ) -> "Node":
        self.val = val
        self.left = left
        self.right = right
        self.above = above
        self.below = below


class ChoiceNode(Node):
    def __init__(self, val: str) -> "ChoiceNode":
        super().__init__(val=val, left=self, right=self)
        self.no_constraints: int = 0


class ConstraintNode(Node):
    def __init__(self, val: str) -> "ConstraintNode":
        super().__init__(val=val, above=self, below=self)
        self.no_choices: int = 0


class DancingLinks(Cover):
    def __init__(self) -> "DancingLinks":
        self.choices: list[ChoiceNode] = []
        self.constraints: list[ConstraintNode] = []

    def push(self, node: Node):
        ...

    def pop(self, node: Node) -> Node:
        ...
