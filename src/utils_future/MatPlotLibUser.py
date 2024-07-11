import matplotlib.pyplot as plt


class MatPlotLibUser:
    @staticmethod
    def remove_grids():
        ax = plt.gca()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)
