import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import ListedColormap

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

def draw_tasking(N, M, P, fill_in):
    fig, ax = plt.subplots(figsize=(M, N))
    arr = (np.arange(N*M) < P).astype(int)
    if len(fill_in):
        arr[np.array(fill_in) - 1] = 2
    arr = arr.reshape(N, M)[::-1,:]

    ax.xaxis.set_tick_params(labeltop=True)
    ax.xaxis.set_tick_params(labelbottom=False)

    if 0 not in arr: lmap = ListedColormap(['pink', 'lightblue'])
    else: lmap = ListedColormap(['w', 'pink', 'lightblue'])
                                
    ax.pcolormesh(arr, edgecolors='k', linewidth=2, cmap=lmap)
    ax.set_xticks(np.arange(M + 1))
    ax.yaxis.set_major_locator(mticker.FixedLocator(np.arange(N + 1)))
    ax.set_yticklabels(np.arange(N, -1, -1))

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            id = (N-i-1)*M+j + 1
            if id <= P:
                text = plt.text(j+0.5, i+0.5, id, 
                        ha="center", va="center", color="k", fontsize='xx-large')
    plt.show()

#draw_tasking(3, 8, 20, [1])