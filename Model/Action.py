#This class will represent a single action and specify if oGCD, GCD, effects it adds, etc.

import Effect
import Job
import Player
class Ability:

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect):
        self.id = id #Id of spell
        self.GCD = GCD #True if is a GCD
        self.CastTime = CastTime #Castime of the spell
        self.Potency = Potency
        self.ManaCost = ManaCost
        self.RecastTime = RecastTime
        self.Effect = Effect


class BLMAbility(Ability):

    def __init__(self, id, GCD, CastTime,RecastTime, Potency, ManaCost, IsFire, IsIce, Effect):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect)
        self.IsFire = IsFire    #if fire spell
        self.IsIce = IsIce  #If ice spell

    def Cast(self, Player):
        tempSpell = BLMAbility(self.id, self.Name, self.GCD, self.CastTime,self.RecastTime, self.Potency, self.ManaCost, self.IsFire, self.IsIce)
        
        for Effect in Player.EffectList:
            Effect(Player, tempSpell)

        #Spell has now been updated with every effect
        #Add new effect to player
        tempSpell.Effect(Player)

        return tempSpell


#BLM Ability


def AddAstralFire1(Player):

    if(Player.AstralFireStack >=0 and Player.AstralFireStack <3 and Player.UmbralIceStack == 0):
        Player.AstralFireStack+=1
    elif (Player.AstralFireStack == 0 and Player.UmbralIceStack >=1):
        Player.AstralFireStack = 0
        Player.UmbralIceStack = 0

def AddAstralFire3(Player):
    Player.AstralFireStack = 3

Fire1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, True, False, AddAstralFire1)
Fire2 = BLMAbility(1, True, 2.17, 2.17, 140, 200, True, False, ())
Fire3 = BLMAbility(2, True, 2.17, 2.17, 140, 200, True, False, AddAstralFire3)
Fire4 = BLMAbility(3, True, 2.17, 2.17, 140, 200, True, False, ())

Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True)
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True)
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True)
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True)





    

    
