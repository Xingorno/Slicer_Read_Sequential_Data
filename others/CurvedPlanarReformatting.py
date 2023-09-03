# Get a dental CT scan
import SampleData
volumeNode = SampleData.SampleDataLogic().downloadDentalSurgery()[1]

# Define curve
curveNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsCurveNode')
curveNode.CreateDefaultDisplayNodes()
curveNode.GetCurveGenerator().SetNumberOfPointsPerInterpolatingSegment(25) # add more curve points between control points than the default 10
curveNode.AddControlPoint(vtk.vtkVector3d(-45.85526315789473,	-104.59210526315789,	74.67105263157896))
curveNode.AddControlPoint(vtk.vtkVector3d(-50.9078947368421,	-90.06578947368418,	66.4605263157895))
curveNode.AddControlPoint(vtk.vtkVector3d(-62.27631578947368,	-78.06578947368419,	60.7763157894737))
curveNode.AddControlPoint(vtk.vtkVector3d(-71.86705891666716,	-58.04403581456746,	57.84679891116521))
curveNode.AddControlPoint(vtk.vtkVector3d(-74.73084356325877,	-48.67611043794342,	57.00664267528636))
curveNode.AddControlPoint(vtk.vtkVector3d(-88.17105263157895,	-35.75,	55.092105263157904))
curveNode.AddControlPoint(vtk.vtkVector3d(-99.53947368421052,	-35.75,	55.092105263157904))
curveNode.AddControlPoint(vtk.vtkVector3d(-107.75,	-43.96052631578948,	55.092105263157904))
curveNode.AddControlPoint(vtk.vtkVector3d(-112.80263157894736,	-59.118421052631575,	56.355263157894754))
curveNode.AddControlPoint(vtk.vtkVector3d(-115.32894736842104,	-73.01315789473684,	60.144736842105274))
curveNode.AddControlPoint(vtk.vtkVector3d(-125.43421052631578,	-83.74999999999999,	60.7763157894737))
curveNode.AddControlPoint(vtk.vtkVector3d(-132.3815789473684,	-91.96052631578947,	63.934210526315795))
curveNode.AddControlPoint(vtk.vtkVector3d(-137.43421052631578,	-103.96052631578947,	67.72368421052633))

sliceNode = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')
rotationAngleDeg = 180
sliceNode.SetFieldOfView(40,40,1) # zoom in

appLogic = slicer.app.applicationLogic()
sliceLogic = appLogic.GetSliceLogic(sliceNode)
sliceLayerLogic = sliceLogic.GetBackgroundLayer()
reslice = sliceLayerLogic.GetReslice()
reslicedImage = vtk.vtkImageData()

# Straightened volume (useful for example for visualization of curved vessels)
straightenedVolume = slicer.modules.volumes.logic().CloneVolume(volumeNode, 'straightened')

# Capture a number of slices orthogonal to the curve and append them into a volume.
# sliceToWorldTransform = curvePointToWorldTransform * RotateZ(rotationAngleDeg)
curvePointToWorldTransform = vtk.vtkTransform()
sliceToWorldTransform = vtk.vtkTransform()
sliceToWorldTransform.Concatenate(curvePointToWorldTransform)
sliceToWorldTransform.RotateZ(rotationAngleDeg)
sliceNode.SetXYZOrigin(0,0,0)
numberOfPoints = curveNode.GetCurvePointsWorld().GetNumberOfPoints()
append = vtk.vtkImageAppend()

for pointIndex in range(numberOfPoints):
    print(pointIndex)
    curvePointToWorldMatrix = vtk.vtkMatrix4x4()
    curveNode.GetCurvePointToWorldTransformAtPointIndex(pointIndex, curvePointToWorldMatrix)
    curvePointToWorldTransform.SetMatrix(curvePointToWorldMatrix)
    sliceToWorldTransform.Update()
    sliceNode.GetSliceToRAS().DeepCopy(sliceToWorldTransform.GetMatrix())
    sliceNode.UpdateMatrices()
    slicer.app.processEvents()
    tempSlice = vtk.vtkImageData()
    tempSlice.DeepCopy(reslice.GetOutput())
    append.AddInputData(tempSlice)

append.SetAppendAxis(2)
append.Update()
straightenedVolume.SetAndObserveImageData(append.GetOutput())

# Create panoramic volume by mean intensity projection along an axis of the straightened volume
import numpy as np
panoramicVolume = slicer.modules.volumes.logic().CloneVolume(straightenedVolume, 'panoramic')
panoramicImageData = panoramicVolume.GetImageData()
straightenedImageData = straightenedVolume.GetImageData()
panoramicImageData.SetDimensions(straightenedImageData.GetDimensions()[2], straightenedImageData.GetDimensions()[1], 1)
panoramicImageData.AllocateScalars(straightenedImageData.GetScalarType(), straightenedImageData.GetNumberOfScalarComponents())
panoramicVolumeArray = slicer.util.arrayFromVolume(panoramicVolume)
straightenedVolumeArray = slicer.util.arrayFromVolume(straightenedVolume)
panoramicVolumeArray[0, :, :] = np.flip(straightenedVolumeArray.mean(2).T)
slicer.util.arrayFromVolumeModified(panoramicVolume)
panoramicVolume.SetSpacing(4.0, 0.5, 0.5) # just approximate spacing (would need to properly compute from FOV and image size)
sliceNode.SetOrientationToAxial()
slicer.util.setSliceViewerLayers(background=panoramicVolume, fit=True)