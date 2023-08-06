import sys
import pandas as pd
class Dupamb:
    def __init__(self,filename,header=None):
        self.data = pd.read_csv(filename,header=header)
        self.d = self.data.iloc[:,:].values
        self.head = self.d[0,:]
        self.d = self.d[1:,:]
    def removeDupAmb(self,outfilename="out.csv"):
        lst = []
        for i in range(0,len(self.d)):
            st = ""
            for j in range(0,len(self.d[i])):
                st = st + str(self.d[i,j]) + " "
            lst.append(st)
        l = set(lst)
        diction = {}
        for i in l:
            if i[i.index(" "):] in diction.keys():
                if diction[i[i.index(" "):]]!=i[0:i.index(" ")]:
                    diction[i[i.index(" "):]]=-1
            else:
                diction[i[i.index(" "):]]=i[0:i.index(" ")]
        k = []
        for i in diction.keys():
            if diction[i]==-1:
                k.append(i)
        for i in k:
            del(diction[i])
        f = open(outfilename,"w")
        f.write(",".join(self.head)+"\n")
        for i in diction.keys():
            f.write(diction[i]+i.rstrip().replace(" ",",")+"\n")
        f.close()

def interpolation(x,xx,yy):
	s = 0
	for i in range(0,len(xx)):
		p = 1
		for j in range(0,len(xx)):
			if i!=j:
				p*=(((x-xx[j])/(xx[i]-xx[j])))
		s+=(p*(yy[i]))
	return s
if __name__=="__main__":
	try:
		filename = sys.argv[1]
		obj = Dupamb(filename)
		obj.removeDupAmb()
		data = pd.read_csv('out.csv',header=None)
		data = data.iloc[:,:].values
		head = data[0,:]
		data = data[1:,:]
		data = data.astype('float64')
		x = data[:,1:]
		y = data[:,1]
		row = len(x)
		col = len(x[0])
		w = [float(w) for w in sys.argv[3].split(',')]
		k = [float(w) for w in sys.argv[2].split(',')]
		ans = 0
		for i in range(0,col):
			flag = 0
			for j in range(0,row):
				if x[j,i]==k[i]:
					ans+=y[j]*w[i]
					flag = 1
					break
			if flag==0:
				ans+=interpolation(k[i],x[:,i],y*w[i])
		print(ans)
	except:
		print("Exception occurred")