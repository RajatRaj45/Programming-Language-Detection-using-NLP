
from collections import defaultdict
import os
import numpy as np
import pickle
class DFA:
    # def __init__(self):
    #     self.transitions = defaultdict(dict)
    #     self.final_states = set()
    #     self.dead_end = set()

    def __init__(self, s=None):
        self.transitions = defaultdict(dict)
        self.final_states = set()
        self.dead_end = set() 
        if s!=None:
            for i in range(len(s)):
                self.transitions[(i, s[i])] = i + 1
            self.final_states.add(len(s))
            self.dead_end.add(len(s))

    def DFA_id(self):
        for i in range(26):
            ch = chr(ord('a') + i)
            chc = chr(ord('A') + i)
            self.transitions[(0, ch)] = 1
            self.transitions[(0, chc)] = 1
            self.transitions[(1, chc)] = 1
            self.transitions[(1, ch)] = 1
        for i in range(10):
            ch = chr(ord('0') + i)
            self.transitions[(1, ch)] = 1
        self.transitions[(1, '_')] = 1
        self.final_states.add(1)

    def DFA_num(self):
        for i in range(1, 10):
            ch = chr(ord('0') + i)
            self.transitions[(0, ch)] = 1
        for i in range(10):
            ch = chr(ord('0') + i)
            self.transitions[(1, ch)] = 1
        self.transitions[(0, '0')] = 2
        self.final_states.add(1)
        self.final_states.add(2)

    def parse(self, s):
        # 0->DEAD, 1->MATCH, 2->MATCH&POTENTIAL, 3->POTENTIAL
        curr_state = 0
        for i in range(len(s)):
            if (curr_state, s[i]) not in self.transitions:
                return 0
            curr_state = self.transitions[(curr_state, s[i])]
        if curr_state in self.final_states:
            if curr_state in self.dead_end:
                return 1
            return 2
        return 3

def initialiseTokens():
    tokens = []
    s = [
        #C++ 
        "include", "bits/stdc++.h", "iostream", "using", "namespace", "std", "main", "cout", "cin", ">>", "<<", "push_back", "vector", "long long", ";", "scanf", "%d", "size", "ll",
        #python
        "def", "print", ":", "import", "from", "input()", "range", "in", "elif", "len", "enumerate", 
        #java
        "public static void main", "public void main", "System", "Scanner", "java", "util", "io", "String", "args",
        #sql
        "SELECT", "FROM", "WHERE", "INSERT", "UPDATE", "DELETE", "ALTER", "CREATE", "PRIMARY KEY", "FOREIGN KEY", "UNIQUE", "ORDER BY", "GROUP BY", "HAVING", "JOIN", "IN", "DISTINCT", "AS",
        #COMMON
        "(", ")", "{", "}", ".", "#", "->"
    ]
    for st in s:
        d = DFA(st)
        tokens.append(d)

    d1 = DFA()
    d1.DFA_num()
    tokens.append(d1)
    d2 = DFA()
    d2.DFA_id()
    tokens.append(d2)
    return tokens

def getFeatureVector(file_path):
    with open(file_path, "r") as filesrc:
        sourceCode = " ".join(line.strip() for line in filesrc)
    # print(sourceCode)
    srcCode = ""
    for i in range(len(sourceCode)):
        if sourceCode[i]==' ':
            if i!=0:
                if sourceCode[i-1]!=' ':
                    srcCode = srcCode + sourceCode[i]
        else:
            srcCode = srcCode + sourceCode[i]
    sourceCode = srcCode
    # print(sourceCode)
    tokens = initialiseTokens()
    prevMatchedToken = -1
    prevMatchedTokenIdx = -1
    curr = ""
    res = []
    i=0
    count_wrong=1
    while i<len(sourceCode):
        char=sourceCode[i]
        if 1==0:
            #does nothing
            piyosx=2
        else:
            curr += char
            pot = False
            match = False
            for d in range(len(tokens)):
                val = tokens[d].parse(curr)
                if val >= 2:
                    pot = True
                if (val == 1 or val == 2) and not match:
                    prevMatchedToken = d
                    prevMatchedTokenIdx = i
                    match = True
                    # print(f"MATCHED {curr} {d}")
            if not pot:
                if prevMatchedToken == -1:
                    curr = ""
                    i=prevMatchedTokenIdx+count_wrong
                    count_wrong+=1
                    continue
                count_wrong=1
                lexeme = curr[:len(curr)-i + prevMatchedTokenIdx]
                # print(f"TRYING TO PUSH {lexeme} FROM {curr}")
                tok = prevMatchedToken
                res.append((lexeme, tok))
                prevMatchedToken = -1
                curr = ""
                i = prevMatchedTokenIdx
        if i == len(sourceCode) - 1:
            if prevMatchedToken == -1:
                i=i+1
                continue
            count_wrong=1
            lexeme = curr[:len(curr)-i + prevMatchedTokenIdx]
            tok = prevMatchedToken
            res.append((lexeme, tok))
            prevMatchedToken = -1
            curr = ""
            i = prevMatchedTokenIdx
        
        i=i+1
    feature_vector = []
    Y = []#0->C++ 1->PYTHON 2->JAVA 3->SQL
    for i in range(len(tokens)):
        feature_vector.append(0)
    for p in res:
        # print(f"{p[0]} {p[1]}")
        feature_vector[p[1]]+=1
    return feature_vector



def get_words_in_directory(directory):
    feature_matrix = []
    Y=[]
    temp=0
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            curr_feature_vector = getFeatureVector(file_path)
            # print(curr_feature_vector)
            feature_matrix.append(curr_feature_vector)
            # print(len(feature_matrix))
            Y.append(temp)
        temp+=1
    return (feature_matrix, Y)



if __name__ == "__main__":

    (feature_matrix, Y)=get_words_in_directory("C:\\Users\\hp\\OneDrive\\Desktop\\VSCode\\compilerDesign\\CP2\\codesForTraining")
    # feature_matrix, Y=get_words_in_directory("")
    # print(len(feature_matrix))
    # print(len(feature_matrix[0]))
    # print(Y)
    X = np.array(feature_matrix)
    Y = np.array(Y)
    np.save('./X.npy', X)
    np.save('./Y.npy', Y)

