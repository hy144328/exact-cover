import abc

class Cover[ChoiceT, ConstraintT](abc.ABC):
    @property
    @abc.abstractmethod
    def choices(self) -> list[ChoiceT]:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def constraints(self) -> list[ConstraintT]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_choices(self, constraint: ConstraintT) -> list[ChoiceT]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_constraints(self, choice: ChoiceT) -> list[ConstraintT]:
        raise NotImplementedError()

class MutableCover[ChoiceT, ConstraintT](Cover[ChoiceT, ConstraintT]):
    @abc.abstractmethod
    def drop_choice(self, choice: ChoiceT):
        raise NotImplementedError()

    @abc.abstractmethod
    def drop_constraint(self, constraint: ConstraintT):
        raise NotImplementedError()

    @abc.abstractmethod
    def restore_choice(self, choice: ChoiceT):
        raise NotImplementedError()

    @abc.abstractmethod
    def restore_constraint(self, constraint: ConstraintT):
        raise NotImplementedError()

    @abc.abstractmethod
    def next_constraint(self) -> ConstraintT:
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
