# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Extensions\LING_Registration\ReadSequentialData\Resources\UI\ReadSequentialData.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ReadSequentialData(object):
    def setupUi(self, ReadSequentialData):
        ReadSequentialData.setObjectName("ReadSequentialData")
        ReadSequentialData.resize(318, 458)
        self.gridLayout = QtWidgets.QGridLayout(ReadSequentialData)
        self.gridLayout.setObjectName("gridLayout")
        self.InputsCollapsibleButton = ctkCollapsibleButton(ReadSequentialData)
        self.InputsCollapsibleButton.setObjectName("InputsCollapsibleButton")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.InputsCollapsibleButton)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.frame_2 = QtWidgets.QFrame(self.InputsCollapsibleButton)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setObjectName("label_8")
        self.gridLayout_6.addWidget(self.label_8, 1, 0, 1, 1)
        self.lineEdit_ScalingDir = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_ScalingDir.setObjectName("lineEdit_ScalingDir")
        self.gridLayout_6.addWidget(self.lineEdit_ScalingDir, 2, 1, 1, 1)
        self.lineEdit_TransSeqDir = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_TransSeqDir.setObjectName("lineEdit_TransSeqDir")
        self.gridLayout_6.addWidget(self.lineEdit_TransSeqDir, 1, 1, 1, 1)
        self.lineEdit_USSeqDir = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_USSeqDir.setObjectName("lineEdit_USSeqDir")
        self.gridLayout_6.addWidget(self.lineEdit_USSeqDir, 0, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_6.addWidget(self.label_9, 0, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_6.addWidget(self.label_10, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 3, 0, 1, 1)
        self.lineEdit_CTDir = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_CTDir.setObjectName("lineEdit_CTDir")
        self.gridLayout_6.addWidget(self.lineEdit_CTDir, 3, 1, 1, 1)
        self.gridLayout_5.addWidget(self.frame_2, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.InputsCollapsibleButton, 0, 0, 1, 1)
        self.VisibilityCollapsibleButton_2 = ctkCollapsibleButton(ReadSequentialData)
        self.VisibilityCollapsibleButton_2.setProperty("collapsed", False)
        self.VisibilityCollapsibleButton_2.setObjectName("VisibilityCollapsibleButton_2")
        self.formLayout = QtWidgets.QFormLayout(self.VisibilityCollapsibleButton_2)
        self.formLayout.setObjectName("formLayout")
        self.frame_3 = QtWidgets.QFrame(self.VisibilityCollapsibleButton_2)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 1)
        self.lineEdit_ReslicedImgDir = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit_ReslicedImgDir.setObjectName("lineEdit_ReslicedImgDir")
        self.gridLayout_4.addWidget(self.lineEdit_ReslicedImgDir, 0, 1, 1, 1)
        self.applyButton = QtWidgets.QPushButton(self.frame_3)
        self.applyButton.setEnabled(True)
        self.applyButton.setObjectName("applyButton")
        self.gridLayout_4.addWidget(self.applyButton, 1, 0, 1, 1)
        self.saveAllButton = QtWidgets.QPushButton(self.frame_3)
        self.saveAllButton.setObjectName("saveAllButton")
        self.gridLayout_4.addWidget(self.saveAllButton, 1, 1, 1, 1)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.frame_3)
        self.gridLayout.addWidget(self.VisibilityCollapsibleButton_2, 4, 0, 1, 1)
        self.GenerateCollapsibleButton = ctkCollapsibleButton(ReadSequentialData)
        self.GenerateCollapsibleButton.setObjectName("GenerateCollapsibleButton")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.GenerateCollapsibleButton)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.GenerateCollapsibleButton)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_TransSeq = QtWidgets.QPushButton(self.frame)
        self.pushButton_TransSeq.setObjectName("pushButton_TransSeq")
        self.gridLayout_3.addWidget(self.pushButton_TransSeq, 2, 2, 1, 1)
        self.comboBox_USSeq = qMRMLNodeComboBox(self.frame)
        self.comboBox_USSeq.setEnabled(True)
        self.comboBox_USSeq.setProperty("nodeTypes", ['vtkMRMLSequenceNode'])
        self.comboBox_USSeq.setProperty("showChildNodeTypes", False)
        self.comboBox_USSeq.setProperty("addEnabled", True)
        self.comboBox_USSeq.setProperty("removeEnabled", True)
        self.comboBox_USSeq.setProperty("editEnabled", False)
        self.comboBox_USSeq.setProperty("renameEnabled", True)
        self.comboBox_USSeq.setObjectName("comboBox_USSeq")
        self.gridLayout_3.addWidget(self.comboBox_USSeq, 0, 1, 1, 1)
        self.comboBox_TransSeq = qMRMLNodeComboBox(self.frame)
        self.comboBox_TransSeq.setEnabled(True)
        self.comboBox_TransSeq.setProperty("nodeTypes", ['vtkMRMLSequenceNode'])
        self.comboBox_TransSeq.setProperty("showChildNodeTypes", False)
        self.comboBox_TransSeq.setProperty("addEnabled", True)
        self.comboBox_TransSeq.setProperty("removeEnabled", True)
        self.comboBox_TransSeq.setProperty("renameEnabled", True)
        self.comboBox_TransSeq.setObjectName("comboBox_TransSeq")
        self.gridLayout_3.addWidget(self.comboBox_TransSeq, 2, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.pushButton_USSeq = QtWidgets.QPushButton(self.frame)
        self.pushButton_USSeq.setObjectName("pushButton_USSeq")
        self.gridLayout_3.addWidget(self.pushButton_USSeq, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 4, 0, 1, 1)
        self.pushButton_loadCT = QtWidgets.QPushButton(self.frame)
        self.pushButton_loadCT.setObjectName("pushButton_loadCT")
        self.gridLayout_3.addWidget(self.pushButton_loadCT, 4, 2, 1, 1)
        self.pushButton_loadScaling = QtWidgets.QPushButton(self.frame)
        self.pushButton_loadScaling.setObjectName("pushButton_loadScaling")
        self.gridLayout_3.addWidget(self.pushButton_loadScaling, 3, 2, 1, 1)
        self.comboBox_ScalTrans = qMRMLNodeComboBox(self.frame)
        self.comboBox_ScalTrans.setEnabled(True)
        self.comboBox_ScalTrans.setProperty("nodeTypes", ['vtkMRMLLinearTransformNode'])
        self.comboBox_ScalTrans.setProperty("showChildNodeTypes", False)
        self.comboBox_ScalTrans.setProperty("addEnabled", True)
        self.comboBox_ScalTrans.setProperty("removeEnabled", True)
        self.comboBox_ScalTrans.setProperty("renameEnabled", True)
        self.comboBox_ScalTrans.setObjectName("comboBox_ScalTrans")
        self.gridLayout_3.addWidget(self.comboBox_ScalTrans, 3, 1, 1, 1)
        self.comboBox_CT = qMRMLNodeComboBox(self.frame)
        self.comboBox_CT.setEnabled(True)
        self.comboBox_CT.setProperty("nodeTypes", ['vtkMRMLScalarVolumeNode'])
        self.comboBox_CT.setProperty("showChildNodeTypes", False)
        self.comboBox_CT.setProperty("addEnabled", True)
        self.comboBox_CT.setProperty("removeEnabled", True)
        self.comboBox_CT.setProperty("renameEnabled", True)
        self.comboBox_CT.setObjectName("comboBox_CT")
        self.gridLayout_3.addWidget(self.comboBox_CT, 4, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.GenerateCollapsibleButton, 1, 0, 1, 1)
        self.VisibilityCollapsibleButton = ctkCollapsibleButton(ReadSequentialData)
        self.VisibilityCollapsibleButton.setProperty("collapsed", False)
        self.VisibilityCollapsibleButton.setObjectName("VisibilityCollapsibleButton")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.VisibilityCollapsibleButton)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.frame_4 = QtWidgets.QFrame(self.VisibilityCollapsibleButton)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.DataVisibilityCheckBox = QtWidgets.QCheckBox(self.frame_4)
        self.DataVisibilityCheckBox.setText("")
        self.DataVisibilityCheckBox.setObjectName("DataVisibilityCheckBox")
        self.horizontalLayout.addWidget(self.DataVisibilityCheckBox)
        self.gridLayout_7.addWidget(self.frame_4, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.VisibilityCollapsibleButton, 2, 0, 1, 1)

        self.retranslateUi(ReadSequentialData)
        ReadSequentialData.mrmlSceneChanged['vtkMRMLScene*'].connect(self.comboBox_USSeq.setMRMLScene)
        ReadSequentialData.mrmlSceneChanged['vtkMRMLScene*'].connect(self.comboBox_TransSeq.setMRMLScene)
        ReadSequentialData.mrmlSceneChanged['vtkMRMLScene*'].connect(self.comboBox_ScalTrans.setMRMLScene)
        ReadSequentialData.mrmlSceneChanged['vtkMRMLScene*'].connect(self.comboBox_CT.setMRMLScene)
        QtCore.QMetaObject.connectSlotsByName(ReadSequentialData)

    def retranslateUi(self, ReadSequentialData):
        _translate = QtCore.QCoreApplication.translate
        self.InputsCollapsibleButton.setProperty("text", _translate("ReadSequentialData", "Inputs Directories (tracked US)"))
        self.label_8.setText(_translate("ReadSequentialData", "Trans Seq dir:"))
        self.label_9.setText(_translate("ReadSequentialData", "US Seq dir: "))
        self.label_10.setText(_translate("ReadSequentialData", "Scal. dir:"))
        self.label.setText(_translate("ReadSequentialData", "CT/MRI dir:"))
        self.VisibilityCollapsibleButton_2.setProperty("text", _translate("ReadSequentialData", "Save Resliced Images "))
        self.label_7.setText(_translate("ReadSequentialData", "Resliced Img dir: "))
        self.applyButton.setToolTip(_translate("ReadSequentialData", "Run the algorithm."))
        self.applyButton.setText(_translate("ReadSequentialData", "Save Single"))
        self.saveAllButton.setText(_translate("ReadSequentialData", "Save All"))
        self.GenerateCollapsibleButton.setProperty("text", _translate("ReadSequentialData", "Generate Nodes"))
        self.pushButton_TransSeq.setText(_translate("ReadSequentialData", "Generate"))
        self.comboBox_USSeq.setToolTip(_translate("ReadSequentialData", "Define the US sequence node."))
        self.comboBox_TransSeq.setToolTip(_translate("ReadSequentialData", "Define the transformation sequence node."))
        self.label_5.setText(_translate("ReadSequentialData", "Scal. Trans:"))
        self.label_3.setText(_translate("ReadSequentialData", "Trans Seq:"))
        self.label_2.setText(_translate("ReadSequentialData", "US Seq:"))
        self.pushButton_USSeq.setText(_translate("ReadSequentialData", "Generate"))
        self.label_6.setText(_translate("ReadSequentialData", "CT/MRI:"))
        self.pushButton_loadCT.setText(_translate("ReadSequentialData", "Load"))
        self.pushButton_loadScaling.setText(_translate("ReadSequentialData", "Load"))
        self.comboBox_ScalTrans.setToolTip(_translate("ReadSequentialData", "Define the scaling transformation node."))
        self.comboBox_CT.setToolTip(_translate("ReadSequentialData", "Define the CT/MRI volume node."))
        self.VisibilityCollapsibleButton.setProperty("text", _translate("ReadSequentialData", "Visibilit (need to refine)"))
        self.label_4.setText(_translate("ReadSequentialData", "CT/MRI Data Visibility: "))
        self.DataVisibilityCheckBox.setToolTip(_translate("ReadSequentialData", "If checked, values above threshold are set to 0. If unchecked, values below are set to 0."))

from ctkCollapsibleButton import ctkCollapsibleButton
from qMRMLNodeComboBox import qMRMLNodeComboBox
from qMRMLWidget import qMRMLWidget
