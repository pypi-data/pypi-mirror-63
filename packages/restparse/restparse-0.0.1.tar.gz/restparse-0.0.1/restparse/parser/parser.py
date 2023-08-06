from .abs_parser import AbsParser
from .param import Param
from .params import Params
from .exceptions import (
    ParserParamRequiredError,
    ParserTypeError,
    ParserInvalidChoiceError,
    DuplicateParamError
)


class Parser(AbsParser):
    """ Concrete Parser """

    def __init__(self, description=None, allowed_types=None):
        """ Returns an instance of Parser

        Args:
            description (str): A description of the parser (None)
            allowed_types (list): A list of allowed types (str, int, float, list, dict, bool, None)
        """
        super().__init__(description=description)
        self.params = {}
        if allowed_types:
            if not type(allowed_types) in (list, set, tuple):
                raise TypeError(f"Allowed types must be list, set or tuple, not {type(allowed_types)}")
            else:
                self.allowed_types = allowed_types
        else:
            self.allowed_types = {str, int, float, list, dict, bool, None}

    def add_param(
        self,
        name,
        type=None,
        dest=None,
        description=None,
        required=False,
        choices=None,
        default=None,
    ):
        """ Add a parameter to the parser

        Args:
            name (str): The parameter name
            type (type): The type to which the parser should expect
            dest (str): The name of the attribute to be added to the object returned by parse_params()
            description (str): A description of the param
            required (bool): Whether or not the param may be omitted
            choices (container): A container of the allowable values for the argument
            default: The value produced if the argument is absent from the params
        """

        # Check type
        if type not in self.allowed_types:
            raise ParserTypeError(f"Invalid type '{type}' for param {name}")

        # Check default type
        if default and type:
            try:
                default = type(default)
            except ValueError:
                raise ParserTypeError(
                    f"Invalid default value type '{type}' for param {name}"
                )

        # Create a new Param and add it to the self.params dict {name: Param}
        a = Param(
            name,
            type=type,
            dest=dest,
            description=description,
            required=required,
            default=default,
            choices=choices,
        )

        if name in self.params:
            raise DuplicateParamError(f"Duplicate parameter '{name}'")
        else:
            self.params[name] = a

    def parse_params(self, data=None):
        """ Parse a dict """

        params = Params()

        if not data:
            data = {}

        for name, arg in self.params.items():

            value = data.get(arg.name, None)

            if not value:
                value = None

            # Check choices
            if arg.choices:
                if value not in arg.choices and value is not None:
                    raise ParserInvalidChoiceError(f"Value '{value}' not in choices")

            # Check required
            if arg.required and value is None:
                raise ParserParamRequiredError(f"Missing required value for {arg.name}")

            # Check value type
            if value and arg.type and type(value) != arg.type:
                try:
                    arg.type(value)
                except Exception:
                    raise ParserTypeError(
                        f"Incorrect type ({type(value)}) for {arg.name}"
                    )

            # Set the parser attribute
            if arg.default and not value:
                setattr(self, arg.name, arg.default)
                setattr(params, arg.name, arg.default)
                params.add_param(arg.name)
            elif arg.dest:
                setattr(self, arg.dest, value)
                setattr(params, arg.dest, value)
                params.add_param(arg.name)
            else:
                setattr(self, arg.name, value)
                setattr(params, arg.name, value)
                params.add_param(arg.name)

        return params
