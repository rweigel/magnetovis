from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from paraview.util.vtkAlgorithm import smproxy, smproperty, smhint, smdomain

from magnetovis.Plugins.StructuredGrid import StructuredGridPlugin

@smproxy.source(name="MagnetovisDipole", label="MagnetovisDipole")
@smhint.xml('<ShowInMenu category="Magnetovis"/>')
class DipolePlugin(VTKPythonAlgorithmBase):

    from magnetovis import extract_script
    from magnetovis.Objects.StructuredGrid import Script

    # This is used to populate Script text area
    Script = extract_script(Script, None, xml_encode=True)
    Script = "# If script modified, drop-down values will be ignored&#xa;" + Script

    # TODO: The panel_visibility is ignored here.
    panel_visibility = "never"
    DefaultPointFunction = "dipole(M=7.788E22)"
 
    def __init__(self, **default_values):

        VTKPythonAlgorithmBase.__init__(self,
                nInputPorts=0,
                nOutputPorts=1,
                outputType='vtkStructuredGrid')

        StructuredGridPlugin.__init__(self)

        # Extract kwargs and defaults from point function
        # TODO: Do once for each point function
        def GetKwargs(self):
            from magnetovis import extract_kwargs, iso2ints
            kwargs = extract_kwargs(self.point_function)
            kwargs['name'] = self.point_function.split("(")[0]
            kwargs = {
                    'extents': self.extents,
                    'point_array_functions': {"dipole": {"array_name": "B", "M": self.M}},
                    'time': iso2ints(self.time),
                    'coord_sys': self.coord_sys,
                    'Nx': self.Nx,
                    'Ny': self.Ny,
                    'Nz': self.Nz
            }
            return kwargs

        self.GetKwargs = GetKwargs

    RequestData = StructuredGridPlugin.RequestData
    RequestInformation = StructuredGridPlugin.RequestInformation

    # Ordering of GUI elements is alphabetical. See proposed fix for this at
    # https://gitlab.kitware.com/paraview/paraview/-/merge_requests/2846

    @smproperty.xml("""<DoubleVectorProperty 
        name="DipoleMoment" 
        label="Dipole Moment"
        command="SetDipoleMoment" 
        number_of_elements="1"
        default_values="7.788E22">
       <Documentation>Dipole moment in A/m^2</Documentation>
     </DoubleVectorProperty>""")
    def SetDipoleMoment(self, DipoleMoment):
        print("SetDipoleMoment called.")
        self.M = DipoleMoment
        self.Modified()

    SetPointFunction = StructuredGridPlugin.SetPointFunctionWrapper(DefaultPointFunction, panel_visibility=panel_visibility)
    SetCoordinateSystem = StructuredGridPlugin.SetCoordinateSystem
    SetNxNyNz = StructuredGridPlugin.SetNxNyNz
    SetTime =  StructuredGridPlugin.SetTime
    SetXExtent =  StructuredGridPlugin.SetXExtent
    SetYExtent =  StructuredGridPlugin.SetYExtent
    SetZExtent =  StructuredGridPlugin.SetZExtent
    SetScript = StructuredGridPlugin.SetScript
