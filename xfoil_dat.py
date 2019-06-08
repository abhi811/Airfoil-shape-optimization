
import subprocess as sp
import os
import shutil
import sys
import string
import time

xfoilpath = r'C:\Users\HP\Desktop\AeroOpt\Xfoil\python_Xfoil_Genetics_src\xfoil.exe'


def Xfoil(name, Ncrit, Re ):
    def Cmd(cmd):
        ps.stdin.write(bytes(cmd+'\n','utf-8'))
    try :
        os.remove(name+'.log')
    except :
        pass
    ps = sp.Popen(xfoilpath ,stdin=sp.PIPE,stderr=sp.PIPE,stdout=sp.PIPE)
    ps.stderr.close()
    ss='load '+name+'.dat'
    Cmd(ss)
    Cmd('OPER')
    Cmd('Vpar')
    Cmd('N '+str(Ncrit))
    Cmd(' ')
    Cmd('visc '+str(Re))
    Cmd('PACC')
    Cmd(name+'.log') 
    Cmd(' ')         
    Cmd('aseq 0.0 15.0 1.0')
    Cmd(' ')    
    
    ps.stdout.close()
    ps.stdin.close()
    ps.wait()
    


def getLDmax(name):
    filename = name+".log"
    f = open(filename, 'r')
    flines = f.readlines()
    LDmax = 0
    for i in range(12,len(flines)):
        #print flines[i]
        words = str.split(flines[i]) 
        LD = float(words[1])/float(words[2])
        if(LD>LDmax):
            LDmax = LD
    return LDmax
