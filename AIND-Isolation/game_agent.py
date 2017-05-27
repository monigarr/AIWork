"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves**2/(1+opp_moves))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(own_moves/(1+opp_moves**2))



def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return 1.108*float(own_moves**2/(1+opp_moves))+0.972*float(own_moves/(1+opp_moves**2))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        return self.minimax_search(game, depth)[1]
        
    def minimax_search(self, game, depth, maximizing_player=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        legal_moves = game.get_legal_moves(game.active_player)


        # return the score and the none move if reaches the max depth of no more legal moves
        if depth <= 0 or len(legal_moves) == 0:
            return self.score(game, self), (-1, -1)

        # init the best value of min/max node
        if maximizing_player:
            best_value = [float("-inf"), legal_moves[0]]
        else:
            best_value = [float("inf"), legal_moves[0]]

        # start searching
        for move in legal_moves:
            new_game = game.forecast_move(move)
            old_value = best_value[0]
            if maximizing_player:
                best_value[0] = max(best_value[0], self.minimax_search(new_game, depth - 1, False)[0])
            else:
                best_value[0] = min(best_value[0], self.minimax_search(new_game, depth - 1, True)[0])
            if best_value[0] != old_value:
                best_value[1] = move

        return best_value



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        
        legal_moves = game.get_legal_moves(game.active_player)
        if not legal_moves:  # if no legal moves
            return -1, -1

        next_move = random.choice(legal_moves)
        depth_i = 1 # the iterative depth
        try:
            while True: # while time limit not reached
                next_move = self.alphabeta(game, depth=depth_i)
                depth_i += 1
        except SearchTimeout:
            return next_move
            
        return next_move
        
        

        

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        return self.alpha_beta_search(game, depth)[1]
    
    def alpha_beta_search(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        if game.utility(self) != 0.0:
            return game.utility(self), (-1, -1)

        # get the legal moves
        legal_moves = game.get_legal_moves(game.active_player)


        # if no more moves or reach the max depth
        if len(legal_moves) == 0 or depth <= 0:
            return self.score(game, self), (-1, -1)

        if not maximizing_player:  # a min node
            best_value = [beta, legal_moves[0]]
            for move in legal_moves:
                new_game = game.forecast_move(move)
                old_value = best_value[0]
                best_value[0] = min(best_value[0],
                                 self.alpha_beta_search(new_game, depth - 1, alpha, best_value[0], True)[0])
                if best_value[0] != old_value:
                    best_value[1] = move
                if best_value[0] <= alpha:  # pruning
                    break

        else:  # a max node
            best_value = [alpha, legal_moves[0]]
            for move in legal_moves:
                new_game = game.forecast_move(move)
                old_value = best_value[0]
                best_value[0] = max(best_value[0],
                                 self.alpha_beta_search(new_game, depth - 1, best_value[0], beta, False)[0],
                                 )
                if best_value[0] != old_value:
                    best_value[1] = move
                if best_value[0] >= beta:  # pruning
                    break

        return best_value
    
    def alpha_beta_search_1(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers
        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)
        Returns
        ----------
        float
            The score for the current search branch
        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0:
             return self.score(game, self), (-1, -1)
        if game.utility(self) != 0.0:
            return game.utility(self), (-1, -1)
        legal_moves=game.get_legal_moves()
        best_move = legal_moves[0]
        if maximizing_player:
            # for each child node
            for move in legal_moves:
                child_game = game.forecast_move(move)
                #get alpha value of child  -  child node is minimizing node
                value, _ = self.alpha_beta_search(child_game, depth - 1,alpha,beta, maximizing_player=False)
                #print(alpha,value, move)
                #max(value,alpha)
                if value > alpha:
                    alpha = value
                    best_move = move
                # prune when alpha>= beta
                if alpha >= beta:
                    break

            return alpha,best_move

        else:
            # for each child node
            for move in legal_moves:
                child_game = game.forecast_move(move)
                # get beta value of child  -  child node is maximizing node
                value, _ = self.alpha_beta_search(child_game, depth - 1, alpha, beta, maximizing_player=True)
                # min(value,beta)

                if value < beta:
                    beta = value
                    best_move = move

                # prune when alpha>= beta

                if alpha >= beta:
                    break

        return beta, best_move 
        