from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ContourPlot:
    def __init__(self, times, f0, voiced_flag, voiced_probs, title="Pitch Contour", xlabel="Time (s)", ylabel="Frequency (Hz)"):
        self.times = times
        self.f0 = f0
        self.voiced_flag = voiced_flag
        self.voiced_probs = voiced_probs
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel

    def plot_pitch(self):
        fig = Figure(figsize=(10, 6),dpi=100, facecolor='#12121c')
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)

        # style plot
        ax.plot(self.times, self.f0, label = 'F0',color='#8e44ad', linewidth=2)
        ax.fill_between(self.times, 0, self.f0, where=self.voiced_flag, color='#8e44ad', alpha=0.3, label='Voiced Regions')

        ax.set_title(self.title, fontsize=16, color='#e6e6f0')
        ax.set_xlabel(self.xlabel, fontsize=14, color='#e6e6f0')
        ax.set_ylabel(self.ylabel, fontsize=14, color='#e6e6f0')
        ax.tick_params(axis='both', colors='#e6e6f0')
        ax.set_facecolor('#12121c')
        for spine in ax.spines.values():
            spine.set_color('#e6e6f0')

        ax.grid(True, linestyle='--',alpha=0.5)
        ax.legend(loc='upper right')

        return canvas