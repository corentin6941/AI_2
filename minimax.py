
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
        self.dictExpanded = {}
        
        
    def hashPosFood(self, state):
        """
        Arguments:
        ----------
        - `state`: a game state see `pacman.GameState`.

        Return:
        -------

        -`key`: a string that is made with the position of
        pacman hashed and the grid of position
        of foods (getFood) hashed.

        Note:
        -----
        Only the two data of the state mentioned above are taken
        into account in the hash function.

        """
        hash1 = hash(state.getPacmanPosition())
        hash2 = hash(state.getFood())
        hash3 = hash(state.getGhostPosition(1))
        key = str(hash1) + ' ' + str(hash2) + ' ' + str(hash3)
        return key
    def inExplored(state)
        key = self.hashPosFood(state)
        
        pacmanPos = state.getPacmanPosition()
        food = state.getFood()
        ghostPos = state.getGhostPosition()
        
        list =[pacmanPos, food, ghostPos]
        if key not in self.dictExpanded:
            self.dictExpanded[key] = [list]
            return False
        else :
            for element in dictionnary[key]:
                if element == list :
                    return True
            self.dictExpanded[key].append(list)
            return False
            
            
    def minimax(self, node, depth, player, dictionnary):
        if depth == 0 or node[0].isWin() or node[0].isLose() or self.inExpanded(node[0]):
            print (node[0].getScore(), node[1])
            return (node[0].getScore(), node[1])
        
        # Maximize function (Pacman)
        if player:
            value = (float("-inf"), "Directions.STOP")
            for successor in node[0].generatePacmanSuccessors():
                
                key = self.hashPosFood(successor[0])
                if key not in dictionnary:
                    pacmanPos = successor[0].getPacmanPosition()
                    food = successor[0].getFood()
                    ghostPos = successor[0].getGhostPosition(1)
                    dictionnary[key] = [[pacmanPos, food, ghostPos]]
                    successor_value = self.minimax(successor, depth - 1, 0, dictionnary)
                    tmp = max(value[0], successor_value[0])
                    if(tmp == successor_value[0]):
                        value = successor_value
                    print (value[1])
            return value
        
        # Minimize function (Ghost)
        else:
            value = (float("inf"), "Directions.STOP")
            for successor in node[0].generateGhostSuccessors(1):
                key = self.hashPosFood(successor[0])
                if key not in dictionnary:
                    pacmanPos = successor[0].getPacmanPosition()
                    food = successor[0].getFood()
                    ghostPos = successor[0].getGhostPosition(1)
                    dictionnary[key] = [[pacmanPos, food, ghostPos]]
                    successor_value = self.minimax(successor, depth - 1, 1, dictionnary)
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
        dictExpanded = {}
        node = (state, "Directions.STOP")
        move = self.minimax(node, 2, 1, dictExpanded)
        print(move)
        return move[1][1]
