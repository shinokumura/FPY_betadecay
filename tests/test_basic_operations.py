from scripts.decay_data import DecayData

nuclide = "92-U-235-00"
# nuclide = "91-Pa-231-00"
# nuclide = "37-Rb-93-00"
DecayData.load_decay_data(decaydataname="ENDF8.1")
d = DecayData(nuclide=nuclide, decaydataname="ENDF8.1")
print(d.get_daughters())
print(d.get_halflife_formatted())
print(d.get_decaymodes())
print(d.get_progonies())
