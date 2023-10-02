import matplotlib.pyplot as plt
import numpy as np
import math


class Plots:
    def tlplot(self, values, timestamps):
        plt.bar(timestamps, values)
        plt.xlabel('Timestamps')
        plt.ylabel('Training load')
        plt.show()

    def plot_ffm(self, PTE, NTE, P, days):


        # Plotting both the curves simultaneously
        plt.plot(days, PTE, color='g', label='PTE')
        plt.plot(days, NTE, color='r', label='NTE')
        plt.plot(days, P, color ='b', label='modeled performance')
        plt.axhline(y=0, linestyle='--', color='grey', label='P(0)')

        # Naming the x-axis, y-axis and the whole graph
        plt.xlabel("Days")
        plt.ylabel("Performance")
        plt.title("")

        # Adding legend, which helps us recognize the curve according to it's color
        plt.legend()

        # To load the display window
        plt.show()