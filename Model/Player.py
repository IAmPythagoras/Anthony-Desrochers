#This class will represent a player with a job, etc.
#It will first be assumed to only be a BLM
import Action

class player:

    def __init__(self, Job, GCDTimer, ActionSet):
        self.Job = Job,
        self.GCDTimer = GCDTimer
        self.ActionSet = ActionSet  #List of actions to be performed in order
        self.EffectList = []
        self.Casting = False
        self.oGCDLock = False



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

        while(timer < TimeLimit):

            nextSpell = self.ActionSet[spellCounter]

            if(not self.Casting):
                #Will have to check if next spell if oGCD or GCD
                if(not self.oGCDLock):
                    #If not locked by oGCD
                    #Then just have to check if we are in between two GCD
                    if(nextSpell.GCD):
                        #If spell is a GCD
                    else:
                        #spell is an oGCD
                        



        

            



    


