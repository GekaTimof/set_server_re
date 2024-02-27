import json
import copy

color = ['blue', 'red', 'green']
shape = ['ovals', 'waves', 'diamonds']
fill = ['shaded', 'unpainted', 'striped']
count = ['one', 'two', 'three']

params = [color, shape, fill, count]
paramsNames = ['color', 'shape', 'fill', 'count']

def find_set(data):
    data_re = copy.deepcopy(data)

    for i, card in enumerate(data_re['cards']):
        data_re['cards'][i].pop('id', None)

    # get cards pairs
    for i1, card1 in enumerate(data_re['cards'][:-2]):
        for i2, card2 in enumerate(data_re['cards'][i1+1:-1]):

            # checking for set
            card3 = {}
            for attribute, value in card1.items():
                if (card2.get(attribute) == value):
                    card3[attribute] = value
                else:
                    card3[attribute] = 6 - card2.get(attribute) - value

            if card3 in data_re['cards'][i2+1:]:
                print(" card for set:")

                for card in [card1, card2, card3]:
                    print(data['cards'][data_re['cards'].index(card)]['id'])
                    for num, param in enumerate(params):
                        print(param[data['cards'][data_re['cards'].index(card)][paramsNames[num]] - 1])
                    print()


# get json from file
with open('../../Desktop/Computing systems/set/responce.json', 'r') as json_file:
    data = json.load(json_file)

find_set(data)