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
            t=lin[6]
            m=lin[9]
            s=lin[12]
            std = Student(id, y, t, m, s) 
            students.append(std)

    return students 

def main(stds):
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
        ...
         
    def sit_together(a, b):
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
        for j in range(0, len(studentsID)):
            if (stds[i].rmob == 'R'):
                problem.addConstraint(rmobseats, stds[i].id)
                problem.addConstraint(not_together, (stds[i].id, stds[j].id))

            if ((stds[i].troub=='C') and (stds[j].troub=='C')):
                problem.addConstraint(not_together, (stds[i].id , stds[j].id))

        if (stds[i].year=='1'):
            problem.addConstraint(first_block, stds[i].id)
        else:
            problem.addConstraint(second_block, stds[i].id)

    #for sol in problem.getSolutions():
    #    print(f"One solution is : {sol}")
    print(problem.getSolution())
    print(f"The number of solutions is {len(problem.getSolution())}")
    

if __name__ == "__main__":
    stds= read_info()    
    main(stds)