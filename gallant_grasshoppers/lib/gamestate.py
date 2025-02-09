import json
import os
from os.path import dirname
from pathlib import Path

from .load import Loader

# Use this python file location to find the project root.
PROJECT_ROOT = Path(dirname(dirname(__file__)))

SAVE_TEMPLATE = PROJECT_ROOT / "static" / "save_template.json"

DEFAULT_SAVE_NAME = "save.json"
DEFAULT_SAVE_LOCATION = PROJECT_ROOT / "saves"

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
* Remember to only use ints and no floats
"""


class GameState:
    """Class to manage everything relating to game specific data v1 implementation"""

    def __init__(self, save_name: str = None, save_location: str = None):

        loader = Loader()

        self.save_location = save_location

        # jumpyapple: We will delay the save loading until user decide if they
        # want to continue from the save or start a new session.

        # The `_` in the name is because we will be using @property.
        self._phase = "manual"  # the default phase is manual.
        self.bpt = 0

        # Here are all of the ones in the game
        self.available_upgrades = loader.upgrades
        self.available_achievements = loader.achievements
        self.available_generators = loader.generators

    @property
    def phase(self) -> str:
        """Getter of _phase."""
        return self._phase

    @phase.setter
    def phase(self, phase: str) -> None:
        """Setter of _phase."""
        self._phase = phase

    # TODO will this ever be needed other than in testing.
    def __deleteSave(self) -> None:
        """Deletes the current save"""
        os.remove(self.save_location)

    def newGame(self) -> None:
        """Return from template the empty save game."""
        self.save_location = f"{DEFAULT_SAVE_LOCATION}/{DEFAULT_SAVE_NAME}"

        with open(SAVE_TEMPLATE, "r") as f:
            return json.load(f)

    def saveGame(self) -> None:
        """Convert state into a json string and save it to a file"""
        self.state["phase"] = self._phase

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
        if not os.path.exists(self.save_location):
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

    def buyGenerator(self, generator_id: str) -> bool:
        """Given the generatorId add the generator to your list of generators

        Remember to check if there is enough funds
        Remember to recalculate the bpt or boxes per tick?
        """
        # TODO whole function can be better optimized do that later
        generator_to_buy = next(
            (
                generator
                for generator in self.available_generators
                if generator["ID"] == generator_id
            ),
            None,
        )

        if generator_to_buy is None:
            return False

        cost = generator_to_buy["COST"]
        if self.getCash() - cost < 0:
            return False

        has_generator = self.state[GENERATORS].get(generator_id, None)
        if has_generator is None:
            # If the player doesn't already own a generator add the data and set amount to 1
            self.state[GENERATORS][generator_id] = generator_to_buy.update(
                {"amount": 1}
            )
        else:
            self.state[GENERATORS][generator_id]["amount"] = (
                self.state[GENERATORS][generator_id]["amount"] + 1
            )

        self.recalculateBPT()

        return True

    def recalculateBPT(self) -> None:
        """Use all upgrades and generators to recalculate the new value for bpt"""
        # First do all calculations that are relating to the generators
        generators = self.getGenerators()

        new_bpt = 0
        for generator in generators:
            bpt = generator["BPT"]
            amount = generator["amount"]
            new_bpt = new_bpt + (bpt * amount)
        self.bpt = new_bpt

        # Now add the multiplyers of the upgrades
        upgrades = self.getUpgrades()
        print(upgrades)

    def makeBox(self) -> None:
        """Function will make a single box"""
        self.state[CASH] = self.state[CASH] + 1

    def getPurchasableGenerators(self) -> list:
        """Show all generators that the player can buy at any time"""
        pass

    def getPurchasableUpgrades(self) -> list:
        """Show all of the upgrades the player can buy that they don't already own"""
        pass

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
