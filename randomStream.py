import random

class Stream(object):
    def choiceStream(items: list = []):
        return random.choice(items)
    
    def randomIntSteram() -> int:
        return random.randint(100000, 999999999)