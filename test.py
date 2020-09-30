def genInp(a,inps,out):
    if(len(inps)!=a):
        return(print("error size mismatch!"))
    file1 = open("test.tcl","w") 
    file1.write("h Vdd\nl Gnd\n")
    file1.write("w "+" ".join(inps)+" "+out+"\n")
    arr = [0 for i in range(a)]
    state = ["l" for i in range(a)]
    for j in range(2**a):
        num=bin(j)[2:]
        while(len(num))<a:
            num = "0"+num
        for i in range(a):
            if num[i]=="1":
                file1.write("h "+inps[i]+"\n")
            else:
                file1.write("l "+inps[i]+"\n")
        file1.write("s\n")
    return 0

def getInpChars():
    a = int(input("How many inputs do you have?\n"))
    str = input("Enter the input characters seperated by spaces\n")
    out = input("Enter the output name\n")
    str = str.split()
    print(len(str))
    genInp(a,str,out)


getInpChars()
