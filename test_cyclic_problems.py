#!/usr/bin/env python3
"""Test para verificar problemas reportados con escaleras cíclicas y Jokers consecutivos"""

from game_logic import validate_run

print("=" * 70)
print("TESTS DE PROBLEMAS REPORTADOS")
print("=" * 70)
print()

# Test 1: Q, Joker, AS, 2 (Joker como K) - ESCALERA CÍCLICA
print("Test 1: Q, Joker, AS, 2 (Joker como K - escalera cíclica)")
cards_cyclic = [
    {'is_joker': False, 'rank': 'Q', 'suit': 'hearts', 'id': 'c1'},
    {'is_joker': True, 'rank': 'Joker', 'suit': 'hearts', 'id': 'j1'},
    {'is_joker': False, 'rank': 'A', 'suit': 'hearts', 'id': 'c2'},
    {'is_joker': False, 'rank': '2', 'suit': 'hearts', 'id': 'c3'}
]
valid, message = validate_run(cards_cyclic)
print(f"  Resultado: {valid}, Mensaje: {message}")
print(f"  ESPERADO: True (debería ser válida)")
print()

# Test 2: Joker, Joker, 3, 4, 5 - JOKERS CONSECUTIVOS
print("Test 2: Joker, Joker, 3, 4, 5 (dos Jokers consecutivos al inicio)")
cards_consecutive_jokers = [
    {'is_joker': True, 'rank': 'Joker', 'suit': 'spades', 'id': 'j1'},
    {'is_joker': True, 'rank': 'Joker', 'suit': 'spades', 'id': 'j2'},
    {'is_joker': False, 'rank': '3', 'suit': 'spades', 'id': 'c1'},
    {'is_joker': False, 'rank': '4', 'suit': 'spades', 'id': 'c2'},
    {'is_joker': False, 'rank': '5', 'suit': 'spades', 'id': 'c3'}
]
valid, message = validate_run(cards_consecutive_jokers)
print(f"  Resultado: {valid}, Mensaje: {message}")
print(f"  ESPERADO: False (NO debería permitir Jokers consecutivos)")
print()

# Test 3: J, Q, K, AS (escalera cíclica sin Joker - para verificar)
print("Test 3: J, Q, K, AS (escalera cíclica sin Joker)")
cards_cyclic_no_joker = [
    {'is_joker': False, 'rank': 'J', 'suit': 'diamonds', 'id': 'c1'},
    {'is_joker': False, 'rank': 'Q', 'suit': 'diamonds', 'id': 'c2'},
    {'is_joker': False, 'rank': 'K', 'suit': 'diamonds', 'id': 'c3'},
    {'is_joker': False, 'rank': 'A', 'suit': 'diamonds', 'id': 'c4'}
]
valid, message = validate_run(cards_cyclic_no_joker)
print(f"  Resultado: {valid}, Mensaje: {message}")
print(f"  ESPERADO: True (debería ser válida)")
print()

# Test 4: K, AS, 2, 3 (escalera cíclica sin Joker)
print("Test 4: K, AS, 2, 3 (escalera cíclica sin Joker)")
cards_cyclic2 = [
    {'is_joker': False, 'rank': 'K', 'suit': 'clubs', 'id': 'c1'},
    {'is_joker': False, 'rank': 'A', 'suit': 'clubs', 'id': 'c2'},
    {'is_joker': False, 'rank': '2', 'suit': 'clubs', 'id': 'c3'},
    {'is_joker': False, 'rank': '3', 'suit': 'clubs', 'id': 'c4'}
]
valid, message = validate_run(cards_cyclic2)
print(f"  Resultado: {valid}, Mensaje: {message}")
print(f"  ESPERADO: True (debería ser válida)")
print()

# Test 5: 3, 4, Joker, Joker, 7 (Jokers consecutivos en medio)
print("Test 5: 3, 4, Joker, Joker, 7 (dos Jokers consecutivos en medio)")
cards_consecutive_middle = [
    {'is_joker': False, 'rank': '3', 'suit': 'hearts', 'id': 'c1'},
    {'is_joker': False, 'rank': '4', 'suit': 'hearts', 'id': 'c2'},
    {'is_joker': True, 'rank': 'Joker', 'suit': 'hearts', 'id': 'j1'},
    {'is_joker': True, 'rank': 'Joker', 'suit': 'hearts', 'id': 'j2'},
    {'is_joker': False, 'rank': '7', 'suit': 'hearts', 'id': 'c3'}
]
valid, message = validate_run(cards_consecutive_middle)
print(f"  Resultado: {valid}, Mensaje: {message}")
print(f"  ESPERADO: False (NO debería permitir Jokers consecutivos)")
print()

# Test 6: Joker, K, AS, 2 (Joker como Q - escalera cíclica)
print("Test 6: Joker, K, AS, 2 (Joker como Q - escalera cíclica)")
cards_cyclic_joker_start = [
    {'is_joker': True, 'rank': 'Joker', 'suit': 'spades', 'id': 'j1'},
    {'is_joker': False, 'rank': 'K', 'suit': 'spades', 'id': 'c1'},
    {'is_joker': False, 'rank': 'A', 'suit': 'spades', 'id': 'c2'},
    {'is_joker': False, 'rank': '2', 'suit': 'spades', 'id': 'c3'}
]
valid, message = validate_run(cards_cyclic_joker_start)
print(f"  Resultado: {valid}, Mensaje: {message}")
print(f"  ESPERADO: True (debería ser válida)")
print()

print("=" * 70)
print("FIN DE TESTS")
print("=" * 70)
