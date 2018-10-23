import numpy as np
from itertools import permutations

#read from file
field = np.loadtxt("towersudoku.txt",np.int8)
dim = np.size( field[0])-2

#found is used to store if a value on the field is already assigned or not
found =np.array( [ [ 0 for x in range(dim) ] for x in range(dim) ])

#stores the remaining possibilties
possible_columns = [ [] for x in range(dim) ]
possible_rows = [ [] for x in range(dim) ]



def getcolumn(n):
    return field[1:-1,n]
def getrow(n):
    return field[n,1:-1]
def gettowernumber_column(n):
    s = field[:,n]
    return (s[0],s[-1])
def gettowernumber_row(n):
    s = field[n,:]
    return (s[0],s[-1])

## k is the number of towers viewed from below, l from high
def towernumbers_col(n,upper=True,lower=True):
    j = 0;
    k = 0;
    p=0;
    l=0;

    if(upper):
        for i in range(dim):
            if (n[i] > j):
                k = k + 1
                j = n[i];
    if(lower):
        for i in range(dim):
            if(n[dim-i-1]>p):
                p = n[dim-i-1]
                l = l+1
    return (k,l);

#todo: maak dit beter
def generate_column(n):
    a = [x + 1 for x in range(dim)]
    goal = gettowernumber_column(n)
    upper = False if goal[0]==0 else True
    lower = False if goal[1] == 0 else True
    #print(goal)
    for perm in permutations(a):
        if(towernumbers_col(perm,upper,lower) == goal):
            possible_columns[n-1].append(list(perm))
    #print(possible_columns[n])
    return


#todo: maak dit beter
def generate_row(n):
    a = [x + 1 for x in range(dim)]
    goal = gettowernumber_row(n)
    upper = False if goal[0]==0 else True
    lower = False if goal[1] == 0 else True
    #print(goal)

    for perm in permutations(a):
        if(towernumbers_col(perm,upper,lower) == goal):
            possible_rows[n-1].append(list(perm))
    #print(possible_rows[n])
    return

def reduce_crossfield(n):
    change =True ;
    while change:
        change =False;
        for i in range(dim):
            if( np.sum(n[i,:])==1):
                change = True
                f = n[i,:]
                index = np.where(f==1)
                n[:,index]=0
                n[i,index]=2
        for i in range(dim):
            if( np.sum(n[:,i])==1):
                change = True
                index = np.where(n[:,i]==1)
                n[index,:]=0
                n[index,i]=2

    certain_fields = n//2
    uncertain_fields = n - (n//2)*2

    return certain_fields,uncertain_fields

#start of solving sudoku
print(field)


for i in range(dim):
    generate_column(i+1);

for i in range(dim):
    generate_row(i+1);

#it is not always possible to solve the tower sudoku from high to low -> several iterations are needed
iteration = 0

while np.sum( np.sum(  field[1:-1,1:-1] ) ) != dim*( dim*(dim+1)/2) :

    iteration = iteration +1;
    print("===============poging%d============="%iteration)

    #the tower sudoku is solved from highest number to the lowest
    #different order would require more passes
    for current_number in range(dim,0,-1):
        # the crossfield represents the possible places where the current number can go
        # the rows and colums are matched afterwards
        crossfield_column= np.array([ [ 0  for j in range(dim)] for i in range(dim) ])
        crossfield_row = np.array([ [ 0  for j in range(dim)] for i in range(dim) ])

        #indexation: first row,then column
        for i in range(dim):
            for j in range(dim):
                for lists in possible_columns[i]:
                    if(lists[j] == current_number):
                        crossfield_column[j][i]=1
                        break

        for j in range(dim):
            for i in range(dim):
                for lists in possible_rows[j]:
                    if(lists[i] == current_number):
                        crossfield_row[j][i]=1
                        break

        reduced,uncertain = reduce_crossfield(crossfield_row*crossfield_column)

        #the 1-found factor makes sure that a number is not added twice the next iteration
        field[1:-1,1:-1] += reduced*current_number*(1-found)
        found = found + reduced;


        print("%d ingevuld:"%current_number)
        print(field)

        #remove unused colums and rows
        for i in range(dim):
            index = np.where(reduced[:,i]+uncertain[:,i] == 1)[0]
            r=[]
            for j in index:
                #print(j)
                r = r+ [x for x in possible_columns[i] if x[j] == current_number]
            possible_columns[i] = r

        for i in range(dim):
            index = np.where(reduced[i,:]+uncertain[i,:] == 1)[0]
            r=[]
            for j in index:
                #print(j)
                r = r+ [x for x in possible_rows[i] if x[j] == current_number]
            possible_rows[i] = r


print("==================OPLOSSING:===================")

print(field)