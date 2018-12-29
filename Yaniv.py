## ## YANIV ## ##
 
##Project started while recovering from a bike accident. 
#First time using classes and coding offline. 
#Slightly concussed so code a bit deranged in some places.

# Yaniv is an Israeli card game
# https://en.wikipedia.org/wiki/Yaniv_(card_game)
# In this version players yaniv under 7 and receive 5 starting cards.
# Players can set their own score threshold to play to. 

#There is an easy AI who I can beat 8 out of 10 games. 
#The AI can play running flushes and pairs and will try to ASSAF you.
#The AI will not pick up high cards to create running flushes. 
#AI will thumb cards


#Packages#
import random

#Variables#
Full_Deck = [
             'AH','2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH',
             'AD','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD',
             'AS','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS',
             'AC','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC',
             'XX','XX'
            ]
Discard_Deck = [
                 ]
Card_Values = {
                'A': 1,'2' : 2,'3' : 3,'4': 4,'5':5,'6':6,'7':7,'8':8,'9':9,'1':10,'J':11,'Q':12,'K':13, 'X':0
                }

#Classes#
class player():
    def __init__(self, Current_Hand, Score, Name, AI, Ynv):
            self.current_hand = Current_Hand
            self.score = Score
            self.name = Name
            self.AI = AI
            self.yaniv = Ynv
    #Used for scoring
    def calc_total_score(self):
            total = self.score
            if self.yaniv == 1:
                self.score = total
            else:
                for c in self.current_hand:
                    if c[1] == 'X':
                        total = total + 0
                    elif c[1] == '0':
                        total = total + 10
                    elif c[0] == 'A':
                        total = total + 1 
                    elif is_number(c[0]) is not True:
                        total = total + 10
                    else:
                        total = total + int(c[0])
                    self.score = total
    #Used by the AI to determine best move
    def calc_score(self):
            total = 0
            for c in self.current_hand:
                    if c[0] == 'X':
                        total = total + 0
                    elif c[1] == '0':
                        total = total + 10
                    elif c[0] == 'A':
                        total = total + 1 
                    elif is_number(c[0]) is not True:
                        total = total + 10
                    else:
                        total = total + int(c[0])
            return total
    def find_pairs(self):
        pairs = []
        for c,n in zip(self.current_hand,range(0,len(self.current_hand))):
            for b,m in zip(self.current_hand,range(0,len(self.current_hand))):
                 if c[0] == b[0] and n != m and Card_Values[c[0]] > 1:
                    ca = str(n+1)+str(m+1)
                    pairs.append(ca)
        return pairs
    
    def find_highcard(self):
        hcard = []
        nmr = 0
        for c in self.current_hand:
            hcard.append(Card_Values[c[0]])
        for h in hcard:
            if h == max(hcard):
                idx = nmr
            nmr = nmr + 1
        high_card = str(idx +1) 
        return high_card
        
    def find_rf(self):
        #to find a running flush we are going to nest three for loops
        rf = []
        for c1,n1 in zip(self.current_hand,range(0,len(self.current_hand))):
            first_value = Card_Values[c1[0]]
            first_suit = c1[1]
            for c2,n2 in zip(self.current_hand,range(0,len(self.current_hand))):
                second_value = Card_Values[c2[0]]
                second_suit = c2[1]
                #abs absolute value, great for differences
                if abs(second_value - first_value) == 1 and first_suit == second_suit:
                     for c3,n3 in zip(self.current_hand,range(0,len(self.current_hand))):
                         third_value = Card_Values[c3[0]]
                         third_suit = c3[1]
                         if abs(second_value - third_value) == 1 and third_value != first_value and third_suit == first_suit:
                             runflush = str(n1+1)+str(n2+1)+str(n3+1)
                             rf.append(runflush)
                             return rf
        return rf


#The ASCII Card Class is modified from Stack Overflow user 'Vader'
#https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards
class Card(object):
    card_values = {
        'A': 0,  # value of the ace is high until it needs to be low
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
        '8': 8,
        '9': 9,
        '1': 10,
        'J': 10,
        'Q': 10,
        'K': 10,
        'X':0
    }
    def __init__(self, suit, rank):
        """
        :param suit: The face of the card, e.g. Spade or Diamond
        :param rank: The value of the card, e.g 3 or King
        """
        self.suit = suit.capitalize()
        self.rank = rank
        self.points = self.card_values[rank]



#Functions#
def User_Input(f,s): 
    vld = False
    while vld == False:
        if s == 1:
            try:
                pn = int(input(f))
                if pn == 0:
                    raise Exception
            except:
                print('Invalid Choice')
            else:
                vld = True
        else:
            pn = str(input(f))
            if pn:
                vld = True
    return pn

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
  
#reshuffling function modified from jonrsharp
#https://codereview.stackexchange.com/questions/88684/shift-elements-left-by-n-indices-in-a-list     
def shift_left(lst, n):
    """Shifts the lst over by n indices

    >>> lst = [1, 2, 3, 4, 5]
    >>> shift_left(lst, 2)
    >>> lst
    [3, 4, 5, 1, 2]
    """
    #added numel term as original function shifts right instead of left 
    numel = len(lst)-1
    
    if n <0:
        raise ValueError('n must be a positive integer')
    #this is a cool example of recursion - the function references itself within the code
    if n > 0:
        lst.insert(numel, lst.pop(0))  # shift one place
        shift_left(lst, n-1)  # repeat    

def rule_check(Current_Hand,X):
   
    #player chooses one card
    valid = True
    
    X_played = False
    TX_played = False
    fix = []
    Tfix = []
    
    
    #check that no number has been typed twice 
    Xset = set(X)
    if len(X) != len(Xset):
        valid = False
        return valid
    
    #check that the card positions chosen are not greater than the hand size
    hand_size = len(Current_Hand)
    for i in X:
        truei = i+1
        if truei > hand_size:
            valid = False
            return valid
        
        #check that all the values in X are positive integers
        if truei - 1 < 0:
            valid = False
            return valid
    
    #player tries to play more than one card
    if len(X) > 1:
        valid = False
        idx = 0
        for i in X:
                #player tries to play a joker (we make it equal to one of the cards played next to it)
                if Current_Hand[i] == 'XX':
                    #player tries two jokers
                    if X_played == True:
                        TX_played = True
                        Tfix = idx
                        #the previous card was a joker
                        if fix == idx-1:
                            try:
                                Current_Hand[i] = Current_Hand[X[idx+1]]
                            except:
                                Current_Hand[i] = Current_Hand[X[idx-2]]
                        else:
                            Current_Hand[i] = Current_Hand[X[idx-1]]
                    else:
                        X_played = True
                        fix = idx
                    if idx == 0:
                        Current_Hand[i] = Current_Hand[X[idx+1]]
                    else:
                        Current_Hand[i] = Current_Hand[X[idx-1]]
                idx = idx + 1
                        
        #player tries to play a pair
        if len(X) == 2:
            if Current_Hand[X[0]][0] == Current_Hand[X[1]][0]:
                valid = True
        
        #player tries to play three of a kind
        elif len(X) == 3:
            if Current_Hand[X[0]][0] == Current_Hand[X[1]][0] == Current_Hand[X[2]][0]:
                valid = True
         
         #player tries to play four of a kind
        elif len(X) == 4:
            if Current_Hand[X[0]][0] == Current_Hand[X[1]][0] == Current_Hand[X[2]][0] == Current_Hand[X[3]][0]:
                valid = True   
                
        #player tries to play a running flush
        if valid == False:
            rf = []
            sts = []
            no_cards =len(X)
            
            for i in X:
                
                if Current_Hand[i][0] == '1':
                    sts.append(Current_Hand[i][2])
                else:
                    sts.append(Current_Hand[i][1])
                
                #print(Current_Hand) # For use in debugging
                
                #player tries to play a picture card
                if is_number(Current_Hand[i][0]) is not True:
                    if Current_Hand[i][0] == 'J':
                        rf.append(11)
                    if Current_Hand[i][0] == 'Q':
                        rf.append(12)
                    if Current_Hand[i][0] == 'K':
                        rf.append(13)
                    if Current_Hand[i][0] == 'A':
                        rf.append(1)
                
                else:
                    if int(Current_Hand[i][0]) == 1:
                        rf.append(10)
                    else:
                        rf.append(int(Current_Hand[i][0]))
                
            #check the running flash is valid using range comparison and that the player has only used one suit
            if X_played == False:
                if (max(rf)-min(rf)) == (no_cards-1) or max(rf) - min(rf) == 0:
                    if len(set(sts)) == 1:
                        valid = True
            
            #different validation rules exist if the player has used a joker
            elif X_played == True:
                ##if 2 Xs are played we Could have 7XX10 or 1X3X either is fine (although the second is pointless)
                if max(rf)-min(rf) == (no_cards-2) or max(rf)-min(rf) == (no_cards-1):
                    #print(sts) # for use in debugging
                    if len(set(sts)) == 1:
                        valid = True
            
        #reset the joker
        if X_played == True:
                Current_Hand[X[fix]] = 'XX'
        #reset the second joker
        if TX_played == True:
                 Current_Hand[X[Tfix]] = 'XX'
           
        return valid

def Card_Choice(plyr,Top_Card,Flip_Card,Current_Hand):
    
    X = []
    print('It\'s your turn', plyr.name)
    print('Top Card(s):')
    tc = []
    Flip = False
    Played_Card = []
    Player_Choice = ''
    
    #If the top card is a ten
    if Top_Card[0][1] == '0':
        tc.append(Card(Top_Card[0][2],Top_Card[0][0]))
    else:
        tc.append(Card(Top_Card[0][1],Top_Card[0][0]))
    #If there are two top cards
    if len (Top_Card) > 1: 
        if Top_Card[1][1] == '0':
            tc.append(Card(Top_Card[1][2],Top_Card[1][0]))
        else:
            tc.append(Card(Top_Card[1][1],Top_Card[1][0])) 
    
    #Show the players pick up options
    print(ascii_version_of_card(*tc))
    print('Discard')
    no = ['1: ','2: ','3: ','4: ','5: ']
    
    valid = False
    Yaniv = False
    tpc = []
    
    for i,n in zip(Current_Hand,no):
        #The player has a ten in hand
        if i[1] == '0':
            tpc.append(Card(i[2],i[0]))
        else:
            tpc.append(Card(i[1],i[0]))
    
    #Show the player discard options
    print(ascii_version_of_card(*tpc))
    
    #The player chooses a card
    while valid == False:
        
        #The player is an AI
        if plyr.AI:
            X = AI_choose_discard(plyr,Top_Card,Flip_Card,Current_Hand)
        else:
            X = User_Input(('Discard (1-'+str(len(Current_Hand))+'): '),0)
            ##Player accesses help 
            
            if X == 'Help' or X == 'help':
                print('\n''Input the position number of the card you want to discard.''\n'
                      'For multiple cards input the positions without spaces.''\n'
                      'E.g. 124: Will discard cards in the 1st,2nd and 4th position.''\n'
                      'XX cards are jokers''\n'
                      'Input Y to Yaniv and E to Exit.''\n''\n''Illegal Entries will print:')
            
            X=list(X)
        
            
        ##Player wants to end game 
        if X[0] == 'E' or X[0] == 'e':
            raise SystemExit
        
        #The player tries to Yaniv
        if X[0] == 'Y' or  X[0] == 'y':
            total = 0
            for c in Current_Hand:
                if c[1] == 'X':
                    total = total + 0
                elif c[1] == '0':
                    total = total + 10
                elif c[0] == 'A':
                    total = total + 1 
                elif is_number(c[0]) is not True:
                    total = total + 10
                else:
                    total = total + int(c[0])
            if total < 8:
                valid = True
                Yaniv = True
                return Flip_Card, Top_Card, Current_Hand, Yaniv, Player_Choice
        
        #The player chooses to discard cards
        else:
            try:
                X = [int(e)-1 for e in X]
            except:
                #the player has typed a letter instead of a number
                print('Invalid Choice')
                continue
            
            valid = rule_check(Current_Hand,X)
            
        #the player has chosen an illegal set of cards    
        if valid == False:
            print('Invalid Choice')
            
    #The player has chosen to play more than one card, determine the NTC 
    if len(X) > 1:
        
        for i in X:
            Played_Card.append(Card_Values[Current_Hand[i][0]])
            
        max_value = max(Played_Card)
        max_index = Played_Card.index(max_value)
        min_value = min(Played_Card)
        min_index = Played_Card.index(min_value)
        sec_min_index = Played_Card.index(sorted(Played_Card)[1])
        sec_min_value = sorted(Played_Card)[1]
        
        
        if len(X) > 2:
            tri_min_index = Played_Card.index(sorted(Played_Card)[2])
        
        #if the player has a pair
        if len(X) == 2:
            NTC = [Current_Hand[X[0]],Current_Hand[X[1]]]
        
        #if the player has a joker 
        elif min_value == 0 :
            #if the player has two jokers we assume they both go in the middle 
            if sec_min_value == 0:
                NTC = [Current_Hand[X[max_index]],Current_Hand[X[tri_min_index]]]
            #check whether the joker belongs in the middle
            elif max_value - sec_min_value == len(X) - 1:
                NTC = [Current_Hand[X[max_index]],Current_Hand[X[sec_min_index]]]
            else:
                NTC = [Current_Hand[X[max_index]],Current_Hand[X[min_index]]]
        #otherwise NTC is max and min 
        else:
            NTC = [Current_Hand[X[max_index]],Current_Hand[X[min_index]]]
    else:
        NTC = [Current_Hand[X[0]]]
    
    for c in X:
        Discard_Deck.append(Current_Hand[c])
    Current_Hand = [i for j,i in enumerate(Current_Hand) if j not in X]
    
    #The player chooses a card to pick up 
    print('Pick Up')
    vpu = False
    while vpu == False:
        vpu = True
        
    #There are multiple top cards for the player to choose between
        if len(Top_Card) > 1:
            print('1: ',Top_Card[0])
            print('2: ',Top_Card[1])
            print('3: ','Flip_Card')
            
            if plyr.AI:
                Y = AI_choose_pickup(plyr,Top_Card,Flip_Card,Current_Hand)
            else:
                Y = User_Input('Pick Up: ',1)
                
            if Y == 1:
                Current_Hand.append(Top_Card[0])
                Discard_Deck.remove(Top_Card[0])
                Player_Choice = Top_Card[0]
            elif Y == 2:
                Current_Hand.append(Top_Card[1])
                Discard_Deck.remove(Top_Card[1])
                Player_Choice = Top_Card[1]

            elif Y == 3:
                Current_Hand.append(Flip_Card[0])
                Current_Deck.remove(Flip_Card[0])
                Flip = True
                Player_Choice = 'Flip Card'
                
            else:
                #the player has typed an out of index number
                print('Invalid Choice')
                vpu = False
        
        #There is only one top card
        else:
            print('1: ',Top_Card[0])
            print('2: ','Flip_Card')
            if plyr.AI:
                Y = AI_choose_pickup(plyr,Top_Card,Flip_Card,Current_Hand)
            else:
                Y = User_Input('Pick Up ',1)
            if Y == 1:
                Current_Hand.append(Top_Card[0])
                Discard_Deck.remove(Top_Card[0])
                Player_Choice = Top_Card[0]

            elif Y == 2:
                Current_Hand.append(Flip_Card[0])
                Current_Deck.remove(Flip_Card[0])
                Flip = True
                Player_Choice = 'Flip Card'
                
            else:
                #the player has typed an out of index number
                print('Invalid Choice')
                vpu = False
        
        #Can the player 'thumb' the card?
        if Flip == True:
            if Flip_Card[0][0] == NTC[0][0]:
                print(Flip_Card,NTC[0])
                if plyr.AI:
                    thumb = 'Y'
                else:
                    thumb = User_Input('Thumb? (Y/N)',0)
                if thumb == 'Y' or thumb =='y':
                    Current_Hand.remove(Flip_Card[0])
                    Discard_Deck.append(Flip_Card[0])
                    NTC = [Flip_Card[0]]
                               
    Top_Card = NTC
    Flip_Card = random.sample(Current_Deck,1)
    
    return Flip_Card, Top_Card, Current_Hand, Yaniv, Player_Choice


def AI_choose_discard(plyr,Top_Card,Flip_Card,Current_Hand):
    sco = plyr.calc_score()
    pairs = plyr.find_pairs()
    rf = plyr.find_rf()
    if sco < 5:
        X = 'Y'
    elif rf:
        X = rf[0]
    elif pairs:
            X = pairs[0]
    else:
        X = plyr.find_highcard()
    print(X)
    return X

def AI_choose_pickup(plyr,Top_Card,Flip_Card,Current_Hand):
    ##First check whether or not the top card could be used to make a pair 
    for c in Current_Hand:
        if Top_Card[0][0] == c[0]:
            Y = 1
            return Y
        if len(Top_Card) > 1:
            if Top_Card[1][0] == c[0]:
                Y = 2
                return Y
    # if not choose the smallest card
    CV = Card_Values[Top_Card[0][0]]
    print(CV)
    if CV < 6:
        Y = 1
    else:
        Y = 2 
    #if there are multiple top cards choose the lowest
    if len(Top_Card) > 1:
        CV2 = Card_Values[Top_Card[1][0]]
        print(CV2)
        if CV2 < CV:
            CV = CV2
            if CV < 6:
                    Y = 2
            else:
                    Y = 3   
    return Y

##The ASCII Card functions are taken from StackOver Flow user 'Vader' and can be accessed here: 
#https://codereview.stackexchange.com/questions/82103/ascii-fication-of-playing-cards
#The comments below are Vaders
def ascii_version_of_card(*cards, return_string=True):
    """
    Instead of a boring text version of the card we render an ASCII image of the card.
    :param cards: One or more card objects
    :param return_string: By default we return the string version of the card, but the dealer hide the 1st card and we
    keep it as a list so that the dealer can add a hidden card in front of the list
    """
    # we will use this to prints the appropriate icons for each card
    suits_name = ['S', 'D', 'H', 'C','X']
    suits_symbols = ['♠', '♦', '♥', '♣','X']

    # create an empty list of list, each sublist is a line
    lines = [[] for i in range(9)]

    for index, card in enumerate(cards):
        # "King" should be "K" and "10" should still be "10"
        if card.rank == '1':  # ten is the only one who's rank is 2 char long
            rank = '10'
            space = ''  # if we write "10" on the card that line will be 1 char to long
        else:
            rank = card.rank[0]  # some have a rank of 'King' this changes that to a simple 'K' ("King" doesn't fit)
            space = ' '  # no "10", we use a blank space to will the void
        # get the cards suit in two steps
        suit = suits_name.index(card.suit)
        suit = suits_symbols[suit]

        # add the individual card on a line by line basis
        lines[0].append('┌─────────┐')
        lines[1].append('│{}{}       │'.format(rank, space))  # use two {} one for char, one for space or char
        lines[2].append('│         │')
        lines[3].append('│         │')
        lines[4].append('│    {}    │'.format(suit))
        lines[5].append('│         │')
        lines[6].append('│         │')
        lines[7].append('│       {}{}│'.format(space, rank))
        lines[8].append('└─────────┘')

    result = []
    for index, line in enumerate(lines):
        result.append(''.join(lines[index]))

    # hidden cards do not use string
    if return_string:
        return '\n'.join(result)
    else:
        return result


def ascii_version_of_hidden_card(*cards):
    """
    Essentially the dealers method of print ascii cards. This method hides the first card, shows it flipped over
    :param cards: A list of card objects, the first will be hidden
    :return: A string, the nice ascii version of cards
    """
    # a flipper over card. # This is a list of lists instead of a list of string becuase appending to a list is better then adding a string
    lines = [['┌─────────┐'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['│░░░░░░░░░│'], ['└─────────┘']]

    # store the non-flipped over card after the one that is flipped over
    cards_except_first = ascii_version_of_card(*cards[1:], return_string=False)
    for index, line in enumerate(cards_except_first):
        lines[index].append(line)

    # make each line into a single list
    for index, line in enumerate(lines):
        lines[index] = ''.join(line)

    # convert the list into a single string
    return '\n'.join(lines)


###########################################################################################
###############################{##Begin_________Yaniv##}###################################
###########################################################################################

#Main Script#
valid = False

while valid == False:
    pn = abs(User_Input('How many players (1-5)?   ',1))
    if pn < 6:
        valid = True
        
players = []
Current_Hand = []
for i in range(0,pn):
    nom = User_Input('Player name?  ',0)
    ia = User_Input('Are you a human? (Y/N)  ',0)
    if ia == 'Y' or ia == 'y':
        ia = 0
    else:
        ia = 1
    players.append(player(Current_Hand,0,nom,ia,0))
    

game_score = User_Input('What is the score threshold?   ',1)
        
game_end = False        
play = False

print('For help, when prompted to discard input \'help\'')

while play == False:
    
    while game_end == False:
       
        Yaniv = False
        
        #reset the deck (strange behaviour, requires Full_Deck variable to be restated inside while loop)
        Full_Deck = [
             'AH','2H','3H','4H','5H','6H','7H','8H','9H','10H','JH','QH','KH',
             'AD','2D','3D','4D','5D','6D','7D','8D','9D','10D','JD','QD','KD',
             'AS','2S','3S','4S','5S','6S','7S','8S','9S','10S','JS','QS','KS',
             'AC','2C','3C','4C','5C','6C','7C','8C','9C','10C','JC','QC','KC',
             'XX','XX'
            ]
        Current_Deck = Full_Deck
       
        
        #Deal out cards
        for p in players:
            p.yaniv = 0
            p.current_hand = []
            p.current_hand = random.sample(Current_Deck,5)
            for c in p.current_hand:
                Current_Deck.remove(c)
           
            
        #Flip over top card
        Top_Card = random.sample(Current_Deck,1)
        #The top card is of low value (optional house rule)
        if Card_Values[Top_Card[0][0]] < 3:
            print('Next round you should remember Gentleman\'s Rules, and Leave the Top Card Alone')
            
        Current_Deck.remove(Top_Card[0])
        Discard_Deck.append(Top_Card[0])
        Flip_Card = random.sample(Current_Deck,1)
        
        input("New round, Press Enter to continue...")
        scores = []   
        Update_String = []

        while Yaniv == False:
            
            ldex = 0 
            
            for p in players:
                
                other_player = p.name
                
                #Does the deck need reshuffling?
                if len(Current_Deck) < 3:
                    Current_Deck.extend(Discard_Deck)
                    Discard_Deck = []
                    Top_Card = random.sample(Current_Deck,1)
                    Current_Deck.remove(Top_Card[0])
                    Discard_Deck.append(Top_Card[0])
                
                #Player discards and picks up
                print('\n' * 50)
                #print the last players move
                print(' '.join(Update_String))
                
                print(p.name,' it is your turn!')
                
                #print other players hand size
                for op in players:
                    if op.name != other_player:
                        print(op.name,' has a hand of ',len(op.current_hand),' cards')
                        
                        
                input("Press Enter to continue...")
                print('\n' * 50)
                
                Flip_Card, Top_Card, p.current_hand, Yaniv, Player_Choice = Card_Choice(p,Top_Card,Flip_Card,p.current_hand)
                Update_String = [p.name,'picked up',Player_Choice]
                
                #Did player Yaniv?
                if Yaniv == True:
                    print(p.name,' has yanived!')
                    p.yaniv = 1
                    #move the yaniv player to first player and rework list
                    shift_left(players, ldex)
                    break
                
                ldex = ldex + 1 
                
        #check for assaf
        for p in players:
            scores.append(p.calc_score())
            ixd =+ 1
            if p.yaniv == 1:
                idx = ixd
        #retrieve the yaniv score
        ys = scores[idx-1]
        ##retrieve the minimum score
        minscore = min(float(s) for s in scores)
        
        #check there is only one person with that score
        indices_check = [i for i, x in enumerate(scores) if x == minscore]
        if len(indices_check) > 1:
            uniyaniv = False
        else:
            uniyaniv = True
        
        ##are they the same?
        if ys == minscore and uniyaniv == True:
            pass
        else:
        #punish assafed player
            for p in players:
                if p.yaniv == 1:
                    p.score = p.score + 30
                    p.yaniv = 0 
                    print(p.name, ' has been assafed!')
        
        #calculate total score
        for p in players:
            p.calc_total_score()
            if p.score % 50 == 0:
                if p.score is not 0:
                     p.score = p.score - 50
                     print(p.name, 'you hit a multiple of 50, lucky you')
            print(p.name,' your score is ',p.score)
            if p.score > game_score:
                    game_end = True
            
    
    print('Score threshold exceeded, therefore Game over')
    
    #reset the player score
    
           
    #user chooses whether to play again
    plag = User_Input('Play again? (Y/N)'  ,0)
    if plag == 'N' or plag == 'n':
        play = True
    else:
        game_end = False
        for p in players:
            p.score = 0
  

print('exiting...')

