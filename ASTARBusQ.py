#!/usr/bin/python3
import sys
from queue import PriorityQueue

class Student:
    def __init__(self, id, troub, mob, pos):
        self.id=id
        self.troub=troub
        self.rmob=mob
        self.pos=pos

class Node:
    def __init__(self, ste, g, h):
        self.state=ste
        self.gcost=g
        self.hcost=h

class State: #esto hay q rellenarlo 
    def __init__(self, id, p) -> None:
        ... #CÓMO SE DEFINE UN STATE, HACER ESTA PREGUNTA 


def read_info():
    students=[]
    with open(sys.argv[1], 'r') as my_file:
        lines = my_file.readlines()
        info=lines[0]
        info = info [1:-2]        #eliminate first "{" and last "}"
        splitted = info.split(", ")
        for i in range (0, len(splitted)):
            info_student= splitted[i]
            id=info_student[1]
            t=info_student[2]
            m=info_student[3]
            pos=info_student[7:]
            std = Student(id, t, m, pos) 
            students.append(std)
           
    return students,  my_file.name

def checkformat():
    if (len(sys.argv)<3):
        print('Incorrect format: Try again')
        print('ASTARBusQ.py  <path students>  <heuristic>')
        sys.exit()

def main(stds, name, heur):
    ...

def BFSsearch(init_state, f_state):
    open= PriorityQueue() #this will be a vector<state>open. EN QUÉ MOMENTO RELLENAMOS ESTO 
    open.put(init_state)
    closed=[] #something of the type 
    sucess=False
    while (not open.empty()) or (sucess==True):
        n=open.get()
        if (n == f_state): 
            ...





if __name__ == "__main__":
    stds, name_file= read_info()  
    checkformat() 
    heur= sys.argv[2]
    main(stds, name_file, heur)