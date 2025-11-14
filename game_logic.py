"""
Game Logic for Continental Card Game
Contains all game rules, validation, and card handling logic
"""
import random
import uuid
from typing import List, Dict, Optional, Tuple
from enum import Enum

class CardSuit(str, Enum):
    SPADES = '♠'
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    JOKER = 'JOKER'

class CardRank(str, Enum):
    ACE = 'A'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    JOKER = 'JOKER'

# Round requirements
ROUND_REQUIREMENTS = {
    1: {'cards': 7, 'sets': [3, 3], 'runs': []},
    2: {'cards': 8, 'sets': [3], 'runs': [4]},
    3: {'cards': 9, 'sets': [], 'runs': [4, 4]},
    4: {'cards': 10, 'sets': [3, 3, 3], 'runs': []},
    5: {'cards': 11, 'sets': [3, 3], 'runs': [4]},
    6: {'cards': 12, 'sets': [3], 'runs': [4, 4]},
    7: {'cards': 13, 'sets': [], 'runs': []},
}

def get_num_decks(num_players: int) -> int:
    if num_players <= 4:
        return 2
    elif num_players <= 7:
        return 3
    else:
        return 4

def create_deck(num_decks: int = 2) -> List[Dict]:
    deck = []
    suits = [CardSuit.SPADES, CardSuit.HEARTS, CardSuit.DIAMONDS, CardSuit.CLUBS]
    ranks = [CardRank.ACE, CardRank.TWO, CardRank.THREE, CardRank.FOUR, CardRank.FIVE,
             CardRank.SIX, CardRank.SEVEN, CardRank.EIGHT, CardRank.NINE, CardRank.TEN,
             CardRank.JACK, CardRank.QUEEN, CardRank.KING]
    
    for _ in range(num_decks):
        for suit in suits:
            for rank in ranks:
                deck.append({
                    'suit': suit.value,
                    'rank': rank.value,
                    'id': str(uuid.uuid4()),
                    'is_joker': False
                })
        for _ in range(2):
            deck.append({
                'suit': CardSuit.JOKER.value,
                'rank': CardRank.JOKER.value,
                'id': str(uuid.uuid4()),
                'is_joker': True
            })
    
    random.shuffle(deck)
    return deck

def get_card_value(card: Dict) -> int:
    rank = card['rank']
    if rank == 'JOKER':
        return 50
    elif rank == 'A':
        return 20
    elif rank in ['J', 'Q', 'K']:
        return 10
    else:
        return int(rank)

def get_rank_value(rank: str) -> int:
    rank_values = {
        'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
        '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13
    }
    return rank_values.get(rank, 0)

def validate_set(cards: List[Dict]) -> Tuple[bool, str]:
    if len(cards) < 3:
        return False, "Un trío necesita al menos 3 cartas"
    
    jokers = [c for c in cards if c['is_joker']]
    normal_cards = [c for c in cards if not c['is_joker']]
    
    if len(jokers) >= len(normal_cards):
        return False, "Debe haber más cartas normales que Jokers"
    
    if len(normal_cards) == 0:
        return False, "No puede haber solo Jokers"
    
    ranks = [c['rank'] for c in normal_cards]
    if len(set(ranks)) > 1:
        return False, "Todas las cartas deben ser del mismo número"
    
    return True, "Trío válido"

def validate_run(cards: List[Dict]) -> Tuple[bool, str]:
    """Validate run respecting card order (Jokers cannot be consecutive)"""
    if len(cards) < 4:
        return False, "Una escalera necesita al menos 4 cartas"

    jokers = [c for c in cards if c['is_joker']]
    normal_cards = [c for c in cards if not c['is_joker']]

    if len(jokers) >= len(normal_cards):
        return False, "Debe haber más cartas normales que Jokers"

    if len(normal_cards) == 0:
        return False, "No puede haber solo Jokers"

    suits = [c['suit'] for c in normal_cards]
    if len(set(suits)) > 1:
        return False, "Todas las cartas deben ser del mismo palo"

    # CRITICAL: Check for consecutive Jokers in ANY position
    for i in range(len(cards) - 1):
        if cards[i].get('is_joker') and cards[i + 1].get('is_joker'):
            return False, "No puede haber Jokers consecutivos"

    # Extract positions and values of normal cards (respecting order from frontend)
    card_positions = []
    for i, card in enumerate(cards):
        if not card['is_joker']:
            card_positions.append((i, get_rank_value(card['rank'])))

    if not card_positions:
        return False, "No puede haber solo Jokers"

    # Sort by position to maintain order
    card_positions.sort(key=lambda x: x[0])

    # Extract just the values in order
    values_in_order = [val for pos, val in card_positions]

    # Try non-cyclic sequence first
    is_valid_normal, msg_normal = _validate_run_sequence(cards, card_positions, values_in_order, cyclic=False)
    if is_valid_normal:
        return True, "Escalera válida"

    # If normal sequence fails, try cyclic (K-A wrapping)
    # Cyclic only makes sense if we have high cards (J, Q, K) and Ace
    has_ace = 1 in values_in_order or 14 in values_in_order
    has_high_card = any(v >= 11 for v in values_in_order)

    if has_ace and has_high_card:
        is_valid_cyclic, msg_cyclic = _validate_run_sequence(cards, card_positions, values_in_order, cyclic=True)
        if is_valid_cyclic:
            return True, "Escalera válida"

    # Return the non-cyclic error message as default
    return False, msg_normal


def _validate_run_sequence(cards: List[Dict], card_positions: List, values_in_order: List[int], cyclic: bool = False) -> Tuple[bool, str]:
    """Helper function to validate a run sequence (cyclic or non-cyclic)"""

    # Make a copy to avoid modifying original
    card_positions = list(card_positions)
    values_in_order = list(values_in_order)

    # Adjust values for cyclic sequences
    if cyclic:
        # In cyclic mode, we need to detect if we're wrapping around K->A->2
        # Strategy:
        # 1. Convert all Aces (1) to 14
        # 2. Detect if we have low cards (2-4) that come AFTER the Ace in position
        # 3. Convert those low cards to virtual values (15, 16, 17, etc.)

        has_ace = any(val == 1 for pos, val in card_positions)
        ace_position = None

        # Find Ace position if it exists
        for pos, val in card_positions:
            if val == 1:
                ace_position = pos
                break

        adjusted_positions = []
        for pos, val in card_positions:
            if val == 1:
                # Ace becomes 14
                adjusted_positions.append((pos, 14))
            elif has_ace and ace_position is not None and pos > ace_position and val <= 4:
                # Low cards (2-4) AFTER Ace in position become 15, 16, 17, etc.
                # 2 -> 15, 3 -> 16, 4 -> 17
                adjusted_positions.append((pos, val + 13))
            else:
                adjusted_positions.append((pos, val))

        card_positions = adjusted_positions
        values_in_order = [val for pos, val in card_positions]

    first_pos, first_val = card_positions[0]
    last_pos, last_val = card_positions[-1]

    # Count jokers in different positions
    jokers_before = first_pos
    jokers_after = len(cards) - 1 - last_pos

    # Calculate sequence range
    start_val = first_val - jokers_before
    end_val = last_val + jokers_after

    # Validate range
    if start_val < 1:
        return False, "La secuencia va por debajo del AS"

    if cyclic:
        # For cyclic, allow up to ~17-18 (A, 2, 3, 4, 5)
        if end_val > 18:
            return False, "La secuencia cíclica es demasiado larga"
    else:
        # Non-cyclic: strict range check (1-14)
        if end_val > 14:
            return False, "La secuencia va por encima del AS"

    # Verify length
    expected_length = end_val - start_val + 1
    if expected_length != len(cards):
        return False, "Las cartas no forman una secuencia válida"

    # Check that normal cards are in the right positions
    for pos, val in card_positions:
        expected_val = start_val + pos
        if val != expected_val:
            return False, "Las cartas no están en orden consecutivo"

    return True, "Escalera válida"

def try_sequence(values, num_jokers, total_length, cyclic):
    """Try to form a sequence with given values and jokers"""
    if len(values) == 0:
        return False
    
    # For cyclic, convert Ace to 14 if there are high cards
    if cyclic and 1 in values and any(v >= 11 for v in values):
        values_adjusted = []
        for v in values:
            if v == 1:
                values_adjusted.append(14)
            else:
                values_adjusted.append(v)
        values = sorted(values_adjusted)
    
    min_val = values[0]
    max_val = values[-1]
    span = max_val - min_val + 1
    
    if span != total_length:
        return False
    
    # Check gaps can be filled with jokers
    all_positions = set(range(min_val, max_val + 1))
    filled_positions = set(values)
    gaps = sorted(all_positions - filled_positions)
    
    if len(gaps) != num_jokers:
        return False
    
    # Check no consecutive jokers
    sequence = []
    for pos in range(min_val, max_val + 1):
        if pos in filled_positions:
            sequence.append('card')
        else:
            sequence.append('joker')
    
    for i in range(len(sequence) - 1):
        if sequence[i] == 'joker' and sequence[i + 1] == 'joker':
            return False
    
    return True

def validate_meld_group(melds: List[Dict], round_num: int) -> Tuple[bool, str]:
    requirements = ROUND_REQUIREMENTS[round_num]
    
    if round_num == 7:
        return True, "Ronda 7: debe bajar todas las cartas en un turno"
    
    sets = [m for m in melds if m['type'] == 'set']
    runs = [m for m in melds if m['type'] == 'run']
    
    required_sets = requirements['sets']
    required_runs = requirements['runs']
    
    if len(sets) < len(required_sets):
        return False, f"Faltan tríos: necesitas {len(required_sets)}, tienes {len(sets)}"
    
    if len(runs) < len(required_runs):
        return False, f"Faltan escaleras: necesitas {len(required_runs)}, tienes {len(runs)}"
    
    for i, required_size in enumerate(required_sets):
        if i >= len(sets):
            break
        if len(sets[i]['cards']) < required_size:
            return False, f"Trío {i+1} debe tener al menos {required_size} cartas"
    
    for i, required_size in enumerate(required_runs):
        if i >= len(runs):
            break
        if len(runs[i]['cards']) < required_size:
            return False, f"Escalera {i+1} debe tener al menos {required_size} cartas"
    
    return True, "Combinaciones válidas"

def calculate_hand_points(hand: List[Dict]) -> int:
    return sum(get_card_value(card) for card in hand)

def calculate_negative_points(round_num: int) -> int:
    return -10 * round_num

def sort_run_cards(cards: List[Dict]) -> List[Dict]:
    """Sort run cards maintaining joker positions"""
    normal_cards = [c for c in cards if not c['is_joker']]
    jokers = [c for c in cards if c['is_joker']]
    
    if not normal_cards:
        return cards
    
    normal_values = [get_rank_value(c['rank']) for c in normal_cards]
    
    # Check if cyclic
    has_high = any(v >= 11 for v in normal_values)
    has_ace = 1 in normal_values
    
    value_to_card = {}
    for card in normal_cards:
        val = get_rank_value(card['rank'])
        if has_high and val == 1:
            value_to_card[14] = card
        else:
            value_to_card[val] = card
    
    sorted_values = sorted(value_to_card.keys())
    
    result = []
    all_positions = list(range(sorted_values[0], sorted_values[-1] + 1))
    
    joker_idx = 0
    for pos in all_positions:
        if pos in value_to_card:
            result.append(value_to_card[pos])
        elif joker_idx < len(jokers):
            result.append(jokers[joker_idx])
            joker_idx += 1
    
    while joker_idx < len(jokers):
        result.append(jokers[joker_idx])
        joker_idx += 1
    
    return result