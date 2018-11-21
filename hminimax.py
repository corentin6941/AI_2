
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
        self.posFoods =[]
        self.dictVisited = {}  
        
    def manhattanDistance(self, xy1, xy2):
        """

        Arguments:
        ----------
        - `xy1`,`xy2`: two position [x1,y1] and [x2,y2].

        Return:
        -------
        - the manhattan distance between the two position xy1 an xy2

         (This function was given in the file util.py)
        """

        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
    
    def evals(self,state):
        
        if state.isLose():
            return float("-inf")
        
        
        
        score = state.getScore() 
        ghostPos = state.getGhostPositions()[0]
        pacmanPos = state.getPacmanPosition()
        distGhost = self.manhattanDistance(ghostPos,pacmanPos)
        
        if state.isWin():
            return self.maxScore+score
        
     
        gridFood =state.getFood()
        nbFoods = state.getNumFood()
        
        
        distFoodMax =0
        distFoodMin = (gridFood.height+gridFood.width)
        
        for posFood in self.posFoods:
            
            if gridFood[posFood[0]][posFood[1]]:
                distFood = self.manhattanDistance(posFood,pacmanPos)
               
                if distFoodMax < distFood:
                    distFoodMax = distFood

                    
                if distFoodMin > distFood:
                    distFoodMin =distFood

       
        return score - 1*distFoodMin +0.09*distGhost  -4*nbFoods
    
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
    
    def isVisited(self,state):
        key = self.hashPosFood(state)
        
        pacmanPos = state.getPacmanPosition()
        food = state.getFood()
        ghostPos = state.getGhostPositions()
        
        stateComponent = (pacmanPos, food, ghostPos)
        if key not in self.dictVisited:
            return False
        else :
            for element in self.dictVisited[key]:
                if element == stateComponent :
                    return True
            return False
            
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
        if depth ==10 or node.isWin() or node.isLose():
            
            return self.evals(node)
        
        
        # Maximize function (Pacman)
        if player:
            
            value = float("-inf")
            hasNoneChild = True
            for successor in node.generatePacmanSuccessors():
                
                if self.isVisited(successor[0]):
                    continue
                
                if  self.isBestDepth(successor[0],depth): 
                    
                    successor_value = self.minimax(successor[0], depth +1, 0, alpha, beta)

                    if not successor_value :
                        continue
                    if successor_value > value:
                        value = successor_value
                        hasNoneChild = False
                        if depth == 0:
                            
                            self.move = successor[1]
                        if value >= beta:
                            return value
                        alpha = max (alpha,value)
                        
                       
            if hasNoneChild:
                return None
            return value
        
        # Minimize function (Ghost)
        else:
            value = float("inf")
            hasNoneChild = True
            for successor in node.generateGhostSuccessors(1):
                if self.isVisited(successor[0]):
                    continue
                if self.isBestDepth(successor[0],depth) :
                    
                    successor_value = self.minimax(successor[0], depth + 1, 1, alpha, beta)
                    if not successor_value :
                        continue
                    if successor_value < value:
                        value = successor_value
                        hasNoneChild = False
                       
                        if value <= alpha:
                            return value
                        beta = min(beta,value)
                        
            if hasNoneChild:
                return None
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
        
        self.move = Directions.STOP
        if not self.posFoods:
            
            gridFood = state.getFood()
            self.maxScore = state.getNumFood()*10 +0.09*(gridFood.height +gridFood.width)+700
            
            for i in range(gridFood.width):
                for j in range(gridFood.height):
                    if gridFood[i][j]:
                        self.posFoods.append([i,j])
                        
        key = self.hashPosFood(state)
        
        pacmanPos = state.getPacmanPosition()
        food = state.getFood()
        ghostPos = state.getGhostPositions()
        
        stateComponent = (pacmanPos, food, ghostPos)
        
        if key not in self.dictVisited:
            
            self.dictVisited[key] = [stateComponent]
        else:
            self.dictVisited[key].append(stateComponent)
            
        self.minimax(state, 0, 1,float("-inf"),float("inf"))

        if self.move == Directions.STOP:
            
            self.dictVisited = {}
            self.dictExpanded ={}
            
            self.minimax(state, 0, 1,float("-inf"),float("inf"))

        return self.move
