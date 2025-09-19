import collections.abc

from .base import Cover

class IncidenceMatrix[ChoiceT, ConstraintT](
    Cover[ChoiceT, ConstraintT],
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
