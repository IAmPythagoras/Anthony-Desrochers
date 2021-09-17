#THis class will contain an Effect objet

#Each effect will be a function that we apply on the PlayerObject, it will modify a whatever it has to in this object.
#Each function will be called in order


import Action
import Job
import Player


#Black Mage

def AstralFire(Player, Spell):
    Stack = Player.AstralFireStack

    if (Spell.IsFire):
        Spell.ManaCost*=2#Update Mana cost
        if(Stack == 1): 
            Spell.Potency*=1.4#Update Damage
        elif(Stack == 2): 
            Spell.Potency*=1.6#Update Damage
        elif (Stack == 3): 
            Spell.Potency*=1.8#Update Damage
    elif (Spell.IsIce):
        if(Stack == 1): 
            Spell.Potency*=0.9#Update Damage
            Spell.ManaCost*=0.5
        elif(Stack == 2): 
            Spell.Potency*=0.8#Update Damage
            Spell.ManaCost*=0.25
        elif (Stack == 3): 
            Spell.Potency*=0.7#Update Damage
            Spell.ManaCost*=0
            Spell.CastTime*=0.5

def UmbralIce(Player, Spell):
    Stack = Player.UmbralIceStack
    if(Spell.IsIce):
        if (Stack == 1):
            Spell.ManaCost *= 0.75
        elif (Stack == 2):
            Spell.ManaCost *= 0.5
        elif (Stack == 3):
            Spell.ManaCost = 0
    elif(Spell.IsFire):
        if (Stack == 1):
            Spell.ManaCost *= 0.5
            Spell.Potency *= 0.9
        elif (Stack == 2):
            Spell.ManaCost *= 0.25
            Spell.Potency *= 0.8
        elif (Stack == 3):
            Spell.ManaCost = 0
            Spell.CastTime *= 0.5
            Spell.Potency *= 0.7

def LeyLines(Player, Spell):
    Spell.CastTime*=0.85
    Spell.RecastTime*=0.85

def Enochian(Player, Spell):
    Spell.Potency*=1.15

def TripleCast(Player,Spell):
    Spell.CastTime=0
    Player.TripleCastStack-=1

    if (Player.TripleCastStack == 0):
        Player.EffectList.remove(TripleCast)

def SwiftCast(Player, Spell):
    Spell.CastTime=0
    Player.EffectList.remove(SwiftCast)

def SharpCast(Player,Spell):

    if(Spell.Id == 0):#Id 0 is T3
        Player.T3Prock = 1
        Player.SharpCastStack = 0
    elif(Spell.Id == 1): #Fire 1
        Player.F3Prock == 1
        Player.SharpCastStack = 0

def T3Prock(Player, Spell):

    if(Spell.Id == 0):
        Spell.CastTime = 0
        Spell.Potency = 320
        Spell.ManaCost = 0
        Player.T3Prock = 0


def F3Prock(Player, Spell):

    if (Spell.Id == 2):
        Spell.CastTime = 0
        Spell.ManaCost = 0




        

    #Update the potency of the Spell




    




