from os import path

UPGRADES_FILE_LOCATION = "../static/upgrades.json"
ACHIEVEMENTS_FILE_LOCATION = "../static/achievements.json"
UPGRADES_FILE_LOCATION = "../static/upgrades.json"


"""
Goal is to create a generic loader so that once the game loop has started we can have access to all of the
upgrades, achievements, generators in the game in a single format
"""


class Loader:
    def __init__(self, upgradesPath=UPGRADES_FILE_LOCATION, achievementsPath=None, generatorsPath=None):
        self.upgrades = self.loadJSON(upgradesPath)
        self.achievements = self.loadJSON(achievementsPath)
        self.generators = self.loadJSON(generatorsPath)


    def loadJSON(self, filePath: str):
        if not path.exists(filePath):
            raise Exception(f"Could not find file in location {filePath}")

        upgrades_json = None
        with open(filePath, "r") as File:
            upgrades_json = File.read()

        return upgrades_json


if __name__ == "__main__":
    static_data = Loader()
    print(static_data.upgrades)
