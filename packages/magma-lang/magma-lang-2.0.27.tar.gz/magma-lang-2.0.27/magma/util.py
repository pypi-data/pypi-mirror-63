import magma as m


primitive_to_python_operator_name_map = {
    "and": "and_",
    "or": "or_",
    "xor": "xor",
    "shl": "lshift",
    "lshr": "rshift",
    "ashr": "rshift",
    "urem": "mod",
    "srem": "mod",
    "udiv": "floordiv",
    "sdiv": "floordiv",
    "ule": "le",
    "ult": "lt",
    "uge": "ge",
    "ugt": "gt",
    "sle": "le",
    "slt": "lt",
    "sge": "ge",
    "sgt": "gt",
    "not": "invert"
}


def BitOrBits(width):
    if width is None:
        return m.Bit
    if not isinstance(width, int):
        raise ValueError(f"Expected width to be None or int, got {width}")
    return m.Bits[width]


def pretty_str(t):
    if issubclass(t, m.Tuple):
        args = []
        for i in range(len(t)):
            key_str = str(list(t.keys())[i])
            val_str = pretty_str(list(t.types())[i])
            indent = " " * 4
            val_str = f"\n{indent}".join(val_str.splitlines())
            args.append(f"{key_str} = {val_str}")
        # Pretty print by using newlines + indent
        joiner = ",\n    "
        result = joiner.join(args)
        # Insert first newline + indent and last newline
        result = "\n    " + result + "\n"
        s = f"Tuple({result})"
    elif issubclass(t, m.Bits):
        s = str(t)
    elif issubclass(t, m.Array):
        s = f"Array[{t.N}, {pretty_str(t.T)}]"
    else:
        s = str(t)
    return s


def pretty_print_type(t):
    print(pretty_str(t))
