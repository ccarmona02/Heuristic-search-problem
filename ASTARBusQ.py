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
        self.eval=g+h

class State: #esto hay q rellenarlo. LO PUEDO HACER CON UN DICCIONARIO??
    def __init__(self, id, p) -> None:
        ... #CÓMO SE DEFINE UN STATE, HACER ESTA PREGUNTA. Decidir una estructura 
        #se puede hacer con vectores 

#---------------------------------------------------------------------------------------------

def read_info():
    students=[]
    with open(sys.argv[1], 'r') as my_file:
        lines = my_file.readlines()
        if (len(lines)>1):
            print("Incorrect format of the input file: It must contain only one line")
            sys.exit()

        info=lines[0]
        info = info [1:-2]  #eliminate first "{" and last "}"
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
    if((sys.argv[2]>2) or (sys.argv[2]<1)):
        print('We only have two heuristics available: 1 or 2')
        sys.exit() 

#---------------------------------------------------------------------------------------------

def main(stds, name, heur):
    #set the initial configuration (state) with the postitions of the bus, we have this info stored in stds
    init_state=create_state(stds)
    
    #FALTA POR METER LA LÓGICA 
    #AQUÍ VAMOS A HACER VARIOS LOOPS PARA ANALIZAR BFS (A*), LO PROBAMOS CON TODOS LOS ESTADOS POSIBLES Y VEMOS CUÁL ES EL MEJOR 
    result_state='nolose' #será el estado q menos coste tenga en la evaluation function 
    dict1=convert_to_dict(init_state, stds)
    dict2=convert_to_dict(result_state, stds) #convert resulting state to dict
    print_results(dict1, dict2, heur, name)
    #print_stats(name, heur, ttime, tcost, plen, pcost) WE HAVE TO MEASURE THESE THINGS

def create_state(students):
    ... #HACER ESTO, para poder hacerlo hay q tener claro la estructura del state y rellenarla

def create_node(state, h):
    h=calculate_heur(state, h)
    cost=calculate_cost(state) #cómo lo calculamos?
    return Node(state, cost, h)

def calculate_cost(g_state):
    ...

def calculate_heur(g_state, heur):
    if heur==1:
        ...
    if heur==2:
        ...

def BFSsearch(init_state, f_state, h): #this input parameters are nodes?
    #create a search graph G, with init_state?
    open= PriorityQueue() #EN QUÉ MOMENTO RELLENAMOS ESTO 
    #creamos un nodo que contenga ese initial state
    init_node=create_node(init_state, heur)
    open.put((0, init_node))
    closed=[] #dictionary or list? do we have to retain the cost associated? NS PREGUNTAR 
    while (not open.empty()):
        n=open.get()
        closed.append(n)
        if (n.state == f_state): return n #success. #would have to be 
       
        children=descendants(n) #expand n to get descendants HOW DO WE DO THIS ?? esto es importante 

        for c in children:
            if c in closed: continue #si ya está en closed pero con un valor mayor? tendríamos que sustituirlo?
            open.put(c.eval, c)

def descendants(n)->list: #en la lista estarán los nodos hijos
    ... #CÓMO SE HACE ESTO. ESTO ES IMPORTANTE Y NO TENGO NIDEA 
    #crear nodos con los estados descendientes 




def convert_to_dict(state, students):
    #we have the info of the state (Class State) and with the info stored in stds we have to construct a dictionary 
    result={}
    return result

def print_results(dict1, dict2, heur, name):
    out_file= name + "-" + heur + ".output"
    ofile=open(out_file, 'w')
    ofile.write(f'INITIAL: {dict1} \n') 
    ofile.write(f'FINAL: {dict2} \n') 
    ofile.close()

def print_stats(name, heur, t_time, t_cost, p_length, p_cost): #nidea de que son plan length y plan cost 
    out_file= name + "-" + heur + ".stat"
    ofile=open(out_file, 'w')
    ofile.write(f'Total time: {t_time} \n') 
    ofile.write(f'Total cost: {t_cost} \n') 
    ofile.write(f'Plan time: {p_length} \n') 
    ofile.write(f'Plan cost: {p_cost} \n') 
    ofile.close()

#------------------------------------------------------------------------------------------
#PROGRAM 
if __name__ == "__main__":
    stds, name_file= read_info()  
    checkformat() 
    heur= sys.argv[2]
    main(stds, name_file, heur)