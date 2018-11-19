
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
        self.move = None
        
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
            
            
    def minimax(self, node, depth, player, alpha, beta):
        if node.isWin() or node.isLose():
            
            return node.getScore()
        
        
        # Maximize function (Pacman)
        if player:
            value = float("-inf")
            for successor in node.generatePacmanSuccessors():
                if  self.isBestDepth(successor[0],depth): 
                    successor_value = self.minimax(successor[0], depth +1, 0, alpha, beta) 
                    
                    if successor_value > value:
                        value = successor_value
                        
                        if depth == 0:
                            self.move = successor[1]
                        if value >= beta:
                            return value
                        alpha = max (alpha,value)
                        
                        
           
            return value
        
        # Minimize function (Ghost)
        else:
            value = float("inf")
            
            for successor in node.generateGhostSuccessors(1):
                if self.isBestDepth(successor[0],depth) :
                    successor_value = self.minimax(successor[0], depth + 1, 1, alpha, beta)
                    
                    if successor_value < value:
                        value = successor_value
                       
                        if value <= alpha:
                            return value
                        beta = min(beta,value)
                        
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
        self.minimax(state, 0, 1,float("-inf"),float("inf"))
        
        return self.move
