#!/usr/bin/python3

from constraint import *
import sys 
import numpy as np

class Student:
    def __init__(self, id, y, troub, mob, sibs):
        self.id=id
        self.year=y
        self.troub=troub
        self.rmob=mob
        self.sibs=sibs

#program takes as input a file with info about the students
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

def main():
    #Organize the distribution of students in the bus 
    # 
    # 
    # 
    problem=Problem()


if __name__ == "__main__":
    stds= read_info()
    print(stds[0].id)
    #main()
