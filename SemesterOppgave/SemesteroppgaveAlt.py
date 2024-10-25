import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import matplotlib.image as mpimg
import matplotlib.patches as mpatches
import random
from random import randint



def GenereateRandomYearDataList(intencity: float, seed: int = 0) -> list[int]:
    if seed != 0:
        random.seed(seed)
    centervals = [200, 150, 100, 75, 75, 75, 50, 75, 100, 150, 200, 250, 300]
    centervals = [x * intencity for x in centervals]
    nox = centervals[0]
    inc = True
    noxList = []
    for index in range(1,365):
        if randint(1, 100) > 50:
            inc = not inc
        center = centervals[int(index / 30)]
        dx = min(2.0, max(0.5, nox / center ))
        nox =  nox + randint(1,5) / dx if inc else nox - randint( 1, 5) * dx
        nox = max(10, nox)
        noxList.append(nox)
    return noxList


kron_nox_year = GenereateRandomYearDataList(intencity=1.0, seed = 2)
nord_nox_year = GenereateRandomYearDataList(intencity=.3, seed = 1)
additional_nox_year = GenereateRandomYearDataList(intencity=0.5, seed=3) #Ny

fig, axNox = plt.subplots(figsize=(13, 5))
plt.subplots_adjust(bottom=0.25)

fig.patch.set_facecolor('#ADD8E6')  

quarterYear =  int(input("Kvartal 1-4  (0=Hele Året)  : "))


def get_interval():
    num_labels = 12
    xlabels = ['J' ,'F' ,'M' ,'A' ,'M' ,'J', 'J', 'A', 'S', 'O', 'N', 'D']
    xticks = np.linspace(15, 345, num_labels)
    days_interval = (1, 365)
    if quarterYear == 1:
        xticks = [15,45,75]
        xlabels = ['Jan', 'Feb', 'Mars']
        days_interval = (0,90)
    if quarterYear == 2:
        xticks = [15,45,75]
        xlabels = ['April', 'Mai', 'Juni']
        days_interval = (90, 180)
    if quarterYear == 3:
        xticks = [15, 45, 75]
        xlabels = ['July', 'Aug', 'Sept']
        days_interval = (180, 270)
    if quarterYear == 4:
        xticks = [15, 45, 75]
        xlabels = ['Okt', 'Nov', 'Des']
        days_interval = (270, 365)
        
    axNox.set_xticks(xticks)
    axNox.set_xticklabels(xlabels, fontsize=10)
    axNox.set_title("NOX År" if quarterYear == 0 else f"NOx Kvartal {quarterYear}", fontweight='bold')
    return days_interval


def plot_graph():
    days_interval = get_interval()
    nord_nox = nord_nox_year[days_interval[0]:days_interval[1]]
    kron_nox = kron_nox_year[days_interval[0]:days_interval[1]]
    additional_nox = additional_nox_year[days_interval[0]:days_interval[1]]
    days = len(nord_nox)
    list_days = np.linspace(1, days, days)

    axNox.cla()
    axNox.set_facecolor('#D3D3D3') 
    l1, = axNox.plot(list_days, nord_nox, 'blue', label='Nordnes')
    l2, = axNox.plot(list_days, kron_nox, 'red', label='Kronstad')
    l3, = axNox.plot(list_days, additional_nox, 'green', label='Ny Stasjon')

    axNox.legend(loc='upper left')
    axNox.set_xlabel("Dager")
    axNox.set_ylabel("NOx Verdier")
    axNox.grid(True, linestyle='--')
    
    
    #Gjennomsnitt 
    avg_nord = np.mean(nord_nox)
    avg_krona = np.mean(kron_nox)
    avg_additional = np.mean(additional_nox)

    axNox.text(0.768, 0.2, f"Gjennomsnitt Nordnes: {avg_nord:.2f}\n"
                            f"Gjennomsnitt Kronstad: {avg_krona:.2f}\n"
                            f"Gjennomsnitt Ny Stasjon: {avg_additional:.2f}",
                transform=axNox.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(facecolor='#FFFFFF00', edgecolor='black', boxstyle='round,pad=0.5'))
    
    plt.draw()

plot_graph()
plt.show()

