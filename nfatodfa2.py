from graphviz import Digraph

class NFA:
    def __init__(self, no_state, states, no_alphabet, alphabets, start,
                 no_final, finals, no_transition, transitions):
        self.no_state = no_state
        self.states = states
        self.no_alphabet = no_alphabet
        self.alphabets = alphabets

        # Adding epsilon alphabet to the list
        # and incrementing the alphabet count
        self.alphabets.append('e')
        self.no_alphabet += 1
        self.start = start
        self.no_final = no_final
        self.finals = finals
        self.no_transition = no_transition
        self.transitions = transitions
        self.graph = Digraph()

        # Dictionaries to get index of states or alphabets
        self.states_dict = dict()
        for i in range(self.no_state):
            self.states_dict[self.states[i]] = i
        self.alphabets_dict = dict()
        for i in range(self.no_alphabet):
            self.alphabets_dict[self.alphabets[i]] = i

        # Transition table is of the form
        # [From State + Alphabet pair] -> [Set of To States]
        self.transition_table = dict()
        for i in range(self.no_state):
            for j in range(self.no_alphabet):
                self.transition_table[str(i) + str(j)] = []
        for i in range(self.no_transition):
            self.transition_table[str(self.states_dict[self.transitions[i][0]])
                                  + str(self.alphabets_dict[self.transitions[i][1]])].append(
                                      self.states_dict[self.transitions[i][2]])

    @classmethod
    def fromUser(cls):
        """Method to get input from User"""
        no_state = int(input("Number of States : "))
        states = list(input("States : ").split())
        no_alphabet = int(input("Number of Alphabets : "))
        alphabets = list(input("Alphabets : ").split())
        start = input("Start State : ")
        no_final = int(input("Number of Final States : "))
        finals = list(input("Final States : ").split())
        no_transition = int(input("Number of Transitions : "))
        transitions = []
        print("Enter Transitions (from alphabet to) (e for epsilon): ")
        for i in range(no_transition):
            transitions.append(input("-> ").split())
        return cls(no_state, states, no_alphabet, alphabets, start,
                   no_final, finals, no_transition, transitions)

    def __repr__(self):
        """Method to represent quintuple"""
        return "Q : " + str(self.states) + "\nΣ : " + str(self.alphabets) + \
               "\nq0 : " + str(self.start) + "\nF : " + str(self.finals) + \
               "\nδ : \n" + str(self.transition_table)

    def getEpsilonClosure(self, state):
        """Method to get Epsilon Closure of a state of NFA"""
        closure = dict()
        closure[self.states_dict[state]] = 0
        closure_stack = [self.states_dict[state]]

        while len(closure_stack) > 0:
            cur = closure_stack.pop(0)
            for x in self.transition_table[str(cur) + str(self.alphabets_dict['e'])]:
                if x not in closure.keys():
                    closure[x] = 0
                    closure_stack.append(x)
            closure[cur] = 1
        return closure.keys()

    def getStateName(self, state_list):
        """Get name from set of states to display in the final DFA diagram"""
        name = ''
        for x in state_list:
            name += self.states[x]
        return name

    def isFinalDFA(self, state_list):
        """Check if the set of states is a final state in DFA"""
        for x in state_list:
            for y in self.finals:
                if x == self.states_dict[y]:
                    return True
        return False


print("E-NFA to DFA")

# Example Input
nfa = NFA(
    4,  # Number of states
    ['A', 'B', 'C', 'D'],  # Array of states
    3,  # Number of alphabets
    ['a', 'b', 'c'],  # Array of alphabets
    'A',  # Start state
    1,  # Number of final states
    ['D'],  # Array of final states
    7,  # Number of transitions
    [['A', 'a', 'A'], ['A', 'e', 'B'], ['B', 'b', 'B'],
     ['A', 'e', 'C'], ['C', 'c', 'C'], ['B', 'b', 'D'],
     ['C', 'c', 'D']]  # Array of transitions
)

# Uncomment below line to get input from the user
# nfa = NFA.fromUser()

# Making NFA graph visualization
nfa.graph = Digraph()
for x in nfa.states:
    if x not in nfa.finals:
        nfa.graph.attr('node', shape='circle')
    else:
        nfa.graph.attr('node', shape='doublecircle')
    nfa.graph.node(x)

nfa.graph.attr('node', shape='none')
nfa.graph.node('')
nfa.graph.edge('', nfa.start)

for x in nfa.transitions:
    nfa.graph.edge(x[0], x[2], label=('ε', x[1])[x[1] != 'e'])

nfa.graph.render('nfa', view=True)

# DFA Construction
dfa = Digraph()
epsilon_closure = {x: list(nfa.getEpsilonClosure(x)) for x in nfa.states}

dfa_stack = [epsilon_closure[nfa.start]]
dfa_states = [epsilon_closure[nfa.start]]

if nfa.isFinalDFA(dfa_stack[0]):
    dfa.attr('node', shape='doublecircle')
else:
    dfa.attr('node', shape='circle')
dfa.node(nfa.getStateName(dfa_stack[0]))

dfa.attr('node', shape='none')
dfa.node('')
dfa.edge('', nfa.getStateName(dfa_stack[0]))

while len(dfa_stack) > 0:
    cur_state = dfa_stack.pop(0)
    for al in range(nfa.no_alphabet - 1):
        from_closure = set()
        for x in cur_state:
            from_closure.update(set(nfa.transition_table[str(x) + str(al)]))
        if len(from_closure) > 0:
            to_state = set()
            for x in list(from_closure):
                to_state.update(set(epsilon_closure[nfa.states[x]]))
            if list(to_state) not in dfa_states:
                dfa_stack.append(list(to_state))
                dfa_states.append(list(to_state))
                if nfa.isFinalDFA(list(to_state)):
                    dfa.attr('node', shape='doublecircle')
                else:
                    dfa.attr('node', shape='circle')
                dfa.node(nfa.getStateName(list(to_state)))
            dfa.edge(nfa.getStateName(cur_state),
                     nfa.getStateName(list(to_state)),
                     label=nfa.alphabets[al])
        else:
            if -1 not in dfa_states:
                dfa.attr('node', shape='circle')
                dfa.node('ϕ')
                for alpha in range(nfa.no_alphabet - 1):
                    dfa.edge('ϕ', 'ϕ', nfa.alphabets[alpha])
                dfa_states.append(-1)
            dfa.edge(nfa.getStateName(cur_state), 'ϕ', label=nfa.alphabets[al])

dfa.render('dfa', view=True)
