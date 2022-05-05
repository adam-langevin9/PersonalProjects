from abc import abstractmethod


class AVisitor:
    @abstractmethod
    def visit(obj):
        pass


class AVisitable:
    def accept(self, visitor: AVisitor):
        return visitor.visit(self)
