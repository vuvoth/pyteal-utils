from pyteal import Exp, Expr, If, Int, Subroutine, TealType

# TODO: Wide math?


@Subroutine(TealType.uint64)
def exp10(x: TealType.uint64) -> Expr:
    """Returns 10^x, useful for things like total supply of an asset"""
    return Exp(Int(10), x)


@Subroutine(TealType.uint64)
def max(a: TealType.uint64, b: TealType.uint64) -> Expr:
    """Returns the max of 2 integers"""
    return If(a > b, a, b)


@Subroutine(TealType.uint64)
def min(a: TealType.uint64, b: TealType.uint64) -> Expr:
    """Returns the min of 2 integers"""
    return If(a < b, a, b)


@Subroutine(TealType.uint64)
def div_ceil(a: TealType.uint64, b: TealType.uint64) -> Expr:
    """Returns the result of division rounded up to the next integer"""
    q = a / b
    return If(a % b > Int(0), q + Int(1), q)
