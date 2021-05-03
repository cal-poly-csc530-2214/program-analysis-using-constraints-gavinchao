from z3 import *

# prog must not have statements that span multiple lines
# lines are denoted by newline character '\n'
# returns a list of unknowns and constraints required to satisfy the unknowns
def find_constraints(prog):
   # unknowns/variables in the program
   unknowns = []

   # constraints in the program to solve for
   constraints = []

   # a list of repeated unknowns
   extras = []

   # split the program into each line of the program
   prog = prog.replace(';','')
   prog = prog.split('\n')
   
   print(prog)

   for line in prog:
      # assigning variables to an integer value
      if ':=' in line:
         line = line.split()
         eq = line.index(':=')       
         constraints.append(line[eq-1] + ' == ' + "".join(line[eq+1:]))
         if not line[eq-1] in unknowns:
            unknowns.append(line[eq-1])

      # used for arguments in function, but only works for one argument
      elif 'int' in line:
         line = line.replace('(', '')
         line = line.replace(')', '')
         line = line.split()
         int_t = line.index('int')
         constraints.append(line[int_t+1])
         if not line[int_t+1] in unknowns:
            unknowns.append(line[int_t+1])
      
      # assumes the line is in the form x++ (nothing else in the line)
      elif '++' in line:         
         line = line.split('++')
         if line[0] in unknowns:
            for ex in extras[::-1]:
               if line[0] in ex:
                  ex = ex.split('_')
                  extras.append(line[0]+'_'+str(int(ex[1]) + 1))
                  constraints.append(line[0]+'_'+str(int(ex[1]) + 1) + ' == ' + line[0]+'_'+ex[1] + ' + 1')
                  break
            else:
               extras.append(line[0]+'_1')
               constraints.append(line[0]+'_1 == ' + line[0]+ ' + 1')
      
      # assumes the line is in the form x++ (nothing else in the line)
      elif '--' in line:         
         line = line.split('--')
         if line[0] in unknowns:
            for ex in extras[::-1]:
               if line[0] in ex:
                  ex = ex.split('_')
                  extras.append(line[0]+'_'+str(int(ex[1]) + 1))
                  constraints.append(line[0]+'_'+str(int(ex[1]) + 1) + ' == ' + line[0]+'_'+ex[1] + ' - 1')
                  break
            else:
               extras.append(line[0]+'_1')
               constraints.append(line[0]+'_1 == ' + line[0]+ ' - 1')
      


      # the assert is something that needs to be a constraint to follow, so just add it to the list
      elif 'assert' in line:
         line = line.replace('(', " ").replace(')', " ")
         line = line.split('assert')
         constraint = line[1].strip()
         if ' = ' in constraint:
            constraint = constraint.replace('=', '==')
         constraints.append(constraint)
   
   # prints all for debugging
   print(unknowns)
   print(constraints)
   print(extras)

   return (unknowns, constraints, extras)

if __name__ == "__main__":
   find_constraints(
         "PV1 (int y) {\n" +
         'x := −50;\n' + 
         'while (x < 0) {\n' + 
               'x := x + y;\n' + 
               'y++;\n' +
         '}\n' +
         'assert(y > 0)\n'+
         '}')