import inspect
from .exceptions import BadParamType, BadReturnType
import typing
from itertools import zip_longest

TFunc = typing.TypeVar("TFunc")


def type_check(ignore_self=False) -> typing.Callable[[TFunc], TFunc]:
    """Decorator factory to add type checking to a function.

    Add type checking to a function. Optionally, ignore the self parameter.
    Procedures should either omit the `return` type-hint or type-hint it to None.
    All parameters must be type-hinted.

    Keyword Arguments:
        ignore_self {bool} -- Do not type-check the `self` argument (default: {False})

    Raises:
        TypeError: If the number of arguments passed is more than the number accepted
        TypeError: If the number of arguments passed is less than the number accepted
        BadParamType: If any argument is missing an annotation (except `self` as set)
        BadParamType: If any argument is of the wrong type
        BadReturnType: If a procedure returns a value
        BadReturnType: If a function returns a value of the wrong type

    Returns:
        typing.Callable[[TFunc], TFunc] -- Decorator to type-check a function
    """

    class NoValue:
        """Used as a special None"""

    def _type_check(func: TFunc) -> TFunc:
        """Generated decorator. Obeys `ignore_self` and type-checks the function"""
        annotations = func.__annotations__
        arg_names = inspect.getargs(func.__code__).args  # type: ignore

        def out_func(*args):
            """Decorated function. Obeys `ignore_self` and type-checks the arguments"""
            for i, (arg_name, arg) in enumerate(
                zip_longest(arg_names, args, fillvalue=NoValue)
            ):
                if i == 0 and arg_name == "self" and ignore_self:
                    continue
                if arg_name is NoValue:
                    raise TypeError(f"Too many arguments passed")
                if arg is NoValue:
                    raise TypeError(f"Too few arguments passed")
                if arg_name not in annotations:
                    raise BadParamType(f"Parameter {arg_name} missing annotation")
                if not isinstance(arg, annotations[arg_name]):
                    raise BadParamType(
                        f"Parameter '{arg_name}' is of type '{type(arg).__name__}'"
                        f", expected '{annotations[arg_name].__name__}'"
                    )
            result = func(*args)
            if not annotations.get("return"):
                if result is not None:
                    raise BadReturnType(f"Procedure returned value ({result!r})")
            elif not isinstance(result, annotations["return"]):
                raise BadReturnType(
                    f"Function returned value of type '{type(result).__name__}'"
                    f", expected type '{annotations['return'].__name__}'"
                )
            return result

        return typing.cast(TFunc, out_func)

    return _type_check
