
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
        self.move = None
        self.dictMove = {}
        self.depth = 0

    def hashPosFood(self, state, depth):
        """
        Arguments:
        ----------
        - `state`: a game state see `pacman.GameState`.

        Return:
        -------

        -`key`: a string that is made with the position of
        pacman , the grid of position
        of foods (getFood) ,  position of ghost and the depth.

        Note:
        -----
        Only the four data of the state mentioned above are taken
        into account in the hash function.

        """
        hash1 = hash(state.getPacmanPosition())
        hash2 = hash(state.getFood())
        posGhost = state.getGhostPositions()[0]
        hash3 = hash((posGhost[0], posGhost[1]))
        hash4 = hash(depth)
        key = str(hash1) + ' ' + str(hash2) + ' ' + str(hash3)
        key = key + ' ' + str(hash4)
        return key

    def minimax(self, node, depth, player, stateExpanded):
        """
        Arguments:
        ----------
        - `state`: a game state see `pacman.GameState`.
        - `depth` : depth in which we found `state`.
        - `player`: this variable is either 0 (for MIN player) or 1 (for
                     the MAX player)
        Return:
        -------

        -value : the best value (here the score) that the direct moves of
        the state can lead.
        -None : if the state is already expanded with a lower depth

        Note: The moves are stored in self.dictMove (dynamic programming)
        """
        # utility function
        if node.isWin() or node.isLose():

            return node.getScore()

        # updating stateExpanded
        stateComponent = (
                 node.getGhostPositions()[0],
                 node.getPacmanPosition(),
                 node.getFood()
                 )

        newStateExpanded = stateExpanded.copy()

        newStateExpanded.add(stateComponent)

        # Maximize function (Pacman)
        if player:
            value = float("-inf")
#            key = self.hashPosFood(node)

            # hasNoneChild is true if all the child of node returns None
            hasNoneChild = True
            for successor in node.generatePacmanSuccessors():

                stateComponent = (
                         successor[0].getGhostPositions()[0],
                         successor[0].getPacmanPosition(),
                         successor[0].getFood()
                         )
                if stateComponent not in newStateExpanded:

                    successor_value = self.minimax(
                            successor[0], depth + 1, 0, newStateExpanded)

                    if not successor_value:  # if it is None we skip the child
                        continue

                    # getting the gretter value
                    if successor_value > value:
                        value = successor_value
                        hasNoneChild = False
                        bestMove = successor[1]

                        if depth == 0:  # saves the first move
                            self.move = successor[1]

            if hasNoneChild:  # if all the child are None returns None
                return None
            # add the best move in dictMove
            key = self.hashPosFood(node, depth)
            self.dictMove[key] = bestMove

            return value

        # Minimize function (Ghost)
        else:
            value = float("inf")
            # hasNoneChild is true if all the child of node returns None
            # or all the successors are already expand with a better depth
            hasNoneChild = True
            for successor in node.generateGhostSuccessors(1):
                stateComponent = (
                         successor[0].getGhostPositions()[0],
                         successor[0].getPacmanPosition(),
                         successor[0].getFood()
                         )
                if stateComponent not in newStateExpanded:
                    successor_value = self.minimax(
                            successor[0], depth + 1, 1, newStateExpanded)

                    if not successor_value:  # if it is None we skip the child
                        continue
                    # getting the lower value
                    if successor_value < value:
                        value = successor_value
                        hasNoneChild = False

            if hasNoneChild:  # preventing cycle
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

        if not self.move:  # if the moves are not computed we call minimax

            self.minimax(state, 0, 1, set())
            self.depth = self.depth + 2

        else:  # if the move is computed we
            # return the corresponding one in self.dictMove
            key = self.hashPosFood(state, self.depth)
            self.move = self.dictMove[key]
            self.depth = self.depth + 2

        return self.move
