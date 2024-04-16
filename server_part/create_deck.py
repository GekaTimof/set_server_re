from random import shuffle

def create_deck():
    card_id = 0
    deck = []

    for color in range(1, 4):
        for shape in range(1, 4):
            for fill in range(1, 4):
                for count in range(1, 4):
                    if card_id < 10:
                        deck.append("0" + str(card_id) + "." + str(color) + str(shape) + str(fill) + str(color))
                    else:
                        deck.append(str(card_id) + "." + str(color) + str(shape) + str(fill) + str(color))
                    card_id += 1
    shuffle(deck)

    return "*".join(deck)