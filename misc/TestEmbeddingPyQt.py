# From ParaView email list. (TODO: Find link.)

# See also
#  https://discourse.paraview.org/t/run-paraview-in-pyqt5-widget-python/8243/2
#  https://discourse.paraview.org/t/dynamic-paraview-plugins-using-python/1793
#  https://public.kitware.com/pipermail/paraview-developers/2012-April/001491.html
#  https://markmail.org/message/pga4zilxynswhdef#query:+page:1+mid:f5zuw7izv5e262md+state:results

from paraview.util.vtkAlgorithm import *
from paraview import vtk

from PyQt5 import QtCore, QtGui, QtWidgets

# ------------------------------------
# A simple dialog
# ------------------------------------
class TestDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout(self)
        qbtn = QtWidgets.QPushButton('Quit', self)
        # qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.clicked.connect(self.on_click)
        self.setWindowTitle('Quit button')
        layout.addWidget(qbtn)
        self.setLayout(layout)
        self.show()

    def on_click(self):
        print('Clicked')
        self.close()


#------------------------------------------------------------------------------
# A filter example.
#------------------------------------------------------------------------------
@smproxy.filter()
@smproperty.input(name="InputDataset", port_index=0)
@smdomain.datatype(dataTypes=["vtkDataSet"], composite_data_supported=False)
class TestEmbeddingPyQt(VTKPythonAlgorithmBase):
    def __init__(self):
        VTKPythonAlgorithmBase.__init__(self, nInputPorts=1, nOutputPorts=1, outputType="vtkPolyData")

    def FillInputPortInformation(self, port, info):
        if port == 0:
            info.Set(self.INPUT_REQUIRED_DATA_TYPE(), "vtkDataSet")

        return 1

    @smproperty.xml(""" 
                    <Property
                        name="NextStep"
                        command="NextStep"
                    panel_widget="command_button"/>
                """)
    def NextStep(self):
        print('NextStep')
        dialog = TestDialog()
        dialog.exec_()

    def RequestData(self, request, inInfoVec, outInfoVec):
        from vtkmodules.vtkCommonDataModel import vtkDataSet, vtkPolyData
        input0 = vtkDataSet.GetData(inInfoVec[0], 0)
        output = vtkPolyData.GetData(outInfoVec, 0)
        # do work
        print("Pretend work done!")

        return 1
