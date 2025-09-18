import collections.abc

import exact_cover.cover.base

class IncidenceMatrix[ChoiceT, ConstraintT](
    exact_cover.cover.base.Cover[ChoiceT, ConstraintT],
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

        self.index_dropped: set[ChoiceT] = set()
        self.columns_dropped: set[ConstraintT] = set()

    @property
    def choices(self) -> list[ChoiceT]:
        return [
            choice_it
            for choice_it in self.index
            if choice_it not in self.index_dropped
        ]

    @property
    def constraints(self) -> list[ConstraintT]:
        return [
            constraint_it
            for constraint_it in self.columns
            if constraint_it not in self.columns_dropped
        ]

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

    def drop_choice(self, choice: ChoiceT):
        if choice not in self.index:
            raise KeyError(f"Choice {choice} does not exist.")

        if choice in self.index_dropped:
            raise KeyError(f"Choice {choice} already dropped.")

        self.index_dropped.add(choice)

    def drop_constraints(self, constraint: ConstraintT):
        if constraint not in self.columns:
            raise KeyError(f"Constraint {constraint} does not exist.")

        if constraint in self.columns_dropped:
            raise KeyError(f"Constraint {constraint} already dropped.")

        self.columns_dropped.add(constraint)

    def restore_choice(self, choice: ChoiceT):
        if choice not in self.index:
            raise KeyError(f"Choice {choice} does not exist.")

        if choice not in self.index_dropped:
            raise KeyError(f"Choice {choice} never dropped.")

        self.index_dropped.remove(choice)

    def restore_constraint(self, constraint: ConstraintT):
        if constraint not in self.columns:
            raise KeyError(f"Constraint {constraint} does not exist.")

        if constraint not in self.columns_dropped:
            raise KeyError(f"Constraint {constraint} never dropped.")

        self.columns_dropped.remove(constraint)
