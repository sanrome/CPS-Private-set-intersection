from protocol import *
from player import Player

alice = Player("Alice",[1, 2, 3,3,  5, 12],public_key)

bob = Player("Bob",[2, 3,3, 9, 12],public_key)

charlie = Player("Charlie",[0, 2, 3,3,  7],public_key)

daniel = Player("Daniel",[ 2, 3,3, 133, 54],public_key)

emma = Player("Emma",[2, 3, 7, 3, 54],public_key)


players = [alice, bob, charlie, daniel, emma]

print("\n================================")
print("PLAYERS")
print("================================")

for p in players:
    print(f"\nPlayer: {p.id}")
    print("Private Set:", p.set)
    print("Polynomial:", p.polynomial)


#run protocol

print("\n================================")
print("RUNNING PROTOCOL")
print("================================")

final_polynomial = run_protocol(players, c= 4)

print("\nFinal Polynomial:")
print(final_polynomial)


#intersection calculation

intersection = roots(players[0].set,final_polynomial)

print("\n================================")
print("RECOVERED INTERSECTION")
print("================================")

print(intersection)