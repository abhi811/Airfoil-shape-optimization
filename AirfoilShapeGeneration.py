from BezierN import BezierN
from xfoil_dat import *



def gen2airfoil(gen,name):
    upx = [0, 0,  0.25,0.5,0.75,1]
    downx = upx

    upy =   [0]*6
    downy = [0]*6
    upy   [1] = gen[0]
    downy [1] = - gen[1]
    upy   [2] = gen[2] + gen[5]
    upy   [3] = gen[3] + gen[6]
    upy   [4] = gen[4] + gen[7]
    downy [2] = gen[2] - gen[5]
    downy [3] = gen[3] - gen[6]
    downy [4] = gen[4] - gen[7]
    
    n=50;
    MyBezier = BezierN(6)
    pupx  = MyBezier.interpolate(upx   ,n)
    pupy  = MyBezier.interpolate(upy   ,n)
    pdownx= MyBezier.interpolate(downx ,n)
    pdowny= MyBezier.interpolate(downy ,n)

   
    foilfile = open(name+".dat",'w')
    foilfile.write(name+"\n")
    for i in range (n,0,-1):
         foilfile.write(  " %1.6f    %1.6f\n" %(pupx[i],pupy[i]))
    for i in range (0,n+1):
         foilfile.write(  " %1.6f    %1.6f\n" %(pdownx[i],pdowny[i]))
    foilfile.close()





