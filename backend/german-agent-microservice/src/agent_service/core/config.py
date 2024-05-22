import configparser
import os
import logging

class Config:
    """
    reads a configuration file and stores settings in a dictionary for a
    specified class.
    """
    DIR = os.path.dirname(__file__)
    def __init__(self, class_name):
        self.config = configparser.ConfigParser()
        self.class_name = class_name
        self.filename = os.path.abspath(os.path.join(self.DIR, f'config-{class_name}.ini'))
        self._settings = {}
        self.load_config()

    def load_config(self):
        """
        reads the config file and store all settings in a dictionary.
        """
        try:
            self.config.read(self.filename)
            if 'Settings' in self.config:
                for key in self.config['Settings']:
                    self._settings[key] = self.config['Settings'][key]
        except FileNotFoundError:
            logging.ERROR(f"config file for clas {self.class_name} not found.")

    def get_settings(self):
        """
        returns the settings dictionary.
        """
        return self._settings