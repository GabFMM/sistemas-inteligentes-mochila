class Problem:
    
    # items is an array of pairs in this format: [w, v]
    # w is the item weight
    # v is the item value 
    def __init__(self, maxWeight, items):
        self.maxWeight = maxWeight;
        self.items = items;