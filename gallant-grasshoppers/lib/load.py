from os import path
import json

UPGRADES_FILE_LOCATION = "../static/upgrades.json"
ACHIEVEMENTS_FILE_LOCATION = "../static/achievements.json"
UPGRADES_FILE_LOCATION = "../static/upgrades.json"


"""
Goal is to create a generic loader so that once the game loop has started we can have access to all of the
upgrades, achievements, generators in the game in a single format
"""


class Loader:
    """Loader class to get all static data needed for the game"""

    def __init__(
        self,
        upgradesPath: str = UPGRADES_FILE_LOCATION,
        achievementsPath: str = ACHIEVEMENTS_FILE_LOCATION,
        generatorsPath: str = UPGRADES_FILE_LOCATION,
    ) -> None:
        self.upgrades = self.loadJSON(upgradesPath)
        self.achievements = self.loadJSON(achievementsPath)
        self.generators = self.loadJSON(generatorsPath)

    def loadJSON(self, filePath: str) -> dict:
        """Generic json loader that checks to see if the file exists before loading in data as a dict"""
        if not path.exists(filePath):
            raise Exception(f"Could not find file in location {filePath}")

        loaded_json = None
        with open(filePath, "r") as File:
            loaded_json = File.read()

        return json.loads(loaded_json)


if __name__ == "__main__":
    static_data = Loader()
    # print(static_data.upgrades)
