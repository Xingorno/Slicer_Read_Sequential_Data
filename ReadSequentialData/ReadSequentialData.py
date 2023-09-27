import logging
import os
import numpy as np
import vtk
import re
import string
import slicer
import time
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin


#
# ReadSequentialData
#

class ReadSequentialData(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ReadSequentialData"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["John Doe (AnyWare Corp.)"]  # TODO: replace with "Firstname Lastname (Organization)"
    # TODO: update with short description of the module and a link to online module documentation
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#ReadSequentialData">module documentation</a>.
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""

    # Additional initialization step after application startup is complete
    # slicer.app.connect("startupCompleted()", registerSampleData)



#
# ReadSequentialDataWidget
#

class ReadSequentialDataWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

    slicer.mymod = self

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/ReadSequentialData.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = ReadSequentialDataLogic()

    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    
    self.ui.lineEdit_USSeqDir.connect('textChanged(QString)', self.updateParameterNodeFromGUI)
    self.ui.lineEdit_TransSeqDir.connect('textChanged(QString)', self.updateParameterNodeFromGUI)
    self.ui.lineEdit_ScalingDir.connect('textChanged(QString)', self.updateParameterNodeFromGUI)
    self.ui.lineEdit_CTDir.connect('textChanged(QString)', self.updateParameterNodeFromGUI)
    self.ui.lineEdit_ReslicedImgDir.connect('textChanged(QString)', self.updateParameterNodeFromGUI)
    self.ui.checkBox_flip.connect("toggled(bool)", self.updateParameterNodeFromGUI)
    self.ui.comboBox_USSeq.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.comboBox_TransSeq.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.comboBox_ScalTrans.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.comboBox_CT.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)

    # Buttons
    self.ui.pushButton_USSeq.connect('clicked(bool)', self.onPushButton_USSeq)
    self.ui.pushButton_TransSeq.connect('clicked(bool)', self.onPushButton_TransSeq)
    self.ui.pushButton_loadScaling.connect('clicked(bool)', self.onPushButton_loadScaling)
    self.ui.pushButton_loadCT.connect('clicked(bool)', self.onPushButton_loadCT)
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.ui.saveAllButton.connect('clicked(bool)', self.onSaveAllButton)

    # Make sure parameter node is initialized (needed for module reload)
    self.initializeParameterNode()


  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    # Make sure parameter node exists and observed
    self.initializeParameterNode()

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    # Parameter node will be reset, do not use it anymore
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    """
    Ensure parameter node exists and observed.
    """
    # Parameter node stores all user choices in parameter values, node selections, etc.
    # so that when the scene is saved and reloaded, these settings are restored.

    self.setParameterNode(self.logic.getParameterNode())

    # Select default input nodes if nothing is selected yet to save a few clicks for the user
    

  def setParameterNode(self, inputParameterNode):
    """
    Set and observe parameter node.
    Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    """

    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    # Initial GUI update
    self.updateGUIFromParameterNode()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """
    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    self._updatingGUIFromParameterNode = True

    # Update node selectors and sliders
    self.ui.lineEdit_USSeqDir.setText(self._parameterNode.GetParameter("USSeqDir"))
    self.ui.lineEdit_TransSeqDir.setText(self._parameterNode.GetParameter("TransSeqDir"))
    self.ui.lineEdit_ScalingDir.setText(self._parameterNode.GetParameter("ScalingDir"))
    self.ui.lineEdit_CTDir.setText(self._parameterNode.GetParameter("CTDir"))
    self.ui.lineEdit_ReslicedImgDir.setText(self._parameterNode.GetParameter("ReslicedImgDir"))
    self.ui.checkBox_flip.checked = (self._parameterNode.GetParameter("Flip") == "True")

    self.ui.comboBox_USSeq.setCurrentNode(self._parameterNode.GetNodeReference("USSeq"))
    self.ui.comboBox_TransSeq.setCurrentNode(self._parameterNode.GetNodeReference("TransSeq"))
    self.ui.comboBox_ScalTrans.setCurrentNode(self._parameterNode.GetNodeReference("ScalingTrans"))
    self.ui.comboBox_CT.setCurrentNode(self._parameterNode.GetNodeReference("CT_MRI"))

    self.ui.DataVisibilityCheckBox.checked = (self._parameterNode.GetParameter("VisibilityFlag") == "True")

    # Update buttons states and tooltips
    if self._parameterNode.GetParameter("USSeqDir") and self._parameterNode.GetNodeReference("USSeq"):
      self.ui.pushButton_USSeq.toolTip = "Compute US sequence"
      self.ui.pushButton_USSeq.enabled = True
    else:
      self.ui.pushButton_USSeq.toolTip = "Select input and output nodes"
      self.ui.pushButton_USSeq.enabled = False

    if self._parameterNode.GetParameter("TransSeqDir") and self._parameterNode.GetNodeReference("TransSeq"):
      self.ui.pushButton_TransSeq.toolTip = "Compute transformation sequence"
      self.ui.pushButton_TransSeq.enabled = True
    else:
      self.ui.pushButton_TransSeq.toolTip = "Select input and output nodes"
      self.ui.pushButton_TransSeq.enabled = False
    
    if self._parameterNode.GetParameter("ScalingDir") and self._parameterNode.GetNodeReference("ScalingTrans"):
      self.ui.pushButton_loadScaling.toolTip = "Load scaling transformation"
      self.ui.pushButton_loadScaling.enabled = True
    else:
      self.ui.pushButton_loadScaling.toolTip = "Select input and output nodes"
      self.ui.pushButton_loadScaling.enabled = False
    
    if self._parameterNode.GetParameter("CTDir") and self._parameterNode.GetNodeReference("CT_MRI"):
      self.ui.pushButton_loadCT.toolTip = "Load CT/MRI data"
      self.ui.pushButton_loadCT.enabled = True
    else:
      self.ui.pushButton_loadCT.toolTip = "Select input and output nodes"
      self.ui.pushButton_loadCT.enabled = False

    if self._parameterNode.GetParameter("ReslicedImgDir"):
      self.ui.pushButton_loadCT.toolTip = "Save resliced Image with a assigned folder"
      self.ui.pushButton_loadCT.enabled = True
    else:
      self.ui.pushButton_loadCT.toolTip = "Save resliced Image, but need to give a folder first"
      self.ui.pushButton_loadCT.enabled = False


    # All the GUI updates are done
    self._updatingGUIFromParameterNode = False
    

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """
    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return
    
    wasModified = self._parameterNode.StartModify() # Modify all properties in a single batch

    self._parameterNode.SetParameter("USSeqDir", self.ui.lineEdit_USSeqDir.text)
    self._parameterNode.SetParameter("TransSeqDir", self.ui.lineEdit_TransSeqDir.text)
    self._parameterNode.SetParameter("ScalingDir", self.ui.lineEdit_ScalingDir.text)
    self._parameterNode.SetParameter("CTDir", self.ui.lineEdit_CTDir.text)
    self._parameterNode.SetParameter("ReslicedImgDir", self.ui.lineEdit_ReslicedImgDir.text)
    self._parameterNode.SetParameter("Flip", "True" if self.ui.checkBox_flip.checked else "False")

    self._parameterNode.SetNodeReferenceID("USSeq", self.ui.comboBox_USSeq.currentNodeID)    
    self._parameterNode.SetNodeReferenceID("TransSeq", self.ui.comboBox_TransSeq.currentNodeID)
    self._parameterNode.SetNodeReferenceID("ScalingTrans", self.ui.comboBox_ScalTrans.currentNodeID)
    self._parameterNode.SetNodeReferenceID("CT_MRI", self.ui.comboBox_CT.currentNodeID)

    self._parameterNode.SetParameter("VisibilityFlag", "True" if self.ui.DataVisibilityCheckBox.checked else "False")

    self._parameterNode.EndModify(wasModified)


  
  # Save resliced images
  def onApplyButton(self):
    """
    Run processing when user clicks "Apply" button.
    """
    # with slicer.util.tryWithErrorDisplay("Failed to compute results.", waitCursor=True):
    # volumeNode = self._parameterNode.GetNodeReference("CT_MRI")
    
    dir = self.ui.lineEdit_CTDir.text
    for filename in os.listdir(dir): # making sure the file postfix  is  "image format"
      absolute_filename_ = os.path.join(dir, filename)
      absolute_filename = absolute_filename_.replace("\\", "\\\\") # in the raw version, "\\" will be printed as "\", therefore we replaced "\\" with "\\\\"
      
      #########Test the vtkimage data correctness##############
      reader = vtk.vtkMetaImageReader()
      reader.SetFileName(absolute_filename)
      reader.Update()
      volume_vtk = reader.GetOutput() # vtkimagedata with correct origin, spacing and direction




    # load sequence broswer node
    sequenceBrowserNode = self._parameterNode.GetNodeReference("SequenceBroswerNode_trackedUS")
    NthItem = sequenceBrowserNode.GetSelectedItemNumber()
    
    # To get the resliced image name for the original image names
    USSequneceNode = self._parameterNode.GetNodeReference("USSeq")
    USImageNode = USSequneceNode.GetNthDataNode(NthItem)
    reslicedImgName = USImageNode.GetName()

    transformSequenceNode = self._parameterNode.GetNodeReference("TransSeq")
    transformationNode = transformSequenceNode.GetNthDataNode(NthItem)

    # transformationNode = slicer.util.getNode("Transform_0050")
    layoutManager = slicer.app.layoutManager()
    redWidget = layoutManager.sliceWidget("Red")
    sliceNode = redWidget.mrmlSliceNode()
    

    # sliceNode.SetDimensions(*sliceShape, 1)
    # sliceNode.SetDimensions(674, 401, 1)
    # sliceNode.SetFieldOfView(*sliceShape, 1)
    # sliceNode.SetFieldOfView(550, 200, 1)
    # sliceNode.SetXYZOrigin(-64.3689, -56.2447, 0)

    # Set the xyz origin, which defines as the center of US image
    T_imgPixel_imgMM_LPS = self.logic.ReadSlicerTransfrom(self._parameterNode.GetParameter("ScalingDir") + "\\T_imgPixel_imgMM.txt")
    img_depth = 16
    imageSpacing, mask, height = self.logic.ReadMetaInfoFromDepthSetting(img_depth)
    
    center_pixel = np.array([(mask[3]-mask[2]+1)*0.5, (mask[1]-mask[0]+1)*0.5, 0, 1])
    xyzOrigin_LPS_mm = np.dot(T_imgPixel_imgMM_LPS, center_pixel)
    # print(xyzOrigin_LPS_mm)
    xyzOrigin_RAS_mm  = np.array([-xyzOrigin_LPS_mm[0],-xyzOrigin_LPS_mm[1], xyzOrigin_LPS_mm[2], 1] )
    # sliceNode.SetXYZOrigin(-0.67, -67.213, 0)
    sliceNode.SetXYZOrigin(xyzOrigin_RAS_mm[0], xyzOrigin_RAS_mm[1], xyzOrigin_RAS_mm[2])
    sliceNode.SetSliceResolutionMode(0)

    # enum SliceResolutionModeType
    #    {
    #      SliceResolutionMatchVolumes=0,
    #      SliceResolutionMatch2DView,
    #      SliceFOVMatch2DViewSpacingMatchVolumes,
    #      SliceFOVMatchVolumesSpacingMatch2DView,
    #      SliceResolutionCustom
    #    }

    imageReslice = redWidget.sliceLogic().GetBackgroundLayer().GetReslice()
  
    # imageReslice.SetSlabModeToMean()
    # imageReslice.SetSlabNumberOfSlices(10) # mean of 10 slices will computed
    # imageReslice.SetSlabSliceSpacingFraction(0.3) # spacing between each slice is 0.3 pixel (total 10 * 0.3 = 3 pixel neighborhood)
  
    transformToWrold = vtk.vtkMatrix4x4()
    transformationNode.GetMatrixTransformToWorld(transformToWrold)

    sliceNode.SetSliceToRASByNTP(transformToWrold.GetElement(0, 2), transformToWrold.GetElement(1, 2), transformToWrold.GetElement(2, 2), transformToWrold.GetElement(0, 0), transformToWrold.GetElement(1, 0), transformToWrold.GetElement(2, 0), transformToWrold.GetElement(0, 3), transformToWrold.GetElement(1, 3), transformToWrold.GetElement(2, 3), 0)
    sliceNode.Modified()
    slicer.app.processEvents()
    imageReslice.Update()
    imageData = imageReslice.GetOutput()

    # imageData = imageReslice.GetOutputDataObject(0)
    # create a new volume node
    # reslicedVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "reslicedVolume")
    # try: 
    #   import vtkplotlib as vpl
    # except:
    #   slice.util.pip_install('vtkplotlib')
    #   import vtkplotlib as vpl
    # fileName = "E:\\PROGRAM\\Project_PhD\\Slicing_verification\\Database\\LING_20220715_slicing_verification_1\\Sweep_Video_02\\Reordered_files\\Reordered_images\\Image_0002.bmp"

    # imageData_test = vpl.image_io.read(path=fileName, raw_bytes=None, format = '.bmp', convert_to_array=False)
    

    # reslicedVolume.SetOrigin(imageData.GetOrigin())
    # reslicedVolume.SetSpacing(imageData.GetSpacing())
    # reslicedVolume.SetIJKToRASDirections(imageData.GetDirectionMatrix())
    # transform = vtk.vtkMatrix4x4()
    # transform = imageData.GetIndexToPhysicalMatrix()
    # reslicedVolume.SetIJKToRASMatrix(transform)
    # reslicedVolume.SetAndObserveImageData(imageData)
    # reslicedVolume.CreateDefaultDisplayNodes()
    # reslicedVolume.CreateDefaultStorageNode()
    # print(sliceNode)

    # # save to png file
    table = vtk.vtkScalarsToColors()
    range = imageData.GetScalarRange()
    table.SetRange(range[0], range[1]) # set the range of your data values
    
    convert = vtk.vtkImageMapToColors()
    convert.SetLookupTable(table)
    convert.SetOutputFormatToRGB()
    convert.SetInputData(imageData)
    convert.Update()

    # writer = vtk.vtkPNGWriter()
    # writer.SetInputData(convert.GetOutput())

    # directory = self._parameterNode.GetParameter("ReslicedImgDir")
    # filename ="Resliced" + reslicedImgName + ".png"
    # path = directory +"\\" + filename
    # writer.SetFileName(path)
    # writer.Write()

    # fieldOfView = sliceNode.GetFieldOfView()
    # Dimensions = sliceNode.GetDimensions()
    # metaFilename = "Meta" + reslicedImgName + ".txt"
    # metaFilePath = directory +"\\" +metaFilename
    # lines = ['FOV:  ' + str(fieldOfView[0]) + '  ' + str(fieldOfView[1]) + '  ' +str(fieldOfView[2]),  'Dims:  ' + str(Dimensions[0]) + '  ' + str(Dimensions[1]) + '  ' +str(Dimensions[2])]
    # with open(metaFilePath, 'w') as f:
    #   for line in lines:
    #     f.write(line)
    #     f.write('\n')

    # print(transformToWrold)
    slabNumber = 1
    self.logic.VolumeReslice(volume_vtk, transformToWrold, reslicedImgName, img_depth, slabNumber)

    print("==================================================================")
    print(filename + " saved successfully!")
    print("==================================================================") 

    #
    # Save this image by using the Slicer slice view
    #
    # sliceNode1 = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
    # appLogic = slicer.app.applicationLogic()
    # sliceLogic = appLogic.GetSliceLogic(sliceNode1)
    # sliceLayerLogic = sliceLogic.GetBackgroundLayer()
    # reslice = sliceLayerLogic.GetReslice()
    # reslice.SetSlabModeToMean()
    # reslice.SetSlabNumberOfSlices(10) # mean of 10 slices will computed
    # reslice.SetSlabSliceSpacingFraction(0.3) # spacing between each slice is 0.3 pixel (total 10 * 0.3 = 3 pixel neighborhood)
    # sliceNode1.Modified()
    # imageData1 = reslice.GetOutput()

    # table = vtk.vtkScalarsToColors()
    # range = imageData1.GetScalarRange()
    # table.SetRange(range[0], range[1]) # set the range of your data values
    
    # convert1 = vtk.vtkImageMapToColors()
    # convert1.SetLookupTable(table)
    # convert1.SetOutputFormatToRGB()
    # convert1.SetInputData(imageData1)
    # convert1.Update()

    # writer1 = vtk.vtkPNGWriter()
    # writer1.SetInputData(convert1.GetOutput())
    # writer1.SetFileName("ImageData2Png1.png")
    # writer1.Write()


  # Save resliced images
  def onSaveAllButton(self):
    """
    Run processing when user clicks "Apply" button.
    """
    # with slicer.util.tryWithErrorDisplay("Failed to compute results.", waitCursor=True):
    volumeNode = self._parameterNode.GetNodeReference("CT_MRI")
    
    # load sequence broswer node
    sequenceBrowserNode = self._parameterNode.GetNodeReference("SequenceBroswerNode_trackedUS")
    numItems = sequenceBrowserNode.GetNumberOfItems()
    USSequneceNode = self._parameterNode.GetNodeReference("USSeq")
    transformSequenceNode = self._parameterNode.GetNodeReference("TransSeq")
    layoutManager = slicer.app.layoutManager()
    redWidget = layoutManager.sliceWidget("Red")
    sliceNode = redWidget.mrmlSliceNode()
    # Set the xyz origin, which defines as the center of US image
    T_imgPixel_imgMM_LPS = self.logic.ReadSlicerTransfrom(self._parameterNode.GetParameter("ScalingDir") + "\\T_imgPixel_imgMM.txt")
    img_depth = 14
    imageSpacing, mask, height = self.logic.ReadMetaInfoFromDepthSetting(img_depth)
    
    center_pixel = np.array([(mask[3]-mask[2]+1)*0.5, (mask[1]-mask[0]+1)*0.5, 0, 1])
    xyzOrigin_LPS_mm = np.dot(T_imgPixel_imgMM_LPS, center_pixel)
    # print(xyzOrigin_LPS_mm)
    xyzOrigin_RAS_mm  = np.array([-xyzOrigin_LPS_mm[0],-xyzOrigin_LPS_mm[1], xyzOrigin_LPS_mm[2], 1] )
    x = range(numItems)
    for NthItem in x:
      print(NthItem)
      
      # To get the resliced image name for the original image names
      
      USImageNode = USSequneceNode.GetNthDataNode(NthItem)
      reslicedImgName = USImageNode.GetName()

      transformationNode = transformSequenceNode.GetNthDataNode(NthItem)


      # sliceNode.SetDimensions(*sliceShape, 1)
      # sliceNode.SetDimensions(674, 401, 1)
      # sliceNode.SetFieldOfView(*sliceShape, 1)
      # sliceNode.SetFieldOfView(550, 200, 1)
      # sliceNode.SetXYZOrigin(-64.3689, -56.2447, 0)

      sliceNode.SetXYZOrigin(xyzOrigin_RAS_mm[0], xyzOrigin_RAS_mm[1], xyzOrigin_RAS_mm[2])
      sliceNode.SetSliceResolutionMode(0)

      # enum SliceResolutionModeType
      #    {
      #      SliceResolutionMatchVolumes=0,
      #      SliceResolutionMatch2DView,
      #      SliceFOVMatch2DViewSpacingMatchVolumes,
      #      SliceFOVMatchVolumesSpacingMatch2DView,
      #      SliceResolutionCustom
      #    }

      imageReslice = redWidget.sliceLogic().GetBackgroundLayer().GetReslice()

      # imageReslice.SetSlabModeToMean()
      # imageReslice.SetSlabNumberOfSlices(10) # mean of 10 slices will computed
      # imageReslice.SetSlabSliceSpacingFraction(0.3) # spacing between each slice is 0.3 pixel (total 10 * 0.3 = 3 pixel neighborhood)

      transformToWrold = vtk.vtkMatrix4x4()
      transformationNode.GetMatrixTransformToWorld(transformToWrold)

      sliceNode.SetSliceToRASByNTP(transformToWrold.GetElement(0, 2), transformToWrold.GetElement(1, 2), transformToWrold.GetElement(2, 2), transformToWrold.GetElement(0, 0), transformToWrold.GetElement(1, 0), transformToWrold.GetElement(2, 0), transformToWrold.GetElement(0, 3), transformToWrold.GetElement(1, 3), transformToWrold.GetElement(2, 3), 0)
      sliceNode.Modified()
      slicer.app.processEvents()
      imageReslice.Update()
      imageData = imageReslice.GetOutput()

      # imageData = imageReslice.GetOutputDataObject(0)
      # create a new volume node
      # reslicedVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "reslicedVolume")
      # try: 
      #   import vtkplotlib as vpl
      # except:
      #   slice.util.pip_install('vtkplotlib')
      #   import vtkplotlib as vpl
      # fileName = "E:\\PROGRAM\\Project_PhD\\Slicing_verification\\Database\\LING_20220715_slicing_verification_1\\Sweep_Video_02\\Reordered_files\\Reordered_images\\Image_0002.bmp"

      # imageData_test = vpl.image_io.read(path=fileName, raw_bytes=None, format = '.bmp', convert_to_array=False)
      


      # # save to png file
      table = vtk.vtkScalarsToColors()
      dataRange = imageData.GetScalarRange()
      table.SetRange(dataRange[0], dataRange[1]) # set the range of your data values
      
      convert = vtk.vtkImageMapToColors()
      convert.SetLookupTable(table)
      convert.SetOutputFormatToRGB()
      convert.SetInputData(imageData)
      convert.Update()

      writer = vtk.vtkPNGWriter()
      writer.SetInputData(convert.GetOutput())

      directory = self._parameterNode.GetParameter("ReslicedImgDir")
      filename ="Resliced" + reslicedImgName + ".png"
      path = directory +"\\" + filename
      writer.SetFileName(path)
      writer.Write()

      fieldOfView = sliceNode.GetFieldOfView()
      Dimensions = sliceNode.GetDimensions()
      metaFilename = "Meta" + reslicedImgName + ".txt"
      metaFilePath = directory +"\\" +metaFilename
      lines = ['FOV:  ' + str(fieldOfView[0]) + '  ' + str(fieldOfView[1]) + '  ' +str(fieldOfView[2]),  'Dims:  ' + str(Dimensions[0]) + '  ' + str(Dimensions[1]) + '  ' +str(Dimensions[2])]
      with open(metaFilePath, 'w') as f:
        for line in lines:
          f.write(line)
          f.write('\n')

      
      print("==================================================================")
      print(filename + " saved successfully!")
      print("==================================================================") 
      #
      # Save this image by using the Slicer slice view
      #
      # sliceNode1 = slicer.mrmlScene.GetNodeByID("vtkMRMLSliceNodeRed")
      # appLogic = slicer.app.applicationLogic()
      # sliceLogic = appLogic.GetSliceLogic(sliceNode1)
      # sliceLayerLogic = sliceLogic.GetBackgroundLayer()
      # reslice = sliceLayerLogic.GetReslice()
      # reslice.SetSlabModeToMean()
      # reslice.SetSlabNumberOfSlices(10) # mean of 10 slices will computed
      # reslice.SetSlabSliceSpacingFraction(0.3) # spacing between each slice is 0.3 pixel (total 10 * 0.3 = 3 pixel neighborhood)
      # sliceNode1.Modified()
      # imageData1 = reslice.GetOutput()

      # table = vtk.vtkScalarsToColors()
      # range = imageData1.GetScalarRange()
      # table.SetRange(range[0], range[1]) # set the range of your data values
      
      # convert1 = vtk.vtkImageMapToColors()
      # convert1.SetLookupTable(table)
      # convert1.SetOutputFormatToRGB()
      # convert1.SetInputData(imageData1)
      # convert1.Update()

      # writer1 = vtk.vtkPNGWriter()
      # writer1.SetInputData(convert1.GetOutput())
      # writer1.SetFileName("ImageData2Png1.png")
      # writer1.Write()

  def onPushButton_USSeq(self):
    
    dir = self.ui.lineEdit_USSeqDir.text # converting from "\" to "\\" 
    sequenceNode_US = self._parameterNode.GetNodeReference("USSeq")
    Nth = 1
    TotalN = len(os.listdir(dir))
    filenames = os.listdir(dir)
    absolute_filename_ = os.path.join(dir, filenames[0])
    absolute_filename = absolute_filename_.replace("\\", "\\\\") # in the raw version, "\\" will be printed as "\", therefore we replaced "\\" with "\\\\"
    loadedVolumeNode = slicer.util.loadVolume(absolute_filename, {"singleFile": True})
    
    if self.ui.checkBox_flip.checked == True: # the US image has been flipped
      transformNode_flip = slicer.vtkMRMLTransformNode()
      slicer.mrmlScene.AddNode(transformNode_flip)
      transform_matrix_flip = vtk.vtkMatrix4x4()
      transform_matrix_flip.SetElement(0, 0, -1)
      imageDimensions = loadedVolumeNode.GetImageData().GetDimensions()
      imageSpacings = loadedVolumeNode.GetImageData().GetSpacing()
      transform_matrix_translate = vtk.vtkMatrix4x4()
      transform_matrix_translate.SetElement(0, 3, imageDimensions[0]*0.5*imageSpacings[0])

      transform_matrix_translate_inverted = vtk.vtkMatrix4x4()
      transform_matrix_translate_inverted.SetElement(0, 3, -imageDimensions[0]*0.5*imageSpacings[0])

      transform_matrix_concatenated = vtk.vtkMatrix4x4()
      vtk.vtkMatrix4x4.Multiply4x4(transform_matrix_flip, transform_matrix_translate, transform_matrix_concatenated)
      vtk.vtkMatrix4x4.Multiply4x4(transform_matrix_translate_inverted, transform_matrix_concatenated, transform_matrix_concatenated)
      transformNode_flip.SetMatrixTransformToParent(transform_matrix_concatenated)

      slicer.mrmlScene.RemoveNode(slicer.util.getNode(loadedVolumeNode.GetID()))
      for filename in filenames: # making sure the file postfix  is  "image format"
        absolute_filename_ = os.path.join(dir, filename)
        absolute_filename = absolute_filename_.replace("\\", "\\\\") # in the raw version, "\\" will be printed as "\", therefore we replaced "\\" with "\\\\"
        # print(absolute_filename)
        loadedVolumeNode = slicer.util.loadVolume(absolute_filename, {"singleFile": True})
        # loadedVolumeNode.GetDisplayNode().SetAndObserveColorNodeID("vtkMRMLColorTableNodeRed")
        # Whehter flipping the US images
        
        loadedVolumeNode.SetAndObserveTransformNodeID(transformNode_flip.GetID())
        loadedVolumeNode.HardenTransform()
        
        filename_ = filename.split('.')
        itemIndex_ = filename_[0].split('_')
        itemIndex = itemIndex_[1]
        sequenceNode_US.SetDataNodeAtValue(loadedVolumeNode, itemIndex)
        slicer.mrmlScene.RemoveNode(slicer.util.getNode(loadedVolumeNode.GetID()))
      slicer.mrmlScene.RemoveNode(slicer.util.getNode(transformNode_flip.GetID()))
    else:
      slicer.mrmlScene.RemoveNode(slicer.util.getNode(loadedVolumeNode.GetID()))
      for filename in filenames: # making sure the file postfix  is  "image format"
        absolute_filename_ = os.path.join(dir, filename)
        absolute_filename = absolute_filename_.replace("\\", "\\\\") # in the raw version, "\\" will be printed as "\", therefore we replaced "\\" with "\\\\"
        # print(absolute_filename)
        loadedVolumeNode = slicer.util.loadVolume(absolute_filename, {"singleFile": True})
        # loadedVolumeNode.GetDisplayNode().SetAndObserveColorNodeID("vtkMRMLColorTableNodeRed")
        # Whehter flipping the US images
        
        filename_ = filename.split('.')
        itemIndex_ = filename_[0].split('_')
        itemIndex = itemIndex_[1]
        sequenceNode_US.SetDataNodeAtValue(loadedVolumeNode, itemIndex)
        slicer.mrmlScene.RemoveNode(slicer.util.getNode(loadedVolumeNode.GetID()))
        # print("Loading sequence data......{0}%".format(Nth/TotalN*100))
        # Nth = Nth + 1
        # time.sleep(0.05)
    
    
    # Create a sequence browser node for the new merged sequence
    # sequenceBrowserNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSequenceBrowserNode", "Sequence_tracked_US")
    sequenceBrowserNode = self._parameterNode.GetNodeReference("SequenceBroswerNode_trackedUS")
    sequenceBrowserNode.AddSynchronizedSequenceNode(sequenceNode_US)
    slicer.modules.sequences.toolBar().setActiveBrowserNode(sequenceBrowserNode)

    # Show proxy noe in slice vidwers
    proxyNode = sequenceBrowserNode.GetProxyNode(sequenceNode_US)
    slicer.util.setSliceViewerLayers(background=proxyNode)
    print("==================================================================")
    print('Genearting sequence node (US image) successfully!')
    print("==================================================================")
    # self.ui.textEdit_US.setPlainText("Push button US clicked and set the text in this QTextEdit_US")
  def onPushButton_TransSeq(self):
    
    dir = self.ui.lineEdit_TransSeqDir.text # converting from "\" to "\\" 
    sequenceNode_Trans = self._parameterNode.GetNodeReference("TransSeq")
    # Nth = 1
    # TotalN = len(os.listdir(dir))
    for filename in os.listdir(dir): # making sure the file postfix  is  "image format"
      absolute_filename_ = os.path.join(dir, filename)
      absolute_filename = absolute_filename_.replace("\\", "\\\\") # in the raw version, "\\" will be printed as "\", therefore we replaced "\\" with "\\\\"
      # print(absolute_filename)
      loadedTransformNode = slicer.util.loadTransform(absolute_filename)
      filename_ = filename.split('.')
      itemIndex_ = filename_[0].split('_')
      itemIndex = itemIndex_[1]
      sequenceNode_Trans.SetDataNodeAtValue(loadedTransformNode, itemIndex)
      slicer.mrmlScene.RemoveNode(slicer.util.getNode(loadedTransformNode.GetID()))
      # print("Loading sequence data......{0}%".format(Nth/TotalN*100))
      # Nth = Nth + 1
      # time.sleep(0.05)
    # Create a sequence browser node for the new merged sequence
    # sequenceBrowserNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSequenceBrowserNode", "Sequence_tracked_US")
    
    sequenceBrowserNode = self._parameterNode.GetNodeReference("SequenceBroswerNode_trackedUS")
    sequenceBrowserNode.AddSynchronizedSequenceNode(sequenceNode_Trans)
    slicer.modules.sequences.toolBar().setActiveBrowserNode(sequenceBrowserNode)

    # Show proxy noe in slice vidwers
    proxyNode = sequenceBrowserNode.GetProxyNode(sequenceNode_Trans)
    slicer.util.setSliceViewerLayers(background=proxyNode)
    print("==================================================================")
    print('Genearting sequence node (transformation) successfully!')
    print("==================================================================")


  def onPushButton_loadScaling(self):
    dir = self.ui.lineEdit_ScalingDir.text # converting from "\" to "\\" 
    # node_Trans = self.ui.comboBox_ScalTrans.currentNode()
    for filename in os.listdir(dir): # making sure the file postfix  is  "image format"
      absolute_filename_ = os.path.join(dir, filename)
      absolute_filename = absolute_filename_.replace("\\", "\\\\") # in the raw version, "\\" will be printed as "\", therefore we replaced "\\" with "\\\\"
      # print(absolute_filename)
      loadedNode = slicer.util.loadTransform(absolute_filename)
      self.ui.comboBox_ScalTrans.currentNode().CopyContent(loadedNode)
      # self._parameterNode.SetNodeReferenceID("ScalingTrans", node_Trans.currentNodeID)
      slicer.mrmlScene.RemoveNode(slicer.util.getNode(loadedNode.GetID()))
    # self.updateGUIFromParameterNode()
    print("==================================================================")
    print('Genearting transformation node successfully!')
    print("==================================================================")


  def onPushButton_loadCT(self):
    dir = self.ui.lineEdit_CTDir.text
    for filename in os.listdir(dir): # making sure the file postfix  is  "image format"
      absolute_filename_ = os.path.join(dir, filename)
      absolute_filename = absolute_filename_.replace("\\", "\\\\") # in the raw version, "\\" will be printed as "\", therefore we replaced "\\" with "\\\\"
      
      if self._parameterNode.GetNodeReference("CT_MRI") is None:
        loadedVolumeNode = slicer.util.loadVolume(absolute_filename, {"singleFile": True})
        #  not being used now
      else:
        loadedVolumeNode = slicer.util.loadVolume(absolute_filename, {"singleFile": True})
        self.ui.comboBox_CT.currentNode().CopyContent(loadedVolumeNode)
        # self._parameterNode.SetNodeReferenceID("ScalingTrans", node_Trans.currentNodeID)
        slicer.mrmlScene.RemoveNode(slicer.util.getNode(loadedVolumeNode.GetID()))

        # #########Test the vtkimage data correctness##############
        # reader = vtk.vtkMetaImageReader()
        # reader.SetFileName(absolute_filename)
        # reader.Update()
        # self.volume_vtk = reader.GetOutput()

    print("==================================================================")
    print('Loading CT/MRI volume node successfully!')
    print("==================================================================") 
#
# ReadSequentialDataLogic
#

class ReadSequentialDataLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  # def readSequential2DImage(self, directory)
  # Inputs: the directory including all the sequential 2D US images
  # Outputs: an array to store all the sequential nodes


  # def readSequentialTransformations(self, directory)
  # Inputs: the directory including all the transformation matrixs
  # Outputs: an array to store all the sequential nodes


  # def convertToSequenceNode(self) 
  # Inputs: could be image volume node or transformation node
  # Outputs: converted sequence node


  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

  def VolumeReslice(self, volume, slicingMatrix, reslicedImgName, USImg_depth ,slabNum = 1, slabMode = 2):
    ### INPUTS
    # volume: vtkImageData, this could be any 3D volume data (CT, MRI or 3D US)
    # slicingTransformation, vtkMatrix4x4
    # USImg_depth: this is specially for calibrated US, the depth info can help us obtain the image size, spacing 
    # slabNum: slabNum = 0 (default), if slabNum > 0; each ouput slice will actually be a composite of N slices (symetric slicing from left and right sides)
    # slabMode: if slabNum > 0, different slabMode can be chosen (VTK_IMAGE_SLAB_MIN : 0; VTK_IMAGE_SLAB_MAX: 1, VTK_IMAGE_SLAB_MEAN: 2 (default), VTK_IMAGE_SLAB_SUM: 3)

    ### OUTPUTS
    # reslicedImg: vtkImagedata format

    #################################################################################################
    ### Reslicing defination 
    # Reslicing origin: since our 2D US image is spatially tracked, the reslicng origin is determined by the origin of the 2D US image (left-upper corner) + spatially tracked position
    # Reslicing orientation: same as the "slicingTransformation"
    # Resliced image resolution: same as the input 2D US image, which is obtained from "USImg_depth" 
    # Resliced image size: same as the input 2D US image, which is obtained from "USImg_depth"
    # Interpolation mode: "VTK_NEAREST_INTERPOLATION", "VTK_LINEAR_INTERPOLATION", "VTK_CUBIC_INTERPOLATION"
    #################################################################################################

    # Reslicing Origin + orientation
    imageSpacing, mask, imageHeight = self.ReadMetaInfoFromDepthSetting(USImg_depth)
    slicingTransform = vtk.vtkTransform()

    translateXYZ_delta = [-(mask[3]-mask[2]+1)*0.5*imageSpacing[0], 0, 0, 1]
   
    translateXYZ_delta_new = [0, 0, 0, 1]
    inOrigin = volume.GetOrigin()
    inExtent = volume.GetExtent()
    inSpacing = volume.GetSpacing()
    inCenter = [inOrigin[0] + inSpacing[0]*(inExtent[1] - inExtent[0] +1) *0.5,
                inOrigin[1] + inSpacing[1]*(inExtent[3] - inExtent[2] +1) *0.5,
                inOrigin[2] + inSpacing[2]*(inExtent[5] - inExtent[4] +1) *0.5]

    # print("INPUT imagedata.................")
    # print("inOrigin: ", inOrigin)
    # print("inExtent: ", inExtent)
    # print("inSpacing: ", inSpacing)
    # print("inCenter: ", inCenter)
    # print("INPUT imagedata Done.............")
    
    for slab_shift in range(-slabNum, slabNum+1):

      slicingMatrix_new = vtk.vtkMatrix4x4()
      slicingMatrix_new.DeepCopy(slicingMatrix)
      slicingMatrix_new = self.TransformationFromRASToLPS(slicingMatrix)

      # shifting the slicing position along Z axis
      delta_shift = [0, 0, slab_shift*inSpacing[2], 1]
      shifted_translation = [0, 0, 0, 0]
      slicingMatrix_new.MultiplyPoint(delta_shift, shifted_translation)
      slicingMatrix_new.SetElement(0, 3, shifted_translation[0])
      slicingMatrix_new.SetElement(1, 3, shifted_translation[1])
      slicingMatrix_new.SetElement(2, 3, shifted_translation[2])
      slicingMatrix_new.SetElement(3, 3, shifted_translation[3])

      slicingMatrix_new_invert = vtk.vtkMatrix4x4()
      vtk.vtkMatrix4x4.Invert(slicingMatrix_new, slicingMatrix_new_invert)

      slicingTransform.PostMultiply()
      slicingTransform.Translate(-inCenter[0], -inCenter[1], -inCenter[2])
      slicingTransform.SetMatrix(slicingMatrix_new_invert)
      slicingTransform.Translate(inCenter[0], inCenter[1], inCenter[2])
      slicingTransform.Inverse()
      slicingTransform.Update()
      
      reslicer = vtk.vtkImageReslice()
      reslicer.SetInputData(volume)
      # reslicer.SetResliceTransform(slicingTransform)
      reslicer.SetResliceAxes(slicingTransform.GetMatrix())
      reslicer.SetInterpolationModeToCubic()
      reslicer.SetOutputScalarType(-1) # same as the input
      reslicer.SetOutputDimensionality(2)
      reslicer.Update()
      reslicedImg = reslicer.GetOutput()

      # convert to .png image
      table = vtk.vtkScalarsToColors()
      intensityRange = reslicedImg.GetScalarRange()
      table.SetRange(intensityRange[0], intensityRange[1]) # set the range of your data values
      
      convert = vtk.vtkImageMapToColors()
      convert.SetLookupTable(table)
      convert.SetOutputFormatToRGB()
      convert.SetInputData(reslicedImg)
      convert.Update()

      flip = vtk.vtkImageFlip()
      flip.SetInputConnection(convert.GetOutputPort())
      flip.SetFilteredAxis(1)
      writer = vtk.vtkPNGWriter()
      writer.SetInputConnection(flip.GetOutputPort())

      # save to .png file
      if slab_shift < 0:
        slab_shift_name = "neg" + str(abs(slab_shift))
      else:
        slab_shift_name = "pos" + str(slab_shift)

      directory = self.getParameterNode().GetParameter("ReslicedImgDir")
      filename ="Resliced" + reslicedImgName + slab_shift_name + ".png"
      path = directory +"\\" + filename
      writer.SetFileName(path)
      writer.Write()



    slicingMatrix_new = vtk.vtkMatrix4x4()
    slicingMatrix_new.DeepCopy(slicingMatrix)
    slicingMatrix_new = self.TransformationFromRASToLPS(slicingMatrix)
    slicingMatrix_new_invert = vtk.vtkMatrix4x4()
    vtk.vtkMatrix4x4.Invert(slicingMatrix_new, slicingMatrix_new_invert)

    slicingTransform.PostMultiply()
    slicingTransform.Translate(-inCenter[0], -inCenter[1], -inCenter[2])
    slicingTransform.SetMatrix(slicingMatrix_new_invert)
    slicingTransform.Translate(inCenter[0], inCenter[1], inCenter[2])
    slicingTransform.Inverse()
    slicingTransform.Update()
    
    reslicer = vtk.vtkImageReslice()
    reslicer.SetInputData(volume)
    # reslicer.SetResliceTransform(slicingTransform)
    reslicer.SetResliceAxes(slicingTransform.GetMatrix())
    reslicer.SetInterpolationModeToCubic()
    reslicer.SetOutputScalarType(-1) # same as the input
    # reslicer.SetOutputDimensionality(2)
    reslicer.Update()
    reslicedImg = reslicer.GetOutput()
    
    # save to .mha file
    filename_mha ="ReslicedVol" + reslicedImgName + ".mha"
    path_mha = directory +"\\" + filename_mha
    writer_mha = vtk.vtkMetaImageWriter()
    writer_mha.SetInputData(reslicedImg)
    writer_mha.SetFileName(path_mha)
    writer_mha.Write()




    # # # initialize the pixels here
    # # reslicedImg.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1) # image type and number of components
    # volumeNode = slicer.vtkMRMLScalarVolumeNode()
    # volumeNode.SetAndObserveImageData(reslicedImg)
    # volumeNode.SetSpacing(imageSpacing[0], imageSpacing[1], imageSpacing[2])
    # # volumeNode.SetOrigin()
    # # volumeNode.SetAndObserveImageData(volume)
    # volumeNode = slicer.mrmlScene.AddNode(volumeNode)
    # volumeNode.CreateDefaultDisplayNodes()

    return reslicedImg    
  def TransformationFromRASToLPS(self, transformation_RAS):
    # transformation_RAS: vtkMatrix4x4
    T_RAS_to_LPS = vtk.vtkMatrix4x4()
    T_RAS_to_LPS.Identity()
    T_RAS_to_LPS.SetElement(0, 0, -1)
    T_RAS_to_LPS.SetElement(1, 1, -1)
    T_temp = vtk.vtkMatrix4x4()
    transformation_LPS = vtk.vtkMatrix4x4()
    vtk.vtkMatrix4x4().Multiply4x4(T_RAS_to_LPS, transformation_RAS, T_temp)
    vtk.vtkMatrix4x4().Multiply4x4(T_temp, T_RAS_to_LPS, transformation_LPS)
    return transformation_LPS

  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    # if not parameterNode.GetParameter("Threshold"):
    #   parameterNode.SetParameter("Threshold", "100.0")
    # if not parameterNode.GetParameter("Invert"):
    #   parameterNode.SetParameter("Invert", "false")

    if not parameterNode.GetParameter("USSeqDir"):
      parameterNode.SetParameter("USSeqDir", "Copy and Paste the folder directory!")
    if not parameterNode.GetParameter("TransSeqDir"):
      parameterNode.SetParameter("TransSeqDir", "Copy and Paste the folder directory!")
    if not parameterNode.GetParameter("ScalingDir"):
      parameterNode.SetParameter("ScalingDir", "Copy and Paste the folder directory!")
    if not parameterNode.GetParameter("CTDir"):
      parameterNode.SetParameter("CTDir", "Copy and Paste the folder directory!")
    if not parameterNode.GetParameter("ReslicedImgDir"):
      parameterNode.SetParameter("ReslicedImgDir", "Copy and Paste the folder directory!")
    if not parameterNode.GetNodeReference("SequenceBroswerNode_trackedUS"):
      sequenceBrowserNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSequenceBrowserNode", "SequenceBroswerNode_trackedUS")
      parameterNode.SetNodeReferenceID("SequenceBroswerNode_trackedUS", sequenceBrowserNode.GetID())

  def ReadSlicerTransfrom(self, file_path):
    f = open(file_path,"r")
    lines = f.readlines()
    # the 4th line includes the affine transformation numbers
    parameters = lines[3].split(" ")
    transform_affine_inv = np.array([[float(parameters[1]),float(parameters[2]), float(parameters[3]), float(parameters[10])], [float(parameters[4]),float(parameters[5]), float(parameters[6]), float(parameters[11])], [float(parameters[7]),float(parameters[8]), float(parameters[9]), float(parameters[12])], [0, 0, 0, 1]])
    transform_affine = np.linalg.inv(transform_affine_inv)
    f.close()
    return transform_affine
  
  def ConvertToSlicerTransform(self, transformation_LPS, outputPath):
    print("This approach is to convert the transformation (LPS) to the format that can be directly loaded to 3D slicer")
    # transformation_LPS: 4 by 4 matrix (numpy)
    transformation_LPS_inv = np.linalg.inv(transformation_LPS)
    delimiter = ' '
    transformation_str = 'Parameters: ' + delimiter + str(transformation_LPS_inv.item(0, 0)) + delimiter + str(transformation_LPS_inv.item(0, 1)) + delimiter + str(transformation_LPS_inv.item(0, 2)) \
    + delimiter + str(transformation_LPS_inv.item(1, 0)) + delimiter + str(transformation_LPS_inv.item(1, 1)) + delimiter + str(transformation_LPS_inv.item(1, 2)) \
    + delimiter + str(transformation_LPS_inv.item(2, 0)) + delimiter + str(transformation_LPS_inv.item(2, 1)) + delimiter + str(transformation_LPS_inv.item(2, 2)) \
    + delimiter + str(transformation_LPS_inv.item(0, 3)) + delimiter + str(transformation_LPS_inv.item(1, 3)) + delimiter + str(transformation_LPS_inv.item(2, 3)) +'\n'
    # print(transformation_str)

    transformation_cell = '#Insight Transform File V1.0 \n' + '#Transform 0 \n' +  'Transform: AffineTransform_double_3_3 \n' + transformation_str + 'FixedParameters: 0 0 0'  
    
    # open txt file
    text_file = open(outputPath, "w+")
    text_file.write(transformation_cell)
    text_file.close()

  #
    # Objective: read meta information from the US image with a specific depth
    #
  def ReadMetaInfoFromDepthSetting(self, depth):
    ROILeft = 0
    ROITop = 0
    ROIWidth = 0
    ROIHeight = 0
    imageSpacing = np.array([0, 0, 0], dtype='f')
    if depth == 18:
        imageSpacing[0:3] = [0.319, 0.319, 1]
        ROILeft = 80
        ROITop = 120
        ROIWidth = 752
        ROIHeight = 564
    elif depth == 16:
        imageSpacing[0:3] = [0.286, 0.286, 1]
        ROILeft = 80
        ROITop = 123
        ROIWidth = 752
        ROIHeight = 560
    elif depth == 14:
        imageSpacing[0:3] = [0.251, 0.251, 1]
        ROILeft = 79
        ROITop = 127
        ROIWidth = 752
        ROIHeight = 558
    elif depth == 12:
        imageSpacing[0:3] = [0.218, 0.218, 1]
        ROILeft = 74
        ROITop = 132
        ROIWidth = 752
        ROIHeight = 550
    elif depth == 11:
        imageSpacing[0:3] = [0.200, 0.200, 1]
        ROILeft = 71
        ROITop = 135
        ROIWidth = 752
        ROIHeight = 550
    elif depth == 10:
        imageSpacing[0:3] = [0.185, 0.185, 1]
        ROILeft = 71
        ROITop = 140
        ROIWidth = 752
        ROIHeight = 542
    elif depth == 9:
        imageSpacing[0:3] = [0.171, 0.171, 1]
        ROILeft = 68
        ROITop = 153
        ROIWidth = 752
        ROIHeight = 526
    elif depth == 8.1:
        imageSpacing[0:3] = [0.160, 0.160, 1]
        ROILeft = 71
        ROITop = 162
        ROIWidth = 752
        ROIHeight = 506
    else:
        print("checking the depth of US image!")
    
    imageHeight = ROIHeight
    mask = np.array([ROITop, ROITop + ROIHeight, ROILeft, ROILeft + ROIWidth])
    return imageSpacing, mask, imageHeight

  def process(self, inputVolume, outputVolume, imageThreshold, invert=False, showResult=True):
    """
    Run the processing algorithm.
    Can be used without GUI widget.
    :param inputVolume: volume to be thresholded
    :param outputVolume: thresholding result
    :param imageThreshold: values above/below this threshold will be set to 0
    :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
    :param showResult: show output volume in slice viewers
    """

    if not inputVolume or not outputVolume:
      raise ValueError("Input or output volume is invalid")

    import time
    startTime = time.time()
    logging.info('Processing started')

    # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
    cliParams = {
      'InputVolume': inputVolume.GetID(),
      'OutputVolume': outputVolume.GetID(),
      'ThresholdValue' : imageThreshold,
      'ThresholdType' : 'Above' if invert else 'Below'
      }
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
    # We don't need the CLI module node anymore, remove it to not clutter the scene with it
    slicer.mrmlScene.RemoveNode(cliNode)

    stopTime = time.time()
    logging.info(f'Processing completed in {stopTime-startTime:.2f} seconds')


#
# ReadSequentialDataTest
#

class ReadSequentialDataTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ReadSequentialData1()

  def test_ReadSequentialData1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Get/create input data

    import SampleData
    registerSampleData()
    inputVolume = SampleData.downloadSample('ReadSequentialData1')
    self.delayDisplay('Loaded test data set')

    inputScalarRange = inputVolume.GetImageData().GetScalarRange()
    self.assertEqual(inputScalarRange[0], 0)
    self.assertEqual(inputScalarRange[1], 695)

    outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
    threshold = 100

    # Test the module logic

    logic = ReadSequentialDataLogic()

    # Test algorithm with non-inverted threshold
    logic.process(inputVolume, outputVolume, threshold, True)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], threshold)

    # Test algorithm with inverted threshold
    logic.process(inputVolume, outputVolume, threshold, False)
    outputScalarRange = outputVolume.GetImageData().GetScalarRange()
    self.assertEqual(outputScalarRange[0], inputScalarRange[0])
    self.assertEqual(outputScalarRange[1], inputScalarRange[1])

    self.delayDisplay('Test passed')
