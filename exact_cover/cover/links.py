# Copyright (C) 2025  Hans Yu <hans.yu@outlook.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import abc
import collections.abc

from . import base

class AbstractNode(abc.ABC):
    @abc.abstractmethod
    def cut(self):  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def attach(self):   # pragma: no cover
        raise NotImplementedError()

class ChoiceNode[ChoiceT](AbstractNode):
    def __init__(self, choice: ChoiceT):
        self.left: ChoiceNode[ChoiceT] = self
        self.right: ChoiceNode[ChoiceT] = self

        self.choice = choice

    def cut(self):
        self.left.right = self.right
        self.right.left = self.left

    def attach(self):
        self.left.right = self
        self.right.left = self

class ConstraintNode[ConstraintT](AbstractNode):
    def __init__(self, constraint: ConstraintT):
        self.above: ConstraintNode[ConstraintT] = self
        self.below: ConstraintNode[ConstraintT] = self

        self.constraint = constraint

    def cut(self):
        self.above.below = self.below
        self.below.above = self.above

    def attach(self):
        self.above.below = self
        self.below.above = self

class Node[ChoiceT, ConstraintT](
    ChoiceNode[ChoiceT],
    ConstraintNode[ConstraintT],
):
    def __init__(self, choice: ChoiceT, constraint: ConstraintT):
        self.left: ChoiceNode[ChoiceT] = self
        self.right: ChoiceNode[ChoiceT] = self
        self.above: ConstraintNode[ConstraintT] = self
        self.below: ConstraintNode[ConstraintT] = self

        self.choice = choice
        self.constraint = constraint

    def cut(self):
        self.left.right = self.right
        self.right.left = self.left
        self.above.below = self.below
        self.below.above = self.above

    def attach(self):
        self.left.right = self
        self.right.left = self
        self.above.below = self
        self.below.above = self

class DancingLinks[ChoiceT, ConstraintT](
    base.MutableCover[ChoiceT, ConstraintT],
):
    def __init__(
        self,
        choices: collections.abc.Sequence[ChoiceT],
        constraints: collections.abc.Sequence[ConstraintT],
    ):
        self.index = {
            choice_it: ChoiceNode(choice_it)
            for choice_it in choices
        }
        self.columns = {
            constraint_it: ConstraintNode(constraint_it)
            for constraint_it in constraints
        }
        self.stack: list[ChoiceNode[ChoiceT] | ConstraintNode[ConstraintT]] = []

    def drop_node(self, node: ChoiceNode[ChoiceT] | ConstraintNode[ConstraintT]):
        node.cut()
        self.stack.append(node)

    def restore_node(self) -> ChoiceNode[ChoiceT] | ConstraintNode[ConstraintT]:
        node = self.stack.pop()
        node.attach()
        return node

    def create_node(self, choice: ChoiceT, constraint: ConstraintT) -> Node:
        node_choice = self.index[choice]
        node_constraint = self.columns[constraint]
        node = Node(choice, constraint)

        node.left = node_choice
        node.right = node_choice.right
        node.above = node_constraint
        node.below = node_constraint.below

        node.attach()
        return node

    @property
    def choices(self) -> list[ChoiceT]:
        return list(self.index.keys())

    @property
    def constraints(self) -> list[ConstraintT]:
        return list(self.columns.keys())

    def get_choices(self, constraint: ConstraintT) -> list[ChoiceT]:
        node_it = self.columns[constraint].below
        res: list[ChoiceT] = []

        while isinstance(node_it, Node):
            res.append(node_it.choice)
            node_it = node_it.below

        return res

    def get_constraints(self, choice: ChoiceT) -> list[ConstraintT]:
        node_it = self.index[choice].right
        res: list[ConstraintT] = []

        while isinstance(node_it, Node):
            res.append(node_it.constraint)
            node_it = node_it.right

        return res

    def drop_choice(self, choice: ChoiceT):
        node_it = self.index.pop(choice)
        while node_it is not node_it.right:
            self.drop_node(node_it)
            node_it = node_it.right
        self.drop_node(node_it)

    def drop_constraint(self, constraint: ConstraintT):
        node_it = self.columns.pop(constraint)
        while node_it is not node_it.below:
            self.drop_node(node_it)
            node_it = node_it.below
        self.drop_node(node_it)

    def restore_choice(self, choice: ChoiceT):
        node_it = self.restore_node()
        while isinstance(node_it, Node):
            node_it = self.restore_node()

        if not isinstance(node_it, ChoiceNode): # pragma: no cover
            raise ValueError("Expected ChoiceNode.")

        if node_it.choice != choice:    # pragma: no cover
            raise ValueError(f"Expected {choice} but got {node_it.choice}.")

        self.index[choice] = node_it

    def restore_constraint(self, constraint: ConstraintT):
        node_it = self.restore_node()
        while isinstance(node_it, Node):
            node_it = self.restore_node()

        if not isinstance(node_it, ConstraintNode): # pragma: no cover
            raise ValueError("Expected ConstraintNode.")

        if node_it.constraint != constraint:    # pragma: no cover
            raise ValueError(f"Expected {constraint} but got {node_it.constraint}.")

        self.columns[constraint] = node_it

    def next_constraint(self) -> ConstraintT:
        return next(iter(self.columns))
