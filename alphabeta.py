
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
        self.dictMove = {}
        self.depth = 0
        self.move = None

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

    def minimax(self, node, depth, player, alpha, beta, stateExpanded):
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

        -value : the best value (here the score) that the direct moves of
        the state can lead.
        -None : if the state is already expanded

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
                        successor[0], depth + 1, 1, alpha, beta,
                        newStateExpanded)

                    if not successor_value:  # if it is None we skip the child
                        continue

                    # getting the gretter value

                    if successor_value > value:

                        hasNoneChild = False
                        value = successor_value
                        bestMove = successor[1]

                        if value >= beta:
                            return value
                        alpha = max(alpha, value)

                        if depth == 0:  # saves the first move
                            self.move = successor[1]

            if hasNoneChild:  # preventing cycle
                # if all the child are None or expanded returns None
                return None
            key = self.hashPosFood(node, depth)
            self.dictMove[key] = bestMove
            return value

        # Minimize function (Ghost)
        else:
            value = float("inf")

            # hasNoneChild is true if all the child of node returns None
            hasNoneChild = True
            for successor in node.generateGhostSuccessors(1):

                stateComponent = (
                         successor[0].getGhostPositions()[0],
                         successor[0].getPacmanPosition(),
                         successor[0].getFood()
                         )

                if stateComponent not in newStateExpanded:  # preventing cycles
                    successor_value = self.minimax(
                        successor[0], depth + 1, 1, alpha, beta,
                        newStateExpanded)

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
            self.depth = self.depth + 2
            self.minimax(state, 0, 1, float("-inf"), float("inf"), set())

        else:
            key = self.hashPosFood(state, self.depth)
            if key not in self.dictMove:  # if the move is not computed we
                # we free dictMove and compute the moves.
                self.depth = 0
                self.dictMove = {}
                self.minimax(state, 0, 1, float("-inf"), float("inf"), set())
                self.depth = self.depth + 2
            else:  # if the move is computed we
                # return the corresponding one in self.dictMove
                self.move = self.dictMove[key]
                self.depth = self.depth + 2

        return self.move
