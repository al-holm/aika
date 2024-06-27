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
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.class_name = class_name
        self.filename = os.path.abspath(
            os.path.join(self.DIR, f"configs/config-{class_name}.ini")
        )
        self._settings = {}
        self.load_config()

    def load_config(self):
        """
        reads the config file and store all settings in a dictionary.
        """
        try:
            self.config.read(self.filename)
            if "Settings" in self.config:
                for key in self.config["Settings"]:
                    self._settings[key] = self.config["Settings"][key]
        except FileNotFoundError:
            logging.ERROR(f"config file for clas {self.class_name} not found.")

    def get_settings(self):
        """
        returns the settings dictionary.
        """
        return self._settings

    def update_llm(self, llm: str):
        self.config.read(self.filename)
        self.config.set("Settings", "llm", llm)
        # save to a file
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)

    def set_llm(llm, task_type):
        config_agent = Config("agent")
        config_agent.update_llm(llm)
        config_tools = Config(f"tool-exe-{task_type.value}")
        config_tools.update_llm(llm)
