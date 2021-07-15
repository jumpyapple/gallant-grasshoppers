import unittest

from gallant_grasshoppers.lib.gamestate import GameState


class GameStateTest(unittest.TestCase):
    """All tests relating to testing the state of the game"""

    def setUp(self) -> None:
        """Generic Game Setup"""
        # print('I know Im creating a new game every test... its been a while... :)')
        self.Game = GameState()
        # return super().setUp()

    def test_ticker(self) -> None:
        """Make sure the increment works"""
        self.assertEqual(self.Game.getCash(), 0)
        for _ in range(5):
            self.Game.makeBox()
        self.assertEqual(self.Game.getCash(), 5)

    def test_isDataLoaded(self) -> None:
        """Check if the loader is working for GameState"""
        self.assertIsNotNone(self.Game.available_achievements)
        self.assertIsNotNone(self.Game.available_generators)
        self.assertIsNotNone(self.Game.available_upgrades)

    def test_buyUpgrade(self) -> None:
        """Buy a single upgrade from the list"""
        two_thousand = 2000
        # First give yourself some funds
        self.Game.changeCash(two_thousand)

        upgrade_to_buy = self.Game.available_upgrades[0]
        upgrade_id = upgrade_to_buy["ID"]
        upgrade_cost = upgrade_to_buy["REQUIREMENTS"][0]["amount"]

        self.Game.buyUpgrade(upgrade_id)
        game_cash = self.Game.getCash()

        self.assertEqual(len(self.Game.getUpgrades()), 1)
        self.assertEqual(two_thousand - upgrade_cost, game_cash)

    def test_changeCash(self) -> None:
        """Be able to inject extra cash into the players account but not go below zero"""
        self.assertEqual(self.Game.getCash(), 0)
        self.Game.changeCash(1000)
        self.assertEqual(self.Game.getCash(), 1000)
        self.Game.changeCash(-2000)
        self.assertEqual(self.Game.getCash(), 1000)
        self.Game.changeCash(-500)
        self.assertEqual(self.Game.getCash(), 500)

    def test_purchasableGenerators(self) -> None:
        """Should only show the basic generators unlocked from the start"""
        self.assertEqual(len(self.Game.getGenerators()), 0)
        self.assertEqual(len(self.Game.getPurchasableGenerators()), 2)


if __name__ == "__main__":
    unittest.main()
