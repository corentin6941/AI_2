
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

        self.dictExpanded = {}  # stores the state expanded
        self.move = None
        self.posFoods = []
        self.dictVisited = {}  # stores state visited

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

    def evals(self, state):
        """
        Arguments:
        ----------
        - `state`: a game state see `pacman.GameState`.

        Return:
        -------

        -value : evaluation of the final score
        (score - 1*distFoodMin +0.09*distGhost  -4*nbFoods)
        if the state is a winning state it returns a high number
        (self.maxScore+score)
        if the state is a loosing state it returns -inf

        """
        # loosing end
        if state.isLose():
            return float("-inf")

        # winning end
        score = state.getScore()

        if state.isWin():
            return self.maxScore+score

        ghostPos = state.getGhostPositions()[0]
        pacmanPos = state.getPacmanPosition()
        distGhost = self.manhattanDistance(ghostPos, pacmanPos)
        gridFood = state.getFood()
        nbFoods = state.getNumFood()

        # computation of the shortest manhattanDistance bewteen pacman
        # and a food
        distFoodMin = (gridFood.height+gridFood.width)

        for posFood in self.posFoods:

            if gridFood[posFood[0]][posFood[1]]:
                distFood = self.manhattanDistance(posFood, pacmanPos)

                if distFoodMin > distFood:
                    distFoodMin = distFood

        return score - 1*distFoodMin + 0.09*distGhost - 4*nbFoods

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
        hash3 = hash((posGhost[0], posGhost[1]))

        key = str(hash1) + ' ' + str(hash2) + ' ' + str(hash3)

        return key

    def isVisited(self, state):
        """
        Arguments:
        ----------
        - `state`: a game state see `pacman.GameState`.

        Return:
        -------

        -True : if `state` is in dictVisited

        -False : if `state` is not in dictVisited

        """

        key = self.hashPosFood(state)

        pacmanPos = state.getPacmanPosition()
        food = state.getFood()
        ghostPos = state.getGhostPositions()

        stateComponent = (pacmanPos, food, ghostPos)
        if key not in self.dictVisited:
            return False
        else:
            for element in self.dictVisited[key]:
                if element == stateComponent:
                    return True
            return False

    def isBestDepth(self, state, depth):
        """
        Arguments:
        ----------
        - `state`: a game state see `pacman.GameState`.
        - `depth` : depth in which we found `state`.

        Return:
        -------

        -True : if state is not in dictExpanded or
        if `depth` is lower than the one of the corresponding state
        in dictExpanded.

        -False : if `state` is already in dictExpanded and has a greater
        or equal `depth`.

        Note: Each time we finds a lower depth we update dictExpanded
        and if the state wasn't in dictExpanded we add the new companents
        in the dictionnary
        """

        key = self.hashPosFood(state)
        # compute the component of the state
        pacmanPos = state.getPacmanPosition()
        food = state.getFood()
        ghostPos = state.getGhostPositions()

        stateComponent = (pacmanPos, food, ghostPos)

        if key not in self.dictExpanded:
            # dictExpanded contains list to prevent from collision
            self.dictExpanded[key] = [[stateComponent, depth]]
            return True
        else:
            for element in self.dictExpanded[key]:  # travel the lis
                if element[0] == stateComponent:
                    if depth < element[1]:  # updates the depth if better
                        element[1] = depth
                        return True
                    return False  # if the depth is not the best returns false
            self.dictExpanded[key].append(
                [stateComponent, depth])  # updates dict
            return True

    def minimax(self, node, depth, player, alpha, beta):
        """
        Arguments:
        ----------
        - `state`: a game state see `pacman.GameState`.
        - `depth` : depth in which we found `state`.
        - `alpha` : the highest value at any choice point along the pass of MAX
        - `beta`  : the lowest value at any choice point along the pass of MIN
        - `player`: this variable is either 0 (for MIN player) or 1 (for
                     the MAX player)
        Return:
        -------

        -value : the best value (here the value returned by evals)
        that the direct moves of the state can lead.
        -None : if the state is already expanded with a lower depth

        Note: The final move is stored in self.move
        """

        # cutoff test
        if depth == 10 or node.isWin() or node.isLose():

            return self.evals(node)

        # Maximize function (Pacman)
        if player:
            value = float("-inf")
            key = self.hashPosFood(node)
            # hasNoneChild is true if all the child of node returns None
            hasNoneChild = True
            for successor in node.generatePacmanSuccessors():
                if self.isBestDepth(successor[0], depth):

                    successor_value = self.minimax(
                        successor[0], depth + 1, 0, alpha, beta)

                    if not successor_value:  # if it is None we skip the child
                        continue

                    # getting the gretter value

                    if successor_value > value:

                        hasNoneChild = False
                        value = successor_value

                        if value >= beta:
                            return value
                        alpha = max(alpha, value)

                        if depth == 0:  # saves the first move
                            self.move = successor[1]

                        else:  # save the moves in self.dictExpanded
                            [key, index] = self.keysInDict(node)
                            if len(self.dictExpanded[key][index]) == 2:
                                self.dictExpanded[key][index].append(
                                    successor[1])

                            if len(self.dictExpanded[key][index]) = =3:
                                self.dictExpanded[key][index][2] = successor[1]
            # if all the child are None or expanded returns None
            if hasNoneChild:  # preventing cycle
                return None
            return value

        # Maximize function (Pacman)
        if player:

            value = float("-inf")
            # hasNoneChild is true if all the child of node returns None
            hasNoneChild = True

            for successor in node.generatePacmanSuccessors():

                # visited state aren't considered
                if self.isVisited(successor[0]):
                    continue

                if self.isBestDepth(successor[0], depth):  # preventing cycles

                    successor_value = self.minimax(
                        successor[0], depth + 1, 0, alpha, beta)

                    if not successor_value:  # saves the first move
                        continue

                    # getting the gretter value
                    if successor_value > value:
                        value = successor_value
                        hasNoneChild = False

                        if depth == 0:
                            self.move = successor[1]
                        if value >= beta:
                            return value
                        alpha = max(alpha, value)

            if hasNoneChild:  # preventing cycle
                # if all the child are None, expanded or visited returns None
                return None
            return value

        # Minimize function (Ghost)
        else:

            value = float("inf")
            # hasNoneChild is true if all the child of node returns None
            hasNoneChild = True
            for successor in node.generateGhostSuccessors(1):
                if self.isVisited(successor[0]):
                    continue
                if self.isBestDepth(successor[0], depth):  # preventing cycles

                    successor_value = self.minimax(
                            successor[0], depth + 1, 1, alpha, beta)
                    if not successor_value:
                        continue
                    # getting the lower value
                    if successor_value < value:
                        value = successor_value
                        hasNoneChild = False

                        if value <= alpha:
                            return value
                        beta = min(beta, value)

            if hasNoneChild:  # preventing cycle
                # if all the child are None, expanded or visited returns None
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

        self.move = Directions.STOP  # if no move are found pacman doesn't move

        if not self.posFoods:
            # initilyse posFoods & maxScore
            gridFood = state.getFood()
            self.maxScore = state.getNumFood()*10
            + 0.09*(gridFood.height + gridFood.width) + 700

            for i in range(gridFood.width):
                for j in range(gridFood.height):
                    if gridFood[i][j]:
                        self.posFoods.append([i, j])

        # we compute the state components

        key = self.hashPosFood(state)

        pacmanPos = state.getPacmanPosition()
        food = state.getFood()
        ghostPos = state.getGhostPositions()

        stateComponent = (pacmanPos, food, ghostPos)
        # if state is not visited we store it in dictVisited and call minimax
        if not self.isVisited(state):

            if key not in self.dictVisited:
                self.dictVisited[key] = [stateComponent]
            else:
                self.dictVisited[key].append(stateComponent)

            self.minimax(state, 0, 1, float("-inf"), float("inf"))
        # if no moves are found we clear dict expanded and visited
        # and recall minimax
        if self.move == Directions.STOP:

            self.dictVisited = {}
            self.dictExpanded = {}

            self.minimax(state, 0, 1, float("-inf"), float("inf"))

        return self.move
