#This class will represent a player with a job, etc.
#It will first be assumed to only be a BLM


#Black Mage

#Exceptions

class FailedToCast(Exception):
    pass



#EFFECT.PY


def AstralFire(Player, Spell):
    Stack = Player.AstralFireStack

    if (Spell.IsFire):
        if(Stack == 1): 
            if (Spell.id != 4) : Spell.ManaCost*=2#Update Mana cost
            Spell.Potency*=1.4#Update Damage
        elif(Stack == 2): 
            if (Spell.id != 4) : Spell.ManaCost*=2#Update Mana cost
            Spell.Potency*=1.6#Update Damage
        elif (Stack == 3): 
            if (Spell.id != 4) : Spell.ManaCost*=2#Update Mana cost
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
        Player.SharpCastStack = 0
        Player.EffectList.remove(SharpCastEffect)
        return T3ProckEffect
    elif(Spell.id == 0): #Fire 1
        Player.F3Prock == 1
        Player.SharpCastStack = 0
        Player.EffectList.remove(SharpCastEffect)
        return F3ProckEffect

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

def UmbralHeartEffect(Player, Spell):
    if(Player.UmbralHeartStack >= 1 and Spell.IsFire and Player.AstralFireStack >= 1):
        if(Spell.id != 5):
            Spell.ManaCost/=2
            Player.UmbralHeartStack-=1
    elif(Player.UmbralHeartStack <= 0):
        Player.UmbralHeartStack = 0
        Player.EffectList.remove(UmbralHeartEffect)


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

def AFUICheck(Player):

    if(Player.AFUITimer <= 0):
        Player.AstralFireStack = 0
        Player.UmbralIceStack = 0

def EnochianLostCheck(Player):

    if(Player.AstralFireStack == 0 and Player.UmbralIceStack == 0):
        Player.EffectList.remove(Enochian)
        Player.Enochian = False


#RequirementSpellCheck
#Checks requirement, and subtratcs whatever ressources was used
def ManaCheck(Player, Spell):
    if (Player.Mana >= Spell.ManaCost):
        print("taking mana : " + str(Player.Mana) + " : " +str(Spell.ManaCost))
        Player.Mana -= Spell.ManaCost
        print("mana taken: " + str(Player.Mana) + " : " +str(Spell.ManaCost))
        return True
    return False

def PolyglotCheck(Player, Spell):
    if (Player.PolyglotStack >=1):
        Player.PolyglotStack -= 1
        return True
    return False

def FireSpellCheck(Player, Spell):
    print("Hey brother")
    if (Player.AstralFireStack >= 1 and Player.Enochian and ManaCheck(Player, Spell)):
        return True
    return False

def IceSpellCheck(Player, Spell):
    if (Player.UmbralIceStack >= 1 and Player.Enochian and ManaCheck(Player, Spell)):
        return True
    return False

def LeyLinesCheck(Player, Spell):
    return Player.LeyLinesCD == 0

def TripleCastCheck(Player, Spell):
    return Player.TripleCastCD == 0

def SharpCastCheck(Player, Spell):
    return Player.SharpCastCD == 0

def SwiftCastCheck(Player, Spell):
    return Player.SwiftCastCD ==0

def EnochianCheck(Player, Spell):
    return (Player.EnochianCD == 0) and ((Player.AstralFireStack >= 1) or (Player.UmbralIceStack >= 1))

def ManaFrontCheck(Player, Spell):
    return (Player.ManaFrontCD == 0)

def TransposeCheck(Player, Spell):
    return (Player.TransposeCD == 0)


#ACTION.PY

class Ability:

    def __init__(self, id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, RequirementCheck):
        self.id = id #Id of spell
        self.GCD = GCD #True if is a GCD
        self.CastTime = CastTime #Castime of the spell
        self.Potency = Potency
        self.ManaCost = ManaCost
        self.RecastTime = RecastTime
        self.EffectOnCast = Effect
        self.RequirementCheck = RequirementCheck

    def __str__(self):
        return "Potency : " + str(self.Potency) + " CastTime : " + str(self.CastTime) + " RecastTime : " + str(self.RecastTime) + " ManaCost : " + str(self.ManaCost)

class BLMAbility(Ability):

    def __init__(self, id, GCD, CastTime,RecastTime, Potency, ManaCost, IsFire, IsIce, Effect, RequirementCheck):
        super().__init__(id, GCD, CastTime, RecastTime, Potency, ManaCost, Effect, RequirementCheck)
        self.IsFire = IsFire    #if fire spell
        self.IsIce = IsIce  #If ice spell

    def Cast(self, Player):
        tempSpell = BLMAbility(self.id, self.GCD, self.CastTime,self.RecastTime, self.Potency, self.ManaCost, self.IsFire, self.IsIce, self.EffectOnCast, self.RequirementCheck)

        newEffect = []

        for Effect in Player.EffectList:
            newEffect.append(Effect(Player, tempSpell))


        if(not (tempSpell.RequirementCheck(Player, tempSpell))):
            print("Does not meet requirement to cast the spell. Aborting")
            print("Was trying to cast : " + str(self.id))
            print("Mana : " + str(Player.Mana))
            print(tempSpell)
            raise FailedToCast("failed to cast spell")

        for effect in newEffect:
            if (effect != None):
                Player.EffectList.append(effect)


        #Check if has enough mana, and if yes update mana. If not enough mana, we end the program.

        tempSpell.EffectOnCast(Player)

        print(" Spell information : " + str(tempSpell))

        #Spell has now been updated with every effect
        #Add new effect to player


        return tempSpell




#PLAYER.PY



class player:

    def __init__(self, GCDTimer, ActionSet, EffectList,PrePullSet):
        self.GCDTimer = GCDTimer
        self.ActionSet = ActionSet  #List of actions to be performed in order
        self.EffectList = EffectList
        self.Casting = False
        self.oGCDLock = False
        self.GCDLock = False
        self.Mana = 10000
        self.EffectCDList = []
        self.DOTList = []
        self.PrePullSet = PrePullSet



class BlackMage(player):

    def __init__(self, GCDTimer, ActionSet, PrePullSet):
        super().__init__(GCDTimer, ActionSet, [AstralFire, UmbralIce], PrePullSet)
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
        self.TransposeCD = 0


    def getState(self):
        #this function returns the current state of the player
        return [self.AstralFireStack, self.UmbralIceStack, self.Enochian, self.PolyglotStack, self.AFUITimer, self.UmbralHeartStack, self.T3Prock, self.F3Prock, self.SharpCastStack, self.TripleCastStack
        , self.SwiftCastStack, self.T3Timer, self.F3Timer, self.LeyLinesTimer, self.LeyLinesCD, self.SharpCastCD, self.TripleCastCD, self.SwiftCastCD, self.EnochianCD, self.ManaFrontCD, self.TransposeCD
        ]
    def updateCD(self, time):
        if (self.LeyLinesCD > 0) : self.LeyLinesCD = max(0,self.LeyLinesCD - time)
        if (self.SharpCastCD > 0) :self.SharpCastCD = max(0,self.SharpCastCD - time)
        if (self.TripleCastCD > 0) :self.TripleCastCD = max(0,self.TripleCastCD - time)
        if (self.SwiftCastCD > 0) :self.SwiftCastCD = max(0,self.SwiftCastCD - time)
        if (self.EnochianCD > 0) :self.EnochianCD = max(0,self.EnochianCD - time)
        if (self.ManaFrontCD > 0) :self.ManaFrontCD = max(0,self.ManaFrontCD - time)
        if (self.TransposeCD > 0) :self.TransposeCD = max(0,self.TransposeCD - time)

    def updateTimer(self, time):
         if (self.LeyLinesTimer > 0) : self.LeyLinesTimer = max(0,self.LeyLinesTimer - time)
         if (self.T3Timer > 0) : self.T3Timer = max(0,self.T3Timer - time)
         if (self.AFUITimer > 0) : self.AFUITimer = max(0, self.AFUITimer-time)


        


    def PerformActionSetBlackMage(self, timeUnit, TimeLimit):
        ServerTick = 3
        NextServerTick = 3
        timer = 0
        spellCounter = 0
        TotalPotency = 0
        timeBeforeNextGCD = 0
        PolyglotStackCountDown = 0

        #PrePull Part

        for PrePullSpell in self.PrePullSet:
            #PrePullSpell Object will have at what time before the pull, and the spell itself
            #For now, it is assume PrePullSet has one oGCD and one GCD
            #print("bruh?")
            if (PrePullSpell[1].GCD):
                #last spell before we begin
                PrePullSpell[1].Cast(self)
                TotalPotency+= PrePullSpell[1].Potency
            else:
                #Spell is OGCD
                PrePullSpell[1].Cast(self)

                self.updateCD(PrePullSpell[0])
            #print("bruh?")

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
                    print("Mana Left : " + str(self.Mana))
                    print("CD =>  " + str(self.LeyLinesCD) + "  :  " + str(self.SharpCastCD) + "  :  "+ str(self.TripleCastCD)+ "  :  "+ str(self.SwiftCastCD)+ "  :  "+ str(self.EnochianCD)+ "  :  "+ str(self.ManaFrontCD)+ "  :  "+ str(self.TransposeCD))
                    tempSpell = nextSpell.Cast(self)
                    self.updateCD(tempSpell.CastTime)
                    self.updateTimer(tempSpell.CastTime)
                    NextServerTick -= tempSpell.CastTime
                    #print(str(tempSpell))

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
                print("Mana Left : " + str(self.Mana))
                print("CD =>  " + str(self.LeyLinesCD) + "  :  " + str(self.SharpCastCD) + "  :  "+ str(self.TripleCastCD)+ "  :  "+ str(self.SwiftCastCD)+ "  :  "+ str(self.EnochianCD)+ "  :  "+ str(self.ManaFrontCD)+ "  :  "+ str(self.TransposeCD))

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
                    #print(str(i) + "hhhhhhhh")
                    self.EffectCDList.remove(i)


            #Check ServerTick Mechanic
            if (NextServerTick <= 0):
                #Do thing
                NextServerTick = 3 - (timer %3)

                PolyglotStackCountDown+=1

                if (PolyglotStackCountDown == 10):
                    PolyglotStackCountDown = 0
                    self.PolyglotStack = 1

                if (self.UmbralIceStack == 1):
                    self.Mana = min(10000, self.Mana + 3200)
                elif (self.UmbralIceStack == 2):
                    self.Mana = min(10000, self.Mana + 4700)
                elif(self.UmbralIceStack == 3):
                    self.Mana = min(10000, self.Mana + 6200)

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
        Player.AFUITimer = 15
    elif (Player.AstralFireStack == 0 and Player.UmbralIceStack >=1):
        Player.AstralFireStack = 0
        Player.UmbralIceStack = 0

def AddAstralFire3(Player):
    Player.AstralFireStack = 3
    Player.UmbralIceStack = 0
    Player.AFUITimer = 15

def AddUmbralIce3(Player):
    Player.UmbralIceStack = 3
    Player.AstralFireStack = 0
    Player.AFUITimer = 15

def AddUmbralIce1(Player):
    print("bruh")

def AddUmbralHeartStack(Player):
    Player.UmbralHeartStack = 3
    Player.EffectList.append(UmbralHeartEffect)

def Enochian(Player):
    Player.Enochian = True
    Player.EnochianCD = 30
    Player.EffectList.append(EnochianEffect)
    Player.EffectCDList.append(EnochianLostCheck)

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
    Player.Mana += 3000
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

def DespairCast(Player):
    AddAstralFire3(Player)
    Player.Mana = 0



#Null Ability (wait)

Wait = BLMAbility(0, True, 5, 5, 0, 0, False, False, empty, ManaCheck)

#BLMSPELL
#Fire Spell
F1 = BLMAbility(1, True, 2.19, 2.19, 180, 800, True, False, AddAstralFire1, ManaCheck)
#F2 = BLMAbility(1, True, 2.17, 2.17, 140, 200, True, False, empty, ManaCheck)#Will not used, so whatever
F3 = BLMAbility(2, True, 3.07, 2.19, 240, 2000, True, False, AddAstralFire3, ManaCheck)
F4 = BLMAbility(3, True, 2.46, 2.19, 300, 800, True, False, empty, FireSpellCheck)
Despair = BLMAbility(4, True, 2.63, 2.19, 380, 800, True, False, DespairCast, FireSpellCheck)

#Ice Spell
B1 = BLMAbility(5, True, 2.19, 2.19, 180, 400, False, True, AddUmbralIce1, ManaCheck)#Not used so whatever
#B2 = BLMAbility(6, True, 2.17, 2.17, 140, 200, False, True, empty, ManaCheck)#AOE so not used
B3 = BLMAbility(6, True, 3.07, 2.19, 240, 800, False, True, AddUmbralIce3, ManaCheck)
B4 = BLMAbility(7, True, 2.46, 2.19, 300, 800, False, True, AddUmbralHeartStack, IceSpellCheck)

#DOT

T3 = BLMAbility(8, True, 2.19, 2.19, 40, 400, False, False, Thunder3, ManaCheck)
T3DOT = BLMAbility(9, False, 0, 0, 40, 0, False, False, empty, ManaCheck)
#Special Damage Spell

Xeno = BLMAbility(10, True, 0.3, 2.19, 750, 0, False, False, empty, PolyglotCheck)

#Boosting Ability

Eno = BLMAbility(11, False, 0.5, 0, 0, 0, False, False, Enochian, EnochianCheck)
Swift = BLMAbility(12, False, 0.5, 0, 0, 0, False, False, SwiftCast, SwiftCastCheck)
Triple = BLMAbility(13, False, 0.5, 0, 0, 0, False, False, TripleCast, TripleCastCheck)
Sharp = BLMAbility(14, False, 0.5, 0, 0, 0, False, False, SharpCast, SharpCastCheck)
Ley = BLMAbility(15, False, 0.5, 0, 0, 0, False, False, LeyLines, LeyLinesCheck)
Transpo = BLMAbility(16, False, 0, 0, 0, 0, False, False, Transpose, TransposeCheck)
Mana = BLMAbility(17, False, 0.5, 0, 0, 0, False, False, ManaFront, ManaFrontCheck)


SpellList = [F1,F3, F4, Despair,B1,B3,B4,T3, T3DOT, Xeno, Eno, Swift, Triple, Sharp, Ley, Transpo, Mana]

#ENDBLMSPELL

JpOpener = [Eno, T3, F4, Triple, F4, F4, Ley, F4, Swift, Despair, Mana,  F4, Despair]
PrePullJpOpener = [ [10, Sharp], [0, F3]]

NoB4Opener = [Eno, T3,  F3, Triple, F4, F4, Ley, F4, Swift, F4, F4, Despair, T3, Mana,  F4, Despair]
PrePullNoB4Opener = [ [10, Sharp], [0, B3]]

list = [T3, Sharp, T3, T3, F1, F1, F1]
Rotation = [B3, Sharp, B4, T3, F3, F4, F4, F4, F1, F4, F4, F4, Despair]

#print(JpOpener + Rotation)


BLM = BlackMage(2.19, NoB4Opener + Rotation, PrePullNoB4Opener)

#####

#print(BLM.PerformActionSetBlackMage(0.1, 100))


class Fight:

    #This class will represent an environment the NN will learn in

    def __init__(self, Player : player):

        self.TotalPotency = 0
        self.TotalTime = 0
        self.TimeLimit = -1
        self.Player = Player

    def step(self, Action, CurrentActionList):
        #This function will return the new state, give the reward (potency per second) and say weither the current try failed and is done
        #In such a case, potency per second will be set to 0
        #It will take an action to represent what the agent deided to do
        #Actions will be numbered from 0 to 18 and represent the Id of the spell it did

        global SpellList #Contains list of spells orderedby ID number
        self.Player.ActionSet += [SpellList[Action]]#Add spell to ActionSet
        #The program will always recompute the total potency per second with the new added spell (should be changed, but for now lets do it
        # like that cuz bruh)
        try:
            
            pastState = self.Player.getState()

            potencyPerSecond = self.Player.PerformActionSetBlackMage(0.01, self.TimeLimit)

            #Player will be updated by the PerformActionSetBlackMage function, and it will be considered to be the next state

            return self.Player.getState(), potencyPerSecond, False

        except FailedToCast:
            done = True
            return self.Player.getState(), 0, done
        
        








    

        



                        



        

            



    


