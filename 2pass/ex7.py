# -*- coding: utf-8 -*-
from ast import arguments
import sys

from onepass import two_pass

assembler_command = {
    "AND":"000","ADD":"001","LDA":"002","STA":"003"
    ,"BUN":"004","BSA":"005","ISZ":"006","CLA":"7800"
    ,"CLE":"7400","CMA":"7200","CME":"7100","CIR":"7080"
    ,"CIL":"7040","INC":"7020","SPA":"7010","SNA":"7008"
    ,"SZA":"7004","HLT":"7001","INP":"F800","OUT":"F400"
    ,"SKI":"F200","SKO":"F100","ION":"F080","IOF":"F040"
    }
assembler_16_stem1={
    "A":"41","B":"42","C":"43","D":"44","E":"45"
    ,"F":"46","G":"47","H":"48","I":"49","J":"4A","K":"4B","L":"4C"
    ,"M":"4D","N":"4E","O":"4F","P":"50","Q":"51","R":"52","S":"53"
    ,"T":"54","U":"55","V":"56","W":"57","X":"58","Y":"59","Z":"5A"
    ,",":"2C","space":"20","(":"28",")":"29","*":"2A","+":"2B","-":"2D"
    ,".":"2E","/":"2F","=":"3D","CR":"0D"
    }
assembler_16_step2={
    "0":"30","1":"31","2":"32","3":"33","4":"34","5":"35","6":"36"
    ,"7":"37","8":"38","9":"39","A":"41","B":"42","C":"43","D":"44","E":"45"
    ,"F":"46","G":"47","H":"48","I":"49","J":"4A","K":"4B","L":"4C"
    ,"M":"4D","N":"4E","O":"4F","P":"50","Q":"51","R":"52","S":"53"
    ,"T":"54","U":"55","V":"56","W":"57","X":"58","Y":"59","Z":"5A"
    }
def First_pass(asm):
    # Memory_word = [] # 0,1,2,3,4,5,6
    # Memory_word_padding = [] # padding 000,001,002,003,004,005,006
    # org = 0 #초기값
    asm_list = [] # asm -> 문장 -> 단어 2중 리스트
    for i in range(len(asm)):
        asm_list.append(asm[i].lstrip().replace("\n","").split())

    org = 0 #초기값
    try:
        org = int(asm_list[0][1])
    except:
        org = int(0)

    Memory_word = [] # 0,1,2,3,4,5,6
    for i in range(len(asm)-2):
        Memory_word.append(org+i)    

    Memory_word_padding = [] # padding 000,001,002,003,004,005,006
    for i in range(len(Memory_word)):
        if(len(str(Memory_word[i])) == 1):
            Memory_word_padding.append("00"+str(Memory_word[i]))
        elif(len(str(Memory_word[i])) == 2):
            Memory_word_padding.append("0"+str(Memory_word[i]))
        else:
            Memory_word_padding.append(str(Memory_word[i]))

    Memory_word_padding_asm_list = asm_list #필요 없으면 지워도됨
    for i in range(len(asm_list)):
        if(Memory_word_padding_asm_list[i][0] == "ORG" or Memory_word_padding_asm_list[i][0] == "END"):
            pass
        else:
            Memory_word_padding_asm_list[i].insert(0,Memory_word_padding[i-1])
    #print(Memory_word_padding_asm_list)
    sudo_LC = []
    sudo_command = []
    sudo_command_list = []
    for i in range(len(asm_list)):
        if(len(asm_list[i])== 4):
            sudo_LC.append(int(asm_list[i][0]))
            sudo_command.append(asm_list[i])
    for i in range(len(sudo_LC)):
        if( len(str(sudo_LC[i])) == 1 ):
            sudo_LC[i] = "000"+str(sudo_LC[i])
        if( len(str(sudo_LC[i])) == 2 ):
            sudo_LC[i] = "00"+str(sudo_LC[i])
        if( len(str(sudo_LC[i])) == 3 ):
            sudo_LC[i] = "0"+str(sudo_LC[i])
    for i in range(len(sudo_command)):
        sudo_command_list.append(sudo_command[i][1])
    I_list = []
    for i in range(len(Memory_word_padding_asm_list)):
        for j in range(len(Memory_word_padding_asm_list[i])):
            if(Memory_word_padding_asm_list[i][j] == "I"):
                I_list.append({i:j})
    return Memory_word_padding_asm_list,sudo_LC,I_list




def bosu(bo):
    check = True
    bo = bo[1:]
    templist = []
    while len(bo) != 16:
        bo = "0"+bo 
    for i in reversed(range(len(bo))):
        if(check):
            if(bo[i] == "1"):
                templist.append(bo[i])
                check = False
            else:
                templist.append(bo[i])
        else:
            if(bo[i] == "1"):
                templist.append("0")
            if(bo[i] == "0"):
                templist.append("1")
    templist.reverse()
    temp = ""
    for i in templist:
        temp = temp +str(i)
    
    return temp   


def two_pass(Memory_word_padding_asm_list,sudo_LC,I_list):
    for i in range(len(Memory_word_padding_asm_list)):
        for j in range(len(Memory_word_padding_asm_list[i])):
            Memory_word_padding_asm_list[i][j]=Memory_word_padding_asm_list[i][j].lstrip().replace(",","")
    del Memory_word_padding_asm_list[0]
    del Memory_word_padding_asm_list[-1]

    for j in range(len(sudo_LC)):
        Memory_word_padding_asm_list[j][2] = sudo_LC[j]
    breakp = 0
    for i in range(len(Memory_word_padding_asm_list)):
        if(Memory_word_padding_asm_list[i][1] == "HLT"):
            Memory_word_padding_asm_list[i][1] = assembler_command["HLT"]
            breakp = i+1
            break
        else:
            Memory_word_padding_asm_list[i][1] = assembler_command[Memory_word_padding_asm_list[i][1]]
    for i in range(breakp,len(Memory_word_padding_asm_list)):
        del Memory_word_padding_asm_list[i][1]
    for i in range(breakp,len(Memory_word_padding_asm_list)):
        del Memory_word_padding_asm_list[i][1]
    for i in range(len(Memory_word_padding_asm_list)):
        if(i == breakp-1):
            pass
        else:
            for j in range(1,len(Memory_word_padding_asm_list[i])):
                temp = int(Memory_word_padding_asm_list[i][j])
                Memory_word_padding_asm_list[i][j] = format(temp, 'b')
    #print(Memory_word_padding_asm_list)
    hlt = ""
    for i in Memory_word_padding_asm_list[breakp-1][1]:
        temp = int(i)
        temp = format(temp, 'b')
        if(len(str(temp)) == 4):
            hlt =hlt + "" + str(temp)
        elif(len(str(temp)) == 3):
            hlt = hlt + "0" + str(temp)
        elif(len(str(temp)) == 2):
            hlt = hlt + "00" + str(temp)
        elif(len(str(temp)) == 1):
            hlt = hlt + "000" + str(temp)
    Memory_word_padding_asm_list[breakp-1][1] = hlt
    print(Memory_word_padding_asm_list)
    if(len(I_list) == 0): #간접 주소 명령어가 없을 경우
        for i in range(0,len(Memory_word_padding_asm_list)):
            for j in range(1,len(Memory_word_padding_asm_list[i])):
                if( "-" in Memory_word_padding_asm_list[i][j]):
                    a = bosu(Memory_word_padding_asm_list[i][j])
                    Memory_word_padding_asm_list[i][j] = a
                else:
                    if(j == 1):
                        temp = Memory_word_padding_asm_list[i][j]
                        print(temp)
                        if(len(str(temp)) == 4):
                            Memory_word_padding_asm_list[i][j] = "" + str(temp)
                        elif(len(str(temp)) == 3):
                            Memory_word_padding_asm_list[i][j] = "0" + str(temp)
                        elif(len(str(temp)) == 2):
                            Memory_word_padding_asm_list[i][j] = "00" + str(temp)
                        elif(len(str(temp)) == 1 and temp != "0"):
                            Memory_word_padding_asm_list[i][j] = "000" + str(temp)
                            
                        else:
                            while len(temp) != 16:
                                temp = "0"+temp 
                            Memory_word_padding_asm_list[i][j] = temp
                    else:
                        temp = Memory_word_padding_asm_list[i][j]
                        if(len(str(temp)) == 4):
                            Memory_word_padding_asm_list[i][j] = "00000000" + str(temp)
                        elif(len(str(temp)) == 3):
                            Memory_word_padding_asm_list[i][j] = "000000000" + str(temp)
                        elif(len(str(temp)) == 2):
                            Memory_word_padding_asm_list[i][j] = "0000000000" + str(temp)
                        elif(len(str(temp)) == 1 and temp != "0"):
                            Memory_word_padding_asm_list[i][j] = "00000000000" + str(temp)
                        else:
                            while len(temp) != 16:
                                temp = "0"+temp 
                            Memory_word_padding_asm_list[i][j] = temp
        asm = []
        for i in range(len(Memory_word_padding_asm_list)):
            temp = ""
            for j in range(len(Memory_word_padding_asm_list[i])):
                if(j == 0):
                    a = Memory_word_padding_asm_list[i][j]
                    temp = temp + str(a) + " "
                else:
                    a = Memory_word_padding_asm_list[i][j]
                    temp = temp + str(a)
            asm.append(temp)
        return asm
    else:#간접 주소 명령어가 있을 경우 수업 좀 더 나가면 구현 바람. 
        pass

def obj_save(asm,path):
    f = open(path, 'w')
    for i in asm:
        data = i+"\n"
        f.write(data)
    f.close()
def path_parser(arg):
    if(len(arg) == 1 or len(arg) == 2):
        print("실행 불가능")
        exit(0)
    return arg[1],arg[2]

def read_asm(path_asm):
    f = open(path_asm, 'r')
    lines = f.readlines()
    f.close()    
    for i in range(len(lines)):
        lines[i] = lines[i].upper() 
    return lines
def main():
    path_asm ,path_obj = path_parser(sys.argv)
    asm = read_asm(path_asm)
    Memory_word_padding_asm_list,sudo_LC,I_list =  First_pass(asm)
    asm = two_pass(Memory_word_padding_asm_list,sudo_LC,I_list)
    obj_save(asm,path_obj)
 

if __name__ == "__main__":
    main()