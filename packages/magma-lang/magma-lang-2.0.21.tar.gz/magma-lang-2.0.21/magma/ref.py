from .compatibility import IntegerTypes
from abc import abstractmethod


__all__ = ['AnonRef', 'InstRef', 'DefnRef', 'ArrayRef', 'TupleRef']
__all__ += ['LazyDefnRef', 'LazyCircuit']


class Ref:
    @abstractmethod
    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return self.qualifiedname()

    @abstractmethod
    def qualifiedname(self, sep="."):
        raise NotImplementedError()

    @abstractmethod
    def anon(self):
        raise NotImplementedError()

    def verilog_name(self):
        return self.qualifiedname("_")


class AnonRef(Ref):
    def __init__(self):
        self.name = None

    def __str__(self):
        return f"AnonymousValue_{id(self)}"

    def qualifiedname(self, sep='.'):
        return f"AnonymousValue_{id(self)}"

    def anon(self):
        return True


class NamedRef(Ref):
    def __init__(self, name):
        if not isinstance(name, (str, int)):
            raise TypeError("Expected string or int")
        self.name = name

    def __str__(self):
        return self.name

    def qualifiedname(self, sep="."):
        return self.name

    def anon(self):
        return False


class InstRef(NamedRef):
    def __init__(self, inst, name):
        super().__init__(name)
        if not inst:
            raise ValueError(f"Bad inst: {inst}")
        self.inst = inst

    def qualifiedname(self, sep="."):
        name = self.name
        if isinstance(self.name, IntegerTypes):
            # Hack, Hack, Hack!
            # NOTE: This is used for verilog instances that don't use named
            # port (wired by index instead), so the ports are referred to by
            # index instead of name and we use the array indexing syntax to
            # represent them
            # See mantle's generic verilog target for example use case
            if sep == ".":
                return f"{self.inst.name}[{self.name}]"
        return self.inst.name + sep + str(name)


class DefnRef(NamedRef):
    def __init__(self, defn, name):
        super().__init__(name)
        if not defn:
            raise ValueError(f"Bad defn: {defn}")
        self.defn = defn

    def qualifiedname(self, sep="."):
        if sep == ".":
            return self.defn.__name__ + sep + self.name
        return self.name


class LazyCircuit:
    name = ""


class LazyDefnRef(DefnRef):
    def __init__(self, name):
        self.name = name
        self._defn = None

    @property
    def defn(self):
        if self._defn is not None:
            return self._defn
        return LazyCircuit

    def qualifiedname(self, sep="."):
        return super().qualifiedname(sep)

    def set_defn(self, defn):
        if self._defn is not None:
            raise Exception("Can only set definition of LazyDefnRef once")
        self._defn = defn


class ArrayRef(Ref):
   def __init__(self, array, index):
       self.array = array
       self.index = index

   def __str__(self):
       return self.qualifiedname()

   def qualifiedname(self, sep="."):
       return f"{self.array.name.qualifiedname(sep=sep)}[{self.index}]"

   def anon(self):
       return self.array.name.anon()


class TupleRef(Ref):
    def __init__(self, tuple, index):
        self.tuple = tuple
        self.index = index

    def __str__(self):
        return self.qualifiedname()

    def qualifiedname(self, sep="."):
        try:
            int(self.index)
            return self.tuple.name.qualifiedname(sep=sep) + "[" + str(self.index) + "]"
        except ValueError:
            return self.tuple.name.qualifiedname(sep=sep) + sep + str(self.index)

    def verilog_name(self):
        return self.tuple.name.verilog_name() + "_" + str(self.index)

    def anon(self):
        return self.tuple.name.anon()
