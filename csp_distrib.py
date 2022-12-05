#!/usr/bin/python3

from constraint import *
import sys 

class Student:
    def __init__(self, id, y, troub, mob, sibs):
        self.id=id
        self.year=y
        self.troub=troub
        self.rmob=mob
        self.sibs=sibs

#program takes as input a file with info about the students
#store information of each 
def read_info():
    students=[]
    with open(sys.argv[1], 'r') as my_file:
        lines = my_file.readlines()
        for i in range (0, len(lines)):
            lin= lines[i]
            lin.split()
            id=lin[0]
            y=lin[3]
            if (y==' '):
                id= lin[0]+lin[1]
                y=lin[4]
                t=lin[7]
                m=lin[10]
                s=lin[13]
                if(len(lin)>15):
                    s=lin[13]+lin[14]
            else:
                t=lin[6]
                m=lin[9]
                s=lin[12]
                if(len(lin)>14):
                   s=lin[12]+lin[13]
            if (int(id)>32):
                print('The total capacity of the bus is exceeded, we will take the first 32 students')
                break

            std = Student(id, y, t, m, s) 
            students.append(std)
           
    return students,  my_file.name

def convert_format(sol):
    correct_format={}
    for i in range(0, len(stds)):
        key=stds[i].id + stds[i].troub + stds[i].rmob
        correct_format[key]= sol[stds[i].id]

    return correct_format

def main(stds, out):
    #Organize the distribution of students in the bus 
    
    problem=Problem()
    domain = range(32)
    studentsID=[]
    for i in range (0, len(stds)):
        studentsID.append(stds[i].id)
  
    problem.addVariables(studentsID, domain)

    #functions for the constraints
    problem.addConstraint(AllDifferentConstraint()) #one and only seat assigned to each student 
    
    def rmobseats (a):
        specific_seats = [1, 2, 3, 4, 13, 14, 15, 16, 17, 18, 19, 20]
        if a in specific_seats:
            return True

    def not_together(a, b):
        if((a%2)==0):
            if (b != a-1):
                return True
        else:
            if (b != a+1):
                return True 

    def not_close(a, b):
        close_area=[] #we defined the concept of close
        if ((a%4)==2): #left of the bus next the aisle 
            close_area.append(a-1)
            close_area.append(a+1)
            close_area.append(a+3)
            close_area.append(a-3)
            close_area.append(a+4)
            close_area.append(a-4)
            close_area.append(a-5)
            close_area.append(a+5)
        elif ((a%4)==0): #window in right part of the bus 
            close_area.append(a-1)
            close_area.append(a-4)
            close_area.append(a+4)
            close_area.append(a+3)
            close_area.append(a-5)
        elif (((a+1)%4)==2):
            close_area.append(a+1)
            close_area.append(a-1)
            close_area.append(a+3)
            close_area.append(a-3)
            close_area.append(a+4)
            close_area.append(a-4)
            close_area.append(a+5)
            close_area.append(a-5)
        else:
            close_area.append(a+1)
            close_area.append(a-3)
            close_area.append(a-4)
            close_area.append(a+4)
            close_area.append(a+5)

        if b not in close_area:
            return True

    def sit_together(a, b): #a sits next to the aisle.
        if((a%2)==0):
            if (b == a-1):
                return True
        else:
            if (b == a+1):
                return True

    def first_block(a):
        if (a<17):
            return True 

    def second_block(b):
        if (b>16):
            return True 

    #establish constraints
    for i in range(0, len(studentsID)):
        excpt=False
        for j in range(0, len(studentsID)):
            if (stds[i].sibs == stds[j].id):
                if (stds[i].year=='2')and(stds[j].year=='1'):
                    excpt=True

                if (stds[i].rmob == 'R') and (stds[j].rmob == 'X'):
                    problem.addConstraint(rmobseats, stds[i].id)
                    problem.addConstraint(not_together, (stds[i].id, stds[j].id))
                elif(stds[i].rmob == 'X') and (stds[j].rmob == 'R'):
                    problem.addConstraint(rmobseats, stds[j].id)
                    problem.addConstraint(not_together, (stds[i].id, stds[j].id))
                elif(stds[i].rmob == 'R') and (stds[j].rmob == 'R'):
                    problem.addConstraint(rmobseats, stds[j].id)
                    problem.addConstraint(rmobseats, stds[i].id)
                    problem.addConstraint(not_together, (stds[i].id, stds[j].id))
                else:
                    if(((stds[i].year=='1') and (stds[j].year=='1'))or((stds[i].year=='2') and (stds[j].year=='2')) or ((stds[i].year=='2') and (stds[j].year=='1'))):
                        problem.addConstraint(sit_together, (stds[i].id, stds[j].id))
                    else:
                        problem.addConstraint(sit_together, (stds[j].id, stds[i].id))

            else:
                if (stds[i].rmob == 'R'):
                    problem.addConstraint(rmobseats, stds[i].id)
                    problem.addConstraint(not_together, (stds[i].id, stds[j].id))
                    if (stds[j].troub=='C'):
                        problem.addConstraint(not_close, (stds[i].id, stds[j].id))

                if ((stds[i].troub=='C') and (stds[j].troub=='C')):
                    problem.addConstraint(not_close, (stds[i].id , stds[j].id))

        if not excpt:
            if (stds[i].year=='1'):
                problem.addConstraint(first_block, stds[i].id)
            else:
                problem.addConstraint(second_block, stds[i].id)
        else:
            problem.addConstraint(first_block, stds[i].id)


    out_file= out + ".output"
    ofile=open(out_file, 'w')
    ofile.write(f'Number of solutions: {len(problem.getSolutions())} \n') 
    count=1
    for i in problem.getSolutions(): 
        new=convert_format(i)
        ofile.write(f'Sol {count} is: {new} \n')
        if(count>4):
            break
        count = count+1
    ofile.close()
    

if __name__ == "__main__":
    stds, name_file= read_info()    
    main(stds, name_file)