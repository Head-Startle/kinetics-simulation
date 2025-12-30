import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation
import numpy as np
from pathlib import Path


def interactive_plot(times, data, species, title=None, outdir=None):
    # set default save directory for toolbar save dialog
    if outdir:
        plt.rcParams['savefig.directory'] = str(outdir)

    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    lines = []
    markers = []
    for i, name in enumerate(species):
        ln, = ax.plot([], [], label=name)
        mk, = ax.plot([], [], marker='o', markersize=4, linestyle='')
        lines.append(ln)
        markers.append(mk)

    ax.set_xlabel('time')
    ax.set_ylabel('concentration')
    ax.set_xlim(times[0], times[-1])
    ax.set_ylim(min(0, data.min()), data.max() * 1.15)
    ax.legend(loc='upper right')

    axcolor = 'lightgoldenrodyellow'
    axpos = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(axpos, 't', 0, len(times) - 1, valinit=0, valstep=1)

    axplay = plt.axes([0.8, 0.02, 0.1, 0.04])
    bplay = Button(axplay, 'Play')
    axrev = plt.axes([0.65, 0.02, 0.1, 0.04])
    brev = Button(axrev, 'Reverse')

    annot = ax.text(0.02, 0.95, '', transform=ax.transAxes, va='top')

    anim = {'running': False, 'direction': 1}

    def update_plot(idx):
        idx = int(idx)
        for i, ln in enumerate(lines):
            ln.set_data(times[:idx+1], data[:idx+1, i])
            markers[i].set_data([times[idx]], [data[idx, i]])
            markers[i].set_color(ln.get_color())
        linestr = [f'{species[i]}={data[idx,i]:.4g}' for i in range(len(species))]
        annot.set_text(f't={times[idx]:.4g}\n' + ', '.join(linestr))
        fig.canvas.draw_idle()

    update_plot(0)
    slider.on_changed(update_plot)

    def play(event):
        anim['running'] = not anim['running']
        bplay.label.set_text('Pause' if anim['running'] else 'Play')

    def rev(event):
        anim['direction'] *= -1
        brev.label.set_text('Forward' if anim['direction'] < 0 else 'Reverse')

    bplay.on_clicked(play)
    brev.on_clicked(rev)

    def update_anim(frame):
        if anim['running']:
            idx = int(slider.val)
            new_idx = idx + anim['direction']
            if new_idx >= len(times):
                new_idx = 0
            elif new_idx < 0:
                new_idx = len(times) - 1
            slider.set_val(new_idx)
        return []

    fig.suptitle(title or 'Kinetics Simulation')
    fig.canvas.manager.set_window_title(title or 'Kinetics Simulation')
    fig.ani = FuncAnimation(fig, update_anim, interval=30, cache_frame_data=False)
    print('Simulation complete. Opening plot window...')
    plt.show()
