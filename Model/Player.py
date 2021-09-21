#This class will represent a player with a job, etc.
#It will first be assumed to only be a BLM


#Black Mage

#EFFECT.PY

def AstralFire(Player, Spell):
    Stack = Player.AstralFireStack

    if (Spell.IsFire):
        if(Stack == 1): 
            Spell.ManaCost*=2#Update Mana cost
            Spell.Potency*=1.4#Update Damage
        elif(Stack == 2): 
            Spell.ManaCost*=2#Update Mana cost
            Spell.Potency*=1.6#Update Damage
        elif (Stack == 3): 
            Spell.ManaCost*=2#Update Mana cost
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

def LeyLinesEffect(Player, Spell):
    Spell.CastTime*=0.85
    Spell.RecastTime*=0.85

def EnochianEffect(Player, Spell):
    Spell.Potency*=1.15

def TripleCastEffect(Player,Spell):
    Spell.CastTime=0
    Player.TripleCastStack-=1

    if (Player.TripleCastStack == 0):
        Player.EffectList.remove(TripleCastEffect)

def SwiftCastEffect(Player, Spell):
    Spell.CastTime=0
    Player.EffectList.remove(SwiftCastEffect)

def SharpCastEffect(Player,Spell):

    if(Spell.id == 16):#Id 0 is T3
        Player.T3Prock = 1
        Player.EffectList.append(T3ProckEffect)
        Player.SharpCastStack = 0
        Player.EffectList.remove(SharpCastEffect)
    elif(Spell.id == 0): #Fire 1
        Player.F3Prock == 1
        Player.EffectList.append(F3ProckEffect)
        Player.SharpCastStack = 0
        Player.EffectList.remove(SharpCastEffect)

def T3ProckEffect(Player, Spell):

    if(Spell.id == 16):
        Spell.CastTime = 0
        Spell.Potency = 320
        Spell.ManaCost = 0
        Player.T3Prock = 0
        Player.EffectList.remove(T3ProckEffect)
        

def F3ProckEffect(Player, Spell):

    if (Spell.id == 2):
        Spell.CastTime = 0
        Spell.ManaCost = 0

#Function called to remove effect

def CheckLeyLines(Player):
    if(Player.LeyLinesTimer <= 0):
        Player.EffectList.remove(LeyLinesEffect)
        Player.LeyLinesTimer = 0
        return CheckLeyLines

def Thunder3DotCheck(Player):
    if(Player.T3Timer <= 0):
        Player.DOTList.remove(T3DOT)
        Player.T3Timer = 0
        return Thunder3DotCheck

#ACTION.PY

class Ability:

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect):
        self.id = id #Id of spell
        self.GCD = GCD #True if is a GCD
        self.CastTime = CastTime #Castime of the spell
        self.Potency = Potency
        self.ManaCost = ManaCost
        self.RecastTime = RecastTime
        self.Effect = Effect

    def __str__(self):
        return "Potency : " + str(self.Potency) + " CastTime : " + str(self.CastTime) + " RecastTime : " + str(self.RecastTime) + " ManaCost : " + str(self.ManaCost)

class BLMAbility(Ability):

    def __init__(self, id, GCD, CastTime,RecastTime, Potency, ManaCost, IsFire, IsIce, Effect):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect)
        self.IsFire = IsFire    #if fire spell
        self.IsIce = IsIce  #If ice spell

    def Cast(self, Player):
        tempSpell = BLMAbility(self.id, self.GCD, self.CastTime,self.RecastTime, self.Potency, self.ManaCost, self.IsFire, self.IsIce, self.Effect)
        
        print("Inside Cast : " + str(tempSpell))

        for Effect in Player.EffectList:
            Effect(Player, tempSpell)

        print("Inside Cast2 : " + str(tempSpell))

        #Spell has now been updated with every effect
        #Add new effect to player
        tempSpell.Effect(Player)


        return tempSpell




#PLAYER.PY



class player:

    def __init__(self, GCDTimer, ActionSet, EffectList):
        self.GCDTimer = GCDTimer
        self.ActionSet = ActionSet  #List of actions to be performed in order
        self.EffectList = EffectList
        self.Casting = False
        self.oGCDLock = False
        self.GCDLock = False
        self.Mana = 10000
        self.EffectCDList = []
        self.DOTList = []



class BlackMage(player):

    def __init__(self, GCDTimer, ActionSet):
        super().__init__(GCDTimer, ActionSet, [AstralFire, UmbralIce])
        #Special
        self.AstralFireStack = 0
        self.UmbralIceStack = 0
        self.Enochian = False
        self.PolyglotStack = 0
        self.AFUITimer = 0
        self.UmbralHeartStack = 0

        #Prock
        self.T3Prock = False
        self.F3Prock = False

        #Ability Effect
        self.SharpCastStack = 0
        self.TripleCastStack = 0
        self.SwiftCastStack = 0
        self.T3Timer = 0
        self.F3Timer = 0
        self.LeyLinesTimer = 0

        #Ability CD
        self.LeyLinesCD = 0
        self.SharpCastCD = 0
        self.TripleCastCD = 0
        self.SwiftCastCD = 0
        self.EnochianCD = 0
        self.ManaFrontCD = 0
        self.TranspodeCD = 0


    def updateCD(self, time):
        if (self.LeyLinesCD > 0) : self.LeyLinesCD = max(0,self.LeyLinesCD - time)
        if (self.SharpCastCD > 0) :self.SharpCastCD = max(0,self.SharpCastCD - time)
        if (self.TripleCastCD > 0) :self.TripleCastCD = max(0,self.TripleCastCD - time)
        if (self.SwiftCastCD > 0) :self.SwiftCastCD = max(0,self.SwiftCastCD - time)
        if (self.EnochianCD > 0) :self.EnochianCD = max(0,self.EnochianCD - time)
        if (self.ManaFrontCD > 0) :self.ManaFrontCD = max(0,self.ManaFrontCD - time)
        if (self.TranspodeCD > 0) :self.TranspodeCD = max(0,self.TranspodeCD - time)

    def updateTimer(self, time):
         if (self.LeyLinesTimer > 0) : self.LeyLinesTimer = max(0,self.LeyLinesTimer - time)
         if (self.T3Timer > 0) : self.T3Timer = max(0,self.T3Timer - time)


        


    def PerformActionSetBlackMage(self, timeUnit, TimeLimit):
        ServerTick = 3
        NextServerTick = 3
        timer = 0
        spellCounter = 0
        TotalPotency = 0
        timeBeforeNextGCD = 0
        while(timer < TimeLimit):


            nextSpell = self.ActionSet[spellCounter]

            if(nextSpell.GCD):
                #If spell is a GCD
                if(not self.GCDLock):
                    print("################################################################################################################################")
                    print("Next spell " + str(nextSpell.id))
                    print('Timer : ' + str(timer))
                    print("AstralFire " + str(self.AstralFireStack))
                    print("UmbralIce " + str(self.UmbralIceStack))
                    print("Effect list : " + str(self.EffectList))
                    print("DOT List : " + str(self.DOTList))
                    tempSpell = nextSpell.Cast(self)
                    self.updateCD(tempSpell.CastTime)
                    self.updateTimer(tempSpell.CastTime)
                    NextServerTick -= tempSpell.CastTime
                    print(str(tempSpell))

                    TotalPotency += tempSpell.Potency #Add potency of spell
                    timer+= tempSpell.CastTime #Fast forward to when next action is possible
                    spellCounter+=1#Upgrade spellCounter
                    
                    timeBeforeNextGCD = max(0, tempSpell.RecastTime - tempSpell.CastTime)
                    self.GCDLock = True #Cannot cast GCD

                    if (spellCounter >= len(self.ActionSet)) : 
                        #timer  = TimeLimit
                        break #If no more spell,we out



            else:
                print("################################################################################################################################")
                print("Next spell " + str(nextSpell.id))
                print('Timer : ' + str(timer))
                print("AstralFire " + str(self.AstralFireStack))
                print("UmbralIce " + str(self.UmbralIceStack))
                print("Effect list : " + str(self.EffectList))
                print("DOT List : " + str(self.DOTList))
                #spell is an oGCD
                tempSpell = nextSpell.Cast(self)
                TotalPotency += tempSpell.Potency
                timer += tempSpell.CastTime#For oGCD, set to about 0.5s (more like animation lock)
                self.updateCD(tempSpell.CastTime)
                self.updateTimer(tempSpell.CastTime)
                timeBeforeNextGCD = max(0, timeBeforeNextGCD - tempSpell.CastTime)
                NextServerTick -= tempSpell.CastTime
                if (spellCounter >= len(self.ActionSet)) : 
                    #timer  = TimeLimit
                    break #If no more spell,we out
                spellCounter+=1
                
            if (timeBeforeNextGCD <= 0):
                self.GCDLock = False
            else:
                timeBeforeNextGCD-=0.01

            if(self.GCDLock):
                timer+=0.01
                self.updateTimer(0.01)
                self.updateCD(0.01)
                NextServerTick -= 0.01

            rList = []
            for Check in self.EffectCDList:
                rList.append(Check(self))
            #print(rList)
            #print("LeyLines Timer : " + str(self.LeyLinesTimer))
            for i in rList:
                if (i != None):
                    print(str(i) + "hhhhhhhh")
                    self.EffectCDList.remove(i)


            #Check ServerTick Mechanic
            if (NextServerTick <= 0):
                #Do thing
                NextServerTick = 3 - (timer %3)

                if (self.UmbralIceStack == 1):
                    self.Mana +=3200
                elif (self.UmbralIceStack == 2):
                    self.Mana += 4700
                elif(self.UmbralIceStack == 3):
                    self.Mana += 6200

                for DOT in self.DOTList:
                    tempDOT = DOT.Cast(self)
                    TotalPotency += tempDOT.Potency
                    print("Applied DOT with a potency of : " + str(tempDOT.Potency))

        return TotalPotency/timer


#### MAIN

def empty(Player):
    pass

def AddAstralFire1(Player):

    if(Player.AstralFireStack >=0 and Player.AstralFireStack <3 and Player.UmbralIceStack == 0):
        Player.AstralFireStack+=1
    elif (Player.AstralFireStack == 0 and Player.UmbralIceStack >=1):
        Player.AstralFireStack = 0
        Player.UmbralIceStack = 0

def AddAstralFire3(Player):
    Player.AstralFireStack = 3
    Player.UmbralIceStack = 0

def AddUmbralIce3(Player):
    Player.UmbralIceStack = 3
    Player.AstralFireStack = 0

def AddUmbralIce1(Player):
    print("bruh")

def AddUmbralHeartStack(Player):
    Player.UmbralHeartStack = 3
    
def RemovePolyGlotStack(Player):
    Player.PolyglotStack-=1

def Enochian(Player):
    Player.Enochian = True
    Player.EnochianCD = 30
    Player.EffectList.append(EnochianEffect)

def SwiftCast(Player):
    Player.SwiftCastCD = 60
    Player.SwiftCasStack = 1
    Player.EffectList.append(SwiftCastEffect)

def TripleCast(Player):
    Player.TripleCastCD = 60
    Player.TripleCastStack = 3
    Player.EffectList.append(TripleCastEffect)

def LeyLines(Player):
    Player.LeyLinesCD = 90
    Player.LeyLinesTimer = 30
    Player.EffectList.append(LeyLinesEffect)
    Player.EffectCDList.append(CheckLeyLines)

def SharpCast(Player):
    Player.SharpCastCD = 30
    Player.SharpCastStack = 1
    Player.EffectList.append(SharpCastEffect)

def ManaFront(Player):
    Player.ManaFrontCD = 180
    #Add mana

def Transpose(Player):
    
    if(Player.UmbralIceStack >= 1):
        Player.UmbralIceStack = 0
        Player.AstralFireStack = 1
    elif(Player.AstralFireStack >= 1):
        Player.UmbralIceStack = 1
        Player.AstralFireStack = 0

def Thunder3(Player):
    if(not( T3DOT in Player.DOTList)) : Player.DOTList.append(T3DOT)
    Player.T3Timer = 24
    if(not( T3DOT in Player.EffectCDList)) : Player.EffectCDList.append(Thunder3DotCheck)



#Null Ability (wait)

Wait = BLMAbility(-1, True, 2.19, 2.19, 0, 0, False, False, empty)

#BLMSPELL
#Fire Spell
F1 = BLMAbility(0, True, 2.19, 2.19, 180, 800, True, False, AddAstralFire1)
F2 = BLMAbility(1, True, 2.17, 2.17, 140, 200, True, False, empty)#Will not used, so whatever
F3 = BLMAbility(2, True, 3.07, 2.19, 240, 2000, True, False, AddAstralFire3)
F4 = BLMAbility(3, True, 2.46, 2.19, 300, 800, True, False, empty)
Despair = BLMAbility(4, True, 2.63, 2.19, 380, -1, True, False, AddAstralFire3)

#Ice Spell
B1 = BLMAbility(5, True, 2.19, 2.19, 180, 400, False, True, AddUmbralIce1)#Not used so whatever
B2 = BLMAbility(6, True, 2.17, 2.17, 140, 200, False, True, empty)#AOE so not used
B3 = BLMAbility(7, True, 3.07, 2.19, 240, 800, False, True, AddUmbralIce3)
B4 = BLMAbility(8, True, 2.46, 2.19, 300, 800, False, True, AddUmbralHeartStack)

#DOT

T3 = BLMAbility(16, True, 2.19, 2.19, 40, 400, False, False, Thunder3)
T3DOT = BLMAbility(17, False, 0, 0, 40, 0, False, False, empty)
#Special Damage Spell

Xeno = BLMAbility(9, True, 0.3, 2.19, 750, 0, False, False, RemovePolyGlotStack)

#Boosting Ability

Eno = BLMAbility(10, False, 0.5, 0, 0, 0, False, False, Enochian)
Swift = BLMAbility(11, False, 0.5, 0, 0, 0, False, False, SwiftCast)
Triple = BLMAbility(12, False, 0.5, 0, 0, 0, False, False, TripleCast)
Sharp = BLMAbility(13, False, 0.5, 0, 0, 0, False, False, SharpCast)
Ley = BLMAbility(14, False, 0.5, 0, 0, 0, False, False, LeyLines)
Transpo = BLMAbility(15, False, 0, 0, 0, 0, False, False, Transpose)


#ENDBLMSPELL

JpOpener = [Sharp, F3, Eno, T3, F4, Triple, F4, F4, Ley, F4, Swift, Despair, F4, Despair, B3, B4]
NoB4Opener = [Sharp, B3, Eno, T3,  F3, Triple, F4, F4, Ley, F4, Swift, F4, F4, Despair, T3, Eno,  F4, Despair, B3, Xeno, B4]
list = [T3, Sharp, T3, T3, F1, F1, F1]
BLM = BlackMage(2.19, JpOpener)

#####

print(BLM.PerformActionSetBlackMage(0.1, 100))



                        



        

            



    


