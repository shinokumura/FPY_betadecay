
from fpy import *
import pandas as pd

''' to convert beoh format to talys format '''
def read_fpy_data():
    with open ("tmpFPY.txt") as f:
        lines = f.readlines()[3:]
    ind = {}

    for line in lines:
        _, z, h, a, _, iso, fpy, cum = slices(line, 7, 3, 1, 3, 3, 3, 12, 14)
        elem = ztoelem(int(z.strip()))
        if int(iso.strip()) > 0:
            product = str(int(z)).strip() + "-" + elem + "-" + str(int(a)).strip()  + "-" + str(iso.strip()).zfill(2)
        else:
            product = str(int(z)).strip() + "-" + elem + "-" + str(int(a)).strip()  + "-00"
        
        # ind[product] = float(cum)
        # ind[product] = "{:15.4e}".format(float(ind))
        ind[product] = '{:.4E}'.format(float(cum))

        # z = int(z)
        # a = int(a)
        # print(ind)
        # print("{:5d}".format(int(z)))
        print("{:5d}{:5d}{:3d}{:15.4e}".format(int(z), int(a), int(iso), float(fpy)))

    return ind

cum=read_fpy_data()
df = pd.DataFrame.from_dict(cum,orient = 'index')
df.to_csv("cum.dat", sep=' ', header=False)



# def decay(N0, tau, hl, time):
#     return tau* N0 * math.exp((-0.693/hl)*time)

def main():
    # n_uranium = []
    # t = []
    N0 = 100
    tau = 2.0
    dt = 5
    time = 50

    t = [0]
    n_uranium = [N0]
    n=int(min((time/dt),100))


    for i in range(0,n-1):
        n_uranium  += [n_uranium[i]-(n_uranium[i]/tau)*dt]
        t += [t[i] + dt]
    print (t,n_uranium)

# read_fpy_data()


def forlooptest():
    fp = ['1 54-Xe-128-00', '2 63-Eu-161-00', '3 66-Dy-165-00']
    iteration = 5
    for t in range(iteration):
        print("iteration:", t)
        for i in fp:
            print(i)
            for j in fp:
                print(j)
                for m in range(2):
                    if m == m:
                        print("here")
        for i in fp:
            print(i)

# forlooptest()