import json
from os import path
from os.path import dirname
from pathlib import Path

# Use this python file location to find the project root.
PROJECT_ROOT = Path(dirname(dirname(__file__)))
UPGRADES_FILE_LOCATION = PROJECT_ROOT / "static" / "upgrades.json"
ACHIEVEMENTS_FILE_LOCATION = PROJECT_ROOT / "static" / "achievements.json"
GENERATORS_FILE_LOCATION = PROJECT_ROOT / "static" / "generators.json"


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
        generatorsPath: str = GENERATORS_FILE_LOCATION,
    ) -> None:
        self.upgrades = self.load_json(upgradesPath)
        self.achievements = self.load_json(achievementsPath)
        self.generators = self.load_json(generatorsPath)

    def load_json(self, file_path: str) -> dict:
        """Generic json loader that checks to see if the file exists before loading in data as a dict"""
        if not path.exists(file_path):
            raise Exception(f"Could not find file in location {file_path}")

        loaded_json = None
        with open(file_path, "r") as file:
            loaded_json = file.read()

        return json.loads(loaded_json)
