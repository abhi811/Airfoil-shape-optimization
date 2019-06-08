class BezierN:
    order = 1
    binom = []
    tts   = []
    ts    = []
    
    def __init__(self, order_):
        self.order=order_
        self.binom = [0]* self.order
        self.ts    = [0]* self.order
        self.tts   = [0]* self.order
        self.binom[0]=1
        for i in range (1,self.order+1):
            temp=self.binom[0]
            for ii in range (1,i):
                temp2= self.binom[ii]
                self.binom[ii]=temp+self.binom[ii]
                temp = temp2


    def interpolate(self,coefs, n ):
        output = [0]*(n+1)
        step = 1.0/float(n)
        t = 0
        output[0]=coefs[0]
        for i in range (1,n+1):
            t+=step
            tt=1.0-t
            ttemp=1.0
            tttemp=1.0
            for j in range (0,self.order):  
                self.ts[j] = ttemp;
                self.tts[self.order-j-1] = tttemp
                ttemp*=t
                tttemp*=tt
            output[i]=0
            for j in range (0,self.order):  
                output[i]+=coefs[j]*self.tts[j]*self.ts[j]*self.binom[j]
        return output




