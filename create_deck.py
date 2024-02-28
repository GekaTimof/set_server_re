

def create_deck():
    card_id = 0
    deck = {"cards": []}

    for color in range(1,4):
        for shape in range(1, 4):
            for fill in range(1, 4):
                for count in range(1, 4):
                    deck["cards"].append({ "id": card_id, "color": color, "shape": shape, "fill": fill, "count": count})
                    card_id += 1
    return deck