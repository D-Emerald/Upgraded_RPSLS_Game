# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 21:45:49 2026

@author: devin
"""

import random
import tkinter as tk


# ============================================================
# GAME RULES
# ============================================================

MOVES = [
    "rock",
    "paper",
    "scissors",
    "lizard",
    "spock"
]

WINNING_MOVES = {
    "rock": {"scissors", "lizard"},
    "paper": {"rock", "spock"},
    "scissors": {"paper", "lizard"},
    "lizard": {"paper", "spock"},
    "spock": {"rock", "scissors"},
}

MOVE_SYMBOLS = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️",
    "lizard": "🦎",
    "spock": "🖖",
}


# ============================================================
# PLAYER CLASSES
# ============================================================

class Player:
    """Base class for all players."""

    def move(self):
        return random.choice(MOVES)

    def learn(self, my_move, opponent_move):
        pass


class RockPlayer(Player):
    """Always chooses rock."""

    def move(self):
        return "rock"


class RandomPlayer(Player):
    """Chooses a random move."""

    def move(self):
        return random.choice(MOVES)


class ReflectPlayer(Player):
    """Copies the opponent's previous move."""

    def __init__(self):
        self.opponent_move = None

    def move(self):
        if self.opponent_move is None:
            return "rock"

        return self.opponent_move

    def learn(self, my_move, opponent_move):
        self.opponent_move = opponent_move


class CyclePlayer(Player):
    """Cycles through all available moves."""

    def __init__(self):
        self.move_index = 0

    def move(self):
        move = MOVES[self.move_index]

        self.move_index = (
            self.move_index + 1
        ) % len(MOVES)

        return move


# ============================================================
# GAME ENGINE
# ============================================================

class Game:
    """Controls the rules and state of a match."""

    def __init__(
        self,
        player,
        opponent,
        total_rounds
    ):
        self.player = player
        self.opponent = opponent

        self.total_rounds = total_rounds

        self.round_number = 0
        self.player_score = 0
        self.opponent_score = 0

    def determine_winner(
        self,
        player_move,
        opponent_move
    ):
        """Determine the winner of a round."""

        if player_move == opponent_move:
            return "draw"

        if opponent_move in WINNING_MOVES[player_move]:
            return "player"

        return "opponent"

    def play_round(self, player_move):
        """Play one round and update the score."""

        opponent_move = self.opponent.move()

        result = self.determine_winner(
            player_move,
            opponent_move
        )

        self.round_number += 1

        if result == "player":
            self.player_score += 1

        elif result == "opponent":
            self.opponent_score += 1

        self.player.learn(
            player_move,
            opponent_move
        )

        self.opponent.learn(
            opponent_move,
            player_move
        )

        return {
            "player_move": player_move,
            "opponent_move": opponent_move,
            "result": result,
            "round": self.round_number,
            "player_score": self.player_score,
            "opponent_score": self.opponent_score,
        }


# ============================================================
# GUI
# ============================================================

class RockPaperScissorsGUI:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Rock, Paper, Scissors, Lizard, Spock Game"
        )

        self.root.geometry("1000x700")
        self.root.minsize(850, 600)

        self.root.configure(
            background="#202124"
        )

        # ----------------------------------------------------
        # Game state
        # ----------------------------------------------------

        self.game = None

        self.opponent_name = ""
        self.opponent_strategy = None

        self.match_name = ""
        self.total_rounds = 1

        self.create_gui()

        self.show_setup()

    # ========================================================
    # GUI CREATION
    # ========================================================

    def create_gui(self):

        # ----------------------------------------------------
        # Main game area
        # ----------------------------------------------------

        self.game_frame = tk.Frame(
            self.root,
            background="#202124"
        )

        self.game_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(25, 10),
            pady=25
        )

        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        self.title_label = tk.Label(
            self.game_frame,
            text="ROCK • PAPER • SCISSORS",
            font=("Arial", 26, "bold"),
            fg="white",
            background="#202124"
        )

        self.title_label.pack()

        self.subtitle_label = tk.Label(
            self.game_frame,
            text="LIZARD • SPOCK",
            font=("Arial", 14),
            fg="#aaaaaa",
            background="#202124"
        )

        self.subtitle_label.pack(
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # Arena
        # ----------------------------------------------------

        self.arena = tk.Frame(
            self.game_frame,
            background="#202124"
        )

        self.arena.pack(
            fill="x",
            pady=15
        )

        # ----------------------------------------------------
        # Player
        # ----------------------------------------------------

        self.player_frame = tk.Frame(
            self.arena,
            background="#292a2d",
            padx=25,
            pady=20
        )

        self.player_frame.pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        tk.Label(
            self.player_frame,
            text="YOU",
            font=("Arial", 14, "bold"),
            fg="white",
            background="#292a2d"
        ).pack()

        self.player_move_label = tk.Label(
            self.player_frame,
            text="❔",
            font=("Arial", 60),
            fg="white",
            background="#292a2d"
        )

        self.player_move_label.pack(
            pady=15
        )

        # ----------------------------------------------------
        # VS
        # ----------------------------------------------------

        self.vs_label = tk.Label(
            self.arena,
            text="VS",
            font=("Arial", 18, "bold"),
            fg="#888888",
            background="#202124"
        )

        self.vs_label.pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------------
        # Opponent
        # ----------------------------------------------------

        self.opponent_frame = tk.Frame(
            self.arena,
            background="#292a2d",
            padx=25,
            pady=20
        )

        self.opponent_frame.pack(
            side="left",
            expand=True,
            fill="both",
            padx=8
        )

        self.opponent_name_label = tk.Label(
            self.opponent_frame,
            text="OPPONENT",
            font=("Arial", 14, "bold"),
            fg="white",
            background="#292a2d"
        )

        self.opponent_name_label.pack()

        self.opponent_move_label = tk.Label(
            self.opponent_frame,
            text="❔",
            font=("Arial", 60),
            fg="white",
            background="#292a2d"
        )

        self.opponent_move_label.pack(
            pady=15
        )

        # ----------------------------------------------------
        # Result
        # ----------------------------------------------------

        self.result_label = tk.Label(
            self.game_frame,
            text="",
            font=("Arial", 24, "bold"),
            fg="white",
            background="#202124"
        )

        self.result_label.pack(
            pady=15
        )

        # ----------------------------------------------------
        # Score
        # ----------------------------------------------------

        self.score_label = tk.Label(
            self.game_frame,
            text="YOU 0 - 0 OPPONENT",
            font=("Arial", 16, "bold"),
            fg="#cccccc",
            background="#202124"
        )

        self.score_label.pack(
            pady=5
        )

        self.round_label = tk.Label(
            self.game_frame,
            text="Round 0 / 1",
            font=("Arial", 13),
            fg="#aaaaaa",
            background="#202124"
        )

        self.round_label.pack(
            pady=5
        )

        # ----------------------------------------------------
        # Move buttons
        # ----------------------------------------------------

        self.move_frame = tk.Frame(
            self.game_frame,
            background="#202124"
        )

        self.move_frame.pack(
            pady=15
        )

        self.move_buttons = []

        for move in MOVES:

            button = tk.Button(
                self.move_frame,
                text=(
                    f"{MOVE_SYMBOLS[move]}\n"
                    f"{move.title()}"
                ),
                font=("Arial", 11, "bold"),
                width=9,
                height=3,
                background="#303134",
                foreground="white",
                activebackground="#45464a",
                activeforeground="white",
                command=lambda m=move: (
                    self.select_move(m)
                )
            )

            button.pack(
                side="left",
                padx=3
            )

            self.move_buttons.append(button)

        # ====================================================
        # RIGHT CONTROL PANEL
        # ====================================================

        self.control_panel = tk.Frame(
            self.root,
            width=260,
            background="#292a2d",
            padx=20,
            pady=25
        )

        self.control_panel.pack(
            side="right",
            fill="y",
            padx=(10, 25),
            pady=25
        )

        self.control_panel.pack_propagate(False)

        # ----------------------------------------------------
        # Panel title
        # ----------------------------------------------------

        tk.Label(
            self.control_panel,
            text="GAME CONTROL",
            font=("Arial", 18, "bold"),
            fg="white",
            background="#292a2d"
        ).pack(
            pady=(0, 25)
        )

        # ----------------------------------------------------
        # Opponent
        # ----------------------------------------------------

        tk.Label(
            self.control_panel,
            text="OPPONENT",
            font=("Arial", 10, "bold"),
            fg="#aaaaaa",
            background="#292a2d"
        ).pack(
            anchor="w"
        )

        self.opponent_button = tk.Button(
            self.control_panel,
            text="Choose Opponent",
            font=("Arial", 11, "bold"),
            width=22,
            command=self.show_opponent_options
        )

        self.opponent_button.pack(
            pady=(5, 20)
        )

        # ----------------------------------------------------
        # Match
        # ----------------------------------------------------

        tk.Label(
            self.control_panel,
            text="MATCH",
            font=("Arial", 10, "bold"),
            fg="#aaaaaa",
            background="#292a2d"
        ).pack(
            anchor="w"
        )

        self.single_round_button = tk.Button(
            self.control_panel,
            text="Single Round",
            font=("Arial", 11, "bold"),
            width=22,
            command=lambda: self.start_match(
                1,
                "Single Round"
            )
        )

        self.single_round_button.pack(
            pady=5
        )

        self.best_of_five_button = tk.Button(
            self.control_panel,
            text="Best of 5",
            font=("Arial", 11, "bold"),
            width=22,
            command=lambda: self.start_match(
                5,
                "Best of 5"
            )
        )

        self.best_of_five_button.pack(
            pady=(0, 20)
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        tk.Label(
            self.control_panel,
            text="STATUS",
            font=("Arial", 10, "bold"),
            fg="#aaaaaa",
            background="#292a2d"
        ).pack(
            anchor="w"
        )

        self.status_label = tk.Label(
            self.control_panel,
            text="Setup required",
            font=("Arial", 12, "bold"),
            fg="#ffd166",
            background="#292a2d",
            wraplength=210,
            justify="left"
        )

        self.status_label.pack(
            anchor="w",
            pady=(5, 25)
        )

        # ----------------------------------------------------
        # Divider
        # ----------------------------------------------------

        tk.Frame(
            self.control_panel,
            height=1,
            background="#444444"
        ).pack(
            fill="x",
            pady=5
        )

        # ----------------------------------------------------
        # New game
        # ----------------------------------------------------

        self.new_game_button = tk.Button(
            self.control_panel,
            text="New Game",
            font=("Arial", 11, "bold"),
            width=22,
            command=self.show_setup
        )

        self.new_game_button.pack(
            pady=(25, 5)
        )
        
        # ----------------------------------------------------
        # Rules
        # ----------------------------------------------------

        self.rules_button = tk.Button(
            self.control_panel,
            text="Rules",
            font=("Arial", 11, "bold"),
            width=22,
            command=self.show_rules
        )

        self.rules_button.pack(
            pady=5
        )

        # ----------------------------------------------------
        # Quit
        # ----------------------------------------------------

        self.quit_button = tk.Button(
            self.control_panel,
            text="Quit",
            font=("Arial", 11, "bold"),
            width=22,
            command=self.root.destroy
        )

        self.quit_button.pack(
            pady=5
        )

    # ========================================================
    # SETUP
    # ========================================================

    def show_setup(self):

        self.game = None

        self.disable_move_buttons()

        self.opponent_button.config(
            state="normal"
        )

        self.single_round_button.config(
            state="disabled"
        )

        self.best_of_five_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="Choose an opponent.",
            fg="#ffd166"
        )

        self.result_label.config(
            text="Choose your opponent",
            fg="white"
        )

    # ========================================================
    # OPPONENT OPTIONS
    # ========================================================

    def show_opponent_options(self):

        self.single_round_button.config(
            state="disabled"
        )

        self.best_of_five_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="Select an opponent.",
            fg="#ffd166"
        )

        # ----------------------------------------------------
        # Remove old option buttons if they exist
        # ----------------------------------------------------

        if hasattr(self, "opponent_option_buttons"):

            for button in self.opponent_option_buttons:
                button.destroy()

        self.opponent_option_buttons = []

        strategies = [
            ("Rock", RockPlayer),
            ("Random", RandomPlayer),
            ("Reflect", ReflectPlayer),
            ("Cycle", CyclePlayer)
        ]

        for name, strategy in strategies:

            button = tk.Button(
                self.control_panel,
                text=name,
                font=("Arial", 10, "bold"),
                width=22,
                command=lambda n=name, s=strategy: (
                    self.select_opponent(n, s)
                )
            )

            button.pack(
                pady=2,
                after=self.opponent_button
            )

            self.opponent_option_buttons.append(
                button
            )

    # ========================================================
    # SELECT OPPONENT
    # ========================================================

    def select_opponent(
        self,
        name,
        strategy
    ):

        self.opponent_name = name
        self.opponent_strategy = strategy

        self.opponent_button.config(
            text=f"Opponent: {name}"
        )

        self.remove_opponent_options()

        self.single_round_button.config(
            state="normal"
        )

        self.best_of_five_button.config(
            state="normal"
        )

        self.status_label.config(
            text="Choose a match.",
            fg="#ffd166"
        )

        self.result_label.config(
            text="Choose your match",
            fg="white"
        )

    def remove_opponent_options(self):

        if hasattr(self, "opponent_option_buttons"):

            for button in self.opponent_option_buttons:
                button.destroy()

            self.opponent_option_buttons = []

    # ========================================================
    # START MATCH
    # ========================================================

    def start_match(
        self,
        total_rounds,
        match_name
    ):

        if self.opponent_strategy is None:
            return

        self.total_rounds = total_rounds
        self.match_name = match_name

        self.game = Game(
            Player(),
            self.opponent_strategy(),
            total_rounds
        )

        self.opponent_name_label.config(
            text=self.opponent_name.upper()
        )

        self.reset_display()

        # ----------------------------------------------------
        # Configuration becomes read-only
        # ----------------------------------------------------

        self.opponent_button.config(
            state="disabled"
        )

        self.single_round_button.config(
            state="disabled"
        )

        self.best_of_five_button.config(
            state="disabled"
        )

        self.status_label.config(
            text="Match in progress.",
            fg="#5cff8d"
        )

        self.enable_move_buttons()

    # ========================================================
    # MOVE SELECTION
    # ========================================================

    def select_move(self, move):

        if self.game is None:
            return

        if (
            self.game.round_number
            >= self.game.total_rounds
        ):
            return

        self.disable_move_buttons()

        self.player_move_label.config(
            text=MOVE_SYMBOLS[move]
        )

        self.opponent_move_label.config(
            text="❔"
        )

        self.countdown(
            3,
            move
        )

    # ========================================================
    # COUNTDOWN
    # ========================================================

    def countdown(
        self,
        number,
        move
    ):

        if number > 0:

            self.result_label.config(
                text=str(number)
            )

            self.root.after(
                500,
                lambda: self.countdown(
                    number - 1,
                    move
                )
            )

        else:

            self.result_label.config(
                text="GO!"
            )

            self.root.after(
                300,
                lambda: self.resolve_round(
                    move
                )
            )

    # ========================================================
    # RESOLVE ROUND
    # ========================================================

    def resolve_round(self, move):

        result = self.game.play_round(
            move
        )

        opponent_move = result[
            "opponent_move"
        ]

        self.opponent_move_label.config(
            text=MOVE_SYMBOLS[
                opponent_move
            ]
        )

        self.animate_battle(
            result
        )

    # ========================================================
    # BATTLE ANIMATION
    # ========================================================

    def animate_battle(self, result):

        self.animate_label(
            self.player_move_label
        )

        self.animate_label(
            self.opponent_move_label
        )

        self.root.after(
            500,
            lambda: self.show_result(
                result
            )
        )

    def animate_label(self, label):

        sizes = [
            40,
            48,
            56,
            64,
            60
        ]

        self.animate_font(
            label,
            sizes
        )

    def animate_font(
        self,
        label,
        sizes
    ):

        if not sizes:
            return

        size = sizes.pop(0)

        label.config(
            font=(
                "Arial",
                size
            )
        )

        self.root.after(
            60,
            lambda: self.animate_font(
                label,
                sizes
            )
        )

    # ========================================================
    # SHOW ROUND RESULT
    # ========================================================

    def show_result(self, result):

        result_type = result["result"]

        if result_type == "player":

            text = "YOU WIN!"
            colour = "#5cff8d"

        elif result_type == "opponent":

            text = "OPPONENT WINS!"
            colour = "#ff6b6b"

        else:

            text = "DRAW!"
            colour = "#ffd166"

        self.result_label.config(
            text=text,
            fg=colour
        )

        self.round_label.config(
            text=(
                f"Round "
                f"{result['round']} / "
                f"{self.total_rounds}"
            )
        )

        self.score_label.config(
            text=(
                f"YOU {result['player_score']} "
                f" - "
                f"{result['opponent_score']} "
                f"{self.opponent_name.upper()}"
            )
        )

        if (
            result["round"]
            >= self.total_rounds
        ):

            self.root.after(
                1000,
                self.show_match_result
            )

        else:

            self.root.after(
                1000,
                self.enable_move_buttons
            )

    # ========================================================
    # MATCH RESULT
    # ========================================================

    def show_match_result(self):

        if (
            self.game.player_score
            > self.game.opponent_score
        ):

            text = "YOU WIN THE MATCH!"
            colour = "#5cff8d"

        elif (
            self.game.player_score
            < self.game.opponent_score
        ):

            text = "OPPONENT WINS THE MATCH!"
            colour = "#ff6b6b"

        else:

            text = "THE MATCH IS A DRAW!"
            colour = "#ffd166"

        self.result_label.config(
            text=text,
            fg=colour
        )

        self.disable_move_buttons()

        self.status_label.config(
            text="Match complete.",
            fg=colour
        )

        self.root.after(
            1200,
            self.show_play_again
        )

    # ========================================================
    # PLAY AGAIN
    # ========================================================

    def show_play_again(self):

        self.status_label.config(
            text="What would you like to do?",
            fg="#ffd166"
        )

        self.single_round_button.config(
            state="normal"
        )

        self.best_of_five_button.config(
            state="normal"
        )

        self.opponent_button.config(
            state="normal"
        )

        self.opponent_button.config(
            text=f"Opponent: {self.opponent_name}"
        )

        self.result_label.config(
            text="Play again?",
            fg="white"
        )
        
       # ========================================================
    # SHOW RULES
    # ========================================================

    def show_rules(self):
        """Display the RPSLS rules in a read-only window."""

        rules_window = tk.Toplevel(self.root)

        rules_window.title(
            "RPSLS Rules"
        )

        rules_window.geometry(
            "500x650"
        )

        rules_window.configure(
            background="#202124"
        )

        rules_window.transient(
            self.root
        )

        title_label = tk.Label(
            rules_window,
            text="GAME RULES",
            font=("Arial", 22, "bold"),
            fg="white",
            background="#202124"
        )

        title_label.pack(
            pady=(20, 10)
        )

        rules_text = """
Rock, Paper, Scissors, Lizard, Spock

Each move defeats two other moves
and loses to two other moves.

WINNING RELATIONSHIPS

Rock 🪨 
Wins against: Scissors, Lizard
Loses against: Paper, Spock

Paper 📄 
Wins against: Rock, Spock
Loses against: Scissors, Lizard

Scissors ✂️ 
Wins against: Paper, Lizard
Loses against: Rock, Spock

Lizard 🦎 
Wins against: Paper, Spock
Loses against: Rock, Scissors

Spock 🖖 
Wins against: Rock, Scissors
Loses against: Paper, Lizard


HOW EACH MOVE WINS

🪨 Rock crushes ✂️ Scissors
🪨 Rock crushes 🦎 Lizard

📄 Paper covers 🪨 Rock
📄 Paper disproves 🖖 Spock

✂️ Scissors cuts 📄 Paper
✂️ Scissors decapitates 🦎 Lizard

🦎 Lizard eats 📄 Paper
🦎 Lizard poisons 🖖 Spock

🖖 Spock smashes 🪨 Rock
🖖 Spock vaporises ✂️ Scissors


DRAW

If both players select the same move,
the round is a draw.

No player receives a point.


SCORING

Round winner: 1 point
Round loser: 0 points
Draw: 0 points

The player with the highest score
at the end of the match wins.
"""

        text = tk.Text(
            rules_window,
            font=("Arial", 11),
            fg="white",
            background="#292a2d",
            insertbackground="white",
            wrap="word",
            padx=20,
            pady=15,
            relief="flat"
        )

        text.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        text.insert(
            "1.0",
            rules_text
        )

        text.config(
            state="disabled"
        )

        close_button = tk.Button(
            rules_window,
            text="Close",
            font=("Arial", 11, "bold"),
            width=14,
            command=rules_window.destroy
        )

        close_button.pack(
            pady=(5, 20)
        )
        
        text.config(
            state="disabled"
        )

    # ========================================================
    # BUTTON CONTROL
    # ========================================================

    def disable_move_buttons(self):

        for button in self.move_buttons:

            button.config(
                state="disabled"
            )

    def enable_move_buttons(self):

        for button in self.move_buttons:

            button.config(
                state="normal"
            )

    # ========================================================
    # RESET DISPLAY
    # ========================================================

    def reset_display(self):

        self.player_move_label.config(
            text="❔",
            font=("Arial", 60)
        )

        self.opponent_move_label.config(
            text="❔",
            font=("Arial", 60)
        )

        self.result_label.config(
            text="Choose your move",
            fg="white"
        )

        self.round_label.config(
            text=(
                f"Round 0 / "
                f"{self.total_rounds}"
            )
        )

        self.score_label.config(
            text=(
                f"YOU 0 - 0 "
                f"{self.opponent_name.upper()}"
            )
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = RockPaperScissorsGUI(root)

    root.mainloop()