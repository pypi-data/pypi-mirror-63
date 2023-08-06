class Params(object):
    """ Params object """

    def __init__(self):
        self._params = set()

    def add_param(self, name):
        self._params.add(name)

    def to_dict(self):

        resp = {}
        for param in self._params:
            resp[param] = getattr(self, param)

        return resp
