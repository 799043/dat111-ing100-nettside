import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons
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
    for index in range(1, 365):
        if randint(1, 100) > 50:
            inc = not inc
        center = centervals[int(index / 30)]
        dx = min(2.0, max(0.5, nox / center))
        nox = nox + randint(1, 5) / dx if inc else nox - randint(1, 5) * dx
        nox = max(10, nox)
        noxList.append(nox)
    return noxList

def GenerateRandomDustDataList(intencity: float, seed: int = 0) -> list[int]:
    return GenereateRandomYearDataList(intencity, seed)

kron_nox_year = GenereateRandomYearDataList(intencity=1.0, seed=2)
nord_nox_year = GenereateRandomYearDataList(intencity=.3, seed=1)
additional_nox_year = GenereateRandomYearDataList(intencity=0.5, seed=3)  
kron_dust_year = GenerateRandomDustDataList(intencity=1.0, seed=4)
nord_dust_year = GenerateRandomDustDataList(intencity=.3, seed=5)

fig = plt.figure(figsize=(10, 5))  
fig.patch.set_facecolor('grey')

axNok = fig.add_axes((0.05, 0.15, 0.45, 0.6)) 
axBergen = fig.add_axes((0.55, 0.07, 0.4, 0.75))  
axSlider = fig.add_axes((0.1, 0.85, 0.1, 0.03))  
axRadio = fig.add_axes((0.8, 0.83, 0.1, 0.1))

coordinates_Nordnes = (100, 100)
coordinates_Kronstad = (1300, 1400)
days_interval = (1, 365)
marked_point = (0, 0)

slider = Slider(axSlider, 'Intervall  ', 0, 4, valinit=0, valstep=1)
radio = RadioButtons(axRadio, ('NOX', 'Asfaltstøv'))

current_data_type = 'NOX' 

def slider_update(val):
    global days_interval
    kvartal = int(val)
    days_interval = (1, 365)
    if kvartal == 1:
        days_interval = (1, 90)
    elif kvartal == 2:
        days_interval = (90, 180)
    elif kvartal == 3:
        days_interval = (180, 270)
    elif kvartal == 4:
        days_interval = (270, 365)
    plot_graph()

def on_click(event):
    global marked_point
    if ax := event.inaxes:
        if ax == axBergen:
            marked_point = (event.xdata, event.ydata)
            plot_graph()

def CalcPointValue(valN, valK):
    distNordnes = math.dist(coordinates_Nordnes, marked_point)
    distKronstad = math.dist(coordinates_Kronstad, marked_point)
    distNordnesKronstad = math.dist(coordinates_Nordnes, coordinates_Kronstad)
    val = (1 - distKronstad / (distKronstad + distNordnes)) * valK + \
          (1 - distNordnes / (distKronstad + distNordnes)) * valN
    val = val * (distNordnesKronstad / (distNordnes + distKronstad)) ** 4
    return val

def draw_circles_stations():
    circle = mpatches.Circle((100, 100), 50, color='blue')
    axBergen.add_patch(circle)
    circle = mpatches.Circle((1300, 1400), 50, color='red')
    axBergen.add_patch(circle)

def draw_label_and_ticks():
    num_labels = 12
    xlabels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    xticks = np.linspace(15, 345, num_labels)

    if days_interval[1] == 90:
        xticks = [15, 45, 75]
        xlabels = ['Jan', 'Feb', 'Mars']
    elif days_interval[1] == 180:
        xticks = [15, 45, 75]
        xlabels = ['April', 'Mai', 'Juni']
    elif days_interval[1] == 270:
        xticks = [15, 45, 75]
        xlabels = ['July', 'Aug', 'Sept']
    elif days_interval[0] == 270:
        xticks = [15, 45, 75]
        xlabels = ['Okt', 'Nov', 'Des']

    axNok.set_xticks(xticks)
    axNok.set_xticklabels(xlabels)

def plot_graph():
    global days_interval, current_data_type
    axNok.cla()
    axNok.set_facecolor('#D3D3D3')
    axBergen.cla()
    
    if current_data_type == 'NOX':
        nord_nox = nord_nox_year[days_interval[0]:days_interval[1]]
        kron_nox = kron_nox_year[days_interval[0]:days_interval[1]]
    else:
        nord_nox = nord_dust_year[days_interval[0]:days_interval[1]]
        kron_nox = kron_dust_year[days_interval[0]:days_interval[1]]
    
    days = len(nord_nox)
    list_days = np.linspace(1, days, days)

    l3 = None
    avg_nord_nox = np.mean(nord_nox)
    avg_kron_nox = np.mean(kron_nox)

    avg_marked_nox = 0.0
    if marked_point != (0, 0):
        nox_point = [CalcPointValue(nord_nox[i], kron_nox[i]) for i in range(days)]
        l3, = axNok.plot(list_days, nox_point, 'darkorange')
        avg_marked_nox = np.mean(nox_point)  
        circle = mpatches.Circle((marked_point[0], marked_point[1]), 50, color='orange')
        axBergen.add_patch(circle)

    l1, = axNok.plot(list_days, nord_nox, 'blue')
    l2, = axNok.plot(list_days, kron_nox, 'red')
    axNok.set_title(f"{current_data_type} verdier")

    if avg_kron_nox != 0:
        percentage_nord_to_kron = (avg_nord_nox / avg_kron_nox) * 100
        percentage_marked_to_kron = (avg_marked_nox / avg_kron_nox) * 100 if avg_marked_nox != 0 else float('inf')
    else:
        percentage_nord_to_kron = float('inf')
        percentage_marked_to_kron = float('inf')

    legend_labels = ["Nordnes", "Kronstad", "Markert plass"]
    average_info = (f'Avg {current_data_type}: \nKronstad: {avg_kron_nox:.2f}\nNordnes: {avg_nord_nox:.2f} '
                    f'({percentage_nord_to_kron:.2f}%)')
    
    if marked_point != (0, 0):
        average_info += f'\nMarkert: {avg_marked_nox:.2f} ({percentage_marked_to_kron:.2f}%)'
        
    lines = [l1, l2]
    
    if l3 is not None:
        lines.append(l3)
        legend_labels.append("Markert plass")

    axNok.legend(lines, legend_labels, bbox_to_anchor=(0.7, 1.3), loc='upper left')
    axNok.grid(linestyle='--')
    draw_label_and_ticks()

    axBergen.axis('off')
    img = mpimg.imread('Bergen.jpg')
    axBergen.imshow(img)
    axBergen.set_title("Kart Bergen")
    draw_circles_stations()

    axBergen.text(0.01, 1.29, average_info, transform=axBergen.transAxes, fontsize=10,
                   verticalalignment='top', horizontalalignment='left',
                   bbox=dict(facecolor='#D3D3D3', alpha=0.5,
                             edgecolor='black', boxstyle='round,pad=0.5'))

    plt.draw()

def radio_update(label):
    global current_data_type
    current_data_type = label
    plot_graph()

slider.on_changed(slider_update)
radio.on_clicked(radio_update)

plt.connect('button_press_event', on_click)

plot_graph()
plt.show()
