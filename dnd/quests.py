import random

class Quest:
    def __init__(self, description, target_type, target_count):
        self.description = description
        self.target_type = target_type
        self.target_count = target_count

def get_random_quests(count):
    possible_quests = [
        Quest("Убити 5 Огрів", "Ogre", 5),
        Quest("Убити 5 ворогів із сокирою", "Axe Enemy", 5),
        Quest("Убити 3 ворогів із мечем", "Sword Enemy", 3)
    ]
    return random.sample(possible_quests, count)