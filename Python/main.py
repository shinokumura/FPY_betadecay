'''
beta decay calculation from the independent FPY data
'''

nuclide = ''

if __name__ == '__main__':
    from config import CONVERT, DECAYHEAT, CUMLATIVE

    if CONVERT:
        from decaydata import convert_ddlibrary
        convert_ddlibrary()
        
    if DECAYHEAT:
        from beta import decayheat
        decayheat()

    if CUMLATIVE:
        from beta import cumlative
        cumlative()

    if nuclide:
        from betadecay_chain import *
        diagram(nuclide)



