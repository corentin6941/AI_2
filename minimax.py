
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
                successor_value = self.minimax(successor, depth - 1, 0)
                tmp = max(value[0], successor_value[0])
                if(tmp == successor_value[0]):
                    value = successor_value
                print (value[1])
            return value
        
        # Minimize function (Ghost)
        else:
            value = (float("inf"), "Directions.STOP")
            for successor in node[0].generateGhostSuccessors(1):
                successor_value = self.minimax(successor, depth - 1, 1)
                tmp = min(value[0], successor_value[0])
                if(tmp == successor_value[0]):
                    value = successor_value
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
        move = self.minimax(node, 2, 1)
        print(move)
        return move[1][1]
