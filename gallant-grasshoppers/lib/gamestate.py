from os import path
import json


SAVE_TEMPLATE = "../static/save_template.json"

DEFAULT_SAVE_NAME = "save.json"
DEFAULT_SAVE_LOCATION = "../saves"


class GameState:
    def __init__(self, save_name=None, save_location=None):
        self.state = self.loadGame(save_name, save_location)
        self.save_location = None

    def saveGame(self):
        pass

    def loadGame(self, save_name: str, save_location: str):
        # Check if the a location and name other was provided for the save
        # If not default
        self.save_location = (
            f"{save_location}/{save_name}"
            if save_name is not None and save_location is not None
            else f"{DEFAULT_SAVE_LOCATION}/{DEFAULT_SAVE_NAME}"
        )

        save_data_as_string = ""
        # Check to see if that save file exists, if not populate it with default data so that the game can start
        if not path.exists(self.save_location):
            with open(SAVE_TEMPLATE, "r") as File:
                save_data_as_string = File.read()

            with open(self.save_location, "w") as File:
                File.write(save_data_as_string)
        else:
            with open(self.save_location, 'r') as File:
                save_data_as_string = File.read()

        # Now load the data into the object as a dictionary
        self.state = json.loads(save_data_as_string)
        print(self.state)

    def changeCash(self, amount: int) -> None:
        self.state["cash"] = self.state["cash"] + amount

    def getCash(self) -> int:
        return self.state["cash"]

    def getGenerators(self):
        return self.state["generators"]

    def getUpgrades(self):
        return self.state["upgrades"]

    def getAchievements(self):
        return self.state["achievements"]

