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
    if((int(sys.argv[2])>2) or (int(sys.argv[2])<1)):
        print('We only have two heuristics available: 1 or 2')
        sys.exit() 


def create_init_dict(students): #ESTO HAY QUE CREARLO CON EL FORMATO CORRECTO 
    dict={}
    positions=[]
    for std in students:
        positions.append(std.pos)
    
    positions.sort()
    count=1
    for i in range(len(positions)):
        for j in range(len(students)):
            if(students[j].pos==positions[i]): 
                key=students[j].id + students[j].troub + students[j].rmob
                dict[key]=count
        count=count+1

    return dict

#---------------------------------------------------------------------------------------------
#Main program and A* search

def main(stds, name, heur):
    #set the initial configuration (state) with the postitions of the bus, we have this info stored in stds
    init_state=[]
    init_node=create_node(init_state, heur, stds)
    result_node= Astar_search(init_node, heur)
     
    dict1=create_init_dict(stds)
    dict2=convert_to_dict(result_node.state, stds) 
    print_results(dict1, dict2, heur, name)
    #print_stats(name, heur, ttime, tcost, plen, pcost) WE HAVE TO MEASURE THESE THINGS


def Astar_search(init_node, h): 
    open= PriorityQueue()  
    open.put((0, init_node))
    closed=[]  
    Exit=False
    while (not open.empty()) or Exit==False:
        elem=open.get()
        print(elem)
        n=elem[1]
        if n in closed: continue
        if (len(n.state) == len(stds)): #es un estado meta. Todos los alumnos asignados  
            Exit=True #success. #exit the search algorithm 
       
        children=descendants(n, h) #expand n to get descendants 
        closed.append(n)
        for c in children:
            open.put((c.eval, c))#c.state))

        if (Exit==True):
            #Solution= path from N to I through pointers, not necessary, ours final state will be a path 
            return n

def create_node(state, h, stds):
    h=calculate_heur(state, h, stds)
    cost=calculate_cost(state, stds) 
    return Node(state, cost, h)

def descendants(n, h): #en la lista estarán los nodos hijos
    descendants=[]
    state=n.state

    for i in range(len(stds)):
        if stds[i].id not in state:
            auxlist=state
            add_to_q(auxlist ,stds[i].id) #this represents the operator 
            nde=create_node(auxlist, h, stds)
            descendants.append(nde)

    return descendants

def add_to_q(q, person): #this is the operator, add a person to the end of the line 
    q.append(person)


def calculate_cost(state, stds): #state is a list, EN EL REPORT HAY QUE EXPLICAR LA INTERPRETACIÓN QUE HACEMOS DEL COSTE 
    count=1
    g_dict={}
    for i in range(len(state)):
        g_dict[state[i]]=count
        count=count+1

    times=[]

    for i in range(len(g_dict)):
        times.append(1)

    for i in g_dict: #iterate through the keys of the dictionary
        student_obj=search_info(i, stds)
        ind=int(i)-1
        excpt=False

        if (student_obj.rmob=='R'):
            times[ind]=times[ind]*3
            if (g_dict[i]==len(g_dict)): #last position
                time=float('inf') #return infinity because is not possible 
                return time
            else:
                for j in g_dict: 
                    if(g_dict[j]==g_dict[i]+1): 
                        student2_obj=search_info(j, stds)
                        if(student2_obj.rmob=='R'):
                            time=float('inf') #not possible if behind a student with reduced mobility there´s another one with the same condition 
                            return time
                        break
                continue

        if(student_obj.troub=='C'): 
            if (g_dict[i]!=len(g_dict)) and (g_dict[i]!=1):        
                times[ind-1]=times[ind-1]*2
                times[ind+1]=times[ind+1]*2
            elif((g_dict[i]==len(g_dict))):
                times[ind-1]=times[ind-1]*2
            else:
                times[ind+1]=times[ind+1]*2

        if(student_obj.troub=='C'): 
            for j in g_dict:
                student2_obj=search_info(j, stds)
                if (g_dict[j]>g_dict[i]) and (student_obj.pos<student2_obj.pos):
                    times[ind]=times[ind]*2

        for j in g_dict:
            if(g_dict[j]==g_dict[i]-1):
                student2_obj=search_info(j, stds) 
                if (student_obj.rmob=='R'): #if this person is behind a reduced mobility student 
                    excpt=True
        
                break

        if excpt: 
            times[ind]=0
            continue


    sum=0
    for i in range(len(times)):
        sum=sum+times[i]
    return sum #final cost 


def calculate_heur(g_state, heur, stds):
    if heur=='1': #cuanto queda para que todos los alumnos estén adjudicados 
        value=len(stds)-len(g_state)
    if heur=='2':
        ...
    return value

#---------------------------------------------------------------------------------------------------------------------------
#Auxiliar functions 
def search_info(id, stds):
    for i in range(len(stds)):
        if (stds[i].id==id): 
            break 
    return stds[i]

def convert_to_dict(state, stds): #convert the list state to a dictionary of the wanted type, use the function search_info
    count=1
    dict={}
    for i in range(len(state)):
        for j in range(len(stds)):
            if (state[i]==stds[j].id):
                student_obj=search_info(state[i], stds)
                break
        key=state[i] + student_obj.troub + student_obj.rmob
        dict[key]=count
        count=count+1

    return dict

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
    """
    sta=[]
    init_node=create_node(sta, '1', stds)
    open= PriorityQueue()  
    open.put((0, init_node))
    n=open.get()
    print(n[1])
    """
    main(stds, name_file, heur)