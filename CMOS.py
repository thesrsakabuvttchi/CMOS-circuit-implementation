import re
import sys



Port = 0
Circ = []



class Gate:
    def __init__(self,typ,inp,top,bottom):
        self.typ = typ
        self.inp = inp
        self.top = top
        self.bottom = bottom
        self.par1 = 2
        self.par2 = 4

def Inverter(inp):
    global Port
    global Circ
    Port +=1
    out = Port
    Circ.extend([Gate("p",inp,"Vdd","n"+str(out)),Gate("n",inp,"n"+str(out),"Gnd")]) 
    return("n"+str(Port))

def Series(typ,inp1,inp2,out=None):
    global Port
    global Circ
    if(typ == "p"):
        top = "Vdd"
    else:
        top = "Gnd"
    Port += 1
    mid = "n"+str(Port)
    if out==None:
        Port += 1
        out = "n"+str(Port)
    Circ.extend([Gate(typ,inp1,top,mid),Gate(typ,inp2,mid,out)])
    return(out)

def Parallel(typ,inp1,inp2,out=None):
    global Port
    global Circ
    if(typ == "p"):
        top = "Vdd" 
    else:
        top = "Gnd"
    if out==None:
        Port += 1
        out = "n"+str(Port)
    Circ.extend([Gate(typ,inp1,top,out),Gate(typ,inp2,top,out)])
    return(out)

def Or(inp1,inp2):
    tmp =Series("p",inp1,inp2)
    Parallel("n",inp1,inp2,tmp)
    tmp = Inverter(tmp)
    return(tmp)

def And(inp1,inp2):
    tmp =Parallel("p",inp1,inp2)
    Series("n",inp1,inp2,tmp)
    tmp = Inverter(tmp)
    return(tmp)


x = input("Enter gate expression\n")
y = re.findall("[a-zA-Z+.()!]+",x)



if(x != ''.join(y)):
    sys.exit("not of specified format!")
if(x.count('(') != x.count(')')):
    sys.exit("Brackets do not match!")
if(len(re.findall("[a-zA-Z]+",x)) != len(re.findall("[+.]",x))+1):
    sys.exit("Not a valid expression!")
if(len(re.findall("[+.][+.]+",x)) >0 ):        
    sys.exit("Not a valid operation!")


#REMOVE EXTRA !'s
tmp = re.findall("[a-zA-Z0-9]+|[+.]|[!]+|[()]",x)
for indx,i in enumerate(tmp):
    if re.match("[!]+",i):
        tmp[indx] = "!" if len(i)%2 else "__GBG__"

while tmp.count("__GBG__")>0:
    tmp.remove("__GBG__")

x="".join(tmp)
print(x)
x = re.findall("[a-zA-Z0-9]+|[+.]|[!]+|[()]",x)
    
OperandStk = []
OperatorStk = []

for i in x:
    if(re.match("[a-zA-Z0-9]+",i)):
        OperandStk.append(i)
    else:
        if(i=="!"):
            OperatorStk.append(i)


        elif(i=="."):
            while OperatorStk[-1:]==["!"]:
                OperatorStk.pop()
                OperandStk.append(Inverter(OperandStk.pop()))
            OperatorStk.append(i)


        elif(i=="+"):
            if(len(OperatorStk)>0):
                while (OperatorStk[-1:]==["!"]) | (OperatorStk[-1:]==["."]):

                    if OperatorStk[-1:]==["!"]:
                        OperatorStk.pop()
                        OperandStk.append(Inverter(OperandStk.pop()))

                    elif OperatorStk[-1:]==["."]:
                        OperatorStk.pop()   
                        in1 = OperandStk.pop()
                        in2 = OperandStk.pop()
                        OperandStk.append(And(in1,in2))                   
            OperatorStk.append(i)


        elif(i=="("):
            OperatorStk.append(i)


        elif(i==")"):
            if(len(OperatorStk)>0):
                while OperatorStk[-1:] != ["("]:
                    if OperatorStk[-1:]==["!"]:
                        OperatorStk.pop()
                        OperandStk.append(Inverter(OperandStk.pop()))
                    elif OperatorStk[-1:]==["."]:
                        OperatorStk.pop()   
                        in1 = OperandStk.pop()
                        in2 = OperandStk.pop()
                        OperandStk.append(And(in1,in2)) 
                    else:
                        OperatorStk.pop()   
                        in1 = OperandStk.pop()
                        in2 = OperandStk.pop()
                        OperandStk.append(Or(in1,in2)) 
            OperatorStk.pop()

while len(OperatorStk)>0:
    if OperatorStk[-1:]==["!"]:
        OperatorStk.pop()
        OperandStk.append(Inverter(OperandStk.pop()))
    elif OperatorStk[-1:]==["."]:
        OperatorStk.pop()   
        in1 = OperandStk.pop()
        in2 = OperandStk.pop()
        OperandStk.append(And(in1,in2)) 
    else:
        OperatorStk.pop()   
        in1 = OperandStk.pop()
        in2 = OperandStk.pop()
        OperandStk.append(Or(in1,in2)) 

file1 = open("file.sim","w") 

for i in Circ:
    bottom = str(i.bottom) if i.bottom!=OperandStk[0] else "out"
    top = str(i.top) if i.top!=OperandStk[0] else "out"
    j= str(i.typ)+" "+str(i.inp)+" "+top+" "+bottom+" 2"+" 4\n" 
    file1.write(j)

file1.close()
