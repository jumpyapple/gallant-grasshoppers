from os import path

UPGRADES_FILE_LOCATION = "../static/upgrades.json"

"""
Goal is to create a generic loader so that once the game loop has started we can have access to all of the
upgrades, achievements, generators in the game in a single format
"""


class Loader:
    def __init__(self):
        self.upgrades = []
        self.achievements = []
        self.generators = []

    def loadUpgrades(self, filePath):
        if not path.exists(filePath):
            raise Exception(f"Could not find file in location {filePath}")

        upgrades_json = None
        with open(filePath, "r") as File:
            # print(File.read())
            upgrades_json = File.read()

        return upgrades_json

    def loadAchievements(self, filePath):
        pass


if __name__ == "__main__":
    upgrades = Loader().loadUpgrades(UPGRADES_FILE_LOCATION)
    print(upgrades)
