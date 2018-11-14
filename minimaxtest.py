
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
        posGhost = state.getGhostPositions()[0]
        hash3 = hash((posGhost[0],posGhost[1]))
        key = str(hash1) + ' ' + str(hash2) + ' ' + str(hash3)
        return key
    
    def isBestDepth(self,state, depth):
        key = self.hashPosFood(state)
        
        pacmanPos = state.getPacmanPosition()
        food = state.getFood()
        ghostPos = state.getGhostPositions()
        
        stateComponent = (pacmanPos, food, ghostPos)
        if key not in self.dictExpanded:
            self.dictExpanded[key] = [[stateComponent,depth]]
            return True
        else :
            for element in self.dictExpanded[key]:
                if element[0] == stateComponent :
                    if depth < element[1]:
                        element[1] = depth
                        return True
                    return False
            self.dictExpanded[key].append([stateComponent,depth])
            return True
            
            
    def minimax(self, node, depth, player):
        if node[0].isWin() or node[0].isLose():
            
            return (node[0].getScore(), node[1])
        
        
        # Maximize function (Pacman)
        if player:
            value = [float("-inf"), "Directions.STOP"]
            for successor in node[0].generatePacmanSuccessors():
                if  self.isBestDepth(successor[0],depth): 
                    successor_value = self.minimax(successor, depth +1, 0) 
                    if successor_value[0] > value[0] :
                        value[0] = successor_value[0]
                        value[1] = successor[0]
            return value
        
        # Minimize function (Ghost)
        else:
            value = [float("inf"), "Directions.STOP"]
            
            for successor in node[0].generateGhostSuccessors(1):
                if self.isBestDepth(successor[0],depth) :
                    successor_value = self.minimax(successor, depth + 1, 1)
                    if successor_value[0] < value[0]:
                        value[0] = successor_value[0]
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
        move =[state,"Directions.STOP"]
       
        node = (state, "Directions.STOP")
        move = self.minimax(node, 0, 1)
        
        return move[1]
