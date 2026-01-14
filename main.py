from ui import run_game
from board import Board
import sys
import tests 
import unittest

def run_tests():
    print("🧪 Starte Unittests...")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(tests)
    runner = unittest.TextTestRunner(verbosity=3)
    runner.failfast = True
    result = runner.run(suite)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)

def main():  
    args = "ai"

    if args == "manual":
        board = Board()
        board.reset()
        run_game(board, True)
    elif args == "ai":
        board = Board()
        board.reset()
        run_game(board, False)
    elif args == "test":
        run_tests()

if __name__ == "__main__":
    main()
