import os
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Button, Label, Entry
from tkinter import messagebox
from blackjack import Blackjack
from card_count import Card_Counter

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack Simulator with Card Counting")
        self.geometry("800x800")

        self.load_cards()

        self.random = np.random.RandomState()
        self.running_count = 0
        self.actionButton = None
        self.dealerLabel = None
        self.playerLabel = None
        self.countLabel = None
        self.valueLabel = None
        self.scoreLabel = None
        self.bustProbLabel = None
        self.hitButton = None
        self.standButton = None
        self.doubleDownButton = None
        self.splitButton = None
        self.surrenderButton = None
        self.insuranceButton = None
        
        self.init_gui()
        self.blackjack_game = Blackjack(players=["Player 1"])
        self.card_counter = Card_Counter(self.blackjack_game, total_decks=6, strategy_name='hi_lo')

    def enable_buttons(self):
        self.hitButton.config(state=tk.NORMAL)
        self.standButton.config(state=tk.NORMAL)
        self.doubleDownButton.config(state=tk.NORMAL)
        self.splitButton.config(state=tk.NORMAL)
        self.surrenderButton.config(state=tk.NORMAL)
        self.insuranceButton.config(state=tk.NORMAL)

    def start(self):
        self.actionButton.config(state=tk.DISABLED)
        self.play_blackjack_round()

    def play_blackjack_round(self):
        # Play a round of blackjack
        self.blackjack_game.play_round()

        # Update card counting metrics
        dealer_card, player_cards = self.get_current_hands()
        self.update_count(dealer_card)
        for card_value in player_cards:
            self.update_count(card_value)

        # Display current hands and card counting metrics
        self.display_current_hands(dealer_card, player_cards)
        self.display_count()

        # Calculate bust probability and display or log the result
        bust_probability = self.card_counter.calculate_bust_probability(self.running_count)
        self.bustProbLabel.config(text=f"Bust Probability: {bust_probability}")

        if not self.blackjack_game.is_game_over():
            self.enable_buttons()
        else:
            self.actionButton.config(state=tk.NORMAL)

    def trigger_player_action(self, action):
        # Implement logic to trigger player actions based on your visual buttons
        # For example, you can use a variable to store the player's action and
        # update it when the corresponding button is clicked.
        # Then, call the appropriate player action method based on that variable.
        # Store the clicked button for later use
        self.clicked_button = action
        # Disable buttons after clicking to prevent multiple clicks
        self.disable_buttons()
        # Call the appropriate player action method based on the button clicked
        self.blackjack_game.player_action(action)

    def trigger_dealer_play(self):
        # Implement logic to trigger dealer play
        dealer_score = self.blackjack_game.dealer.score
        while dealer_score < 17:
            self.blackjack_game.dealer_hit()
            dealer_score = self.blackjack_game.dealer.score
        # Once the dealer has finished playing, you can proceed with the end of the round logic
        self.end_round()

    def get_current_hands(self):
        dealer_hand = self.blackjack_game.dealer.current_hand
        player_cards = [player.current_hand for player in self.blackjack_game.players]
        return dealer_hand, player_cards
    
    def display_current_hands(self, dealer_card, player_cards):
        self.dealerLabel.config(text=f"Dealer's Hand: {dealer_card}")
        self.playerLabel.config(text=f"Player's Hand: {player_cards}")

    def display_count(self):
        self.countLabel.config(text=f"Running Count: {self.running_count}")
        self.valueLabel.config(text=f"Score: {self.card_counter.score}")
        self.scoreLabel.config(text=f"Number of Cards Shown: {self.card_counter.count}")

    def update_count(self, card_value):
        self.card_counter.update_count(card_value)
        self.running_count = self.card_counter.running_count

    def load_cards(self):
        self.cards = []
        ranks = [str(rank) for rank in range(2, 11)] + ['jack', 'queen', 'king', 'ace']
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        for rank in ranks:
            for suit in suits:
                img_path = os.path.join("classic-cards", f"{rank}_of_{suit}.png")
                img = Image.open(img_path)
                img = img.resize((100, 150))
                img = ImageTk.PhotoImage(img)
                self.cards.append(img)

    def init_gui(self):
        self.actionButton = Button(self, text="Start Blackjack Round", command=self.start)
        self.dealerLabel = Label(self, text="Dealer's Hand:")
        self.playerLabel = Label(self, text="Player's Hand:")
        self.countLabel = Label(self, text=f"Running Count: {self.running_count}")
        self.valueLabel = Label(self, text=f"Count: {self.score}")
        self.scoreLabel = Label(self, text=f"Number of Cards Shown: {self.count}")
        self.cardPanel = Label(self)
        self.bustProbLabel = Label(self, text=f"Bust Probability: {self.bust}")  # Label to display bust probability

        self.actionButton.pack()
        self.dealerLabel.pack()
        self.playerLabel.pack()
        self.countLabel.pack()
        self.valueLabel.pack()
        self.scoreLabel.pack()
        self.bustProbLabel.pack()  # Pack the bust probability label
        self.cardPanel.pack()

        # Add buttons for player actions
        self.hitButton = Button(self, text="HIT", command=self.player_hit)
        self.hitButton.pack()

        self.standButton = Button(self, text="STAND", command=self.player_stand)
        self.standButton.pack()

        self.doubleDownButton = Button(self, text="DOUBLE DOWN", command=self.player_double_down)
        self.doubleDownButton.pack()

        self.splitButton = Button(self, text="SPLIT", command=self.player_split)
        self.splitButton.pack()

        self.surrenderButton = Button(self, text="SURRENDER", command=self.player_surrender)
        self.surrenderButton.pack()

        self.insuranceButton = Button(self, text="INSURANCE", command=self.player_insurance)
        self.insuranceButton.pack()

    # Define methods to handle player moves
    def player_hit(self):
        self.blackjack_game.player_action("HIT")
        self.trigger_dealer_play()

    def player_stand(self):
        self.blackjack_game.player_action("STAND")
        self.trigger_dealer_play()

    def player_double_down(self):
        self.blackjack_game.player_action("DOUBLE_DOWN")
        self.trigger_dealer_play()

    def player_split(self):
        self.blackjack_game.player_action("SPLIT")
        self.trigger_dealer_play()

    def player_surrender(self):
        self.blackjack_game.player_action("SURRENDER")
        self.trigger_dealer_play()

    def player_insurance(self):
        self.blackjack_game.player_action("INSURANCE")
        self.trigger_dealer_play()
        
    def disable_buttons(self):
        # Disable all player action buttons
        self.hitButton.config(state=tk.DISABLED)
        self.standButton.config(state=tk.DISABLED)
        self.doubleDownButton.config(state=tk.DISABLED)
        self.splitButton.config(state=tk.DISABLED)
        self.surrenderButton.config(state=tk.DISABLED)
        self.insuranceButton.config(state=tk.DISABLED)

if __name__ == "__main__":
    Main().mainloop()
