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

2. Modify ``TALYS_FPY_FILE`` path in ``Python/config.py`` to read ``yieldZA1.00E-06.fis``.

3. Move to ``Python`` dir.

4.  Run ``python beta.py``.
