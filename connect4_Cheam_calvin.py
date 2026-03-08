import numpy as np
import time

#Constants for program to work w

ROWS  = 6
COLS  = 7
EMPTY = '*'
AI_PIECE     = 'X'
PLAYER_PIECE = 'O'

#aiding board funcs, checking if a column is legitimate

def is_valid_column(board, col):
    return board[0, col] == EMPTY

def valid_columns(board):
    return [c for c in range(COLS) if is_valid_column(board, c)]

def update_board(board, col_choice, piece):
    if not is_valid_column(board, col_choice):
        return None
    board_cp = board.copy()
    for row in range(ROWS - 1, -1, -1):
        if board_cp[row, col_choice] == EMPTY:
            board_cp[row, col_choice] = piece
            return board_cp
    return None

def is_draw(board):
    return len(valid_columns(board)) == 0

#Win detector, loops by row, col and diagonal

def game_evaluation(board, player):
    rows, cols = board.shape
    for r in range(rows):
        for c in range(cols - 3):
            if all(board[r, c + i] == player for i in range(4)):
                return True
    for r in range(rows - 3):
        for c in range(cols):
            if all(board[r + i, c] == player for i in range(4)):
                return True
    for r in range(3, rows):
        for c in range(cols - 3):
            if all(board[r - i, c + i] == player for i in range(4)):
                return True
    for r in range(rows - 3):
        for c in range(cols - 3):
            if all(board[r + i, c + i] == player for i in range(4)):
                return True
    return False

def is_terminal(board):
    return (game_evaluation(board, AI_PIECE) or
            game_evaluation(board, PLAYER_PIECE) or
            is_draw(board))

# Heuristic scorer for Alpha-Beta

def score_window(window, piece):
    opp = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
    score = 0
    piece_count = np.sum(window == piece)
    empty_count = np.sum(window == EMPTY)
    opp_count   = np.sum(window == opp)
    if piece_count == 4:
        score += 100
    elif piece_count == 3 and empty_count == 1:
        score += 5
    elif piece_count == 2 and empty_count == 2:
        score += 2
    if opp_count == 3 and empty_count == 1:
        score -= 4
    return score

def heuristic_score(board, piece):
    score = 0
    centre_array = board[:, COLS // 2]
    score += int(np.sum(centre_array == piece)) * 3
    for r in range(ROWS):
        for c in range(COLS - 3):
            window = board[r, c:c + 4]
            score += score_window(window, piece)
    for c in range(COLS):
        for r in range(ROWS - 3):
            window = board[r:r + 4, c]
            score += score_window(window, piece)
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = np.array([board[r - i, c + i] for i in range(4)])
            score += score_window(window, piece)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = np.array([board[r + i, c + i] for i in range(4)])
            score += score_window(window, piece)
    return score

# Alpha-Beta Pruning

def minimax(board, depth, alpha, beta, maximising):
    """
    Minimax with alpha-beta pruning.
    Returns (score, column).
    maximising=True  -> AI (X) is choosing
    maximising=False -> opponent (O) is choosing
    """
    if is_terminal(board):
        if game_evaluation(board, AI_PIECE):
            return (1_000_000, None)
        elif game_evaluation(board, PLAYER_PIECE):
            return (-1_000_000, None)
        else:
            return (0, None)
    if depth == 0:
        return (heuristic_score(board, AI_PIECE), None)

    cols = valid_columns(board)

    if maximising:
        value = float('-inf')
        best_col = cols[np.random.randint(len(cols))]
        for col in cols:
            new_board = update_board(board, col, AI_PIECE)
            new_score, _ = minimax(new_board, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return (value, best_col)
    else:
        value = float('inf')
        best_col = cols[np.random.randint(len(cols))]
        for col in cols:
            new_board = update_board(board, col, PLAYER_PIECE)
            new_score, _ = minimax(new_board, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return (value, best_col)


def AB_choice(board, side, depth=5):
    """
    Choose the best column using Alpha-Beta pruning (depth-limited minimax).
    side: the piece this AI is playing ('X' or 'O').
    """
    maximising = (side == AI_PIECE)
    _, col = minimax(board, depth, float('-inf'), float('inf'), maximising)
    return col

# Monte Carlo Tree Search

class MCTSNode:
    """A node in the MCTS game tree."""

    def __init__(self, board, side, parent=None, move=None):
        self.board    = board
        self.side     = side        # piece that just moved to reach this node
        self.parent   = parent
        self.move     = move        # column that led to this state
        self.children = []
        self.wins     = 0
        self.visits   = 0
        self._untried = valid_columns(board)
        np.random.shuffle(self._untried)

    @property
    def next_side(self):
        return PLAYER_PIECE if self.side == AI_PIECE else AI_PIECE

    def is_fully_expanded(self):
        return len(self._untried) == 0

    def is_terminal(self):
        return is_terminal(self.board)

    def ucb1(self, c=np.sqrt(2)):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits +
                c * np.sqrt(np.log(self.parent.visits) / self.visits))

    def best_child(self, c=np.sqrt(2)):
        return max(self.children, key=lambda n: n.ucb1(c))

    def expand(self):
        """Expand one untried move and return the new child node."""
        col = self._untried.pop()
        new_board = update_board(self.board, col, self.next_side)
        child = MCTSNode(new_board, self.next_side, parent=self, move=col)
        self.children.append(child)
        return child

    def rollout(self, ai_side):
        """
        Play out a random game from this state.
        Returns +1 if ai_side wins, -1 if opponent wins, 0 for draw.
        """
        sim_board = self.board.copy()
        current   = self.next_side
        while True:
            if game_evaluation(sim_board, AI_PIECE):
                return 1 if ai_side == AI_PIECE else -1
            if game_evaluation(sim_board, PLAYER_PIECE):
                return 1 if ai_side == PLAYER_PIECE else -1
            cols = valid_columns(sim_board)
            if not cols:
                return 0
            col = cols[np.random.randint(len(cols))]
            sim_board = update_board(sim_board, col, current)
            current = PLAYER_PIECE if current == AI_PIECE else AI_PIECE

    def backpropagate(self, result):
        self.visits += 1
        self.wins   += result
        if self.parent:
            self.parent.backpropagate(-result)


def MCTS_choice(board, side, time_limit=1.5):
    """
    Choose the best column using Monte Carlo Tree Search.
    Runs simulations for `time_limit` seconds, then picks the most-visited child.
    """
    root     = MCTSNode(board, side)
    deadline = time.time() + time_limit

    while time.time() < deadline:
        # 1. Selection
        node = root
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
        # 2. Expansion
        if not node.is_terminal() and not node.is_fully_expanded():
            node = node.expand()
        # 3. Simulation
        result = node.rollout(side)
        # 4. Backpropagation
        node.backpropagate(result)

    if not root.children:
        return np.random.choice(valid_columns(board))

    best = max(root.children, key=lambda n: n.visits)
    return best.move

# AI choice 

def ai_choice(board, version, side):
    cols = valid_columns(board)
    if not cols:
        return -1
    if version == 'AB':
        return AB_choice(board, side)
    elif version == 'MCTS':
        return MCTS_choice(board, side)
    else:
        return cols[np.random.randint(len(cols))]

# ---------------------------------------------------------------------------
# Node classes (kept for tree-inspection / future extension)
# ---------------------------------------------------------------------------

class Node:
    def __init__(self, name, children, value):
        self.name     = name
        self.value    = value
        self.children = children

class ABNode(Node):
    def __init__(self, name, children, value,
                 alpha=float('-inf'), beta=float('inf')):
        super().__init__(name, children, value)
        self.alpha = alpha
        self.beta  = beta

#board writing func for prettiness

def print_board(board):
    print("\n  " + "  ".join(str(c) for c in range(COLS)))
    for row in board:
        print("| " + "  ".join(row) + " |")
    print()

#Main func that runs game

def game(board, ai_version, human_playing):
    play_board    = board.copy()
    current_piece = PLAYER_PIECE
    print_board(play_board)

    while True:
        if current_piece == PLAYER_PIECE and human_playing:
            try:
                col = int(input(f"Your turn ({PLAYER_PIECE}) — choose column (0-6): "))
            except ValueError:
                print("Please enter a number between 0 and 6.")
                continue
            if col < 0 or col >= COLS:
                print("Column out of range.")
                continue
            if not is_valid_column(play_board, col):
                print("Column is full. Choose another.")
                continue
        else:
            print(f"AI ({current_piece}, {ai_version}) is thinking...")
            col = ai_choice(play_board, ai_version, current_piece)
            if col == -1:
                return {'winner': None, 'board': play_board}
            print(f"AI chose column {col}")

        new_board = update_board(play_board, col, current_piece)
        if new_board is None:
            print("Invalid move — column is full.")
            continue
        play_board = new_board

        if game_evaluation(play_board, current_piece):
            winner = 'Player' if (current_piece == PLAYER_PIECE and human_playing) else 'AI'
            print_board(play_board)   # always show the final state
            return {'winner': winner, 'board': play_board}

        if is_draw(play_board):
            print_board(play_board)   # always show the final state
            return {'winner': None, 'board': play_board}

        if human_playing:             # only show intermediate boards when a human is watching
            print_board(play_board)

        current_piece = AI_PIECE if current_piece == PLAYER_PIECE else PLAYER_PIECE

# Main that runs setup and calls game, prints winner


def main():
    board = np.full((ROWS, COLS), EMPTY, dtype=str)

    version_input = input(
        "Select AI version (AB, MCTS, or dumb) [default: dumb]: "
    ).strip()
    if version_input not in ('AB', 'MCTS', 'dumb'):
        print("Invalid version — defaulting to 'dumb'.")
        version_input = 'dumb'

    player_input = input(
        "Play yourself? (Y/N) [default: N — AI vs AI]: "
    ).strip().upper()
    human_playing = player_input == 'Y'

    result = game(board, version_input, human_playing)

    if result['winner'] is not None:
        print(f"The {result['winner']} wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()