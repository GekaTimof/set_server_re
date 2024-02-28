from random import shuffle

def create_deck():
    card_id = 0
    deck = []

    for color in range(1,4):
        for shape in range(1, 4):
            for fill in range(1, 4):
                for count in range(1, 4):
                    deck.append({"id": card_id, "color": color, "shape": shape, "fill": fill, "count": count})
                    card_id += 1
    shuffle(deck)
    return deck