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

import collections.abc

from . import base

class IncidenceMatrix[ChoiceT, ConstraintT](
    base.Cover[ChoiceT, ConstraintT],
):
    def __init__(
        self,
        choices: collections.abc.Sequence[ChoiceT],
        constraints: collections.abc.Sequence[ConstraintT],
        data: collections.abc.Mapping[ChoiceT, collections.abc.Collection[ConstraintT]],
    ):
        self.index = choices
        self.columns = constraints
        self.data: dict[ChoiceT, list[ConstraintT]] = {}

        for k in choices:
            self.data[k] = [
                constraint_it
                for constraint_it in constraints
                if constraint_it in data[k]
            ]

    @property
    def choices(self) -> list[ChoiceT]:
        return list(self.index)

    @property
    def constraints(self) -> list[ConstraintT]:
        return list(self.columns)

    def get_choices(
        self,
        constraint: ConstraintT,
    ) -> list[ChoiceT]:
        return [
            k
            for k, v in self.data.items()
            if constraint in v
        ]

    def get_constraints(
        self,
        choice: ChoiceT,
    ) -> list[ConstraintT]:
        return self.data[choice]
