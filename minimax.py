
from pacman_module.game import Agent
from pacman_module.pacman import Directions


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        
    def minimax(self, node, depth, player):
        if depth == 0 or node[0].isWin() or node[0].isLose():
            print (node[0].getScore(), node[1])
            return (node[0].getScore(), node[1])
        
        # Maximize function (Pacman)
        if player:
            value = (float("-inf"), "Directions.STOP")
            for successor in node[0].generatePacmanSuccessors():
                value = max(value, self.minimax(successor, depth + 1, 0))
                print (value[1])
            return value
        
        # Minimize function (Ghost)
        else:
            value = (float("inf"), "Directions.STOP")
            for successor in node[0].generateGhostSuccessors(1):
                value = min(value, self.minimax(successor, depth + 1, 1))
                print (value[1])
            return value

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        node = (state, "Directions.STOP")
        move = self.minimax(node, 0, 1)
        print(move)
        return move[1][1]
