# FPY_betadecay code
Calculate cumulative fission product yield and delayed neutron yield from Talys independent yield output.

## Download
You can download the repository from a terminal using:

```
git clone https://github.com/shinokumura/FPY_betadecay.git
```

## Run
1. Calculate fission yield by Talys using following input file as an example.

```
projectile n
element    U
mass       235
energy     1.00E-6
ejectiles g n
massdis y
fymodel 4
ffmodel 2
elow 1.e-6
Rfiseps 1.e-3
outspectra y
bins 100
channels n
maxchannel 8
```

2. Move to ``Python`` dir.

3. Modify parameters in ``Python/config.py`` as it needs.
```
# for cumulative yield calculation
CUMLATIVE: set ``True``  for calculation of cumulative yield based on ``TALYS_FPY_FILE`` independent yield
TALYS_FPY_FILE: default independent FPY file created by TALYS
DEFAULT_DECAY_FILE: simplified decay data library file

# for decay heat calculation
DECAYHEAT: set ``True`` if time dependent decay heat calculation is required
DECAY_HEAT_CALC_TIME: give time sequence for time dependent decay heat calculation 

# convert ENDF format decay data library into simplified format
CONVERT: set ``True`` if conversion of other decay data library into simplified format
DECAY_DATA_LIB_PATH: decay data library path to convert
```

4.  Run ``python main.py``.
