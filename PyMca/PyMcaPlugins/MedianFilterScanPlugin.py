import numpy

try:
    import Plugin1DBase
except ImportError:
    from . import Plugin1DBase

from PyMca import SpecfitFuns
from PyMca.PyMcaSciPy.signal.median import medfilt1d

class MedianFilterScanPlugin(Plugin1DBase.Plugin1DBase):
    def __init__(self, plotWindow, **kw):
        Plugin1DBase.Plugin1DBase.__init__(self, plotWindow, **kw)
        self.__randomization = True
        self.__methodKeys = []
        self.methodDict = {}
        text = "Use a random order instead\n"
        text += "of the plotting order."
        info = text
        icon = None
        function = self.toggleRandomization
        method = "Toggle Randomization OFF"
        self.methodDict[method] = [function,
                                   info,
                                   icon]
        self.__methodKeys.append(method)
        method = "Toggle Randomization ON"
        text = "Use plotting order instead\n"
        text += "of a random order."
        self.methodDict[method] = [function,
                                   info,
                                   icon]
        self.__methodKeys.append(method)
        function = self.applyMedianFilter
        for i in [3, 5, 7, 9]:
            info = "Replace curves by %d-point median filter" % i
            method = "Replace by %d-point median filter" % i
            self.methodDict[method] = [function,
                                       info,
                                       icon]
            self.__methodKeys.append(method)
        
    #Methods to be implemented by the plugin
    def getMethods(self, plottype=None):
        """
        A list with the NAMES  associated to the callable methods
        that are applicable to the specified plot.

        Plot type can be "SCAN", "MCA", None, ...        
        """
        if self.__randomization:
            return self.__methodKeys[0:1] +  self.__methodKeys[2:]
        else:
            return self.__methodKeys[1:]

    def getMethodToolTip(self, name):
        """
        Returns the help associated to the particular method name or None.
        """
        return self.methodDict[name][1]

    def getMethodPixmap(self, name):
        """
        Returns the pixmap associated to the particular method name or None.
        """
        return None

    def applyMethod(self, name):
        """
        The plugin is asked to apply the method associated to name.
        """
        if name.startswith('Toggle'):
            return self.methodDict[name][0]()
        n = int(name.split('-')[0].split()[-1])
        return self.applyMedianFilter(width=n)

    def toggleRandomization(self):
        if self.__randomization:
            self.__randomization = False
        else:
            self.__randomization = True

    def applyMedianFilter(self, width=3):
        curves = self.getAllCurves()
        nCurves = len(curves)
        if nCurves < width:
            raise ValueError("At least %d curves needed" % width)
            return

        if self.__randomization:
            indices = numpy.random.permutation(nCurves)
        else:
            indices = range(nCurves)

        # get active curve            
        activeCurve = self.getActiveCurve()
        if activeCurve is None:
            activeCurve = curves[0]

        #sort the values
        x0 = activeCurve[0][:]
        y0 = activeCurve[1][:]
        idx = numpy.argsort(x0, kind='mergesort')
        x0 = numpy.take(x0, idx)
        y0 = numpy.take(y0, idx)
        xmin = x0.min()
        xmax = x0.max()
        x0.shape = -1, 1
        nChannels = x0.shape[0]

        # built a couple of temporary array of spectra for handy access
        tmpArray = numpy.zeros((nChannels, nCurves), numpy.float)
        medianSpectra = numpy.zeros((nChannels, nCurves), numpy.float)
        i = 0
        for idx in indices:
            x, y, legend, info = curves[idx][0:4]
            #sort the values
            x = x[:]
            idx = numpy.argsort(x, kind='mergesort')
            x = numpy.take(x, idx)
            y = numpy.take(y, idx)

            #take the portion ox x between limits
            idx = numpy.nonzero((x>=xmin) & (x<=xmax))[0]
            if not len(idx):
                # no overlap
                continue
            
            x = numpy.take(x, idx)
            x.shape = -1, 1
            if numpy.allclose(x, x0):
                # no need for interpolation
                pass
            else:
                # we have to interpolate
                x.shape = -1
                xi = x0[:]
                y = SpecfitFuns.interpol([x], y, xi, y0.min())
            y.shape = -1 
            tmpArray[:, i] = y
            i += 1

        # now perform the median filter
        for i in range(nChannels):
            medianSpectra[i, :] = medfilt1d(tmpArray[i,:],
                                            kernel_size=width)
        tmpArray = None
        # now get the final spectrum
        y = medianSpectra.sum(axis=1) / nCurves
        x0.shape = -1
        y.shape = x0.shape
        legend = "%d Median from %s to %s" % (width,
                                              curves[0][2],
                                              curves[-1][2])
        self.addCurve(x0,
                      y,
                      legend=legend,
                      info=None,
                      replot=True,
                      replace=True)

MENU_TEXT = "1D Median Filter"
def getPlugin1DInstance(plotWindow, **kw):
    ob = MedianFilterScanPlugin(plotWindow)
    return ob

if __name__ == "__main__":
    from PyMca import PyMcaQt as qt
    app = qt.QApplication([])
    from PyMca import Plot1D
    x = numpy.arange(100.)
    y = x * x
    plot = Plot1D.Plot1D()
    plot.addCurve(x, y, "dummy")
    plot.addCurve(x+100, -x*x)
    plugin = getPlugin1DInstance(plot)
    for method in plugin.getMethods():
        print(method, ":", plugin.getMethodToolTip(method))
    plugin.applyMethod(plugin.getMethods()[0])
    curves = plugin.getAllCurves()
    for curve in curves:
        print(curve[2])
    print("LIMITS = ", plugin.getGraphYLimits())
    #app = qt.QApplication()