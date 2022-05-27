# -*- coding: utf-8 -*-
"""
Created on Fri May 27 13:01:44 2022

@author: Devcola
"""

import sys
import random

# User Configuration
num_of_decks = 6
wallet = 500

# Global Variables
DEBUG=False
blank_card=u"\u2588"
club_card=u"\u2663"
diamond_card=u"\u2666"
heart_card=u"\u2665"
spade_card=u"\u2660"
deck_in_play = []
player_hand = []
dealer_hand = []
dealer_hidden = True
winner = None
wager = 0

# Define deck and shuffle cards
def setup_deck():
    global num_of_decks
    global deck_in_play
    cards = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
    suits = [club_card,diamond_card,heart_card,spade_card]
    
    deck = []
    for suit in suits:
        for card in cards:
            deck.append(str(suit) + str(card))

    for _ in range(num_of_decks):
        deck_in_play += deck
    
    random.shuffle(deck_in_play)

# Draw Card from deck
# Return: String Card
# Exception: Empty Deck
def draw_card() -> str:
    global deck_in_play
    if deck_in_play:
        return deck_in_play.pop()
    else:
        raise Exception('Deck is Empty')

# Convert Hand Lists to formatted string
# Input: list of cards
# Input: bool is it the dealer
# Return: hand in string
def hands_to_str(hand, is_dealer) -> str:
    hand_str = ""
    for idx, d in enumerate(hand):
        if idx == 0 and is_dealer and dealer_hidden:
            hand_str += blank_card + blank_card + " " 
        else:   
            hand_str += str(d) + " "   
    return hand_str

# Convert Score to formatted string
# Input: list of cards
# Input: bool is it the dealer
# Return: score in string
def score_to_str(hand, is_dealer) -> str:    
    score_str = ""
    score, alt_score = get_score(hand)
    if is_dealer and dealer_hidden:
        score_str = "(?)"
    else:
        if score != alt_score:
            score_str = "(" + str(score) + "/" + str(alt_score) + ")"
        else:
            score_str = "(" + str(score) + ")"
    return score_str

# Create console GUI
def text_gui():
    dealer_score = score_to_str(dealer_hand, True)
    player_score = score_to_str(player_hand, False)
    
    dealer = ['Dealer: ' + dealer_score, hands_to_str(dealer_hand, True)]
    player = ['Player: ' + player_score,  hands_to_str(player_hand, False)]
    
    print('############################################')
    for players in [dealer, player]:
        for info in players:
            print(info.ljust(25), end='')
        print("")
    print('############################################', end='')

# Get score of hand
# Alt is the larger value for aces
# Input: list of cards
# Return: Int Score
# Return: Int Alt Score for Ace
def get_score(hand) -> int:     
    score = 0
    alt_score = 0

    for p in hand:
        card = (p[1:])
        if card in ["J","Q","K"]:
            score += 10
            alt_score += 10
        elif card == "A":
            score += 1
            alt_score += 11
        else:
            score += int(p[1:])
            alt_score += int(p[1:])

    return score, alt_score

# Input: list of cards
def check_bust(hand) -> bool:
    global winner
    score, alt_score = get_score(hand)
    if score > 21:
        text_gui()
        print("\nYou Bust!")
        winner = "dealer"
        return True
    return False

# Check for blackjack
def check_blackjack():
    global winner
    global dealer_hidden
    
    dealer_score, dealer_alt_score = get_score(dealer_hand)
    player_score, player_alt_score = get_score(player_hand)
    if dealer_alt_score == 21 and player_alt_score != 21:
        print("\nDealer Blackjack!\n")
        dealer_hidden = False
        winner = "dealer"
    elif dealer_alt_score == 21 and player_alt_score == 21:
        print("\nDealer and Player Blackjack!\n")
        winner = "tie"
    elif dealer_alt_score != 21 and player_alt_score == 21:
        print("\nPlayer Blackjack!\n")
        winner = "player_blackjack"
        
# Player's Loop
def user_loop():
    global dealer_hidden
    while True:
        text_gui()
        if winner is not None:
            break
        resp = input("1. Hit\n2. Stand\n")
        if resp == "1":
            card = draw_card()
            print("Player Drew: " + card + "\n")
            player_hand.append(card)
            if check_bust(player_hand):
                break
        elif resp == "2":
            print("Player Stands!\n")
            dealer_hidden = False
            break
        else:
            print("Invalid option!\n")
            
# Dealer's Loop        
def dealer_loop():
    global dealer_hand
    
    while True:
        if winner is not None:
            break
        text_gui()
        score, alt_score = get_score(dealer_hand)
        if score >= 17 or alt_score >= 17:
            print("\nDealer Stands!")
            break
        elif score < 17:
            card = draw_card()
            print("\nDealer Drew: " + card + "\n")
            dealer_hand.append(card)
   
# Betting Loop
def make_wager():
    global wager
    while True:
        print("How much would you like to wager?", end='')
        resp = input()
        try:
            if int(resp) > wallet:
                print("Cannot bet more than your wallet: " + str(wallet) + "!\n")
            elif int(resp) < 0:
                print("Cannot bet less than 0!\n")
            else:
                wager = int(resp)
                print()
                break
        except ValueError:
            print("Bets must be valid numbers!\n")
                

# Decide Winner
def check_win():
    global wallet
    
    dealer_score, dealer_alt_score = get_score(dealer_hand)
    player_score, player_alt_score = get_score(player_hand)
    
    if player_alt_score <= 21:
        player_score = player_alt_score
    if dealer_alt_score <= 21:
        dealer_score = dealer_alt_score
    
    if (player_score > dealer_score) and player_score <= 21:
        print("\nYou Win!\n")
        if winner == 'player_blackjack':
            wallet += wager * 1.5
        else:
            wallet += wager
    elif (player_score == dealer_score) and player_score <= 21:
        print("\nYou Tie!\n")
    else:
        print("\nYou Lost!\n")
        wallet -= wager
        
# Reset game variables 
def reset_vars():
    global dealer_hand
    global player_hand
    global dealer_hidden
    global winner
    global wager
    
    dealer_hand = []
    player_hand = []
    dealer_hidden = True
    winner = None
    wager = 0
    
# Game Loop
def main():
    global dealer_hand
    global player_hand
    
    while True:
        while True:
            print("Black Jack Simulator")
            print("Wallet: " + str(wallet), end='')
            resp = input("1. New Game\n2. Quit\n")
            if resp == "1":
                reset_vars()
                print()
                break
            elif resp == "2":
                sys.exit()
            else:
                print("Invalid option!")
                
        setup_deck()
    
        player_hand.append(draw_card())
        dealer_hand.append(draw_card())
        player_hand.append(draw_card())
        dealer_hand.append(draw_card())
        
        if DEBUG:
            global deck_in_play
            print(get_score(player_hand))
            print("Deck: " + str(deck_in_play))
            print("Dealer: " + str(dealer_hand))
            print("Player: " + str(player_hand))
            
        make_wager()
        check_blackjack()
        user_loop()
        dealer_loop()
        check_win()

# Main
if __name__ == '__main__':
    sys.exit(main())