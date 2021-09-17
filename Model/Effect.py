#THis class will contain an Effect objet

#Each effect will be a function that we apply on the PlayerObject, it will modify a whatever it has to in this object.
#Each function will be called in order


from Action import *


#Black Mage

def AstralFire(Player : BlackMage, Stack, Spell : BLMAbility):

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

def LeyLines(Player, Spell):
    Spell.CastTime*=0.85
    Spell.RecastTime*=0.85

def Enochian(Player, Spell):
    Spell.Potency*=1.15

def TripleCast(Player,Spell):
    Spell.CastTime=0
    Player.TripleCastStack-=1

    if (Player.)

def SharpCast(Player, Spell):



        

    #Update the potency of the Spell




    




