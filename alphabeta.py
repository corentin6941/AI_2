
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
        hash3 = hash((posGhost[0], posGhost[1]))

        key = str(hash1) + ' ' + str(hash2) + ' ' + str(hash3)
        return key

    def keysInDict(self, state):
        """
        Arguments:
        ----------
        - `state`: a game state see `pacman.GameState`.

        Return:
        -------

        -[`key`,`index`]: all the information needed to find the state
        in dictExpanded (i.e. the key of the state in dictExpanded and
        also the index of the state in dictExpanded[key] list.

        -None : if dictExpanded doesn't countain the state

        """

        key = self.hashPosFood(state)

        if key not in self.dictExpanded:
            return None

        # compute the component of the state
        pacmanPos = state.getPacmanPosition()
        food = state.getFood()
        ghostPos = state.getGhostPositions()

        stateComponent = (pacmanPos, food, ghostPos)

        # finds the key  and the index in dictExpanded and returns it
        listInDict = self.dictExpanded[key]
        for i in range(len(listInDict)):
            if listInDict[i][0] == stateComponent:
                return [key, i]
        # if it doesn't find it return None
        # Note: list made to avoid collision problems
        return None

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
            for element in self.dictExpanded[key]:  # travel the list
                if element[0] == stateComponent:
                    if depth < element[1]:  # updates the depth if better
                        element[1] = depth
                        return True
                    return False  # if the depth is not the best returns false
            # state not in dictExpanded but another state has the same key
            self.dictExpanded[key].append([stateComponent, depth])  # updates
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

        -value : the best best value (here the score) that the moves of
        the state can lead.
        -None : if the state is already expanded with a lower depth

        Note: The moves are stored in self.dictExpanded (dynamic programming)
        """
        # utility function
        if node.isWin() or node.isLose():

            return node.getScore()

        # Maximize function (Pacman)
        if player:
            value = float("-inf")
            key = self.hashPosFood(node)
            # hasNoneChild is true if all the child of node returns None
            hasNoneChild = True
            for successor in node.generatePacmanSuccessors():
                if self.isBestDepth(successor[0], depth):

                    successor_value = self.minimax(
                        successor[0], depth + 1, 1, alpha, beta)

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

                            if len(self.dictExpanded[key][index]) == 3:
                                self.dictExpanded[key][index][2] = successor[1]
            if hasNoneChild:  # preventing cycle
                # if all the child are None or expanded returns None
                return None
            return value

        # Minimize function (Ghost)
        else:
            value = float("inf")

            # hasNoneChild is true if all the child of node returns None
            hasNoneChild = True
            for successor in node.generateGhostSuccessors(1):

                if self.isBestDepth(successor[0], depth):  # preventing cycles
                    successor_value = self.minimax(
                        successor[0], depth + 1, 1, alpha, beta)

                    if not successor_value:
                        continue
                    # getting the lower value
                    if successor_value < value:
                        hasNoneChild = False
                        value = successor_value

                        if value <= alpha:
                            return value
                        beta = min(beta, value)

            if hasNoneChild:  # if all the child are None returns None
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
        if not self.move:
            self.minimax(state, 0, 1, float("-inf"), float("inf"))

        else:
            if not self.keysInDict(state):  # if the move is not computed we
                # we free dictExpanded and compute it.
                self.dictExpanded = {}
                self.minimax(state, 0, 1, float("-inf"), float("inf"))

            else:  # if the move is computed we
                # return the corresponding one in self.dictExpanded
                [key, index] = self.keysInDict(state)
            self.move = self.dictExpanded[key][index][2]

        return self.move
