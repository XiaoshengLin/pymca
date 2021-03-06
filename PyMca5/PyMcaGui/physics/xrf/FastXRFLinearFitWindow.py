#/*##########################################################################
#
# The PyMca X-Ray Fluorescence Toolkit
#
# Copyright (c) 2004-2015 European Synchrotron Radiation Facility
#
# This file is part of the PyMca X-ray Fluorescence Toolkit developed at
# the ESRF by the Software group.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#############################################################################*/
__author__ = "V. Armando Sole - ESRF Data Analysis"
__contact__ = "sole@esrf.fr"
__license__ = "MIT"
__copyright__ = "European Synchrotron Radiation Facility, Grenoble, France"

from PyMca5.PyMcaGui import PyMcaQt as qt
from PyMca5.PyMcaGui import PyMca_Icons
IconDict = PyMca_Icons.IconDict
from PyMca5.PyMcaGui import PyMcaFileDialogs
try:
    import h5py
    hasH5py = True
except ImportError:
    hasH5py = False


class FastXRFLinearFitWindow(qt.QWidget):
    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self.setWindowTitle("FastXRFLinearFitWindow")
        self.setWindowIcon(qt.QIcon(qt.QPixmap(IconDict['gioconda16'])))
        self.mainLayout = qt.QGridLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # configuration file
        configLabel = qt.QLabel(self)
        configLabel.setText("Fit Configuration File:")
        self._configLine = qt.QLineEdit(self)
        self._configLine.setReadOnly(True)

        self._configButton = qt.QPushButton(self)
        self._configButton.setText("Browse")
        self._configButton.setAutoDefault(False)
        self._configButton.clicked.connect(self.browseConfigurationFile)

        # output directory
        outdirLabel = qt.QLabel(self)
        outdirLabel.setText("Output dir:")
        self._outdirLine = qt.QLineEdit(self)
        self._outdirLine.setReadOnly(True)

        self._outdirButton = qt.QPushButton(self)
        self._outdirButton.setText('Browse')
        self._outdirButton.setAutoDefault(False)
        self._outdirButton.clicked.connect(self.browseOutputDir)

        # output root
        outrootLabel = qt.QLabel(self)
        outrootLabel.setText("Output root:")
        self._outrootLine = qt.QLineEdit(self)
        self._outrootLine.setReadOnly(False)
        self._outrootLine.setText("IMAGES")

        # output entry
        outentryLabel = qt.QLabel(self)
        outentryLabel.setText("Output entry:")
        self._outentryLine = qt.QLineEdit(self)
        self._outentryLine.setReadOnly(False)
        self._outentryLine.setText("images")

        # output process
        outnameLabel = qt.QLabel(self)
        outnameLabel.setText("Output name:")
        self._outnameLabel = outnameLabel
        self._outnameLine = qt.QLineEdit(self)
        self._outnameLine.setText("fast_xrf_fit")

        # fit options
        boxLabel1 = qt.QLabel(self)
        boxLabel1.setText("Fit options:")
        self._boxContainer1 = qt.QWidget(self) 
        self._boxContainerLayout1 = qt.QHBoxLayout(self._boxContainer1)
        self._boxContainerLayout1.setContentsMargins(0, 0, 0, 0)
        self._boxContainerLayout1.setSpacing(0)
        
        # save options
        boxLabel2 = qt.QLabel(self)
        boxLabel2.setText("Save options:")
        self._boxContainer2 = qt.QWidget(self) 
        self._boxContainerLayout2 = qt.QHBoxLayout(self._boxContainer2)
        self._boxContainerLayout2.setContentsMargins(0, 0, 0, 0)
        self._boxContainerLayout2.setSpacing(0)
        
        # concentrations
        self._concentrationsBox = qt.QCheckBox(self._boxContainer1)
        self._concentrationsBox.setText("calculate concentrations")
        self._concentrationsBox.setChecked(False)
        self._concentrationsBox.setEnabled(True)

        # diagnostics
        self._diagnosticsBox = qt.QCheckBox(self._boxContainer1)
        self._diagnosticsBox.setText("calculate diagnostics")
        self._diagnosticsBox.setChecked(False)
        self._diagnosticsBox.setEnabled(hasH5py)

        # repeat fit on negative contributions
        self._fitAgainBox = qt.QCheckBox(self._boxContainer1)
        self._fitAgainBox.setText("Repeat fit on negative contributions")
        self._fitAgainBox.setChecked(True)
        self._fitAgainBox.setEnabled(True)
        text  = "Fit of pixels with negative peak area\n"
        text += "contributions will be repeated.\n"
        text += "This can seriously slow down the process\n"
        text += "if your sample model is far from the truth."
        self._fitAgainBox.setToolTip(text)

        # generate tiff files
        self._tiffBox = qt.QCheckBox(self._boxContainer2)
        self._tiffBox.setText("TIFF")
        self._tiffBox.setChecked(False)
        self._tiffBox.setEnabled(True)
        
        # generate csv file
        self._csvBox = qt.QCheckBox(self._boxContainer2)
        self._csvBox.setText("CSV")
        self._csvBox.setChecked(False)
        self._csvBox.setEnabled(True)
        
        # generate edf file
        self._edfBox = qt.QCheckBox(self._boxContainer2)
        self._edfBox.setText("EDF")
        self._edfBox.setChecked(True)
        self._edfBox.setEnabled(True)
        
        # generate hdf5 file
        self._h5Box = qt.QCheckBox(self._boxContainer2)
        self._h5Box.setText("HDF5")
        self._h5Box.setChecked(hasH5py)
        self._h5Box.setEnabled(hasH5py)
        self._h5Box.stateChanged.connect(self.toggleH5)
        self.toggleH5(hasH5py)

        # overwrite output
        self._overwriteBox = qt.QCheckBox(self._boxContainer2)
        self._overwriteBox.setText("Overwrite")
        self._overwriteBox.setChecked(True)
        self._overwriteBox.setEnabled(True)
        
        self._boxContainerLayout1.addWidget(self._concentrationsBox)
        self._boxContainerLayout1.addWidget(self._fitAgainBox)
        self._boxContainerLayout1.addWidget(self._diagnosticsBox)
        self._boxContainerLayout2.addWidget(self._h5Box)
        self._boxContainerLayout2.addWidget(self._edfBox)
        self._boxContainerLayout2.addWidget(self._csvBox)
        self._boxContainerLayout2.addWidget(self._tiffBox)
        self._boxContainerLayout2.addWidget(self._overwriteBox)
        
        # weight method
        self._weightWidget = qt.QWidget(self)
        self._weightWidget.mainLayout = qt.QHBoxLayout(self._weightWidget)
        self._weightWidget.mainLayout.setContentsMargins(0, 0, 0, 0)
        self._weightWidget.mainLayout.setSpacing(0)
        self._weightButtonGroup = qt.QButtonGroup(self._weightWidget)
        i = 0
        weightLabel = qt.QLabel(self)
        weightLabel.setText("Weight policy: ")
        for txt in ["No Weight (Fastest)", "Average Weight (Fast)", "Individual Weights (slow)"]:
            button = qt.QRadioButton(self._weightWidget)
            button.setText(txt)
            self._weightButtonGroup.addButton(button)
            self._weightButtonGroup.setId(button, i)
            self._weightWidget.mainLayout.addWidget(button)
            i += 1
        self._weightButtonGroup.buttons()[0].setChecked(True)
        #self._weightWidget.mainLayout.addWidget(qt.HorizontalSpacer(self._weightWidget))

        i = 0
        self.mainLayout.addWidget(configLabel, i, 0)
        self.mainLayout.addWidget(self._configLine, i, 1)
        self.mainLayout.addWidget(self._configButton, i, 2)
        i += 1
        self.mainLayout.addWidget(outdirLabel, i, 0)
        self.mainLayout.addWidget(self._outdirLine, i, 1)
        self.mainLayout.addWidget(self._outdirButton, i, 2)
        i += 1
        self.mainLayout.addWidget(outrootLabel, i, 0)
        self.mainLayout.addWidget(self._outrootLine, i, 1)
        i += 1
        self.mainLayout.addWidget(outentryLabel, i, 0)
        self.mainLayout.addWidget(self._outentryLine, i, 1)
        i += 1
        self.mainLayout.addWidget(outnameLabel, i, 0)
        self.mainLayout.addWidget(self._outnameLine, i, 1)
        i += 1
        self.mainLayout.addWidget(weightLabel, i, 0)
        self.mainLayout.addWidget(self._weightWidget, i, 1, 1, 1)
        i += 1
        self.mainLayout.addWidget(boxLabel1, i, 0)
        self.mainLayout.addWidget(self._boxContainer1, i, 1, 1, 1)
        i += 1
        self.mainLayout.addWidget(boxLabel2, i, 0)
        self.mainLayout.addWidget(self._boxContainer2, i, 1, 1, 1)
        
    def sizeHint(self):
        return qt.QSize(int(1.8 * qt.QWidget.sizeHint(self).width()),
                        qt.QWidget.sizeHint(self).height())

    def browseConfigurationFile(self):
        f = PyMcaFileDialogs.getFileList(parent=self,
                                     filetypelist=["Configuration files (*.cfg)"],
                                     message="Open a fit configuration file",
                                     mode="OPEN",
                                     single=True)
        if len(f):
            self._configLine.setText(f[0])

    def browseOutputDir(self):
        f = PyMcaFileDialogs.getExistingDirectory(parent=self,
                                     message="Please select output directory",
                                     mode="OPEN")
        if len(f):
            self._outdirLine.setText(f)

    def toggleH5(self, state):
        h5Out = bool(state)
        self._outnameLine.setReadOnly(not h5Out)
        self._outnameLine.setEnabled(h5Out)
        self._outnameLabel.setEnabled(h5Out)
        self._diagnosticsBox.setEnabled(h5Out)
        if h5Out:
            self._outnameLine.setStyleSheet("")
        else:
            self._outnameLine.setStyleSheet("color: gray; background-color: darkGray")

    def getParameters(self):
        ddict = {}
        fit = {}
        ddict['fit'] = fit
        fit['configuration'] = qt.safe_str(self._configLine.text())
        fit['weight'] = self._weightButtonGroup.checkedId()
        fit['concentrations'] = self._concentrationsBox.isChecked()
        fit['refit'] = self._fitAgainBox.isChecked()
        output = {}
        ddict['output'] = output
        output['outputDir'] = qt.safe_str(self._outdirLine.text()).replace(" ", "")
        output['outputRoot'] = qt.safe_str(self._outrootLine.text()).replace(" ", "")
        output['fileEntry'] = qt.safe_str(self._outentryLine.text()).replace(" ", "")
        output['fileProcess'] = qt.safe_str(self._outnameLine.text()).replace(" ", "")
        output['tif'] = int(self._tiffBox.isChecked())
        output['csv'] = int(self._csvBox.isChecked())
        output['edf'] = int(self._edfBox.isChecked())
        output['h5'] = int(self._h5Box.isChecked())
        output['overwrite'] = int(self._overwriteBox.isChecked())
        diagnostics = int(self._diagnosticsBox.isChecked())
        output['saveData'] = diagnostics
        output['saveFit'] = diagnostics
        output['saveResiduals'] = diagnostics
        return ddict

class FastXRFLinearFitDialog(qt.QDialog):
    def __init__(self, parent=None):
        qt.QDialog.__init__(self, parent)
        self.setWindowTitle("Fast XRF Linear Fit Dialog")
        self.setWindowIcon(qt.QIcon(qt.QPixmap(IconDict['gioconda16'])))
        self.mainLayout = qt.QGridLayout(self)
        self.mainLayout.setContentsMargins(10, 10, 10, 10)
        self.parametersWidget = FastXRFLinearFitWindow(self)

        self.rejectButton= qt.QPushButton(self)
        self.rejectButton.setAutoDefault(False)
        self.rejectButton.setText("Cancel")

        self.acceptButton= qt.QPushButton(self)
        self.acceptButton.setAutoDefault(False)
        self.acceptButton.setText("OK")

        self.rejectButton.clicked.connect(self.reject)
        self.acceptButton.clicked.connect(self.accept)

        self.mainLayout.addWidget(self.parametersWidget, 0, 0, 5, 4)
        self.mainLayout.addWidget(self.rejectButton, 6, 1)
        self.mainLayout.addWidget(self.acceptButton, 6, 2)

    def getParameters(self):
        return self.parametersWidget.getParameters()

if __name__ == "__main__":
    app = qt.QApplication([])
    w = FastXRFLinearFitDialog()
    ret = w.exec_()
    if ret:
        print(w.getParameters())
    #app.exec_()
