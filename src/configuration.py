"""Class representing configuration of Chainring."""

#
#  (C) Copyright 2017, 2018  Pavel Tisnovsky
#
#  All rights reserved. This program and the accompanying materials
#  are made available under the terms of the Eclipse Public License v1.0
#  which accompanies this distribution, and is available at
#  http://www.eclipse.org/legal/epl-v10.html
#
#  Contributors:
#      Pavel Tisnovsky
#

import configparser


class Configuration:
    """Class representing configuration of Chainring."""

    CONFIG_FILE_NAME = "config.ini"

    def __init__(self, path="."):
        """Initialize the class."""
        self.config = configparser.ConfigParser()
        self.config.read(path + "/" + Configuration.CONFIG_FILE_NAME)

    @property
    def window_width(self):
        """Property holding window width."""
        v = self.config.getint("ui", "window_width")
        return v

    @property
    def app_type(self):
        """Property holding application type."""
        return self.config.get("ui", "app_type")

    @property
    def window_height(self):
        """Property holding window height."""
        return self.config.getint("ui", "window_height")

    @property
    def server_address(self):
        """Property holding server address."""
        return self.config.get("service", "url")

    @property
    def server_port(self):
        """Property holding server port."""
        return self.config.getint("service", "port")

    def write(self):
        """Write the configuration back to disk under different name."""
        with open("config2.ini", "w") as fout:
            self.config.write(fout)
