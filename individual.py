class Individual:

    # representation is an array that contains which items are chosen
    # p.e.: [False, True, True] -> item of index 0 is not used, but 1 is used  
    # representationParts is used for crossover and is an matriz
    # p.e.: [[False, False, True], [True, True]]
    def __init__(self, size, represetationParts=None):
        self.representation = [False] * size
        if represetationParts != None:
            self.buildRepresentation(represetationParts)

    # representationParts is used for crossover and is an matriz
    # p.e.: [[False, False, True], [True, True]] turns to [False, False, True, True, True]
    def buildRepresentation(self, representationParts):
        total_elements = sum(len(part) for part in representationParts)
        if total_elements != len(self.representation):
            raise ValueError("Incompatible size between representation and parts")
        
        index = 0
        for part in representationParts:
            for element in part:
                self.representation[index] = element
                index += 1

    def chooseItem(self, index):
        if index >= 0 and index < len(self.representation):
            self.representation[index] = True