import matplotlib.pyplot as plt
import math

class Plotter:
    @staticmethod
    def plotLine(multiLinePlot: list = [], title: str = "", xLabel: str = "", yLabel: str = ""):
        for line in multiLinePlot:
            plt.plot(line["x"], line["y"], label=line["title"], color=line["color"], lw=line["lw"] , ls=line["ls"])

        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.title(title)
        plt.legend()
        plt.show()

    @staticmethod
    def plotSubplot(multiPlot: list = None):
        rowsCount = math.ceil(len(multiPlot) / 2)

        for index, plot in enumerate(multiPlot):
            ax = plt.subplot(rowsCount, 2, index + 1)
            ax.set_xlabel(plot["xLabel"])
            ax.set_ylabel(plot["yLabel"])
            ax.set_title(plot["title"])
            plt.plot(plot["x"], plot["y"], color=plot["color"], lw=plot["lw"] , ls=plot["ls"])
        plt.show()