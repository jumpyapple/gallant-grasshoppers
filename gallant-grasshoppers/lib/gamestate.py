from os import path
import json
from .load import Loader

SAVE_TEMPLATE = "../static/save_template.json"

DEFAULT_SAVE_NAME = "save.json"
DEFAULT_SAVE_LOCATION = "../saves"

# Constants for accessing the game data
CASH = 'cash'
GENERATORS = 'generators'
UPGRADES = 'upgrades'
ACHIEVEMENTS = 'achievements'



"""
TODO
* Generators need to be changed in order to account for how many of each you have
* There has to be a way to also save generators into the files
* ReIndex anything that has an ID so that it's easier to access it
"""
class GameState:

    def __init__(self, save_name: str = None, save_location: str = None):

        loader = Loader()

        self.save_location = save_location

        # Here is the current object of the game
        self.state = self.loadGame(save_name, save_location)

        self.modifiers = None # With time do something to recalculate the modifiers for te game state

        # Here are all of the ones in the game
        self.available_upgrades = loader.upgrades
        self.available_achievements = loader.achievements
        self.available_generators = loader.generators




    def saveGame(self):
        state_as_string = json.dumps(self.state)
        with open(self.save_location, 'w') as File:
            File.write(state_as_string)

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
            with open(self.save_location, "r") as File:
                save_data_as_string = File.read()

        # Now load the data into the object as a dictionary
        self.state = json.loads(save_data_as_string)
        print(self.state)

    def buyUpgrade(self, upgrade_id: str):
        # TODO index the available instead so that you don't need to do a search every time
        upgrade_to_buy = next(upgrade for upgrade in self.available_upgrades if upgrade["ID"] == upgrade_id)
        self.state[UPGRADES].append(upgrade_to_buy)

    def changeCash(self, amount: int) -> None:
        self.state[CASH] = self.state[CASH] + amount

    def getCash(self) -> int:
        return self.state[CASH]

    def getGenerators(self):
        return self.state[GENERATORS]

    def getUpgrades(self):
        return self.state[UPGRADES]

    def getAchievements(self):
        return self.state[ACHIEVEMENTS]
