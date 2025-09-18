import abc
import collections.abc

import exact_cover.cover

class Solver:
    @abc.abstractmethod
    def solve[ChoiceT, _](
        self,
        cov: exact_cover.cover.Cover[ChoiceT, _],
    ) -> collections.abc.Generator[set[ChoiceT]]:
        raise NotImplementedError()
