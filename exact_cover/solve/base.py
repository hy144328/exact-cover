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

import exact_cover.cover

class Solver(abc.ABC):
    @abc.abstractmethod
    def solve[ChoiceT, _](
        self,
        cov: exact_cover.cover.Cover[ChoiceT, _],
    ) -> collections.abc.Generator[set[ChoiceT]]:   # pragma: no cover
        raise NotImplementedError()
