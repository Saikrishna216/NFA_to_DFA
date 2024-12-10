import pandas as pd

class Node:
    def __init__(self, st, link=None):
        self.st = st
        self.link = link

class Node1:
    def __init__(self, nst=None):
        if nst is None:
            self.nst = [0] * 20
        else:
            self.nst = nst

def insert(r, c, s):
    j = findalpha(c)
    if j == 999:
        print("error")
        exit(0)
    temp = Node(s, transition[r][j])
    transition[r][j] = temp

def findalpha(c):
    try:
        return alphabet.index(c)
    except ValueError:
        return 999

def findfinalstate():
    final_states = []
    for i in range(complete + 1):
        for j in range(1, nostate + 1):
            for k in finalstate:
                if hash[i].nst[j] == k:
                    final_states.append(hash[i])
                    break
    return final_states

def insertdfastate(newstate):
    global complete
    for i in range(complete + 1):
        if compare(hash[i], newstate):
            return 0
    complete += 1
    hash[complete] = newstate
    return 1

def compare(a, b):
    for i in range(1, nostate + 1):
        if a.nst[i] != b.nst[i]:
            return 0
    return 1

def printnewstate(state):
    states = []
    for j in range(1, nostate + 1):
        if state.nst[j] != 0:
            states.append(f"q{state.nst[j]}")
    return "{" + ", ".join(states) + "}"


noalpha = int(input("Enter No of alphabets and alphabets?\n"))
alphabet = [input() for _ in range(noalpha)]
nostate = int(input("Enter the number of states?\n"))
start = int(input("Enter the start state?\n"))
nofinal = int(input("Enter the number of final states?\n"))
finalstate = [int(input("Enter the final states\n")) for _ in range(nofinal)]
notransition = int(input("Enter no of transition?\n"))
print("Enter the transitions in the format <state> <alphabet> <state>\n")

transition = [[None for _ in range(noalpha)] for _ in range(nostate + 1)]
hash = [Node1() for _ in range(20)]
complete = -1

for _ in range(notransition):
    r, c, s = input().split()
    insert(int(r), c, int(s))

newstate = Node1()
newstate.nst[start] = start 
insertdfastate(newstate)

i = -1
transition_data = []
while i != complete:
    i += 1
    newstate = hash[i]
    for k in range(noalpha):
        c = 0
        set = [0] * (nostate + 1)
        for j in range(1, nostate + 1):
            l = newstate.nst[j]
            if l != 0:
                temp = transition[l][k]
                while temp is not None:
                    if set[temp.st] == 0:
                        c += 1
                        set[temp.st] = temp.st
                    temp = temp.link
        if c != 0:
            tmpstate = Node1(set)
            insertdfastate(tmpstate)
            transition_data.append({'State': printnewstate(newstate), 'Alphabet': alphabet[k], 'Next State': printnewstate(tmpstate)})
        else:
            transition_data.append({'State': printnewstate(newstate), 'Alphabet': alphabet[k], 'Next State': 'NULL'})


#print start state
print("Start State: {q",start,"}")
# Printing final states
final_states = findfinalstate()
final_states_str = ", ".join(printnewstate(state) for state in final_states)
print("\nFinal states:", final_states_str)

df = pd.DataFrame(transition_data)

df_pivoted = df.pivot(index='State', columns='Alphabet', values='Next State')

# Fill NaN values with 'NULL'
df_pivoted.fillna('NULL', inplace=True)

print("\nTransition Table:")
print(df_pivoted[::-1])
