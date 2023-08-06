#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This file is part of SysPass Client
#
# Copyright (C) 2020  DigDeo SAS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


import os
from colorama import init, Fore, Style
import syspassclient

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
init(autoreset=True)

# Inspired by: http://zetcode.com/python/yaml/
# Inspired by: https://gitlab.com/Tuuux/galaxie-little-alice/raw/master/GLXLittleAlice/Config.py
import threading

lock = threading.Lock()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# class Singleton(type):
#     instance = None
#
#     def __call__(cls, *args, **kw):
#         if not cls.instance:
#             cls.instance = super(Singleton, cls).__call__(*args, **kw)
#         return cls.instance


class Config(syspassclient.SyspassApi, metaclass=Singleton):
    def __init__(self):
        syspassclient.SyspassApi.__init__(self)

        # Load config file
        self.__rw = None
        self.__data = None
        self.__config_file = None
        self.__authToken = None
        self.__tokenPass = None

        self.rw = True

        self.read()

    @property
    def config_directory(self):
        if 'DD_SYSPASS_CLIENT_CONFIG_DIR' in os.environ:
            return os.path.realpath(os.environ['DD_SYSPASS_CLIENT_CONFIG_DIR'])
        else:
            return os.path.realpath(
                os.path.abspath(
                    os.path.join(
                        os.path.join(
                            os.environ['HOME'],
                            '.config'),
                        'digdeo-syspass-client'
                    )
                )
            )

    @property
    def config_file(self):
        return self.__config_file

    @config_file.setter
    def config_file(self, value=None):
        if self.config_file != value:
            self.__config_file = value

    @property
    def rw(self):
        return self.__rw

    @rw.setter
    def rw(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError('"rw" must be a bool type or None')
        if self.rw != value:
            self.__rw = value

    @property
    def authToken(self):
        # The goal is a function exit with a return as soon of possible
        # Enjoy cher!!!

        # Try the case it have more chance to match first
        if self.rw:
            # priority to the variable
            if 'DD_SYSPASS_CLIENT_AUTH_TOKEN' in os.environ:
                if self.debug and self.debug_level > 0:
                    print(Fore.WHITE + Style.BRIGHT + "DD_SYSPASS_CLIENT_AUTH_TOKEN: ", end='')
                    print(Fore.GREEN + Style.BRIGHT + "{0}".format(os.environ['DD_SYSPASS_CLIENT_AUTH_TOKEN']))
                return os.environ['DD_SYSPASS_CLIENT_AUTH_TOKEN']
            # a second chance from the config file
            if "authToken" in self.data:
                return self.data["authToken"]

        # Explicitly want a action in case of NOT , that is not a simple "else"
        if not self.rw:
            if 'DD_SYSPASS_CLIENT_AUTH_TOKEN_RO' in os.environ:
                if self.debug and self.debug_level > 0:
                    print(Fore.WHITE + Style.BRIGHT + "DD_SYSPASS_CLIENT_AUTH_TOKEN_RO: ", end='')
                    print(Fore.GREEN + Style.BRIGHT + "{0}".format(os.environ['DD_SYSPASS_CLIENT_AUTH_TOKEN_RO']))
                return os.environ['DD_SYSPASS_CLIENT_AUTH_TOKEN_RO']
            if "authTokenRO" in self.data:
                return self.data["authTokenRO"]

        # It is our else
        return None

    @property
    def tokenPass(self):
        if self.rw:
            if 'DD_SYSPASS_CLIENT_TOKEN_PASS' in os.environ:
                if self.debug and self.debug_level > 0:
                    print(Fore.WHITE + Style.BRIGHT + "DD_SYSPASS_CLIENT_TOKEN_PASS: ", end='')
                    print(Fore.GREEN + Style.BRIGHT + "{0}".format(os.environ['DD_SYSPASS_CLIENT_TOKEN_PASS']))
                return os.environ['DD_SYSPASS_CLIENT_TOKEN_PASS']
            if "tokenPass" in self.data:
                return self.data["tokenPass"]

        if not self.rw:
            if 'DD_SYSPASS_CLIENT_TOKEN_PASS_RO' in os.environ:
                if self.debug and self.debug_level > 0:
                    print(Fore.WHITE + Style.BRIGHT + "DD_SYSPASS_CLIENT_TOKEN_PASS_RO: ", end='')
                    print(Fore.GREEN + Style.BRIGHT + "{0}".format(os.environ['DD_SYSPASS_CLIENT_TOKEN_PASS_RO']))
                return os.environ['DD_SYSPASS_CLIENT_TOKEN_PASS_RO']
            if "tokenPassRO" in self.data:
                return self.data["tokenPassRO"]

        return None

    @property
    def api_url(self):
        if 'DD_SYSPASS_CLIENT_API_URL' in os.environ:
            print(Fore.WHITE + Style.BRIGHT + "DD_SYSPASS_CLIENT_API_URL: ", end='')
            print(Fore.GREEN + Style.BRIGHT + "{0}".format(os.environ['DD_SYSPASS_CLIENT_API_URL']))
            return os.environ['DD_SYSPASS_CLIENT_API_URL']
        if "api_url" in self.data:
            return self.data["api_url"]
        return None

    @property
    def data(self):
        """
        Return the config file as Python dictionary structure

        :return: Config as a big dictionary
        :rtype: dict
        """
        return self.__data

    @data.setter
    def data(self, parameters):
        """
        set en data and raise in case of error

        :param parameters: something it like a dictionary key
        :type parameters: dict
        :raise TypeError: 'parameters' is not a dict type
        """
        if self.__data != parameters:
            self.__data = parameters

    def write(self, api_file=None):
        """
        Write the config file

        :param api_file: the file where write data, or None for default one.
        :type api_file: str or None
        """
        if api_file is None:
            api_file = self.api_file

        with open(api_file, "w") as f:
            if self.debug and self.debug_level > 1:
                print(Fore.YELLOW + Style.BRIGHT + "{0}: ".format(self.__class__.__name__.upper()), end='')
                print(Fore.WHITE + Style.BRIGHT + "{0} ".format("Write API file".title()))

                print(Fore.WHITE + Style.BRIGHT + "file: ".title(), end='')
                print(str(self.api_file))
            dump(self.data, f)
            f.close()
            for line in dump(self.data).split("\n"):
                if self.verbose:
                    print(Fore.RED + Style.BRIGHT + "> " + Fore.RESET + Style.RESET_ALL + str(line))

    def read(self,
             api_file=None,
             config_file=None,
             debug=None,
             debug_level=None,
             verbose=None,
             verbose_level=None
             ):
        """
        Read the configuration file

        :param api_file: the file path to to load
        :type api_file: str or None for the default one
        :param config_file: the file it store the dd_ansible_syspass
        :type config_file: str or None for default
        :param debug: True for enable debug
        :type debug: bool
        :param debug_level: The amount of debug message . > 2 will display password in the console
        :type debug_level: int
        :param verbose: True if the syspassclient will write normal operation to the console
        :type verbose: bool
        :param verbose_level: The amount of verbose message you want >2 is really verbose
        :type verbose_level: int
        """
        if config_file is None:
            config_file = self.get_config_file()

        if api_file is None:
            api_file = self.api_file

        # with open(api_file) as f:
        #     self.data = load(f, Loader=Loader)
        #     f.close()
        #     if self.debug and self.debug_level > 1:
        #         print(Fore.YELLOW + Style.BRIGHT + "{0}: ".format(self.__class__.__name__.upper()), end='')
        #         print(Fore.WHITE + Style.BRIGHT + "{0} ".format("Load API File"))
        #
        #         print(Fore.WHITE + Style.BRIGHT + "File: ", end='')
        #         print(api_file)
        #
        #         if self.debug and self.debug_level > 2:
        #             for line in dump(self.data).split("\n"):
        #                 if self.verbose:
        #                     print(Fore.CYAN + Style.BRIGHT + "< " + Fore.RESET + Style.RESET_ALL + str(line))
        self.read_api()
        self.data = self.api_data

        with open(config_file) as f:
            config = load(f, Loader=Loader)
            f.close()
            # print(config)

            if 'syspassclient' not in config:
                raise AttributeError('{0} do not contain syspassclient attribute'.format(config_file))

            if config["syspassclient"] is None:
                raise ImportError('nothing to import ...')

            if "api_url" in config["syspassclient"]:
                self.data["api_url"] = config["syspassclient"]["api_url"]

            if "api_version" in config["syspassclient"]:
                self.data["api_version"] = config["syspassclient"]["api_version"]
                self.api_version = self.data["api_version"]

            if "authToken" in config["syspassclient"]:
                self.data["authToken"] = config["syspassclient"]["authToken"]

            if "tokenPass" in config["syspassclient"]:
                self.data["tokenPass"] = config["syspassclient"]["tokenPass"]

            if "debug" in config["syspassclient"]:
                self.data["debug"] = config["syspassclient"]["debug"]

            if "debug_level" in config["syspassclient"]:
                self.data["debug_level"] = config["syspassclient"]["debug_level"]

            if "verbose" in config["syspassclient"]:
                self.data["verbose"] = config["syspassclient"]["verbose"]

            if "verbose_level" in config["syspassclient"]:
                self.data["verbose_level"] = config["syspassclient"]["verbose_level"]

            if debug is None:
                if "debug" in self.data:
                    self.debug = self.data["debug"]
                else:
                    self.debug = True
            else:
                self.debug = debug

            if debug_level is None:
                if "debug_level" in self.data:
                    self.debug_level = self.data["debug_level"]
                else:
                    self.debug_level = 3
            else:
                self.debug_level = debug_level

            if verbose is None:
                if "verbose" in self.data:
                    self.verbose = self.data["verbose"]
                else:
                    self.verbose = True
            else:
                self.verbose = verbose

            if verbose_level is None:
                if "verbose_level" in self.data:
                    self.verbose_level = self.data["verbose_level"]
                else:
                    self.verbose_level = 3
            else:
                self.verbose_level = verbose_level

        if self.debug and self.debug_level > 1:
            print(Fore.YELLOW + Style.BRIGHT + "{0}: ".format(self.__class__.__name__.upper()), end='')
            print(Fore.WHITE + Style.BRIGHT + "{0} ".format("Load Config File"))

            print(Fore.WHITE + Style.BRIGHT + "File: ", end='')
            print(self.get_config_file())

            if self.debug_level > 2:
                print(
                    Fore.WHITE + Style.BRIGHT +
                    "api_url:" +
                    Style.RESET_ALL +
                    " {0}".format(self.data["api_url"])
                )
                print(
                    Fore.WHITE + Style.BRIGHT +
                    "authToken:" +
                    Style.RESET_ALL +
                    " {0}".format(self.authToken)
                )
                print(
                    Fore.WHITE + Style.BRIGHT +
                    "tokenPass:" +
                    Style.RESET_ALL +
                    " {0}".format(self.tokenPass)
                )

            print(
                Fore.WHITE + Style.BRIGHT +
                "debug:" +
                Style.RESET_ALL + Fore.RESET +
                " {0}".format(self.debug)
            )
            print(
                Fore.WHITE + Style.BRIGHT +
                "debug_level:" +
                Style.RESET_ALL + Fore.RESET +
                " {0}".format(self.debug_level)
            )
            print(
                Fore.WHITE + Style.BRIGHT +
                "verbose:" +
                Style.RESET_ALL + Fore.RESET +
                " {0}".format(self.verbose)
            )
            print(
                Fore.WHITE + Style.BRIGHT + "verbose_level:" + Style.RESET_ALL + Fore.RESET +
                " {0}".format(self.verbose_level)
            )

    def reset(self):
        if self.api_version == "3.0":
            self.data = self.api_3_0
        else:
            self.data = self.api_3_1

    def get_data(self):
        """
        return teh data dictionary

        :return: the data dictionary
        :rtype: dit
        """
        return self.data

    @staticmethod
    def get_empty_config_dict():
        return {
            'syspassclient': {
                'api_url': None,
                'api_version': '3.1',
                'authToken': None,
                'tokenPass': None,
                'debug': True,
                'debug_level': 3,
                'verbose': False,
                'verbose_level': 0
            }
        }

    def get_config_file(self):
        return os.path.join(
            self.config_directory,
            "config.yml",
        )
