class FailedConnection(Exception):

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "Не удачное подключение к сайту"


class CityNotFound(Exception):

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else "CityNotFound"
