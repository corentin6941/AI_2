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
        self.listAction = []
        
        
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
        
        list =[pacmanPos, food, ghostPos, depth]
        if key not in self.dictExpanded:
            self.dictExpanded[key] = [list]
            return True
        else :
            for element in self.dictExpanded[key]:
                if element == list :
                    if depth < element[3]:
                        element[3] = depth
                    return True
            self.dictExpanded[key].append(list)
            return True
            
            
    def minimax(self, node, depth, player):
        if depth == 0 or node[0].isWin() or node[0].isLose():
            print (node[0].getScore(), node[1])
            return (node[0].getScore(), [node[1]])
        
        
        # Maximize function (Pacman)
        if player:
            value = (float("-inf"), ["Directions.STOP"])
            for successor in node[0].generatePacmanSuccessors():
                if  self.isBestDepth(node[0],depth): 
                    successor_value = self.minimax(successor, depth - 1, 0) 
                    tmp = max(value[0], successor_value[0])
                    if tmp == successor_value[0]:
                        value = successor_value
                        childDirList = successor_value[1]
                   
            newDirAction = [node[1]] + newDirectionList
            return (value[0], newDirAction)
        
        # Minimize function (Ghost)
        else:
            value = (float("inf"), ["Directions.STOP"])
            for successor in node[0].generateGhostSuccessors(1):
                if self.isBestDepth(node[0],depth) :
                    successor_value = self.minimax(successor, depth - 1, 1)
                    tmp = min(value[0], successor_value[0])
                    if tmp == successor_value[0] :
                        value[0] = successor_value[0]
                        childDirList = successor_value[1]
                    print (value[1])
                    
            newDirAction = [node[1]]+ childDirAction   
            return (value[0], newDirAction)

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
        if not self.listAction:
            node = (state, "Directions.STOP")
            move = self.minimax(node, 2, 1)
            self.listAction = move[1]
        
        return self.listAction.pop(0)
