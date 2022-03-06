from bateman import *
from decaydata import *
from utilities import format_nuclide
import json


def diagram(nuclide):
    from config import MAX_NUMBER_IN_DIAGRAM
    import networkx as nx
    import matplotlib.pyplot as plt

    progs_dict = progenies(nuclide)
    #### {'42-Mo-99-00': ['43-Tc-99-00', '43-Tc-99-01'], '43-Tc-99-00': ['44-Ru-99-00'], '44-Ru-99-00': [], '43-Tc-99-01': ['44-Ru-99-00', '43-Tc-99-00']}

    pos = {}
    edge_labels = {}
    br_label = []
    rtyp_label = []
    labeldict = {}
    top = len(progs_dict)

    nn = DecayData(nuclide)
    pos[nuclide] = (top, top)
    labeldict[nuclide] = format_nuclide(nuclide) + "\n" + str(nn.get_halflife_formatted())

    for n in range(nn.get_ndm()):
        br_label += [ float(nn.get_branchingratio(n)) ]
        rtyp_label += [ rtyp_to_mode(float(nn.get_rtyp(n))) ]


    appeared = []
    for node, p in enumerate(progs_dict):
        posx = posy = 0
        appeared += [p]
        for d in progs_dict[p]:
            if d not in appeared:
                print(d)
                dd = DecayData(d)
                labeldict[d] = format_nuclide(d)+ "\n" + str(dd.get_halflife_formatted())  #+ "\n" + str(dd.get_halflife())

                for n in range(dd.get_ndm()):
                    br_label +=  [ float(dd.get_branchingratio(n)) ]
                    rtyp_label += [ rtyp_to_mode(float(dd.get_rtyp(n))) ]

                side = progs_dict[p].index(d)
                posx = top + side
                posy = top - (node + 1)
                pos[d] = (posx, posy)

    G = nx.DiGraph(progs_dict)
    # edge_labels = {e: i for e in G.edges for i in range(len(edge_label)) }

    i = 0
    for e in G.edges:
        edge_labels[e] = "{:2.2f}% \n {:5s}".format( float(br_label[i] *100), rtyp_label[i] )
        i += 1

    # nx.draw(Dig, with_labels=True, node_color = "red", edge_color = "gray", node_size = 50, width = 1)
    # nx.draw_networkx_nodes(G, pos, node_color="w", alpha=0.6, node_size=sizes)
    nx.draw(
        G,
        pos=pos,
        labels=labeldict,
        with_labels=True,
        node_size=6000,
        font_size=10,
        node_shape="s",
        node_color="#FFFFFF",
        linewidths=1,
        edgecolors="#000000",
    )

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, verticalalignment='baseline', rotate=False)
    plt.show()

    return G



def draw_chain():
    # nuclide = "37-Rb-93-00"
    nuclide = "55-Cs-141-00"
    # nuclide = "86-Rn-222-00"
    # nuclide = "92-U-235-00"
    # nuclide = "91-Pa-231-00"

    diagram(nuclide)


if __name__ == "__main__":
    draw_chain()

