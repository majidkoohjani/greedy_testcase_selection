import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    @staticmethod
    def plot(xPoints: list = None, yPoints: list = None, multiLinePlot: list = None, title: str = "", xLabel: str = "", yLabel: str = ""):
        # x = np.array(xPoints)
        # y = np.array(yPoints)
        if multiLinePlot != None:
            for line in multiLinePlot:
                plt.plot(line["x"], line["y"], label=line["title"])
        else:
            plt.plot(xPoints, yPoints)
            plt.xlabel(xLabel)
            plt.ylabel(yLabel)
            plt.title(title)
        plt.legend()
        plt.show()

    @staticmethod
    def plotInMultiPlot(multiPlot: list = None):
        for index, plot in enumerate(multiPlot):
            ax = plt.subplot(1, 2, index + 1)
            ax.set_xlabel(plot["xLabel"])
            ax.set_ylabel(plot["yLabel"])
            ax.set_title(plot["title"])
            plt.plot(plot["x"], plot["y"], color=plot["color"], lw=plot["lw"] , ls=plot["ls"])
        plt.show()