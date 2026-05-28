from protocol import *
from player import Player
from collections import Counter


# helper to check if the protocol got the right answer
# uses Counter to handle duplicates correctly (multisets)
def verify(players, result):
    counts = [Counter(p.set) for p in players]
    expected = counts[0]
    for c in counts[1:]:
        expected = expected & c

    got = sorted(result)
    want = sorted(expected.elements())

    print(f"  got:      {got}")
    print(f"  expected: {want}")
    print(f"  {'OK' if got == want else 'FAIL'}")


def run_test(name, players, c=1):
    print(f"\n--- {name} ---")
    for p in players:
        print(f"  {p.id}: {p.set}")
    poly = run_protocol(players, c=c)
    result = recover_intersection(players, poly)
    verify(players, result)


# basic case, two players with some overlap
run_test("basic 2-player",
    [
        Player("Alice", [1, 2, 3, 5], public_key),
        Player("Bob",   [2, 3, 9, 12], public_key),
    ]
)

# multisets, element 2 appears twice in every set so it should appear twice in result
run_test("multiset",
    [
        Player("Alice",   [1, 2, 2, 3, 5, 12], public_key),
        Player("Bob",     [2, 2, 3, 9, 12],    public_key),
        Player("Charlie", [0, 2, 2, 3, 7],     public_key),
    ],
    c=2
)

# no common elements at all, intersection should be empty
run_test("empty intersection",
    [
        Player("Alice",   [1, 3, 5], public_key),
        Player("Bob",     [2, 4, 6], public_key),
        Player("Charlie", [7, 8, 9], public_key),
    ]
)

# everyone has the same set
run_test("identical sets",
    [
        Player("Alice",   [1, 2, 3], public_key),
        Player("Bob",     [1, 2, 3], public_key),
        Player("Charlie", [1, 2, 3], public_key),
    ]
)

# only one shared element across all players
run_test("single common element",
    [
        Player("Alice",   [1, 2, 7],  public_key),
        Player("Bob",     [3, 7, 9],  public_key),
        Player("Charlie", [5, 7, 11], public_key),
    ]
)

# 5 players, tests that the protocol still works as n grows
run_test("five players",
    [
        Player("Alice",   [3, 7, 11, 13], public_key),
        Player("Bob",     [3, 7, 2,  4],  public_key),
        Player("Charlie", [3, 7, 5,  9],  public_key),
        Player("Daniel",  [3, 7, 6,  8],  public_key),
        Player("Emma",    [3, 7, 10, 12], public_key),
    ],
    c=2
)