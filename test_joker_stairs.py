#!/usr/bin/env python3
"""Test for Joker in stairs validation"""

from game_logic import validate_run

# Test 1: Joker, J, Q, K (all same suit) - Joker as 10
cards_test1 = [
    {'is_joker': True, 'rank': 'Joker', 'suit': 'hearts', 'id': 'j1'},
    {'is_joker': False, 'rank': 'J', 'suit': 'hearts', 'id': 'c1'},
    {'is_joker': False, 'rank': 'Q', 'suit': 'hearts', 'id': 'c2'},
    {'is_joker': False, 'rank': 'K', 'suit': 'hearts', 'id': 'c3'}
]

# Test 2: J, Q, K, Joker (all same suit) - Joker as Ace (14)
cards_test2 = [
    {'is_joker': False, 'rank': 'J', 'suit': 'hearts', 'id': 'c1'},
    {'is_joker': False, 'rank': 'Q', 'suit': 'hearts', 'id': 'c2'},
    {'is_joker': False, 'rank': 'K', 'suit': 'hearts', 'id': 'c3'},
    {'is_joker': True, 'rank': 'Joker', 'suit': 'hearts', 'id': 'j1'}
]

# Test 3: 9, Joker, J, Q (all same suit) - Joker as 10
cards_test3 = [
    {'is_joker': False, 'rank': '9', 'suit': 'hearts', 'id': 'c1'},
    {'is_joker': True, 'rank': 'Joker', 'suit': 'hearts', 'id': 'j1'},
    {'is_joker': False, 'rank': 'J', 'suit': 'hearts', 'id': 'c2'},
    {'is_joker': False, 'rank': 'Q', 'suit': 'hearts', 'id': 'c3'}
]

# Test 4: Joker, 3, 4, 5 (all same suit) - Joker as 2
cards_test4 = [
    {'is_joker': True, 'rank': 'Joker', 'suit': 'diamonds', 'id': 'j1'},
    {'is_joker': False, 'rank': '3', 'suit': 'diamonds', 'id': 'c1'},
    {'is_joker': False, 'rank': '4', 'suit': 'diamonds', 'id': 'c2'},
    {'is_joker': False, 'rank': '5', 'suit': 'diamonds', 'id': 'c3'}
]

# Test 5: Joker, 2, 3, 4 (all same suit) - Joker as Ace (1)
cards_test5 = [
    {'is_joker': True, 'rank': 'Joker', 'suit': 'clubs', 'id': 'j1'},
    {'is_joker': False, 'rank': '2', 'suit': 'clubs', 'id': 'c1'},
    {'is_joker': False, 'rank': '3', 'suit': 'clubs', 'id': 'c2'},
    {'is_joker': False, 'rank': '4', 'suit': 'clubs', 'id': 'c3'}
]

# Test 6: Joker, Joker, 3, 4, 5 (all same suit) - Double Jokers at start (as A and 2)
cards_test6 = [
    {'is_joker': True, 'rank': 'Joker', 'suit': 'spades', 'id': 'j1'},
    {'is_joker': True, 'rank': 'Joker', 'suit': 'spades', 'id': 'j2'},
    {'is_joker': False, 'rank': '3', 'suit': 'spades', 'id': 'c1'},
    {'is_joker': False, 'rank': '4', 'suit': 'spades', 'id': 'c2'},
    {'is_joker': False, 'rank': '5', 'suit': 'spades', 'id': 'c3'}
]

# Test 7: A, 2, 3, 4 (all same suit) - Ace as 1
cards_test7 = [
    {'is_joker': False, 'rank': 'A', 'suit': 'hearts', 'id': 'c1'},
    {'is_joker': False, 'rank': '2', 'suit': 'hearts', 'id': 'c2'},
    {'is_joker': False, 'rank': '3', 'suit': 'hearts', 'id': 'c3'},
    {'is_joker': False, 'rank': '4', 'suit': 'hearts', 'id': 'c4'}
]

print("=" * 60)
print("TESTS DE ESCALERAS CON JOKERS")
print("=" * 60)
print()

print("Test 1: Joker, J, Q, K (Joker como 10)")
valid, message = validate_run(cards_test1)
print(f"  ✓ Válido: {valid}, Mensaje: {message}")
assert valid == True, "Este test debería ser válido"
print()

print("Test 2: J, Q, K, Joker (Joker como As/14)")
valid, message = validate_run(cards_test2)
print(f"  ✓ Válido: {valid}, Mensaje: {message}")
assert valid == True, "Este test debería ser válido"
print()

print("Test 3: 9, Joker, J, Q (Joker como 10)")
valid, message = validate_run(cards_test3)
print(f"  ✓ Válido: {valid}, Mensaje: {message}")
assert valid == True, "Este test debería ser válido"
print()

print("Test 4: Joker, 3, 4, 5 (Joker como 2)")
valid, message = validate_run(cards_test4)
print(f"  ✓ Válido: {valid}, Mensaje: {message}")
assert valid == True, "Este test debería ser válido"
print()

print("Test 5: Joker, 2, 3, 4 (Joker como As/1)")
valid, message = validate_run(cards_test5)
print(f"  ✓ Válido: {valid}, Mensaje: {message}")
assert valid == True, "Este test debería ser válido"
print()

print("Test 6: Joker, Joker, 3, 4, 5 (dos Jokers al inicio como As y 2)")
valid, message = validate_run(cards_test6)
print(f"  ✓ Válido: {valid}, Mensaje: {message}")
assert valid == True, "Este test debería ser válido"
print()

print("Test 7: A, 2, 3, 4 (As como 1, sin Jokers)")
valid, message = validate_run(cards_test7)
print(f"  ✓ Válido: {valid}, Mensaje: {message}")
assert valid == True, "Este test debería ser válido"
print()

print("=" * 60)
print("¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
print("=" * 60)
