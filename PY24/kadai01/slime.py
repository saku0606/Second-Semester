import random

class Slime:
    def __init__(self, iti):
        self.iti = iti
    def run(self):
        return self.iti + random.randint(-1, 3)
    
slime1 = Slime(0)

print(slime1.iti)
print(slime1.run()) 