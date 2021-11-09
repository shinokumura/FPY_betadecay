
import json

from config import DEFAULT_DECAY_FILE
from elem import ztoelem

def read_decay_data():
    with open (DEFAULT_DECAY_FILE) as f:
        ln = 1
        lines = f.readlines()
    
    ''' dictionary containing all decay info '''
    decaydata = {}

    while lines:
        ELM = ""
        if ln >= len(lines):
            break
        
        decayinfo = []
        
        ''' read header of nuclide 
        100	read(12,*,end=1000)iz0,ia0,m0,T0,dT0,awr0,ndk0,nsp0,mat0
	    read(12,*)Eb0,dEb0,Eg0,dEg0,Ea0,dEa0
        '''
        head = lines[ln]
        Z = head[0:5].strip()
        A = head[5:11].strip()
        ELM = ztoelem(int(Z))
        LIS = head[10:16].strip().zfill(2)   # ratio of the LIS state nuclide mass to that of neutron
        HL = head[17:31].strip()
        dHL =head[32:46].strip()
        NS= int(head[61:66].strip())    # number of decay mode

        nuclide = str(Z) + "-" + ELM + "-" + str(A) + "-"  + str(int(float(LIS))).zfill(2)

        ''' read energy '''
        infon = lines[ln+1]
        EB = infon[1:16].strip()
        dEB =infon[17:31].strip()
        EG = infon[32:46].strip()
        dEG =infon[47:61].strip()
        EA = infon[62:76].strip()
        dEA =infon[77:91].strip()

        # print(ELM, A, HL)

        ''' read decay infor '''
        decayinfo += lines[ln+2:ln+NS+2]
        DD = {}
        for decay in decayinfo:
            NUM = decayinfo.index(decay)
            RTYP = decay[1:16].strip()  # 0 gamma, 1 beta, 2 ex, 3 IT, 4 alpha, 5 n, 6 SF, 7 proton, 10 unknown
            RFS  = decay[17:30].strip()  # isomeric state flag for daughter nuclide
            Q    = decay[31:46].strip()
            dQ   = decay[47:61].strip()
            BR   = decay[61:76].strip()
            dBR  = decay[77:91].strip()

            daughterZ, daughterA = calc_daughter(float(RTYP), int(Z), int(A))
            daughterELM = ztoelem(int(daughterZ))

            if RFS == "0.0000000E+00":
                ISO = ""
            elif RFS == "1.0000000E+00":
                ISO = "M1"
            elif RFS == "2.0000000E+00":
                ISO = "M2"
            elif RFS == "3.0000000E+00":
                ISO = "M3"
            else:
                ISO = "UNKNOWN"

            # daughter = str(daughterZ) + "-" + daughterELM + "-" + str(daughterA) + "-" + ISO
            # next = str(daughterZ).zfill(3) + str(daughterA).zfill(3) + str(int(float(RFS))).zfill(2)
            daughter = str(daughterZ) + "-" + daughterELM + "-" + str(daughterA) + "-" + str(int(float(RFS))).zfill(2)

            DD.update({NUM: {"RTYP": RTYP, "RFS": RFS, "Q": Q, "BR": BR, "DAUGHTER":daughter}})
        
        decaydata.update({nuclide: {"Z":Z, "ELM":ELM, "MASS": A, "LIS": LIS, "HL": HL, "DecayInfo": DD}})
        
        ln = ln+1+NS+1

    # print (json.dumps(decaydata, indent=2))

    with open('decaydata.json', 'w') as f:
        json.dump(decaydata, f,  indent=2)
    return decaydata


def calc_daughter(RTYP, Z, A):
    if RTYP == 1.0:
        return Z+1, A
    elif RTYP == 1.1:
        return Z+2, A
    elif RTYP == 1.4:
        return Z-1, A-4
    elif RTYP == 1.5:
        return Z+1, A-1
    elif RTYP == 1.55:
        return Z+1, A-2
    elif RTYP == 1.555:
        return Z+1, A-3
    elif RTYP == 1.5555:
        return Z+1, A-4

    elif RTYP == 2.0:
        return Z-1, A
    elif RTYP == 2.2:
        return Z-2, A
    elif RTYP == 2.4:
        return Z-3, A-4
    elif RTYP == 2.7:
        return Z-2, A-1
    elif RTYP == 2.77:
        return Z-3, A-2
    elif RTYP == 2.777:
        return Z-4, A-3

    elif RTYP == 3.0:
        return Z, A
    elif RTYP == 3.4:
        return Z-2, A-4
        
    elif RTYP == 4.0:   # alhpha
        return Z-2, A-4

    elif RTYP == 5.0:
        return Z, A-1
    elif RTYP == 5.5:
        return Z, A-2
    elif RTYP == 5.55:
        return Z, A-3

    elif RTYP == 7.0:
        return Z-1, A-1
    elif RTYP == 7.7:
        return Z-2, A-2
    else:
        return Z, A


decaydata = read_decay_data()

class DecayData:
    def __init__(self, nuclide=None, decaymode=None, y1=None):
        self.nuclide = nuclide  # 40Zr99  without 0 fill
        self.decaymode = decaymode
        self.y1 = y1
        
    def get_ndm(self): #number of decay mode
        if decaydata.get(self.nuclide) is not None:
            return len(decaydata[self.nuclide]['DecayInfo'])
        else:
            return 0

    def get_decaymodes(self): # all modes
        n =  self.get_ndm()
        modes = []
        for n in decaydata[self.nuclide]['DecayInfo']:
            modes += [decaydata[self.nuclide]['DecayInfo'][n]]
        return modes

    def get_halflife(self):
        return decaydata[self.nuclide]['HL']

    def get_decaymode(self,nd): # specific mode
        return decaydata[self.nuclide]['DecayInfo'][nd]

    def get_rtyp(self,nd):
        return decaydata[self.nuclide]['DecayInfo'][nd]['RTYP']

    def get_branchingratio(self,nd):
        return decaydata[self.nuclide]['DecayInfo'][nd]['BR']

    def get_qvalue(self,nd):
        return decaydata[self.nuclide]['DecayInfo'][nd]['Q']

    def get_next(self,nd): # specific mode
        return decaydata[self.nuclide]['DecayInfo'][nd]['DAUGHTER']

