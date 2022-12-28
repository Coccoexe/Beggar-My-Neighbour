import itertools
import multiprocessing
import sys

def compute_match(p1,p2):
    player_1 = [j for i in p1 for j in i]
    player_2 = [j for i in p2 for j in i]
    
    table = []
    value = None
    to_play = 'p1'
    count = 0
    
    while len(player_1) > 0 and len(player_2) > 0:
        
        if count > 100000:
            print("Too many iterations")
            print(p1,p2)
            sys.exit()
        
        count += 1
        
        #play card
        current = player_1.pop(0) if to_play == 'p1' else player_2.pop(0)
        table.append(current)
        
        if current > 0:
            value = current
            to_play = 'p2' if to_play == 'p1' else 'p1'
        else:
            if value == None:
                to_play = 'p2' if to_play == 'p1' else 'p1'
                continue
            else:
                value -= 1
            
        if value == 0:
            if to_play == 'p1':
                player_2.extend(table)
                to_play = 'p2'
            else:
                player_1.extend(table)
                to_play = 'p1'
            table = []
    
    #f len(player_1) == 0:
    #    print('p2 Win, num of iterations:',count)
    #else:
    #    print('p1 Win, num of iterations:',count)

    return

def generate_cards(indexes,max_index,deck):
    if indexes[0] > max_index:
        return None
    
    cards = []
    for i in indexes:
        cards.append(deck[i])
    
    for i in range(len(indexes)-1,-1,-1):
        indexes[i] += 1
        if indexes[i] > max_index:
            indexes[i] = 0
        else:
            break
    
    return cards

def process(indexes,max_index,deck):
    count = indexes[0]
    while True:
        if count % 100000 == 0:
            print('Game', count)
        count += 1
        cards = generate_cards(indexes,indexes[0]+max_index,deck)
        if cards == None:
            break
        compute_match(cards[:2], cards[2:])
    return


if __name__ == '__main__':

    d = [1,0,0,0,0,0,0,2,3,4]

    #calulate all possible combinations of deck's order
    c = list(itertools.permutations(d))
    unq = list(set(c))
    ind = [
            [0,0,0,0],
            [len(unq)//12,len(unq)//12,len(unq)//12,len(unq)//12],
            [len(unq)//6,len(unq)//6,len(unq)//6,len(unq)//6],
            [len(unq)//4,len(unq)//4,len(unq)//4,len(unq)//4],
            [len(unq)//3,len(unq)//3,len(unq)//3,len(unq)//3],
            [len(unq)*5//12,len(unq)*5//12,len(unq)*5//12,len(unq)*5//12],
            [len(unq)//2,len(unq)//2,len(unq)//2,len(unq)//2],
            [len(unq)*7//12,len(unq)*7//12,len(unq)*7//12,len(unq)*7//12],
            [len(unq)*2//3,len(unq)*2//3,len(unq)*2//3,len(unq)*2//3],
            [len(unq)*3//4,len(unq)*3//4,len(unq)*3//4,len(unq)*3//4],
            [len(unq)*5//6,len(unq)*5//6,len(unq)*5//6,len(unq)*5//6],
            [len(unq)*11//12,len(unq)*11//12,len(unq)*11//12,len(unq)*11//12],
            ]
    max_ind = (len(unq)-1)//12

    jobs = []
    for i in range(len(ind)):
        thread = multiprocessing.Process(target=process, args=(ind[i],max_ind,unq))
        jobs.append(thread)

    for j in jobs:
        j.start()
        
    for j in jobs:
        j.join()
        
    print('Done')