"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass
 

def moves_available_chase_opponent(game,player):
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves / (1 + opp_moves ** 2))

def moves_available_distance_to_center_negative(game,player):
    """ negative coefficient added to player's location"""
    center = game.width / 2

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    own_loc = len(game.get_player_location(player))
    opp_loc = len(game.get_player_location(game.get_opponent(player)))  

    own_x = abs(center - own_loc)
    opp_x = abs(center - opp_loc)

    own_y = abs(center - own_loc)
    opp_y = abs(center - opp_loc)

    return float(10 * (own_moves - opp_moves) - (own_x + own_y) + (opp_x + opp_y))

def moves_available_defensive_start(game,player):
    """how many moves does each player have left?
    total_cells = all cells on board
    total_cells - cells less at start of game & more at end of game
    cells               more at start of game & less at end of game
    """

    total_cells = game.width ** 2
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    cells = len(game.get_blank_spaces())

    return float(cells * own_moves - (total_cells - cells) * opp_moves)


#############################
#   MY TOURNAMENT PLAYERS
#############################

def custom_score(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return moves_available_chase_opponent(game,player)
 
def custom_score_2(game, player):
    
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return moves_available_distance_to_center_negative(game,player)

def custom_score_3(game, player):
    
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return moves_available_defensive_start(game,player)



class IsolationPlayer:
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    def get_move(self, game, time_left):
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
    def get_move(self, game, time_left):
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
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
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
                if alpha >= beta:
                    break

        return beta, best_move 
        