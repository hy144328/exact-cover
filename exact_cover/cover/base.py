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

class MutableCover[ChoiceT, ConstraintT](Cover[ChoiceT, ConstraintT]):
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
