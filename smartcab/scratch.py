states= ('up', 'down')
actions = ('left', 'right')
q= {(states[0], actions[0]) : 1, (states[1], actions[0]): 2 , (states[0], actions[1]) : 10, (states[1], actions[1]) : 4 }


def qmax(s):
        v= list()

        for k in actions:
            v.append(q.get((s, k), 0))

        return max(v) 

        #Compute the action based on the argmax_a' (Q(s',a'))
def qargmax(s):
        v= list()

        for k in actions:
            v.append(q.get((s, k), 0))

        return actions[v.index(max(v))]  

print qmax(states[0])
print qargmax(states[0])



