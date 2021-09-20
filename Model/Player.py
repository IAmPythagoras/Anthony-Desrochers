#This class will represent a player with a job, etc.
#It will first be assumed to only be a BLM


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
        tempSpell = BLMAbility(self.id, self.GCD, self.CastTime,self.RecastTime, self.Potency, self.ManaCost, self.IsFire, self.IsIce, self.Effect)
        
        for Effect in Player.EffectList:
            Effect(Player, tempSpell)

        #Spell has now been updated with every effect
        #Add new effect to player
        tempSpell.Effect(Player)

        return tempSpell

class player:

    def __init__(self, GCDTimer, ActionSet):
        self.GCDTimer = GCDTimer
        self.ActionSet = ActionSet  #List of actions to be performed in order
        self.EffectList = []
        self.Casting = False
        self.oGCDLock = False
        self.GCDLock = False
        self.TotalMane = 10000



class BlackMage(player):

    def __init__(self, GCDTimer, ActionSet):
        super().__init__(GCDTimer, ActionSet)
        self.AstralFireStack = 0
        self.UmbralIceStack = 0
        self.Enochian = False
        self.T3Prock = False
        self.F3Prock = False
        self.SharpCastStack = 0
        self.PolyglotStack = 0
        self.TripleCastStack = 0
        self.SwiftCastStack = 0
        self.T3Timer = 0
        self.F3Timer = 0
        self.AFUITimer = 0


        


    def PerformActionSetBlackMage(self, timeUnit, TimeLimit):

        timer = 0
        spellCounter = 0
        TotalPotency = 0
        timeBeforeNextGCD = 0
        while(timer < TimeLimit):

            nextSpell = self.ActionSet[spellCounter]

            if(nextSpell.GCD):
                #If spell is a GCD
                if(not self.GCDLock):
                    tempSpell = nextSpell.Cast(self)
                    TotalPotency += tempSpell.Potency #Add potency of spell
                    timer+= tempSpell.CastTime #Fast forward to when next action is possible
                    spellCounter+=1#Upgrade spellCounter
                    
                    timeBeforeNextGCD = max(0, tempSpell.CastTime - tempSpell.RecastTime)
                    self.GCDLock = True #Cannot cast GCD

                    if (spellCounter >= len(self.ActionSet)) : break #If no more spell,we out



            else:
                #spell is an oGCD
                tempSpell = nextSpell.Cast(self)
                TotalPotency += tempSpell.Potency
                timer += tempSpell.CastTime#For oGCD, set to about 0.5s (more like animation lock)

                timeBeforeNextGCD = max(0, timeBeforeNextGCD - tempSpell.CastingTime)

                if (spellCounter >= len(self.ActionSet)) : break #If no more spell,we out

            if (timeBeforeNextGCD <= 0):
                self.GCDLock = False
            else:
                timeBeforeNextGCD-=0.01

            timer+=0.01

        return TotalPotency/timer


def AddAstralFire1(Player):

    if(Player.AstralFireStack >=0 and Player.AstralFireStack <3 and Player.UmbralIceStack == 0):
        Player.AstralFireStack+=1
    elif (Player.AstralFireStack == 0 and Player.UmbralIceStack >=1):
        Player.AstralFireStack = 0
        Player.UmbralIceStack = 0

def AddAstralFire3(Player):
    Player.AstralFireStack = 3

def AddUmbralIce3(Player):
    Player.UmbralIceStack = 3

def AddUmbralIce1(Player):
    print("bruh")

Fire1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, True, False, AddAstralFire1)
Fire2 = BLMAbility(1, True, 2.17, 2.17, 140, 200, True, False, ())
Fire3 = BLMAbility(2, True, 2.17, 2.17, 140, 200, True, False, AddAstralFire3)
Fire4 = BLMAbility(3, True, 2.17, 2.17, 140, 200, True, False, ())

Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True, AddUmbralIce1)
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True, ())
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True, AddUmbralIce3)
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True, ())

List = [Fire3,Fire1, Fire1]
BLM = BlackMage(2.17, List)

#####

print(BLM.PerformActionSetBlackMage(0.1, 10))



                        



        

            



    


