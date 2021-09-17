#This class will represent a player with a job, etc.
#It will first be assumed to only be a BLM
import Action.Ability

class player:

    def __init__(self, Job, GCDTimer, ActionSet):
        self.Job = Job,
        self.GCDTimer = GCDTimer
        self.ActionSet = ActionSet  #List of actions to be performed in order
        self.EffectList = []



class BlackMage(Player):

    def __init__(self, GCDTimer, ActionSet):
        super().__init__(GCDTimer, ActionSet)
        self.AstralFireStack = 0
        self.UmbralIceStack = 0
        self.Enochian = False
        self.T3Prock = False
        self.F3Prock = False
        self.PolyglotStack = 0
        self.TripleCastStack = 0
        self.SwiftCastStack = 0
        self.T3Timer = 0
        


    def PerformActionSetBlackMage(self):
        #This function will perform the given ActionSet and compute PPS for this given rotation/opener

        totalPotency = 0 #Keep track of the total potency done so far
        timer = 0 #Timer of the fight
        numberGCD = 0

        for Spell in self.ActionSet:
            #Spell here represents an Ability

            totalPotency += Spell.Potency

            if (Spell.GCD):#If the spell is a GCD

                if (Spell.CastTime < self.GCDTimer): timer+=self.GCDTimer#
                else: timer+= Spell.CastTime

            else:
                timer+=0.75


            #Will check for effect

            for Effect in self.EffectList:
                #Do each effect

            



    


