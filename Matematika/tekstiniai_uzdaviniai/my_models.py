import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def Vergnaud():
    arr1 = np.array([['Matų izomorfizmas','Matų sandauga','Kartotinis proporcingumas']])
    arr2 = arr1[:,[0,0,1,1,2]]
    arr2 = np.r_[arr2, [['-','Uždavinys su neišreikštu vienetu',
                         'Ploto skaičiavimas', 'Dekarto sandaugos skaičiavimas','-']]]
    arr2 = np.r_[arr2, [['Kiek kainuoja 12 sausainių, jei 4 sausainiai kainuoja 20 kronų?',
                         'Kiek kainuoja 12 sausainių, jei sausainis kainuoja 5 kronas?',
                         'Koks stačiakampio plotas, jei jo plotis 4 cm, o ilgis 5 cm?',
                         'Kelias poras galima sudaryti iš 4 mergaičių ir 5 berniukų grupės?',
                         'Kiek grūdų sulesa 12 vištų per 12 dienų, jei 4 vištos per 4 dienas sulesa 4 kg grūdų?']]]
    df_fractions = pd.DataFrame(arr2.T, columns=('Subkonstruktas', 'Tipas', 'Kintamųjų paaiškinimai'))
    df_fractions.set_index(['Subkonstruktas',  'Tipas', 'Kintamųjų paaiškinimai'], inplace=True)
    return df_fractions

def Greer():
    arr1 = np.array([['Grupavimas','Rodiklis','Dauginamasis palyginimas', 'Stačiakampė figūra', 'Dekarto sandauga']])
    arr2 = arr1[:,[0,0,1,2,3,3,4]]
    arr2 = np.r_[arr2, [['Skaidymas','Matavimas','-','-','Diskretūs dydžiai', 'Tolydūs dydžiai','-']]]
    arr2 = np.r_[arr2, [['Aš noriu išdalinti 8 sausainius keturiems draugams lygiomis dalimis. Kiek gaus kiekvienas iš jų?',
                         'Aš padalinau 24 sausainius į lygias grupes po 3. Kiek grupių gavau?',
                         '1) Marius suvalgo po 4 guminukus per minutę. Kiek guminukų jis suvalgo per 7 minutes? <br> 2) Mantas eina 6km/h greičiu. Kokią distanciją jis įveiks per 20 min?',
                         'Šiandien iš geografijos aš gavau 8, o iš matematikos 4 kartus mažiau. Kiek gavau iš matematikos?',
                         'Koks sąsiuvinyje nupiešto stačiakampio plotas, jei vienas jo kraštas eina per 8 langelių kraštines, o kitas - per 9?',
                         'Koks stačiakampio, kurio kraštinės yra 2.5cm ir 3.5cm plotas?',
                         'Jei kebabinė siūlo 2 skirtingų dydžių ir 3 rūšių kebabus bei 4 padažus, kelis skirtingus užsakymus galima padaryti?']]]
    df_fractions = pd.DataFrame(arr2.T, columns=('Subkonstruktas', 'Tipas', 'Kintamųjų paaiškinimai'))
    df_fractions.set_index(['Subkonstruktas',  'Tipas', 'Kintamųjų paaiškinimai'], inplace=True)
    return df_fractions


def draw_tasking(ncols, N, colors=dict(), docs=dict(), extent=8, lfont=16):
    """shows a list of problems, N in total, ncols columns, extent is a place for legends"""
    nrows = N//ncols+1
    fig, ax = plt.subplots(figsize=(ncols+extent, nrows))
                       
    ax.set_xticks(np.arange(ncols + 1))
    ax.set_yticks(np.arange(nrows + 1))
    ax.set_xlim(np.array(ax.get_xlim()) + [-0.1, extent+0.1])
    ax.set_ylim(np.array(ax.get_ylim()) + [-0.1, 0.1])
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.axis('off')
    
    #Auto coloring of squares
    d = dict.fromkeys(range(1, N+1), 'pink')
    for color, cells in colors.items():
        for c in cells:
            d[c] = color

    #squares + text fill + legend
    handles = dict()
    for n in np.arange(1, N+1):
        x, y = ((n-1)%ncols, (n-1)//ncols)
        rect = Rectangle(xy=(x, y), width=1, height=1, linewidth=3, 
                         facecolor=d[n], edgecolor='k', label=docs[d[n]])
        ax.add_patch(rect)
        handles[d[n]] = rect
        text = plt.text(x+0.5, y+0.5, s=n, ha="center", va="center", color="k", fontsize='xx-large')
        
    plt.rcParams['legend.handlelength'] = 1
    plt.rcParams['legend.handleheight'] = 1
    ax.legend(handles=handles.values(), prop={'size': lfont})
    plt.show()

#draw_tasking(8, 20, colors={'lightgreen':(1, 6, 20), 'lightblue':(7, 9)},
#                    docs = {'lightgreen': 'Išspręsti ir pasitikrinti uždaviniai', 
#                            'lightblue': 'Uždaviniai kitam kartui',
#                            'pink': 'Nespręsti uždaviniai'},
#                    extent=8, lfont=16)

def draw_division():
    fig = plt.figure()
    plt.xlim(0, 15)
    plt.ylim(0, 16)

    currentAxis = plt.gca()
    currentAxis.add_patch(Rectangle((0, 0), 12, 12, facecolor="lightgreen"))
    currentAxis.add_patch(Rectangle((0, 12), 12, 4, facecolor="forestgreen"))
    currentAxis.add_patch(Rectangle((12, 0), 3, 12, facecolor="seagreen"))
    currentAxis.add_patch(Rectangle((12, 12), 3, 4, facecolor="darkgreen"))
    plt.text(6, 6, 1, ha="center", va="center", color="k", fontsize='xx-large')
    plt.text(6, 14, 2, ha="center", va="center", color="k", fontsize='xx-large')
    plt.text(13.5, 6, 3, ha="center", va="center", color="k", fontsize='xx-large')
    plt.text(13.5, 14, 4, ha="center", va="center", color="k", fontsize='xx-large')
    plt.axis('off')
    plt.show()