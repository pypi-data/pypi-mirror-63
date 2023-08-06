import typing
from types import ModuleType
from .constants import (
    INPUT_PROMPTS,
    TYPE_NAMES,
    TYPE_FLAG_NAMES,
    COMPLEX_REGEX,
    TypeFlags,
)
from .exceptions import InvalidTypeError, VariableLookupError
from importlib import import_module
from .splw_types import *
import re


def import_safe(
    module: str, allow_py_imports: bool = True, allow_pip_install: bool = True
) -> typing.Optional[ModuleType]:
    """Forcibly import a module. Allows suppression of native package search

    Arguments:
        module {str} -- Name of module to look up

    Keyword Arguments:
        allow_py_imports {bool} -- Allow native package import (default: {True})
        allow_pip_install {bool} -- Allow native package search (default: {True})

    Returns:
        Optional[ModuleType] -- Either the imported module, or None if it could not be loaded.
    """
    allow_splw_imports = True
    if allow_splw_imports:
        from sys import stderr

        print("Currently unsupported", file=stderr)
    if allow_py_imports:
        try:
            return import_module(module)
        except ModuleNotFoundError:
            if allow_pip_install:
                print(
                    "Module {} not found. Importing pip to attempt to fetch it. This may take a moment".format(
                        module
                    )
                )
                from pip._internal import main  # type: ignore

                print("Loaded pip. Attempting to fetch as a package from PyPI")
                main(["install", module, "--user"])
                try:
                    return import_module(module)
                except ModuleNotFoundError:
                    pass


def get_safe(
    variable_dict: typing.Dict[str, typing.Any],
    variable: str,
    allow_splw_imports: bool = True,
    allow_py_imports: bool = True,
    allow_pip_install: bool = True,
    allow_bare_words: bool = True,
) -> SPLWType:
    """Get a variable from a variable dict safely; with failsafes

    Arguments:
        variable_dict {Dict[str, Any]} -- The environment variables
        variable {str} -- The variable name to look up

    Keyword Arguments:
        allow_splw_imports {bool} -- Allow SPLW import failsafe (default: {True})
        allow_py_imports {bool} -- Allow native import failsafe (default: {True})
        allow_pip_install {bool} -- Allow native package search (default: {True})
        allow_bare_words {bool} -- Allow coercion to str (default: {True})

    Raises:
        VariableLookupError: All failsafes disabled or failed

    Returns:
        SPLWType -- Located variable
    """
    try:
        return variable_dict[variable]
    except:
        if allow_splw_imports:
            from sys import stderr

            print("Currently unsupported", file=stderr)
        if allow_py_imports:
            try:
                return import_module(variable)
            except ModuleNotFoundError:
                if allow_pip_install:
                    print(
                        "Module {} not found. Importing pip to attempt to fetch it. This may take a moment".format(
                            variable
                        )
                    )
                    from pip._internal import main

                    print("Loaded pip. Attempting to fetch as a package from PyPI")
                    main(["install", variable, "--user"])
                    try:
                        return import_module(variable)
                    except ModuleNotFoundError:
                        pass
        if allow_bare_words:
            return variable
        raise VariableLookupError


def system_identifier(name: str) -> typing.Optional[SPLWType]:
    """Get a Python type from its valid SPLW type names

    Arguments:
        name {str} -- the SPLW type name

    Returns:
        Optional[SPLWType] -- The type, or None if it could not be resolved
    """
    rv: typing.Optional[type] = None
    if name in ["str", "STR", "Str", "string", "STRING", "String"]:
        rv = SPLWString
    if name in ["int", "INT", "Int", "integer", "INTEGER", "Integer"]:
        rv = int
    if name in [
        method(i)
        for method in (str.upper, str.lower, str.title)
        for i in ("float", "real", "number")
    ]:
        rv = float
    if name in [
        method(i)
        for method in (str.upper, str.lower, str.title)
        for i in ("list", "array", "tuple")
    ]:
        rv = SPLWList
    if name in ["bool", "BOOL", "Bool", "boolean", "BOOLEAN", "Boolean"]:
        rv = bool
    if name in ["complex", "Complex", "COMPLEX"]:
        rv = SPLWComplex
    return rv


def get_flags(type_flags: str) -> int:
    """Get the type flags from a type flag string

    Arguments:
        type_flags {str} -- The type flag string, e.g. POS

    Raises:
        InvalidTypeError: The type descriptor is invalid

    Returns:
        int -- The type flags, using `constants.TypeFlags` values
    """
    if type_flags in ["POS", "POSITIVE"]:
        return TypeFlags.ALLOW_POS
    if type_flags in ["NONNEG", "NONNEGATIVE"]:
        return TypeFlags.ALLOW_POS | TypeFlags.ALLOW_ZERO
    if type_flags == "NONZERO":
        return TypeFlags.ALLOW_POS | TypeFlags.ALLOW_NEG
    if type_flags in ["NONPOS", "NONPOSITIVE"]:
        return TypeFlags.ALLOW_NEG | TypeFlags.ALLOW_ZERO
    if type_flags in ["NEG", "NEGATIVE"]:
        return TypeFlags.ALLOW_NEG
    raise InvalidTypeError("Invalid type flag: " + repr(type_flags))


def obeys_flags(number: SPLWNumber, flags: int) -> bool:
    """Determines if the number specified obeys the flags specified

    Arguments:
        number {SPLWNumber} -- Any numeric type
        flags {int} -- A combination of TypeFlags values

    Returns:
        bool -- `True` if `number` is valid for `flags`
    """
    if flags & TypeFlags.ALLOW_ZERO and number == 0:
        return True
    if flags & TypeFlags.ALLOW_POS and number > 0:
        return True
    if flags & TypeFlags.ALLOW_NEG and number < 0:
        return True
    return False


def handle_input(type_name: str) -> SPLWType:
    """Get input for given type name

    Arguments:
        type_name {str} -- SPLW type descriptor

    Raises:
        InvalidTypeError: Type descriptor is too long
        InvalidTypeError: Type descriptor received inappropriate flags
        InvalidTypeError: Invalid type descriptor

    Returns:
        SPLWType -- The value provided by the user
    """
    split_type = type_name.split(" ")
    if len(split_type) > 1:
        if len(split_type) > 2:
            raise InvalidTypeError(
                repr(type_name)
                + " has too many words: "
                + str(len(split_type))
                + " (max 2)"
            )
        input_type = system_identifier(split_type[1])
        if input_type not in OBEYS_FLAGS:
            raise InvalidTypeError(
                repr(split_type[1].upper()) + " cannot receive type flags"
            )
        flags = get_flags(split_type[0])
    else:
        input_type = system_identifier(type_name)
        flags = TypeFlags.DEFAULT

    if input_type is None:
        raise InvalidTypeError(type_name.upper() + " is not a valid type descriptor")

    if input_type in (SPLWString, int, float):
        rv = None
        while rv is None:
            try:
                rv = input_type(input(INPUT_PROMPTS[input_type]))
                if input_type in OBEYS_FLAGS:
                    if not obeys_flags(rv, flags):
                        print(
                            f"That wasn't {TYPE_FLAG_NAMES[flags].format(TYPE_NAMES[input_type][2:])}, try again"
                        )
                        rv = None
            except Exception:
                print(f"That wasn't {TYPE_NAMES[input_type]}, try again")
        return rv
    elif input_type == SPLWList:
        rv = None
        while rv is None:
            try:
                rv = input_type(input(INPUT_PROMPTS[input_type]).split(", "))
            except Exception:
                print(f"That wasn't {TYPE_NAMES[input_type]}, try again")
        return rv
    elif input_type == bool:
        rv = None
        while rv is None:
            try:
                rv = {"y": True, "yes": True, "n": False, "no": False}[
                    input(INPUT_PROMPTS[input_type]).lower()
                ]
            except Exception:
                print(f"That wasn't {TYPE_NAMES[input_type]}, try again")
        return rv
    elif input_type == SPLWComplex:
        rv = None
        while rv is None:
            try:
                tmp = input(INPUT_PROMPTS[input_type]).replace(" ", "")
                match = re.fullmatch(COMPLEX_REGEX, tmp)
                if not match:
                    print(f"That wasn't {TYPE_NAMES[input_type]}, try again")
                    continue
                # [print(match.group(i)) for i in range(7)]
                real = float(match.group(1) or 0)
                imag = float(
                    (match.group(5) + (match.group(6) or "1"))
                    if match.group(5)
                    else "0"
                )
                rv = input_type(real, imag)
                if input_type in OBEYS_FLAGS:
                    if not obeys_flags(rv, flags):
                        print(
                            f"That wasn't {TYPE_FLAG_NAMES[flags].format(TYPE_NAMES[input_type][2:])}, try again"
                        )
                        rv = None
            except Exception:
                print(f"That wasn't {TYPE_NAMES[input_type]}, try again")
        return rv
