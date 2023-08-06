from .abs_param import AbsParam


class Param(AbsParam):
    """ Concrete Param """

    def __init__(
        self,
        name,
        type=None,
        dest=None,
        description=None,
        required=False,
        default=None,
        choices=None,
    ):
        """ Returns a new instance of Arg:

        Args:
             name (str): The parameter name
        Optional args:
            type (type): The value type
            dest (str): The name to assign the vale to (defaults to the name of the param)
            description (str): A description of the param
            required (bool): If True, the parser will require the param
            default: A default value for the param
            choices (list): A list of available choices
        """
        super().__init__(
            name,
            type=type,
            dest=dest,
            description=description,
            required=required,
            default=default,
            choices=choices,
        )
