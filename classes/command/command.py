__author__ = 'alekseymanikin'

import helpers.helpers as helper
from warnings import warn


class Command(object):
    """
    Базовый класс для работы с консольными командами
    """

    OPTIONS = {}
    ':type : dict'

    def __init__(self, command_name: str):
        """
        :param command_name: Имя команды
        :type command_name: unicode
        :return:
        """
        self.options = {}
        self.binary = [helper.get_util(command_name)]

    def _set_single_option_(self, name: str, value: str) -> None:
        """
        Устанавливаем базовые опции
        :type name: unicode
        :type value: basestring|int|bool
        :return:
        """
        if isinstance(value, self.OPTIONS[name]):
            if name.startswith("no-"):
                negator = name.lstrip("no-")
            else:
                negator = "no-%s" % name

            if negator in self.options:
                warn(
                    "Command: mutually exclusive options are present. Last one will be in effect")
                del self.options[negator]

            if name in self.options:
                self.options[name].append(value)
            else:
                self.options[name] = [value]
        else:
            raise TypeError(
                "value '%s' doesn't match option '%s'" %
                (value, name))

    def set_option(self, name: str, values: str or None = None) -> None:
        """
        :type name: unicode
        :type values: unicode
        :return:
        """
        if not isinstance(values, list):
            values = [values]
        for value in values:
            self._set_single_option_(name, value)

    def set_options(self, options: str) -> None:
        """
        :type options: unicode
        :return:
        """
        for option in options:
            if isinstance(option, dict):
                for name in option:
                    self.set_option(name, option[name])
            else:
                if isinstance(option, str):
                    self.set_option(option)
                else:
                    raise TypeError("option '%s' of wrong type" % option)

    def get_args(self) -> list:
        """
        Возвращаем список аргументов
        :return: dict
        """
        args = []
        for option in self.options:
            argument = self.options[option]
            for arg in argument:
                opt = "--%s" % option if arg is None else "--%s=%s" % (
                    option, arg)
                args.append(opt)
        return args

    def get_command(self) -> list:
        """
        Умеет смысл переопределить этот метод в зависимотси от параметров
        :return: команда запуска
        :rtype: str|unicode
        """
        args = self.get_args()
        return self.binary + args
