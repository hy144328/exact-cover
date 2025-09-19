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
