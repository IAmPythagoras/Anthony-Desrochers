#This class will represent a single action and specify if oGCD, GCD, effects it adds, etc.


class Ability:

    def __init__(self, id, Name, GCD, CastTime, RecastTime, Potency, ManaCost):
        self.id = id #Id of spell
        self.Name = Name #Name of spell
        self.GCD = GCD #True if is a GCD
        self.CastTime = CastTime #Castime of the spell
        self.Potency = Potency
        self.ManaCost = ManaCost
        self.RecastTime = RecastTime


class BLMAbility(Ability):

    def __init__(self, id, Name, GCD, CastTime,RecastTime, Potency, ManaCost, IsFire, IsIce):
        super().__init__(id, Name, GCD, CastTime, RecastTime, Potency, ManaCost)
        self.IsFire = IsFire    #if fire spell
        self.IsIce = IsIce  #If ice spell

    

    
