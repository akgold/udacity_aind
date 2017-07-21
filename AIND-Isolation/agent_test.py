"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload

def tl():
	return 11

class MinimaxTest(unittest.TestCase):
	"""Unit tests for MinimaxTests"""

	reload(game_agent)
	player1 = game_agent.MinimaxPlayer()
	player1.time_left = tl
	player2 = game_agent.MinimaxPlayer()

	# setup a board with no moves to make sure returns correctly
	def trivial_setup(self):
		game = isolation.Board(self.player1, self.player2, 2, 2)
		game.apply_move((0, 1))
		game.apply_move((1, 0))
		return game

	def setUp(self, pos1 = (0, 1), pos2 = (1,0)):
		game = isolation.Board(self.player1, self.player2)
		game.apply_move(pos1)
		game.apply_move(pos2)
		return game

	# Test that minimax returns when no moves left
	def testTrivial(self):
		game = self.trivial_setup()
		ret = self.player1.minimax(game, 3)
		self.assertTrue(ret == (-1, -1), ret) 	

	def testMiniMax(self):
		game = self.setUp()
		ret = self.player1.minimax(game, 3)



class AlphaBetaTest(unittest.TestCase):
	reload(game_agent)
	player1 = game_agent.AlphaBetaPlayer()
	player2 = game_agent.AlphaBetaPlayer()

	def setUp(self):
		game = isolation.Board(self.player1, self.player2)
		game.apply_move((0, 1))
		game.apply_move((1, 0))
		return game

	def testAB(self):
		game = self.setUp()
		self.player1.time_left = tl
		print(self.player1.alphabeta(game, 4))

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)




if __name__ == '__main__':
    unittest.main()
