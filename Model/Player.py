#This class will represent a player with a job, etc.
#It will first be assumed to only be a BLM
import Effect
import Job
from Action import *
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
                    timer+= tempSpell.CastingTime #Fast forward to when next action is possible
                    spellCounter+=1#Upgrade spellCounter
                    
                    timeBeforeNextGCD = max(0, tempSpell.CastTime - tempSpell.RecastTime)
                    self.GCDLock = True #Cannot cast GCD

                    if (spellCounter >= len(self.ActionSet)) : break #If no more spell,we out



            else:
                #spell is an oGCD
                tempSpell = nextSpell.Cast(self)
                TotalPotency += tempSpell.Potency
                timer += tempSpell.CastingTime#For oGCD, set to about 0.5s (more like animation lock)

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

Fire1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, True, False, AddAstralFire1)
Fire2 = BLMAbility(1, True, 2.17, 2.17, 140, 200, True, False, ())
Fire3 = BLMAbility(2, True, 2.17, 2.17, 140, 200, True, False, AddAstralFire3)
Fire4 = BLMAbility(3, True, 2.17, 2.17, 140, 200, True, False, ())

Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True)
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True)
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True)
Blizzard1 = BLMAbility(0, True, 2.17, 2.17, 140, 200, False, True)

List = [Fire1,Fire1, Fire1]
BLm = BlackMage(2.17, List)

                        



        

            



    


