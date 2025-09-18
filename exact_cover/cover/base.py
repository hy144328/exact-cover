import abc
import collections.abc

class Cover[ChoiceT, ConstraintT]:
    @property
    @abc.abstractmethod
    def choices(self) -> list[ChoiceT]:
        raise NotImplementedError()

    @abc.abstractmethod
    def iter_constraints(self) -> collections.abc.Generator[ConstraintT]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_choices(self, constraint: ConstraintT) -> list[ChoiceT]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_constraints(self, choice: ChoiceT) -> list[ConstraintT]:
        raise NotImplementedError()

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
