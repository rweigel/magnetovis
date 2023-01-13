def GetTransferFunctionPresets(format="dict"):

  # Not yet used.

  import json
  from paraview import servermanager

  presets = servermanager.vtkSMTransferFunctionPresets.GetInstance()
  np = presets.GetNumberOfPresets()
  names = []
  presets_dict = {}
  for p in range(np):
    names.append(presets.GetPresetName(p))
    presets_dict[presets.GetPresetName(p)] = \
        json.loads(presets.GetPresetAsString(p))

  if format == "dict":
    return presets_dict
  if format == "namelist":
    return names

if __name__ == "__main__":
  print(GetTransferFunctionPresets())