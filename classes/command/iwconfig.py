__author__ = 'alexeyymanikin'

from classes.command.command import Command
DEFAULT_ARGUMENTS = []


class Iwconfig(Command):
    """
    Класс для работы с iwconfig
    """

    OPTIONS = {
    }

    def __init__(self, interface: str):
        """
        :type url: unicode
        :type path: unicode
        :return:
        """
        super(Iwconfig, self).__init__("iwconfig")
        self.interface = interface

    def get_command(self) -> list:
        """
        :return: возвращаем команду запуска
        :rtype: list
        """

        return self.binary + [self.interface]
