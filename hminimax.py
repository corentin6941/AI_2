
from pacman_module.game import Agent
from pacman_module.pacman import Directions
from random import randint

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
        self.nbMaxFood =None
         
        self.a1= 1.4
        self.a2= 1.2
        self.a3= 1
#        self.a1= 1+0.1*randint(0,8)
#        self.a2= 1+0.1*randint(0,8)
#        self.a3= randint(0,10)
#        self.a1= 2.1+0.01*randint(0,20)
#        self.a2= 1.7+0.01*randint(0,20)
#        self.a3= randint(0,10)
        print("({}, {},{})".format(self.a1,self.a2,self.a3))
        
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
            return score
     
        gridFood =state.getFood()
        nbFoods = state.getNumFood()
        
        
        distFoodMax =0
        distFoodMin = (gridFood.height+gridFood.width)
        count =0
        for posFood in self.posFoods:
            
            if gridFood[posFood[0]][posFood[1]]:
                distFood = self.manhattanDistance(posFood,pacmanPos)
                
                count = count +1
               
                if distFoodMax < distFood:
                    distFoodMax = distFood
                    posFoodMax = posFood
                    
                if distFoodMin > distFood:
                    distFoodMin =distFood
                    posFoodMin = posFood
                    
        
        costAprox = distFoodMin + self.manhattanDistance(posFoodMax, posFoodMin)
       
        return score - self.a1*distFoodMin +self.a2*distGhost  -self.a3*nbFoods
#        return score +500/(1+distFoodMax)+10*nbFoods*distFoodMin/(distFoodMax+1)-500/self.nbMaxFood*nbFoods/(1+distGhost)
#        return score +500/(1+distFoodMax) + distGhost+ distFoodMax+10*nbFoods
#        return score - 5*distGhost*nbFoods + nbFoods*distGhost/(distFoodMax+1) +5/(1+distFoodMax)
      
##         
#        return score +500/(1+distFoodMax)+10*nbFoods/(distFoodMax+1)-500/self.nbMaxFood*nbFoods/(1+distGhost)
#        return score +5/(1+distFoodMax)+10*nbFoods/(distFoodMax+1)+5*distGhost*(nbFoods/self.nbMaxFood)**2
#    
    def hashPosFood(self, state):
        #good with dumby return score - distFoodMin*self.nbMaxFood/(1+nbFoods)+ distFoodMax*nbFoods/self.nbMaxFood -2*nbFoods
        #        return score +500/(1+distFoodMax)+10*nbFoods/(distFoodMax+1)-500/self.nbMaxFood*nbFoods/(1+distGhost)
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
        if depth ==13 or node.isWin() or node.isLose():
            
            return self.evals(node)
        
        
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
        self.move = Directions.STOP
        if not self.posFoods:
            gridFood = state.getFood()
            self.nbMaxFood = state.getNumFood()
            for i in range(gridFood.width):
                for j in range(gridFood.height):
                    if gridFood[i][j]:
                        self.posFoods.append([i,j])
        self.minimax(state, 0, 1,float("-inf"),float("inf"))
        
        return self.move
