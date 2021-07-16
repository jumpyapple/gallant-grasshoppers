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

        # Here is the current object of the game
        self.state = self.loadGame(save_name, save_location)

        self.bpt = 0

        # Here are all of the ones in the game
        self.available_upgrades = loader.upgrades
        self.available_achievements = loader.achievements
        self.available_generators = loader.generators

    # TODO will this ever be needed other than in testing.
    def __deleteSave(self) -> None:
        """Deletes the current save"""
        os.remove(self.save_location)

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

    def buyUpgrade(self, upgrade_id: str) -> bool:
        """*Given the upgrade id of an upgrade decrease the cash of the player adding upgrade to their list*"""
        # TODO index the available instead so that you don't need to do a search every time
        upgrade_to_buy = next(
            (
                upgrade
                for upgrade in self.available_upgrades
                if upgrade["ID"] == upgrade_id
            )
        )
        cost = next(
            (
                requirement.get("amount")
                for requirement in upgrade_to_buy["REQUIREMENTS"]
                if requirement["type"] == "CURRENCY"
            ),
            0,
        )

        if self.getCash()-cost < 0:
            return False

        self.changeCash(-cost)
        self.state[UPGRADES].append(upgrade_to_buy)
        self.recalculateBPT()
        return True

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

        bpt_obj = {}
        for generator in generators:
            bpt_obj[generator["ID"]] = {
                "bpt": generator["BPT"],
                "amount": generator["amount"],
                "multiplier": 1
            }

        general_upgrade_modifier = 1
        for upgrade in self.getUpgrades():
            modifiers = upgrade.get("MODIFIERS", None)
            if modifiers is None:
                return
       
            for modifier in modifiers:
                if modifier["modifier"] == "GENERAL":
                    if modifier["action"] == "MULTIPLY":
                        general_upgrade_modifier = general_upgrade_modifier * modifier["amount"]
                    else:
                        general_upgrade_modifier = general_upgrade_modifier + modifier["amount"]
                elif modifier["type"] == "GENERATOR" and modifier["id"] in bpt_obj:
                    generator_id = modifier["id"]

                    multiplier = bpt_obj[generator_id].get("multiplier", 1)
                    if modifier["action"] == "MULTIPLY":
                        multiplier = multiplier * modifier["amount"]
                    else:
                        multiplier = multiplier + modifier["amount"]

        new_bpt = 0
        for generator in bpt_obj.values():
            new_bpt = new_bpt + (generator["bpt"] * generator["amount"] * generator["multiplier"])
        new_bpt = new_bpt * general_upgrade_modifier

        self.bpt = new_bpt

    def makeBox(self) -> None:
        """Function will make a single box"""
        self.state[CASH] = self.state[CASH] + 1

    def getPurchasableGenerators(self) -> list:
        """Show all generators that the player can buy at any time

        Player must own at least 1 of the UNLOCK_ON requirement to unlock the other
        TODO find a way to not have torecalculate all of this eventually - for now just do
        TODO Right now the static/generators needs to be in order for this function to work as intended fix it
        """
        owned_generators = [generator["ID"] for generator in self.getGenerators()]

        purchasableGenerators = []
        for generator in self.available_generators:
            generator_id = generator["ID"]
            if (
                generator_id in owned_generators
                or generator.get("UNLOCK_ON", None) is None
            ):
                purchasableGenerators.append(generator_id)
                continue

            unlock_on = generator.get("UNLOCK_ON", None)
            if unlock_on is not None and unlock_on in owned_generators:
                purchasableGenerators.append(generator_id)
        # TODO in the future it maybe shouldn't just return the IDs of the generators
        return purchasableGenerators

    def getPurchasableUpgrades(self) -> list:
        """Show all of the upgrades the player can buy that they don't already own"""
        pass

    def getState(self) -> None:
        """Get the current state of the game as a dict"""
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
