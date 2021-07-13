import json
from os import path

from load import Loader

SAVE_TEMPLATE = "../static/save_template.json"

DEFAULT_SAVE_NAME = "save.json"
DEFAULT_SAVE_LOCATION = "../saves"

# Constants for accessing the game data
CASH = "cash"
GENERATORS = "generators"
UPGRADES = "upgrades"
ACHIEVEMENTS = "achievements"

DEFAULT_TICK_TIME = 1

"""
TODO
* Generators need to be changed in order to account for how many of each you have
* There has to be a way to also save generators into the files
* ReIndex anything that has an ID so that it's easier to access it
"""


class GameState:
    """Class to manage everything relating to game specific data v1 implementation"""

    def __init__(self, save_name: str = None, save_location: str = None):

        loader = Loader()

        self.save_location = save_location

        # Here is the current object of the game
        self.state = self.loadGame(save_name, save_location)

        self.modifiers = None  # With time do something to recalculate the modifiers for te game state

        # Here are all of the ones in the game
        self.available_upgrades = loader.upgrades
        self.available_achievements = loader.achievements
        self.available_generators = loader.generators

    def saveGame(self) -> None:
        """Convert state into a json string and save it to a file"""
        state_as_string = json.dumps(self.state)
        with open(self.save_location, "w") as File:
            File.write(state_as_string)

    def loadGame(self, save_name: str, save_location: str) -> None:
        """Check if a save already exists, if not create a clean one for first boot"""
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
        return json.loads(save_data_as_string)

    def changeCash(self, amount: int) -> bool:
        """Function to be used when changing the users cash, use negative value to represent cost"""
        if (self.getCash() + amount) < 0:
            return False

        self.state[CASH] = self.state[CASH] + amount
        return True

    def buyUpgrade(self, upgrade_id: str) -> None:
        """*Given the upgrade id of an upgrade decrease the cash of the player adding upgrade to their list*"""
        # TODO index the available instead so that you don't need to do a search every time
        upgrade_to_buy = next(
            (
                upgrade
                for upgrade in self.available_upgrades
                if upgrade["ID"] == upgrade_id
            )
        )
        # TODO maybe change this into have a more intuitive location for cost
        cost = next(
            (
                requirement.get("amount")
                for requirement in upgrade_to_buy["REQUIREMENTS"]
                if requirement["type"] == "CURRENCY"
            ),
            0,
        )

        #  TODO fail if the player does not have enough cash

        self.changeCash(-cost)
        self.state[UPGRADES].append(upgrade_to_buy)

    def makeBox(self) -> None:
        """Function will make a single box"""
        self.state[CASH] = self.state[CASH] + 1

    def getState(self) -> None:
        """Get the current state of the game as s dict"""
        return self.state

    def getCash(self) -> int:
        """Getter function for cash"""
        return self.state[CASH]

    def getGenerators(self) -> list:
        """Getter functon for generators list that the user unlocked"""
        return self.state[GENERATORS]

    def getUpgrades(self) -> list:
        """Getter functon for upgrades list that the user unlocked"""
        return self.state[UPGRADES]

    def getAchievements(self) -> list:
        """Getter functon for achievements list that the user unlocked"""
        return self.state[ACHIEVEMENTS]
