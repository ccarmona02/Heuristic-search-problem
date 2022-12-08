import sys


class Student:
    def __init__(self, id, troub, mob, pos):
        self.id=id
        self.troub=troub
        self.rmob=mob
        self.pos=pos


def read_info():
    students=[]
    with open(sys.argv[1], 'r') as my_file:
        info = my_file.read
        info = info [1:-1]        #eliminate first "{" and last "}"
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
