import random
import re
COIN = ["heads", "tails"]
DICE = [1, 2, 3, 4, 5, 6]
OTHER = ["odd", "even"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["Spades", "Diamonds", "Clubs", "Hearts"]

def check_wager(wager):
    if not wager.isdigit():
        raise ValueError("Please enter a valid number")

    wager = int(wager)

    if wager <= 0:
        raise ValueError("Please enter a positive wager")
    
    return wager

def parse_card(s: str) -> tuple[str, str]:
    match = re.fullmatch(r"(\d+|[AJQK])([A-Za-z]+)", s)
    if not match:
        raise ValueError("Invalid card format")

    rank, suit = match.groups()
    return rank, suit

def flip_coin(wager, call):
    if wager is None and call is None:
        raise ValueError(f"The coin landed {random.choice(COIN)}")

    wager = check_wager(wager)

    if call not in COIN:
        raise ValueError("Please enter a valid call")
    
    outcome = random.choice(COIN)
    return outcome, 1 if (call == outcome) else 0, wager

def roll_dice(wager, call):
    if wager is None and call is None:
        raise ValueError(f"The dice landed on {random.choice(DICE)}")

    wager = check_wager(wager)
    
    if call in OTHER:
        isNum = False
    elif call and call.isdigit() and int(call) in DICE:
        isNum = True
    else:
        raise ValueError("Please enter a valid call")

    outcome = random.choice(DICE)

    if isNum:
        return outcome, 5 if outcome == int(call) else 0, wager

    if call == "odd":
        return outcome, outcome % 2, wager
    else:
        return outcome, 1 if not (outcome % 2) else 0, wager

def draw_card(wager, call):
    rank = random.choice(RANKS)
    suit = random.choice(SUITS)

    if wager is None and call is None:
        raise ValueError(f"You drew the {rank} of {suit}")
    
    wager = check_wager(wager)
    outcome = f"{rank} of {suit} "
    if call is None:
        raise ValueError("Please enter a valid call")

    if call in RANKS:
        return outcome, 12 if (call == rank) else 0, wager
    elif call in SUITS:
        return outcome, 3 if (call == suit) else 0, wager
    
    callRank, callSuit = parse_card(call)

    if callRank in RANKS and callSuit in SUITS:
        return outcome, 51 if (callRank == rank and callSuit == suit) else 0, wager
    else:
        raise ValueError("Please enter a valid call")
    