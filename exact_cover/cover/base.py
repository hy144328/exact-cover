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

class Cover[ChoiceT, ConstraintT](abc.ABC):
    @property
    @abc.abstractmethod
    def choices(self) -> list[ChoiceT]: # pragma: no cover
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def constraints(self) -> list[ConstraintT]: # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def get_choices(self, constraint: ConstraintT) -> list[ChoiceT]:    # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def get_constraints(self, choice: ChoiceT) -> list[ConstraintT]:    # pragma: no cover
        raise NotImplementedError()

class MutableCover[ChoiceT, ConstraintT](
    Cover[ChoiceT, ConstraintT],
):
    @abc.abstractmethod
    def drop_choice(self, choice: ChoiceT): # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def drop_constraint(self, constraint: ConstraintT): # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def restore_choice(self, choice: ChoiceT):  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def restore_constraint(self, constraint: ConstraintT):  # pragma: no cover
        raise NotImplementedError()

    @abc.abstractmethod
    def next_constraint(self) -> ConstraintT:   # pragma: no cover
        raise NotImplementedError()

    def choose(self, choice: ChoiceT):
        constraints_satisfied = self.get_constraints(choice)

        choices_invalidated = [
            choice_it
            for constraint_it in constraints_satisfied
            for choice_it in self.get_choices(constraint_it)
        ]
        choices_invalidated = list(set(choices_invalidated))

        for choice_it in choices_invalidated:
            self.drop_choice(choice_it)

        for constraint_it in constraints_satisfied:
            self.drop_constraint(constraint_it)
