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
