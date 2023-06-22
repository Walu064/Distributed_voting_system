import random

def generate_number():
    list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
    return random.choice(list)


def get_most_common_answer(list : list):    
    counter = {}
    
    for element in list:
        if element in counter:
            counter[element] += 1
        else:
            counter[element] = 1
    
    return max(counter, key=counter.get)
