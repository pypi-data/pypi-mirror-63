# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/travis/build/kcjengr/probe_basic/probe_basic/probe_basic.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1918, 1139)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(11)
        Form.setFont(font)
        Form.setFocusPolicy(QtCore.Qt.ClickFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/probe_basic_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setToolTipDuration(-1)
        Form.setStyleSheet("Form {\n"
"bottom-margin: 0px;\n"
"}")
        Form.setDocumentMode(False)
        Form.setProperty("promptAtExit", False)
        Form.setProperty("promot_on_exit", False)
        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_31 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.horizontalLayout_101 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_101.setContentsMargins(-1, -1, 0, 3)
        self.horizontalLayout_101.setSpacing(0)
        self.horizontalLayout_101.setObjectName("horizontalLayout_101")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout()
        self.verticalLayout_30.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_30.setSpacing(0)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(129, 133, 132))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 141, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        self.tabWidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(15)
        self.tabWidget.setFont(font)
        self.tabWidget.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setStyleSheet("QTabWidget QTabBar::tab {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    min-width: 130px;\n"
"    min-height: 30px;\n"
"    font: 15pt \"bebas kai\";\n"
"}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget.setObjectName("tabWidget")
        self.main_tab = QtWidgets.QWidget()
        self.main_tab.setObjectName("main_tab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.main_tab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_24 = QtWidgets.QFrame(self.main_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_24.sizePolicy().hasHeightForWidth())
        self.frame_24.setSizePolicy(sizePolicy)
        self.frame_24.setMinimumSize(QtCore.QSize(1, 0))
        self.frame_24.setMaximumSize(QtCore.QSize(1, 16777215))
        self.frame_24.setStyleSheet("QFrame{\n"
"border: none;\n"
"background-color: transparent;\n"
"}")
        self.frame_24.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.horizontalLayout.addWidget(self.frame_24)
        self.splitter = QtWidgets.QSplitter(self.main_tab)
        self.splitter.setFocusPolicy(QtCore.Qt.NoFocus)
        self.splitter.setLineWidth(2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(10)
        self.splitter.setObjectName("splitter")
        self.verticalWidget = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.verticalWidget.sizePolicy().hasHeightForWidth())
        self.verticalWidget.setSizePolicy(sizePolicy)
        self.verticalWidget.setMinimumSize(QtCore.QSize(650, 0))
        self.verticalWidget.setMaximumSize(QtCore.QSize(650, 16777215))
        self.verticalWidget.setObjectName("verticalWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalWidget)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setContentsMargins(1, 3, 1, 3)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.recentfilecombobox = RecentFileComboBox(self.verticalWidget)
        self.recentfilecombobox.setMinimumSize(QtCore.QSize(148, 30))
        self.recentfilecombobox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.recentfilecombobox.setStyleSheet("QComboBox {\n"
"    border: 1px solid black;\n"
"    border-radius: 3px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"    padding: 1px 23px 1px 3px;\n"
"    min-width: 6em;\n"
"    color: #ffffff;\n"
"    font: 12pt \"Bebas Kai\";\n"
"}\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 20px;\n"
"     border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"    font: 12pt \"Bebas Kai\";\n"
"}\n"
"QComboBox::down-arrow {\n"
"     image: url(:/images/combobox-arrow.png);\n"
"}\n"
" \n"
"QComboBox QAbstractItemView{\n"
"    background-color: #4f4f4f;\n"
"    color: #999999;\n"
"     selection-background-color: #999999;\n"
"    selection-color: #4f4f4f;\n"
"}")
        self.recentfilecombobox.setProperty("resource", "")
        self.recentfilecombobox.setObjectName("recentfilecombobox")
        self.verticalLayout_2.addWidget(self.recentfilecombobox)
        self.gcodeeditor = GcodeEditor(self.verticalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gcodeeditor.sizePolicy().hasHeightForWidth())
        self.gcodeeditor.setSizePolicy(sizePolicy)
        self.gcodeeditor.setMinimumSize(QtCore.QSize(0, 0))
        self.gcodeeditor.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gcodeeditor.setProperty("editor", False)
        self.gcodeeditor.setObjectName("gcodeeditor")
        self.verticalLayout_2.addWidget(self.gcodeeditor)
        self.frame_3 = QtWidgets.QFrame(self.verticalWidget)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_3.setStyleSheet("QWidget {\n"
"    border-style: none;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    background: none;\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_16.setSpacing(3)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.mdi_entry_box = MDIEntry(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdi_entry_box.sizePolicy().hasHeightForWidth())
        self.mdi_entry_box.setSizePolicy(sizePolicy)
        self.mdi_entry_box.setMinimumSize(QtCore.QSize(0, 40))
        self.mdi_entry_box.setMaximumSize(QtCore.QSize(16777215, 40))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mdi_entry_box.setFont(font)
        self.mdi_entry_box.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mdi_entry_box.setObjectName("mdi_entry_box")
        self.horizontalLayout_16.addWidget(self.mdi_entry_box)
        self.verticalLayout_2.addWidget(self.frame_3)
        self.horizontalLayout.addWidget(self.splitter)
        self.widget_7 = QtWidgets.QWidget(self.main_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.widget_7.setStyleSheet("")
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.vtk_control_buttons = QtWidgets.QWidget(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vtk_control_buttons.sizePolicy().hasHeightForWidth())
        self.vtk_control_buttons.setSizePolicy(sizePolicy)
        self.vtk_control_buttons.setMinimumSize(QtCore.QSize(90, 0))
        self.vtk_control_buttons.setMaximumSize(QtCore.QSize(90, 16777215))
        self.vtk_control_buttons.setStyleSheet(".QWidget{\n"
"    background: rgb(32, 36, 37);\n"
"}")
        self.vtk_control_buttons.setObjectName("vtk_control_buttons")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.vtk_control_buttons)
        self.verticalLayout_8.setContentsMargins(15, 18, 0, 12)
        self.verticalLayout_8.setSpacing(6)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.iso_view_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iso_view_button.sizePolicy().hasHeightForWidth())
        self.iso_view_button.setSizePolicy(sizePolicy)
        self.iso_view_button.setMinimumSize(QtCore.QSize(75, 33))
        self.iso_view_button.setMaximumSize(QtCore.QSize(75, 33))
        self.iso_view_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.iso_view_button.setCheckable(False)
        self.iso_view_button.setObjectName("iso_view_button")
        self.verticalLayout_8.addWidget(self.iso_view_button)
        self.x_view_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_view_button.sizePolicy().hasHeightForWidth())
        self.x_view_button.setSizePolicy(sizePolicy)
        self.x_view_button.setMinimumSize(QtCore.QSize(75, 33))
        self.x_view_button.setMaximumSize(QtCore.QSize(75, 33))
        self.x_view_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_view_button.setStyleSheet("")
        self.x_view_button.setCheckable(False)
        self.x_view_button.setObjectName("x_view_button")
        self.verticalLayout_8.addWidget(self.x_view_button)
        self.y_view_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_view_button.sizePolicy().hasHeightForWidth())
        self.y_view_button.setSizePolicy(sizePolicy)
        self.y_view_button.setMinimumSize(QtCore.QSize(75, 33))
        self.y_view_button.setMaximumSize(QtCore.QSize(75, 33))
        self.y_view_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.y_view_button.setStyleSheet("")
        self.y_view_button.setCheckable(False)
        self.y_view_button.setObjectName("y_view_button")
        self.verticalLayout_8.addWidget(self.y_view_button)
        self.z_view_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.z_view_button.sizePolicy().hasHeightForWidth())
        self.z_view_button.setSizePolicy(sizePolicy)
        self.z_view_button.setMinimumSize(QtCore.QSize(75, 33))
        self.z_view_button.setMaximumSize(QtCore.QSize(75, 33))
        self.z_view_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.z_view_button.setStyleSheet("")
        self.z_view_button.setCheckable(False)
        self.z_view_button.setObjectName("z_view_button")
        self.verticalLayout_8.addWidget(self.z_view_button)
        self.label_29 = QtWidgets.QLabel(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_29.sizePolicy().hasHeightForWidth())
        self.label_29.setSizePolicy(sizePolicy)
        self.label_29.setMinimumSize(QtCore.QSize(60, 1))
        self.label_29.setMaximumSize(QtCore.QSize(60, 1))
        self.label_29.setText("")
        self.label_29.setObjectName("label_29")
        self.verticalLayout_8.addWidget(self.label_29)
        self.pan_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pan_button.sizePolicy().hasHeightForWidth())
        self.pan_button.setSizePolicy(sizePolicy)
        self.pan_button.setMinimumSize(QtCore.QSize(75, 33))
        self.pan_button.setMaximumSize(QtCore.QSize(75, 33))
        self.pan_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pan_button.setStyleSheet("")
        self.pan_button.setCheckable(False)
        self.pan_button.setObjectName("pan_button")
        self.verticalLayout_8.addWidget(self.pan_button)
        self.zoom_in_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoom_in_button.sizePolicy().hasHeightForWidth())
        self.zoom_in_button.setSizePolicy(sizePolicy)
        self.zoom_in_button.setMinimumSize(QtCore.QSize(75, 33))
        self.zoom_in_button.setMaximumSize(QtCore.QSize(75, 33))
        self.zoom_in_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoom_in_button.setStyleSheet("")
        self.zoom_in_button.setCheckable(False)
        self.zoom_in_button.setObjectName("zoom_in_button")
        self.verticalLayout_8.addWidget(self.zoom_in_button)
        self.zoom_out_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoom_out_button.sizePolicy().hasHeightForWidth())
        self.zoom_out_button.setSizePolicy(sizePolicy)
        self.zoom_out_button.setMinimumSize(QtCore.QSize(75, 33))
        self.zoom_out_button.setMaximumSize(QtCore.QSize(75, 33))
        self.zoom_out_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoom_out_button.setStyleSheet("")
        self.zoom_out_button.setCheckable(False)
        self.zoom_out_button.setObjectName("zoom_out_button")
        self.verticalLayout_8.addWidget(self.zoom_out_button)
        self.label_32 = QtWidgets.QLabel(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        self.label_32.setMinimumSize(QtCore.QSize(60, 1))
        self.label_32.setMaximumSize(QtCore.QSize(60, 1))
        self.label_32.setText("")
        self.label_32.setObjectName("label_32")
        self.verticalLayout_8.addWidget(self.label_32)
        self.program_zoom_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.program_zoom_button.sizePolicy().hasHeightForWidth())
        self.program_zoom_button.setSizePolicy(sizePolicy)
        self.program_zoom_button.setMinimumSize(QtCore.QSize(75, 33))
        self.program_zoom_button.setMaximumSize(QtCore.QSize(75, 33))
        self.program_zoom_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.program_zoom_button.setStyleSheet("")
        self.program_zoom_button.setCheckable(False)
        self.program_zoom_button.setObjectName("program_zoom_button")
        self.verticalLayout_8.addWidget(self.program_zoom_button)
        self.machine_zoom_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_zoom_button.sizePolicy().hasHeightForWidth())
        self.machine_zoom_button.setSizePolicy(sizePolicy)
        self.machine_zoom_button.setMinimumSize(QtCore.QSize(75, 33))
        self.machine_zoom_button.setMaximumSize(QtCore.QSize(75, 33))
        self.machine_zoom_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.machine_zoom_button.setStyleSheet("")
        self.machine_zoom_button.setCheckable(False)
        self.machine_zoom_button.setObjectName("machine_zoom_button")
        self.verticalLayout_8.addWidget(self.machine_zoom_button)
        self.label_27 = QtWidgets.QLabel(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setMinimumSize(QtCore.QSize(60, 1))
        self.label_27.setMaximumSize(QtCore.QSize(60, 1))
        self.label_27.setText("")
        self.label_27.setObjectName("label_27")
        self.verticalLayout_8.addWidget(self.label_27)
        self.path_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.path_button.sizePolicy().hasHeightForWidth())
        self.path_button.setSizePolicy(sizePolicy)
        self.path_button.setMinimumSize(QtCore.QSize(75, 33))
        self.path_button.setMaximumSize(QtCore.QSize(75, 33))
        self.path_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.path_button.setStyleSheet("")
        self.path_button.setCheckable(False)
        self.path_button.setObjectName("path_button")
        self.verticalLayout_8.addWidget(self.path_button)
        self.clear_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clear_button.sizePolicy().hasHeightForWidth())
        self.clear_button.setSizePolicy(sizePolicy)
        self.clear_button.setMinimumSize(QtCore.QSize(75, 33))
        self.clear_button.setMaximumSize(QtCore.QSize(75, 33))
        self.clear_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clear_button.setStyleSheet("")
        self.clear_button.setCheckable(False)
        self.clear_button.setObjectName("clear_button")
        self.verticalLayout_8.addWidget(self.clear_button)
        self.label_28 = QtWidgets.QLabel(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setMinimumSize(QtCore.QSize(60, 1))
        self.label_28.setMaximumSize(QtCore.QSize(60, 1))
        self.label_28.setText("")
        self.label_28.setObjectName("label_28")
        self.verticalLayout_8.addWidget(self.label_28)
        self.ortho_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ortho_button.sizePolicy().hasHeightForWidth())
        self.ortho_button.setSizePolicy(sizePolicy)
        self.ortho_button.setMinimumSize(QtCore.QSize(75, 33))
        self.ortho_button.setMaximumSize(QtCore.QSize(75, 33))
        self.ortho_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ortho_button.setStyleSheet("")
        self.ortho_button.setCheckable(True)
        self.ortho_button.setChecked(True)
        self.ortho_button.setAutoExclusive(True)
        self.ortho_button.setObjectName("ortho_button")
        self.mainorthoperspbtnGroup = QtWidgets.QButtonGroup(Form)
        self.mainorthoperspbtnGroup.setObjectName("mainorthoperspbtnGroup")
        self.mainorthoperspbtnGroup.addButton(self.ortho_button)
        self.verticalLayout_8.addWidget(self.ortho_button)
        self.perspective_button = QtWidgets.QPushButton(self.vtk_control_buttons)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.perspective_button.sizePolicy().hasHeightForWidth())
        self.perspective_button.setSizePolicy(sizePolicy)
        self.perspective_button.setMinimumSize(QtCore.QSize(75, 33))
        self.perspective_button.setMaximumSize(QtCore.QSize(75, 33))
        self.perspective_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.perspective_button.setStyleSheet("")
        self.perspective_button.setCheckable(True)
        self.perspective_button.setAutoExclusive(True)
        self.perspective_button.setObjectName("perspective_button")
        self.mainorthoperspbtnGroup.addButton(self.perspective_button)
        self.verticalLayout_8.addWidget(self.perspective_button)
        self.horizontalLayout_10.addWidget(self.vtk_control_buttons)
        self.vtk = VTKBackPlot(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vtk.sizePolicy().hasHeightForWidth())
        self.vtk.setSizePolicy(sizePolicy)
        self.vtk.setStyleSheet("VTKBackPlot {\n"
"    border: solid;\n"
"    border-color: white;\n"
"    border-width: 2px;\n"
"    border-radius: 8px;\n"
"}")
        self.vtk.setProperty("backgroundColor", QtGui.QColor(32, 36, 37))
        self.vtk.setObjectName("vtk")
        self.horizontalLayout_10.addWidget(self.vtk)
        self.horizontalLayout.addWidget(self.widget_7)
        self.tabWidget.addTab(self.main_tab, "")
        self.file_tab = QtWidgets.QWidget()
        self.file_tab.setObjectName("file_tab")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.file_tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_120 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_120.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_120.setContentsMargins(15, 20, 15, 20)
        self.horizontalLayout_120.setSpacing(15)
        self.horizontalLayout_120.setObjectName("horizontalLayout_120")
        self.frame_35 = QtWidgets.QFrame(self.file_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_35.sizePolicy().hasHeightForWidth())
        self.frame_35.setSizePolicy(sizePolicy)
        self.frame_35.setMinimumSize(QtCore.QSize(500, 0))
        self.frame_35.setMaximumSize(QtCore.QSize(500, 16777215))
        self.frame_35.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_35.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_35.setObjectName("frame_35")
        self.verticalLayout_37 = QtWidgets.QVBoxLayout(self.frame_35)
        self.verticalLayout_37.setObjectName("verticalLayout_37")
        self.horizontalLayout_124 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_124.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_124.setObjectName("horizontalLayout_124")
        self.device_folder_up_button = QtWidgets.QPushButton(self.frame_35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_folder_up_button.sizePolicy().hasHeightForWidth())
        self.device_folder_up_button.setSizePolicy(sizePolicy)
        self.device_folder_up_button.setMinimumSize(QtCore.QSize(110, 30))
        self.device_folder_up_button.setMaximumSize(QtCore.QSize(110, 30))
        self.device_folder_up_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.device_folder_up_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/folder_up.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.device_folder_up_button.setIcon(icon1)
        self.device_folder_up_button.setIconSize(QtCore.QSize(30, 17))
        self.device_folder_up_button.setObjectName("device_folder_up_button")
        self.horizontalLayout_124.addWidget(self.device_folder_up_button)
        self.removabledevicecombobox = RemovableDeviceComboBox(self.frame_35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.removabledevicecombobox.sizePolicy().hasHeightForWidth())
        self.removabledevicecombobox.setSizePolicy(sizePolicy)
        self.removabledevicecombobox.setMinimumSize(QtCore.QSize(0, 30))
        self.removabledevicecombobox.setMaximumSize(QtCore.QSize(16777215, 30))
        self.removabledevicecombobox.setObjectName("removabledevicecombobox")
        self.horizontalLayout_124.addWidget(self.removabledevicecombobox)
        self.device_eject_usb_button = QtWidgets.QPushButton(self.frame_35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_eject_usb_button.sizePolicy().hasHeightForWidth())
        self.device_eject_usb_button.setSizePolicy(sizePolicy)
        self.device_eject_usb_button.setMinimumSize(QtCore.QSize(100, 30))
        self.device_eject_usb_button.setMaximumSize(QtCore.QSize(100, 30))
        self.device_eject_usb_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.device_eject_usb_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.device_eject_usb_button.setObjectName("device_eject_usb_button")
        self.horizontalLayout_124.addWidget(self.device_eject_usb_button)
        self.verticalLayout_37.addLayout(self.horizontalLayout_124)
        self.horizontalLayout_125 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_125.setObjectName("horizontalLayout_125")
        self.filesystemtable_2 = FileSystemTable(self.frame_35)
        self.filesystemtable_2.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.filesystemtable_2.setStyleSheet("FileSystemTable {\n"
"    color: black;\n"
"       border: 4px;\n"
"    border-color: rgb(120, 120, 120);\n"
"    border-style: solid;\n"
"    background-color: rgb(238, 238, 236);\n"
"    font: 12pt \"Bebas Kai\";\n"
"}\n"
"\n"
"QHeaderView {\n"
"    background-color: rgb(220, 220, 220);\n"
"    color: black;\n"
"    border: none;\n"
"    border-radius:none;\n"
"    border-style: none;\n"
"    font: 13pt \"Bebas Kai\";\n"
"}")
        self.filesystemtable_2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.filesystemtable_2.setShowGrid(False)
        self.filesystemtable_2.setObjectName("filesystemtable_2")
        self.horizontalLayout_125.addWidget(self.filesystemtable_2)
        self.verticalLayout_37.addLayout(self.horizontalLayout_125)
        self.horizontalLayout_126 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_126.setObjectName("horizontalLayout_126")
        self.device_delete_item_button = QtWidgets.QPushButton(self.frame_35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_delete_item_button.sizePolicy().hasHeightForWidth())
        self.device_delete_item_button.setSizePolicy(sizePolicy)
        self.device_delete_item_button.setMinimumSize(QtCore.QSize(90, 30))
        self.device_delete_item_button.setMaximumSize(QtCore.QSize(90, 30))
        self.device_delete_item_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.device_delete_item_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/delete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.device_delete_item_button.setIcon(icon2)
        self.device_delete_item_button.setIconSize(QtCore.QSize(14, 14))
        self.device_delete_item_button.setObjectName("device_delete_item_button")
        self.horizontalLayout_126.addWidget(self.device_delete_item_button)
        self.device_new_file_button = QtWidgets.QPushButton(self.frame_35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_new_file_button.sizePolicy().hasHeightForWidth())
        self.device_new_file_button.setSizePolicy(sizePolicy)
        self.device_new_file_button.setMinimumSize(QtCore.QSize(100, 30))
        self.device_new_file_button.setMaximumSize(QtCore.QSize(100, 30))
        self.device_new_file_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.device_new_file_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/new_file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.device_new_file_button.setIcon(icon3)
        self.device_new_file_button.setIconSize(QtCore.QSize(12, 16))
        self.device_new_file_button.setObjectName("device_new_file_button")
        self.horizontalLayout_126.addWidget(self.device_new_file_button)
        self.device_new_folder_button = QtWidgets.QPushButton(self.frame_35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_new_folder_button.sizePolicy().hasHeightForWidth())
        self.device_new_folder_button.setSizePolicy(sizePolicy)
        self.device_new_folder_button.setMinimumSize(QtCore.QSize(125, 30))
        self.device_new_folder_button.setMaximumSize(QtCore.QSize(125, 30))
        self.device_new_folder_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.device_new_folder_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/new_folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.device_new_folder_button.setIcon(icon4)
        self.device_new_folder_button.setIconSize(QtCore.QSize(28, 15))
        self.device_new_folder_button.setObjectName("device_new_folder_button")
        self.horizontalLayout_126.addWidget(self.device_new_folder_button)
        self.device_rename_item_button = QtWidgets.QPushButton(self.frame_35)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.device_rename_item_button.sizePolicy().hasHeightForWidth())
        self.device_rename_item_button.setSizePolicy(sizePolicy)
        self.device_rename_item_button.setMinimumSize(QtCore.QSize(90, 30))
        self.device_rename_item_button.setMaximumSize(QtCore.QSize(90, 30))
        self.device_rename_item_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.device_rename_item_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.device_rename_item_button.setObjectName("device_rename_item_button")
        self.horizontalLayout_126.addWidget(self.device_rename_item_button)
        self.verticalLayout_37.addLayout(self.horizontalLayout_126)
        self.horizontalLayout_120.addWidget(self.frame_35)
        self.verticalLayout_36 = QtWidgets.QVBoxLayout()
        self.verticalLayout_36.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_36.setContentsMargins(0, 110, 0, 100)
        self.verticalLayout_36.setSpacing(15)
        self.verticalLayout_36.setObjectName("verticalLayout_36")
        self.copy_from_usb_2 = QtWidgets.QPushButton(self.file_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_from_usb_2.sizePolicy().hasHeightForWidth())
        self.copy_from_usb_2.setSizePolicy(sizePolicy)
        self.copy_from_usb_2.setMinimumSize(QtCore.QSize(60, 90))
        self.copy_from_usb_2.setMaximumSize(QtCore.QSize(60, 90))
        self.copy_from_usb_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.copy_from_usb_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.copy_from_usb_2.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"    padding-right: 4px;\n"
"}")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/tall_right_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy_from_usb_2.setIcon(icon5)
        self.copy_from_usb_2.setIconSize(QtCore.QSize(18, 60))
        self.copy_from_usb_2.setObjectName("copy_from_usb_2")
        self.verticalLayout_36.addWidget(self.copy_from_usb_2)
        self.copy_to_usb_2 = QtWidgets.QPushButton(self.file_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copy_to_usb_2.sizePolicy().hasHeightForWidth())
        self.copy_to_usb_2.setSizePolicy(sizePolicy)
        self.copy_to_usb_2.setMinimumSize(QtCore.QSize(60, 90))
        self.copy_to_usb_2.setMaximumSize(QtCore.QSize(60, 90))
        self.copy_to_usb_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.copy_to_usb_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.copy_to_usb_2.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"    padding-right: 8px;\n"
"}")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/tall_left_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copy_to_usb_2.setIcon(icon6)
        self.copy_to_usb_2.setIconSize(QtCore.QSize(28, 60))
        self.copy_to_usb_2.setObjectName("copy_to_usb_2")
        self.verticalLayout_36.addWidget(self.copy_to_usb_2)
        self.horizontalLayout_120.addLayout(self.verticalLayout_36)
        self.frame_34 = QtWidgets.QFrame(self.file_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_34.sizePolicy().hasHeightForWidth())
        self.frame_34.setSizePolicy(sizePolicy)
        self.frame_34.setMinimumSize(QtCore.QSize(500, 0))
        self.frame_34.setMaximumSize(QtCore.QSize(500, 16777215))
        self.frame_34.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_34.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_34.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_34.setObjectName("frame_34")
        self.verticalLayout_35 = QtWidgets.QVBoxLayout(self.frame_34)
        self.verticalLayout_35.setObjectName("verticalLayout_35")
        self.horizontalLayout_121 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_121.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_121.setObjectName("horizontalLayout_121")
        self.main_folder_up_button = QtWidgets.QPushButton(self.frame_34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_folder_up_button.sizePolicy().hasHeightForWidth())
        self.main_folder_up_button.setSizePolicy(sizePolicy)
        self.main_folder_up_button.setMinimumSize(QtCore.QSize(110, 30))
        self.main_folder_up_button.setMaximumSize(QtCore.QSize(110, 30))
        self.main_folder_up_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.main_folder_up_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.main_folder_up_button.setIcon(icon1)
        self.main_folder_up_button.setIconSize(QtCore.QSize(30, 17))
        self.main_folder_up_button.setObjectName("main_folder_up_button")
        self.horizontalLayout_121.addWidget(self.main_folder_up_button)
        self.recentfilecombobox_2 = RecentFileComboBox(self.frame_34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recentfilecombobox_2.sizePolicy().hasHeightForWidth())
        self.recentfilecombobox_2.setSizePolicy(sizePolicy)
        self.recentfilecombobox_2.setMinimumSize(QtCore.QSize(0, 30))
        self.recentfilecombobox_2.setMaximumSize(QtCore.QSize(16777215, 30))
        self.recentfilecombobox_2.setObjectName("recentfilecombobox_2")
        self.horizontalLayout_121.addWidget(self.recentfilecombobox_2)
        self.main_load_gcode_button = QtWidgets.QPushButton(self.frame_34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_load_gcode_button.sizePolicy().hasHeightForWidth())
        self.main_load_gcode_button.setSizePolicy(sizePolicy)
        self.main_load_gcode_button.setMinimumSize(QtCore.QSize(100, 30))
        self.main_load_gcode_button.setMaximumSize(QtCore.QSize(100, 30))
        self.main_load_gcode_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.main_load_gcode_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.main_load_gcode_button.setObjectName("main_load_gcode_button")
        self.horizontalLayout_121.addWidget(self.main_load_gcode_button)
        self.verticalLayout_35.addLayout(self.horizontalLayout_121)
        self.horizontalLayout_122 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_122.setObjectName("horizontalLayout_122")
        self.filesystemtable = FileSystemTable(self.frame_34)
        self.filesystemtable.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.filesystemtable.setStyleSheet("FileSystemTable {\n"
"    color: black;\n"
"       border: 4px;\n"
"    border-color: rgb(120, 120, 120);\n"
"    border-style: solid;\n"
"    background-color: rgb(238, 238, 236);\n"
"    font: 12pt \"Bebas Kai\";\n"
"}\n"
"\n"
"QHeaderView {\n"
"    background-color: rgb(220, 220, 220);\n"
"    color: black;\n"
"    border: none;\n"
"    border-radius:none;\n"
"    border-style: none;\n"
"    font: 13pt \"Bebas Kai\";\n"
"}")
        self.filesystemtable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.filesystemtable.setShowGrid(False)
        self.filesystemtable.setObjectName("filesystemtable")
        self.horizontalLayout_122.addWidget(self.filesystemtable)
        self.verticalLayout_35.addLayout(self.horizontalLayout_122)
        self.horizontalLayout_123 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_123.setObjectName("horizontalLayout_123")
        self.main_delete_item_button = QtWidgets.QPushButton(self.frame_34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_delete_item_button.sizePolicy().hasHeightForWidth())
        self.main_delete_item_button.setSizePolicy(sizePolicy)
        self.main_delete_item_button.setMinimumSize(QtCore.QSize(90, 30))
        self.main_delete_item_button.setMaximumSize(QtCore.QSize(90, 30))
        self.main_delete_item_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.main_delete_item_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.main_delete_item_button.setIcon(icon2)
        self.main_delete_item_button.setIconSize(QtCore.QSize(14, 14))
        self.main_delete_item_button.setObjectName("main_delete_item_button")
        self.horizontalLayout_123.addWidget(self.main_delete_item_button)
        self.main_new_file_button = QtWidgets.QPushButton(self.frame_34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_new_file_button.sizePolicy().hasHeightForWidth())
        self.main_new_file_button.setSizePolicy(sizePolicy)
        self.main_new_file_button.setMinimumSize(QtCore.QSize(100, 30))
        self.main_new_file_button.setMaximumSize(QtCore.QSize(100, 30))
        self.main_new_file_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.main_new_file_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.main_new_file_button.setIcon(icon3)
        self.main_new_file_button.setIconSize(QtCore.QSize(12, 16))
        self.main_new_file_button.setObjectName("main_new_file_button")
        self.horizontalLayout_123.addWidget(self.main_new_file_button)
        self.main_new_folder_button = QtWidgets.QPushButton(self.frame_34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_new_folder_button.sizePolicy().hasHeightForWidth())
        self.main_new_folder_button.setSizePolicy(sizePolicy)
        self.main_new_folder_button.setMinimumSize(QtCore.QSize(125, 30))
        self.main_new_folder_button.setMaximumSize(QtCore.QSize(125, 30))
        self.main_new_folder_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.main_new_folder_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.main_new_folder_button.setIcon(icon4)
        self.main_new_folder_button.setIconSize(QtCore.QSize(28, 15))
        self.main_new_folder_button.setObjectName("main_new_folder_button")
        self.horizontalLayout_123.addWidget(self.main_new_folder_button)
        self.main_rename_item_button = QtWidgets.QPushButton(self.frame_34)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_rename_item_button.sizePolicy().hasHeightForWidth())
        self.main_rename_item_button.setSizePolicy(sizePolicy)
        self.main_rename_item_button.setMinimumSize(QtCore.QSize(90, 30))
        self.main_rename_item_button.setMaximumSize(QtCore.QSize(90, 30))
        self.main_rename_item_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.main_rename_item_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.main_rename_item_button.setObjectName("main_rename_item_button")
        self.horizontalLayout_123.addWidget(self.main_rename_item_button)
        self.verticalLayout_35.addLayout(self.horizontalLayout_123)
        self.horizontalLayout_120.addWidget(self.frame_34)
        self.frame_36 = QtWidgets.QFrame(self.file_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_36.sizePolicy().hasHeightForWidth())
        self.frame_36.setSizePolicy(sizePolicy)
        self.frame_36.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_36.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_36.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_36.setObjectName("frame_36")
        self.verticalLayout_38 = QtWidgets.QVBoxLayout(self.frame_36)
        self.verticalLayout_38.setContentsMargins(9, -1, 9, 9)
        self.verticalLayout_38.setObjectName("verticalLayout_38")
        self.horizontalLayout_127 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_127.setObjectName("horizontalLayout_127")
        self.gcode_editor_button = QtWidgets.QPushButton(self.frame_36)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gcode_editor_button.sizePolicy().hasHeightForWidth())
        self.gcode_editor_button.setSizePolicy(sizePolicy)
        self.gcode_editor_button.setMinimumSize(QtCore.QSize(0, 30))
        self.gcode_editor_button.setMaximumSize(QtCore.QSize(16777215, 30))
        self.gcode_editor_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.gcode_editor_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.gcode_editor_button.setCheckable(True)
        self.gcode_editor_button.setChecked(True)
        self.gcode_editor_button.setAutoExclusive(True)
        self.gcode_editor_button.setProperty("page", 0)
        self.gcode_editor_button.setObjectName("gcode_editor_button")
        self.fileviewerbtnGroup = QtWidgets.QButtonGroup(Form)
        self.fileviewerbtnGroup.setObjectName("fileviewerbtnGroup")
        self.fileviewerbtnGroup.addButton(self.gcode_editor_button)
        self.horizontalLayout_127.addWidget(self.gcode_editor_button)
        self.setup_viewer_button = QtWidgets.QPushButton(self.frame_36)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.setup_viewer_button.sizePolicy().hasHeightForWidth())
        self.setup_viewer_button.setSizePolicy(sizePolicy)
        self.setup_viewer_button.setMinimumSize(QtCore.QSize(0, 30))
        self.setup_viewer_button.setMaximumSize(QtCore.QSize(16777215, 30))
        self.setup_viewer_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setup_viewer_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.setup_viewer_button.setCheckable(True)
        self.setup_viewer_button.setAutoExclusive(True)
        self.setup_viewer_button.setProperty("page", 1)
        self.setup_viewer_button.setObjectName("setup_viewer_button")
        self.fileviewerbtnGroup.addButton(self.setup_viewer_button)
        self.horizontalLayout_127.addWidget(self.setup_viewer_button)
        self.verticalLayout_38.addLayout(self.horizontalLayout_127)
        self.file_viewer_widget = QtWidgets.QStackedWidget(self.frame_36)
        self.file_viewer_widget.setMinimumSize(QtCore.QSize(457, 0))
        self.file_viewer_widget.setStyleSheet("QStackedWidget{\n"
"    background-color: transparent;\n"
"}")
        self.file_viewer_widget.setObjectName("file_viewer_widget")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_50 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_50.setObjectName("verticalLayout_50")
        self.file_absolute_path = QtWidgets.QLabel(self.page_5)
        self.file_absolute_path.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_absolute_path.sizePolicy().hasHeightForWidth())
        self.file_absolute_path.setSizePolicy(sizePolicy)
        self.file_absolute_path.setMinimumSize(QtCore.QSize(300, 25))
        self.file_absolute_path.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.file_absolute_path.setFont(font)
        self.file_absolute_path.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-radius: 4px;\n"
"    border-color: transparent;\n"
"    color: black;\n"
"      background-color: white;\n"
"    font: 12pt \"Bebas Kai\";\n"
"    padding-left: 6px;\n"
"}")
        self.file_absolute_path.setText("")
        self.file_absolute_path.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.file_absolute_path.setObjectName("file_absolute_path")
        self.verticalLayout_50.addWidget(self.file_absolute_path)
        self.gcodeeditor_2 = GcodeEditor(self.page_5)
        self.gcodeeditor_2.setStyleSheet("GcodeEditor {\n"
"    color: black;\n"
"       border: 4px;\n"
"    border-color: rgb(120, 120, 120);\n"
"    border-style: solid;\n"
"    background-color: rgb(238, 238, 236);\n"
"}")
        self.gcodeeditor_2.setProperty("is_editor", True)
        self.gcodeeditor_2.setObjectName("gcodeeditor_2")
        self.verticalLayout_50.addWidget(self.gcodeeditor_2)
        self.horizontalLayout_129 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_129.setObjectName("horizontalLayout_129")
        self.edit_gcode_button = QtWidgets.QPushButton(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edit_gcode_button.sizePolicy().hasHeightForWidth())
        self.edit_gcode_button.setSizePolicy(sizePolicy)
        self.edit_gcode_button.setMinimumSize(QtCore.QSize(100, 30))
        self.edit_gcode_button.setMaximumSize(QtCore.QSize(100, 30))
        self.edit_gcode_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.edit_gcode_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.edit_gcode_button.setCheckable(True)
        self.edit_gcode_button.setObjectName("edit_gcode_button")
        self.horizontalLayout_129.addWidget(self.edit_gcode_button)
        self.find_replace_button = QtWidgets.QPushButton(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.find_replace_button.sizePolicy().hasHeightForWidth())
        self.find_replace_button.setSizePolicy(sizePolicy)
        self.find_replace_button.setMinimumSize(QtCore.QSize(100, 30))
        self.find_replace_button.setMaximumSize(QtCore.QSize(100, 30))
        self.find_replace_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.find_replace_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.find_replace_button.setObjectName("find_replace_button")
        self.horizontalLayout_129.addWidget(self.find_replace_button)
        self.save_button = QtWidgets.QPushButton(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_button.sizePolicy().hasHeightForWidth())
        self.save_button.setSizePolicy(sizePolicy)
        self.save_button.setMinimumSize(QtCore.QSize(100, 30))
        self.save_button.setMaximumSize(QtCore.QSize(100, 30))
        self.save_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.save_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.save_button.setObjectName("save_button")
        self.horizontalLayout_129.addWidget(self.save_button)
        self.save_as_button = QtWidgets.QPushButton(self.page_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_as_button.sizePolicy().hasHeightForWidth())
        self.save_as_button.setSizePolicy(sizePolicy)
        self.save_as_button.setMinimumSize(QtCore.QSize(100, 30))
        self.save_as_button.setMaximumSize(QtCore.QSize(100, 30))
        self.save_as_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.save_as_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.save_as_button.setObjectName("save_as_button")
        self.horizontalLayout_129.addWidget(self.save_as_button)
        self.verticalLayout_50.addLayout(self.horizontalLayout_129)
        self.file_viewer_widget.addWidget(self.page_5)
        self.page_6 = QtWidgets.QWidget()
        self.page_6.setObjectName("page_6")
        self.verticalLayout_52 = QtWidgets.QVBoxLayout(self.page_6)
        self.verticalLayout_52.setObjectName("verticalLayout_52")
        self.gcodeeditor_4 = GcodeEditor(self.page_6)
        self.gcodeeditor_4.setStyleSheet("GcodeEditor {\n"
"    color: black;\n"
"       border: 4px;\n"
"    border-color: rgb(120, 120, 120);\n"
"    border-style: solid;\n"
"    background-color: rgb(238, 238, 236);\n"
"}")
        self.gcodeeditor_4.setProperty("is_editor", True)
        self.gcodeeditor_4.setObjectName("gcodeeditor_4")
        self.verticalLayout_52.addWidget(self.gcodeeditor_4)
        self.file_viewer_widget.addWidget(self.page_6)
        self.verticalLayout_38.addWidget(self.file_viewer_widget)
        self.horizontalLayout_120.addWidget(self.frame_36)
        self.verticalLayout_5.addLayout(self.horizontalLayout_120)
        self.tabWidget.addTab(self.file_tab, "")
        self.atc_tab = QtWidgets.QWidget()
        self.atc_tab.setObjectName("atc_tab")
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout(self.atc_tab)
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout()
        self.verticalLayout_18.setContentsMargins(12, -1, 6, -1)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.frame_33 = QtWidgets.QFrame(self.atc_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_33.sizePolicy().hasHeightForWidth())
        self.frame_33.setSizePolicy(sizePolicy)
        self.frame_33.setMinimumSize(QtCore.QSize(320, 550))
        self.frame_33.setMaximumSize(QtCore.QSize(320, 550))
        self.frame_33.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}")
        self.frame_33.setObjectName("frame_33")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_33)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_113 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_113.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_113.setSpacing(0)
        self.horizontalLayout_113.setObjectName("horizontalLayout_113")
        self.machine_column_header_9 = QtWidgets.QLabel(self.frame_33)
        self.machine_column_header_9.setMinimumSize(QtCore.QSize(0, 45))
        self.machine_column_header_9.setMaximumSize(QtCore.QSize(16777215, 45))
        self.machine_column_header_9.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179, 172);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"    background: rgb(90, 90, 90);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_9.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_9.setObjectName("machine_column_header_9")
        self.horizontalLayout_113.addWidget(self.machine_column_header_9)
        self.verticalLayout_7.addLayout(self.horizontalLayout_113)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_11.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_11.setSpacing(15)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.insert_atc_tool_input = QtWidgets.QLineEdit(self.frame_33)
        self.insert_atc_tool_input.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.insert_atc_tool_input.sizePolicy().hasHeightForWidth())
        self.insert_atc_tool_input.setSizePolicy(sizePolicy)
        self.insert_atc_tool_input.setMinimumSize(QtCore.QSize(125, 40))
        self.insert_atc_tool_input.setMaximumSize(QtCore.QSize(16777215, 40))
        self.insert_atc_tool_input.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.insert_atc_tool_input.setStyleSheet("font: 17pt;")
        self.insert_atc_tool_input.setAlignment(QtCore.Qt.AlignCenter)
        self.insert_atc_tool_input.setObjectName("insert_atc_tool_input")
        self.horizontalLayout_11.addWidget(self.insert_atc_tool_input)
        self.insert_atc_tool = ActionButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.insert_atc_tool.sizePolicy().hasHeightForWidth())
        self.insert_atc_tool.setSizePolicy(sizePolicy)
        self.insert_atc_tool.setMinimumSize(QtCore.QSize(125, 45))
        self.insert_atc_tool.setMaximumSize(QtCore.QSize(16777215, 45))
        self.insert_atc_tool.setFocusPolicy(QtCore.Qt.NoFocus)
        self.insert_atc_tool.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.insert_atc_tool.setObjectName("insert_atc_tool")
        self.horizontalLayout_11.addWidget(self.insert_atc_tool)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_114 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_114.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_114.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_114.setSpacing(15)
        self.horizontalLayout_114.setObjectName("horizontalLayout_114")
        self.delete_all_atc_tools = ActionButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_all_atc_tools.sizePolicy().hasHeightForWidth())
        self.delete_all_atc_tools.setSizePolicy(sizePolicy)
        self.delete_all_atc_tools.setMinimumSize(QtCore.QSize(125, 45))
        self.delete_all_atc_tools.setMaximumSize(QtCore.QSize(16777215, 45))
        self.delete_all_atc_tools.setFocusPolicy(QtCore.Qt.NoFocus)
        self.delete_all_atc_tools.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.delete_all_atc_tools.setObjectName("delete_all_atc_tools")
        self.horizontalLayout_114.addWidget(self.delete_all_atc_tools)
        self.delete_single_tool = ActionButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_single_tool.sizePolicy().hasHeightForWidth())
        self.delete_single_tool.setSizePolicy(sizePolicy)
        self.delete_single_tool.setMinimumSize(QtCore.QSize(125, 45))
        self.delete_single_tool.setMaximumSize(QtCore.QSize(16777215, 45))
        self.delete_single_tool.setFocusPolicy(QtCore.Qt.NoFocus)
        self.delete_single_tool.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.delete_single_tool.setObjectName("delete_single_tool")
        self.horizontalLayout_114.addWidget(self.delete_single_tool)
        self.verticalLayout_7.addLayout(self.horizontalLayout_114)
        self.horizontalLayout_115 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_115.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_115.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_115.setSpacing(15)
        self.horizontalLayout_115.setObjectName("horizontalLayout_115")
        self.subcallbutton_9 = MDIButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subcallbutton_9.sizePolicy().hasHeightForWidth())
        self.subcallbutton_9.setSizePolicy(sizePolicy)
        self.subcallbutton_9.setMinimumSize(QtCore.QSize(125, 45))
        self.subcallbutton_9.setMaximumSize(QtCore.QSize(16777215, 45))
        self.subcallbutton_9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.subcallbutton_9.setStyleSheet("MDIButton {\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/ccw_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.subcallbutton_9.setIcon(icon7)
        self.subcallbutton_9.setIconSize(QtCore.QSize(20, 20))
        self.subcallbutton_9.setObjectName("subcallbutton_9")
        self.horizontalLayout_115.addWidget(self.subcallbutton_9)
        self.subcallbutton_3 = MDIButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subcallbutton_3.sizePolicy().hasHeightForWidth())
        self.subcallbutton_3.setSizePolicy(sizePolicy)
        self.subcallbutton_3.setMinimumSize(QtCore.QSize(125, 45))
        self.subcallbutton_3.setMaximumSize(QtCore.QSize(16777215, 45))
        self.subcallbutton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.subcallbutton_3.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.subcallbutton_3.setStyleSheet("text-align: right;\n"
"padding-right: 19px;\n"
"font: 16pt \"Bebas Kai\";\n"
"")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/cw_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.subcallbutton_3.setIcon(icon8)
        self.subcallbutton_3.setIconSize(QtCore.QSize(20, 20))
        self.subcallbutton_3.setObjectName("subcallbutton_3")
        self.horizontalLayout_115.addWidget(self.subcallbutton_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_115)
        self.horizontalLayout_116 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_116.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_116.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_116.setSpacing(15)
        self.horizontalLayout_116.setObjectName("horizontalLayout_116")
        self.subcallbutton_11 = MDIButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subcallbutton_11.sizePolicy().hasHeightForWidth())
        self.subcallbutton_11.setSizePolicy(sizePolicy)
        self.subcallbutton_11.setMinimumSize(QtCore.QSize(125, 45))
        self.subcallbutton_11.setMaximumSize(QtCore.QSize(16777215, 45))
        self.subcallbutton_11.setFocusPolicy(QtCore.Qt.NoFocus)
        self.subcallbutton_11.setStyleSheet("MDIButton {\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/left_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.subcallbutton_11.setIcon(icon9)
        self.subcallbutton_11.setIconSize(QtCore.QSize(20, 20))
        self.subcallbutton_11.setObjectName("subcallbutton_11")
        self.horizontalLayout_116.addWidget(self.subcallbutton_11)
        self.subcallbutton_5 = MDIButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subcallbutton_5.sizePolicy().hasHeightForWidth())
        self.subcallbutton_5.setSizePolicy(sizePolicy)
        self.subcallbutton_5.setMinimumSize(QtCore.QSize(125, 45))
        self.subcallbutton_5.setMaximumSize(QtCore.QSize(16777215, 45))
        self.subcallbutton_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.subcallbutton_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.subcallbutton_5.setStyleSheet("MDIButton {\n"
"    text-align: right;\n"
"    padding-right: 10px;\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/right_arrow.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.subcallbutton_5.setIcon(icon10)
        self.subcallbutton_5.setIconSize(QtCore.QSize(20, 20))
        self.subcallbutton_5.setObjectName("subcallbutton_5")
        self.horizontalLayout_116.addWidget(self.subcallbutton_5)
        self.verticalLayout_7.addLayout(self.horizontalLayout_116)
        self.horizontalLayout_117 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_117.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_117.setSpacing(15)
        self.horizontalLayout_117.setObjectName("horizontalLayout_117")
        self.subcallbutton_16 = MDIButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subcallbutton_16.sizePolicy().hasHeightForWidth())
        self.subcallbutton_16.setSizePolicy(sizePolicy)
        self.subcallbutton_16.setMinimumSize(QtCore.QSize(125, 45))
        self.subcallbutton_16.setMaximumSize(QtCore.QSize(16777215, 45))
        self.subcallbutton_16.setFocusPolicy(QtCore.Qt.NoFocus)
        self.subcallbutton_16.setStyleSheet("MDIButton {\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.subcallbutton_16.setIconSize(QtCore.QSize(20, 20))
        self.subcallbutton_16.setObjectName("subcallbutton_16")
        self.horizontalLayout_117.addWidget(self.subcallbutton_16)
        self.subcallbutton_6 = MDIButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subcallbutton_6.sizePolicy().hasHeightForWidth())
        self.subcallbutton_6.setSizePolicy(sizePolicy)
        self.subcallbutton_6.setMinimumSize(QtCore.QSize(125, 45))
        self.subcallbutton_6.setMaximumSize(QtCore.QSize(16777215, 45))
        self.subcallbutton_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.subcallbutton_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.subcallbutton_6.setStyleSheet("font: 16pt \"Bebas Kai\";\n"
"")
        self.subcallbutton_6.setIconSize(QtCore.QSize(20, 20))
        self.subcallbutton_6.setObjectName("subcallbutton_6")
        self.horizontalLayout_117.addWidget(self.subcallbutton_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout_117)
        self.horizontalLayout_118 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_118.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_118.setSpacing(15)
        self.horizontalLayout_118.setObjectName("horizontalLayout_118")
        self.m01_break_button_10 = ActionButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m01_break_button_10.sizePolicy().hasHeightForWidth())
        self.m01_break_button_10.setSizePolicy(sizePolicy)
        self.m01_break_button_10.setMinimumSize(QtCore.QSize(125, 45))
        self.m01_break_button_10.setMaximumSize(QtCore.QSize(16777215, 45))
        self.m01_break_button_10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.m01_break_button_10.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.m01_break_button_10.setObjectName("m01_break_button_10")
        self.horizontalLayout_118.addWidget(self.m01_break_button_10)
        self.m01_break_button_27 = ActionButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m01_break_button_27.sizePolicy().hasHeightForWidth())
        self.m01_break_button_27.setSizePolicy(sizePolicy)
        self.m01_break_button_27.setMinimumSize(QtCore.QSize(125, 45))
        self.m01_break_button_27.setMaximumSize(QtCore.QSize(16777215, 45))
        self.m01_break_button_27.setFocusPolicy(QtCore.Qt.NoFocus)
        self.m01_break_button_27.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.m01_break_button_27.setObjectName("m01_break_button_27")
        self.horizontalLayout_118.addWidget(self.m01_break_button_27)
        self.verticalLayout_7.addLayout(self.horizontalLayout_118)
        self.horizontalLayout_119 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_119.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_119.setSpacing(15)
        self.horizontalLayout_119.setObjectName("horizontalLayout_119")
        self.reference_carousel = MDIButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reference_carousel.sizePolicy().hasHeightForWidth())
        self.reference_carousel.setSizePolicy(sizePolicy)
        self.reference_carousel.setMinimumSize(QtCore.QSize(125, 45))
        self.reference_carousel.setMaximumSize(QtCore.QSize(16777215, 45))
        self.reference_carousel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.reference_carousel.setStyleSheet("MDIButton {\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.reference_carousel.setIconSize(QtCore.QSize(20, 20))
        self.reference_carousel.setObjectName("reference_carousel")
        self.horizontalLayout_119.addWidget(self.reference_carousel)
        self.m01_break_button_14 = ActionButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m01_break_button_14.sizePolicy().hasHeightForWidth())
        self.m01_break_button_14.setSizePolicy(sizePolicy)
        self.m01_break_button_14.setMinimumSize(QtCore.QSize(55, 45))
        self.m01_break_button_14.setMaximumSize(QtCore.QSize(16777215, 45))
        self.m01_break_button_14.setFocusPolicy(QtCore.Qt.NoFocus)
        self.m01_break_button_14.setStyleSheet("QPushButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.m01_break_button_14.setObjectName("m01_break_button_14")
        self.horizontalLayout_119.addWidget(self.m01_break_button_14)
        self.m01_break_button_15 = ActionButton(self.frame_33)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m01_break_button_15.sizePolicy().hasHeightForWidth())
        self.m01_break_button_15.setSizePolicy(sizePolicy)
        self.m01_break_button_15.setMinimumSize(QtCore.QSize(55, 45))
        self.m01_break_button_15.setMaximumSize(QtCore.QSize(16777215, 45))
        self.m01_break_button_15.setFocusPolicy(QtCore.Qt.NoFocus)
        self.m01_break_button_15.setStyleSheet("QPushButton {\n"
"       font: 20pt \"Bebas Kai\";\n"
"}")
        self.m01_break_button_15.setObjectName("m01_break_button_15")
        self.horizontalLayout_119.addWidget(self.m01_break_button_15)
        self.verticalLayout_7.addLayout(self.horizontalLayout_119)
        self.verticalLayout_18.addWidget(self.frame_33)
        self.mdi_entry_box_3 = MDIEntry(self.atc_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdi_entry_box_3.sizePolicy().hasHeightForWidth())
        self.mdi_entry_box_3.setSizePolicy(sizePolicy)
        self.mdi_entry_box_3.setMinimumSize(QtCore.QSize(320, 40))
        self.mdi_entry_box_3.setMaximumSize(QtCore.QSize(320, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mdi_entry_box_3.setFont(font)
        self.mdi_entry_box_3.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mdi_entry_box_3.setObjectName("mdi_entry_box_3")
        self.verticalLayout_18.addWidget(self.mdi_entry_box_3)
        self.horizontalLayout_36.addLayout(self.verticalLayout_18)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setSpacing(0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.dynatc = DynATC(self.atc_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dynatc.sizePolicy().hasHeightForWidth())
        self.dynatc.setSizePolicy(sizePolicy)
        self.dynatc.setMinimumSize(QtCore.QSize(560, 560))
        self.dynatc.setMaximumSize(QtCore.QSize(560, 560))
        self.dynatc.setStyleSheet("QFrame {\n"
"    border: none;\n"
"}")
        self.dynatc.setResizeMode(QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self.dynatc.setObjectName("dynatc")
        self.horizontalLayout_13.addWidget(self.dynatc)
        self.horizontalLayout_36.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_50 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_50.setSpacing(0)
        self.horizontalLayout_50.setObjectName("horizontalLayout_50")
        self.widget_21 = QtWidgets.QWidget(self.atc_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_21.sizePolicy().hasHeightForWidth())
        self.widget_21.setSizePolicy(sizePolicy)
        self.widget_21.setMinimumSize(QtCore.QSize(350, 0))
        self.widget_21.setMaximumSize(QtCore.QSize(350, 16777215))
        self.widget_21.setStyleSheet("")
        self.widget_21.setObjectName("widget_21")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.widget_21)
        self.verticalLayout_14.setContentsMargins(0, 20, 0, 20)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.frame_40 = QtWidgets.QFrame(self.widget_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_40.sizePolicy().hasHeightForWidth())
        self.frame_40.setSizePolicy(sizePolicy)
        self.frame_40.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_40.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"    border-radius: 7px;\n"
"    padding-left: 3px;\n"
"    padding-right: 3px;\n"
"}")
        self.frame_40.setObjectName("frame_40")
        self.horizontalLayout_132 = QtWidgets.QHBoxLayout(self.frame_40)
        self.horizontalLayout_132.setContentsMargins(5, 3, 5, 3)
        self.horizontalLayout_132.setObjectName("horizontalLayout_132")
        self.horizontalLayout_133 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_133.setSpacing(3)
        self.horizontalLayout_133.setObjectName("horizontalLayout_133")
        self.tool_length_10 = StatusLabel(self.frame_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_length_10.sizePolicy().hasHeightForWidth())
        self.tool_length_10.setSizePolicy(sizePolicy)
        self.tool_length_10.setMinimumSize(QtCore.QSize(70, 40))
        self.tool_length_10.setMaximumSize(QtCore.QSize(16777215, 40))
        self.tool_length_10.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 7px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 13pt \"Bebas Kai\";\n"
"}")
        self.tool_length_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tool_length_10.setWordWrap(True)
        self.tool_length_10.setIndent(4)
        self.tool_length_10.setObjectName("tool_length_10")
        self.horizontalLayout_133.addWidget(self.tool_length_10)
        self.horizontalLayout_132.addLayout(self.horizontalLayout_133)
        self.verticalLayout_14.addWidget(self.frame_40)
        self.widget_3 = QtWidgets.QWidget(self.widget_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy)
        self.widget_3.setMinimumSize(QtCore.QSize(0, 280))
        self.widget_3.setMaximumSize(QtCore.QSize(16777215, 280))
        self.widget_3.setObjectName("widget_3")
        self.label_89 = QtWidgets.QLabel(self.widget_3)
        self.label_89.setGeometry(QtCore.QRect(40, 4, 169, 274))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_89.sizePolicy().hasHeightForWidth())
        self.label_89.setSizePolicy(sizePolicy)
        self.label_89.setStyleSheet("image: url(:/images/atc_spindle_tool.png);")
        self.label_89.setText("")
        self.label_89.setScaledContents(True)
        self.label_89.setIndent(0)
        self.label_89.setObjectName("label_89")
        self.loaded_spindle_tool_number = StatusLabel(self.widget_3)
        self.loaded_spindle_tool_number.setGeometry(QtCore.QRect(100, 135, 50, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loaded_spindle_tool_number.sizePolicy().hasHeightForWidth())
        self.loaded_spindle_tool_number.setSizePolicy(sizePolicy)
        self.loaded_spindle_tool_number.setMinimumSize(QtCore.QSize(50, 30))
        self.loaded_spindle_tool_number.setMaximumSize(QtCore.QSize(50, 30))
        self.loaded_spindle_tool_number.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 16pt \"Bebas Kai\";\n"
"}")
        self.loaded_spindle_tool_number.setAlignment(QtCore.Qt.AlignCenter)
        self.loaded_spindle_tool_number.setObjectName("loaded_spindle_tool_number")
        self.verticalLayout_14.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(self.widget_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setMinimumSize(QtCore.QSize(0, 202))
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 202))
        self.widget_4.setObjectName("widget_4")
        self.label_38 = QtWidgets.QLabel(self.widget_4)
        self.label_38.setGeometry(QtCore.QRect(110, 0, 240, 200))
        self.label_38.setStyleSheet("image: url(:/images/tool_probe.png);")
        self.label_38.setText("")
        self.label_38.setScaledContents(True)
        self.label_38.setObjectName("label_38")
        self.verticalLayout_14.addWidget(self.widget_4)
        self.horizontalLayout_50.addWidget(self.widget_21)
        self.horizontalLayout_36.addLayout(self.horizontalLayout_50)
        self.verticalLayout_17 = QtWidgets.QVBoxLayout()
        self.verticalLayout_17.setContentsMargins(-1, -1, 9, 5)
        self.verticalLayout_17.setSpacing(4)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.frame_6 = QtWidgets.QFrame(self.atc_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setMinimumSize(QtCore.QSize(320, 385))
        self.frame_6.setMaximumSize(QtCore.QSize(320, 385))
        self.frame_6.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}")
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_10.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout_10.setSpacing(5)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.machine_column_header_3 = QtWidgets.QLabel(self.frame_6)
        self.machine_column_header_3.setMinimumSize(QtCore.QSize(0, 45))
        self.machine_column_header_3.setMaximumSize(QtCore.QSize(16777215, 45))
        self.machine_column_header_3.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179, 172);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"    background: rgb(90, 90, 90);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_3.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_3.setObjectName("machine_column_header_3")
        self.horizontalLayout_25.addWidget(self.machine_column_header_3)
        self.verticalLayout_10.addLayout(self.horizontalLayout_25)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_26.setContentsMargins(4, 2, 2, 2)
        self.horizontalLayout_26.setSpacing(15)
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.load_spindle_tool_number = VCPLineEdit(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(200)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_spindle_tool_number.sizePolicy().hasHeightForWidth())
        self.load_spindle_tool_number.setSizePolicy(sizePolicy)
        self.load_spindle_tool_number.setMinimumSize(QtCore.QSize(0, 43))
        self.load_spindle_tool_number.setMaximumSize(QtCore.QSize(16777215, 43))
        self.load_spindle_tool_number.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.load_spindle_tool_number.setStyleSheet("font: 17pt;")
        self.load_spindle_tool_number.setAlignment(QtCore.Qt.AlignCenter)
        self.load_spindle_tool_number.setObjectName("load_spindle_tool_number")
        self.horizontalLayout_26.addWidget(self.load_spindle_tool_number)
        self.load_spindle_button = SubCallButton(self.frame_6)
        self.load_spindle_button.setMinimumSize(QtCore.QSize(125, 45))
        self.load_spindle_button.setMaximumSize(QtCore.QSize(16777215, 45))
        self.load_spindle_button.setStyleSheet("QPushButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 16pt;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"")
        self.load_spindle_button.setObjectName("load_spindle_button")
        self.horizontalLayout_26.addWidget(self.load_spindle_button)
        self.verticalLayout_10.addLayout(self.horizontalLayout_26)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_14.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.remove_current_tool = MDIButton(self.frame_6)
        self.remove_current_tool.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_current_tool.sizePolicy().hasHeightForWidth())
        self.remove_current_tool.setSizePolicy(sizePolicy)
        self.remove_current_tool.setMinimumSize(QtCore.QSize(130, 45))
        self.remove_current_tool.setMaximumSize(QtCore.QSize(16777215, 45))
        self.remove_current_tool.setFocusPolicy(QtCore.Qt.NoFocus)
        self.remove_current_tool.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.remove_current_tool.setCheckable(False)
        self.remove_current_tool.setAutoExclusive(True)
        self.remove_current_tool.setObjectName("remove_current_tool")
        self.horizontalLayout_14.addWidget(self.remove_current_tool)
        self.verticalLayout_10.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_135 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_135.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_135.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_135.setSpacing(15)
        self.horizontalLayout_135.setObjectName("horizontalLayout_135")
        self.subcallbutton_12 = MDIButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subcallbutton_12.sizePolicy().hasHeightForWidth())
        self.subcallbutton_12.setSizePolicy(sizePolicy)
        self.subcallbutton_12.setMinimumSize(QtCore.QSize(125, 45))
        self.subcallbutton_12.setMaximumSize(QtCore.QSize(16777215, 45))
        self.subcallbutton_12.setFocusPolicy(QtCore.Qt.NoFocus)
        self.subcallbutton_12.setStyleSheet("font: 16pt \"Bebas Kai\";")
        self.subcallbutton_12.setIcon(icon7)
        self.subcallbutton_12.setIconSize(QtCore.QSize(20, 20))
        self.subcallbutton_12.setObjectName("subcallbutton_12")
        self.horizontalLayout_135.addWidget(self.subcallbutton_12)
        self.subcallbutton_4 = MDIButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.subcallbutton_4.sizePolicy().hasHeightForWidth())
        self.subcallbutton_4.setSizePolicy(sizePolicy)
        self.subcallbutton_4.setMinimumSize(QtCore.QSize(125, 45))
        self.subcallbutton_4.setMaximumSize(QtCore.QSize(16777215, 45))
        self.subcallbutton_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.subcallbutton_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.subcallbutton_4.setStyleSheet("text-align: right;\n"
"padding-right: 19px;\n"
"font: 16pt \"Bebas Kai\";\n"
"")
        self.subcallbutton_4.setIcon(icon8)
        self.subcallbutton_4.setIconSize(QtCore.QSize(20, 20))
        self.subcallbutton_4.setObjectName("subcallbutton_4")
        self.horizontalLayout_135.addWidget(self.subcallbutton_4)
        self.verticalLayout_10.addLayout(self.horizontalLayout_135)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.store_tool_in_spindle = SubCallButton(self.frame_6)
        self.store_tool_in_spindle.setMinimumSize(QtCore.QSize(125, 45))
        self.store_tool_in_spindle.setMaximumSize(QtCore.QSize(16777215, 45))
        self.store_tool_in_spindle.setStyleSheet("QPushButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 16pt;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"")
        self.store_tool_in_spindle.setObjectName("store_tool_in_spindle")
        self.horizontalLayout_21.addWidget(self.store_tool_in_spindle)
        self.verticalLayout_10.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_134 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_134.setContentsMargins(4, 2, 2, 2)
        self.horizontalLayout_134.setSpacing(15)
        self.horizontalLayout_134.setObjectName("horizontalLayout_134")
        self.tool_number_entry_atc_page = VCPLineEdit(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_number_entry_atc_page.sizePolicy().hasHeightForWidth())
        self.tool_number_entry_atc_page.setSizePolicy(sizePolicy)
        self.tool_number_entry_atc_page.setMinimumSize(QtCore.QSize(128, 43))
        self.tool_number_entry_atc_page.setMaximumSize(QtCore.QSize(55, 43))
        self.tool_number_entry_atc_page.setSizeIncrement(QtCore.QSize(0, 40))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.tool_number_entry_atc_page.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_number_entry_atc_page.setFont(font)
        self.tool_number_entry_atc_page.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tool_number_entry_atc_page.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tool_number_entry_atc_page.setStyleSheet("font: 17pt;")
        self.tool_number_entry_atc_page.setFrame(True)
        self.tool_number_entry_atc_page.setAlignment(QtCore.Qt.AlignCenter)
        self.tool_number_entry_atc_page.setObjectName("tool_number_entry_atc_page")
        self.horizontalLayout_134.addWidget(self.tool_number_entry_atc_page)
        self.m6_tool_call_button_atc_page = SubCallButton(self.frame_6)
        self.m6_tool_call_button_atc_page.setMinimumSize(QtCore.QSize(125, 45))
        self.m6_tool_call_button_atc_page.setMaximumSize(QtCore.QSize(16777215, 45))
        self.m6_tool_call_button_atc_page.setStyleSheet("QPushButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 16pt;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"")
        self.m6_tool_call_button_atc_page.setObjectName("m6_tool_call_button_atc_page")
        self.horizontalLayout_134.addWidget(self.m6_tool_call_button_atc_page)
        self.verticalLayout_10.addLayout(self.horizontalLayout_134)
        self.verticalLayout_17.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.atc_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QtCore.QSize(320, 200))
        self.frame_7.setMaximumSize(QtCore.QSize(320, 200))
        self.frame_7.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}")
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setContentsMargins(-1, -1, -1, 6)
        self.verticalLayout_6.setSpacing(5)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.machine_column_header_2 = QtWidgets.QLabel(self.frame_7)
        self.machine_column_header_2.setMinimumSize(QtCore.QSize(0, 45))
        self.machine_column_header_2.setMaximumSize(QtCore.QSize(16777215, 45))
        self.machine_column_header_2.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179, 172);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"    background: rgb(90, 90, 90);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_2.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_2.setObjectName("machine_column_header_2")
        self.horizontalLayout_24.addWidget(self.machine_column_header_2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.m01_break_button_24 = ActionButton(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m01_break_button_24.sizePolicy().hasHeightForWidth())
        self.m01_break_button_24.setSizePolicy(sizePolicy)
        self.m01_break_button_24.setMinimumSize(QtCore.QSize(250, 45))
        self.m01_break_button_24.setMaximumSize(QtCore.QSize(16777215, 45))
        self.m01_break_button_24.setFocusPolicy(QtCore.Qt.NoFocus)
        self.m01_break_button_24.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.m01_break_button_24.setObjectName("m01_break_button_24")
        self.horizontalLayout_19.addWidget(self.m01_break_button_24)
        self.verticalLayout_6.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.m01_break_button_25 = ActionButton(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.m01_break_button_25.sizePolicy().hasHeightForWidth())
        self.m01_break_button_25.setSizePolicy(sizePolicy)
        self.m01_break_button_25.setMinimumSize(QtCore.QSize(250, 45))
        self.m01_break_button_25.setMaximumSize(QtCore.QSize(16777215, 45))
        self.m01_break_button_25.setFocusPolicy(QtCore.Qt.NoFocus)
        self.m01_break_button_25.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.m01_break_button_25.setObjectName("m01_break_button_25")
        self.horizontalLayout_23.addWidget(self.m01_break_button_25)
        self.verticalLayout_6.addLayout(self.horizontalLayout_23)
        self.verticalLayout_17.addWidget(self.frame_7)
        self.horizontalLayout_36.addLayout(self.verticalLayout_17)
        self.tabWidget.addTab(self.atc_tab, "")
        self.tool_tab = QtWidgets.QWidget()
        self.tool_tab.setObjectName("tool_tab")
        self.horizontalLayout_41 = QtWidgets.QHBoxLayout(self.tool_tab)
        self.horizontalLayout_41.setObjectName("horizontalLayout_41")
        self.tabWidget1 = QtWidgets.QTabWidget(self.tool_tab)
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(13)
        self.tabWidget1.setFont(font)
        self.tabWidget1.setStyleSheet("QTabWidget QTabBar::tab {\n"
"    margin-top: 9px;\n"
"    margin-bottom: 9px;\n"
"    min-width: 110px;\n"
"    min-height: 23px;\n"
"    font: 13pt \"bebas kai\";\n"
"}")
        self.tabWidget1.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget1.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget1.setTabBarAutoHide(False)
        self.tabWidget1.setObjectName("tabWidget1")
        self.TOOLTABLE = QtWidgets.QWidget()
        self.TOOLTABLE.setObjectName("TOOLTABLE")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.TOOLTABLE)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.verticalLayout_19 = QtWidgets.QVBoxLayout()
        self.verticalLayout_19.setContentsMargins(12, 2, 2, 23)
        self.verticalLayout_19.setSpacing(0)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.frame_13 = QtWidgets.QFrame(self.TOOLTABLE)
        self.frame_13.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_13.sizePolicy().hasHeightForWidth())
        self.frame_13.setSizePolicy(sizePolicy)
        self.frame_13.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_20.setContentsMargins(-1, 9, -1, -1)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_38.setContentsMargins(5, 5, 5, -1)
        self.horizontalLayout_38.setObjectName("horizontalLayout_38")
        self.tableWidget_2 = ToolTable(self.frame_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(90, 90, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(90, 90, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 235, 238))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(90, 90, 90))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        self.tableWidget_2.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tableWidget_2.setFont(font)
        self.tableWidget_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableWidget_2.setStyleSheet("TootTable,\n"
"QHeaderView {\n"
"    font: 14pt \"Bebas Kai\";\n"
"    background-color: rgb(220, 220, 220);\n"
"    color: black;\n"
"    border: none;\n"
"}\n"
"\n"
"ToolTable {\n"
"       border-top: 8px rgb(120, 120, 120);\n"
"    border-left: 4px  rgb(120, 120, 120);\n"
"    border-bottom: 5px rgb(120, 120, 120);\n"
"    border-right: 4px rgb(120, 120, 120);\n"
"    border-radius: 5px;\n"
"    border-color: rgb(120, 120, 120);\n"
"    border-style: solid;\n"
"    background-color: rgb(120, 120, 120);\n"
"    gridline-color: rgb(203, 203, 203);\n"
"    alternate-background-color: rgb(90, 90, 90);\n"
"}")
        self.tableWidget_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget_2.setLineWidth(3)
        self.tableWidget_2.setMidLineWidth(3)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed|QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableWidget_2.setProperty("showDropIndicator", True)
        self.tableWidget_2.setAlternatingRowColors(True)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget_2.setSortingEnabled(True)
        self.tableWidget_2.setProperty("currentToolColor", QtGui.QColor(42, 56, 255))
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(90)
        self.tableWidget_2.horizontalHeader().setHighlightSections(False)
        self.tableWidget_2.horizontalHeader().setMinimumSectionSize(90)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setCascadingSectionResizes(True)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_2.verticalHeader().setHighlightSections(False)
        self.tableWidget_2.verticalHeader().setMinimumSectionSize(30)
        self.horizontalLayout_38.addWidget(self.tableWidget_2)
        self.verticalLayout_20.addLayout(self.horizontalLayout_38)
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.tool_table_delete_button = QtWidgets.QPushButton(self.frame_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_table_delete_button.sizePolicy().hasHeightForWidth())
        self.tool_table_delete_button.setSizePolicy(sizePolicy)
        self.tool_table_delete_button.setMinimumSize(QtCore.QSize(120, 33))
        self.tool_table_delete_button.setMaximumSize(QtCore.QSize(120, 33))
        self.tool_table_delete_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_table_delete_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.tool_table_delete_button.setObjectName("tool_table_delete_button")
        self.horizontalLayout_37.addWidget(self.tool_table_delete_button)
        self.tool_table_add_tool_button = QtWidgets.QPushButton(self.frame_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_table_add_tool_button.sizePolicy().hasHeightForWidth())
        self.tool_table_add_tool_button.setSizePolicy(sizePolicy)
        self.tool_table_add_tool_button.setMinimumSize(QtCore.QSize(120, 33))
        self.tool_table_add_tool_button.setMaximumSize(QtCore.QSize(120, 33))
        self.tool_table_add_tool_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_table_add_tool_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.tool_table_add_tool_button.setObjectName("tool_table_add_tool_button")
        self.horizontalLayout_37.addWidget(self.tool_table_add_tool_button)
        self.tool_table_import_tool_button = QtWidgets.QPushButton(self.frame_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_table_import_tool_button.sizePolicy().hasHeightForWidth())
        self.tool_table_import_tool_button.setSizePolicy(sizePolicy)
        self.tool_table_import_tool_button.setMinimumSize(QtCore.QSize(120, 33))
        self.tool_table_import_tool_button.setMaximumSize(QtCore.QSize(120, 33))
        self.tool_table_import_tool_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_table_import_tool_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.tool_table_import_tool_button.setObjectName("tool_table_import_tool_button")
        self.horizontalLayout_37.addWidget(self.tool_table_import_tool_button)
        self.tool_table_export_tool_button = QtWidgets.QPushButton(self.frame_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_table_export_tool_button.sizePolicy().hasHeightForWidth())
        self.tool_table_export_tool_button.setSizePolicy(sizePolicy)
        self.tool_table_export_tool_button.setMinimumSize(QtCore.QSize(120, 33))
        self.tool_table_export_tool_button.setMaximumSize(QtCore.QSize(120, 33))
        self.tool_table_export_tool_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_table_export_tool_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.tool_table_export_tool_button.setObjectName("tool_table_export_tool_button")
        self.horizontalLayout_37.addWidget(self.tool_table_export_tool_button)
        self.tool_table_save_button = QtWidgets.QPushButton(self.frame_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_table_save_button.sizePolicy().hasHeightForWidth())
        self.tool_table_save_button.setSizePolicy(sizePolicy)
        self.tool_table_save_button.setMinimumSize(QtCore.QSize(120, 33))
        self.tool_table_save_button.setMaximumSize(QtCore.QSize(120, 33))
        self.tool_table_save_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_table_save_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.tool_table_save_button.setObjectName("tool_table_save_button")
        self.horizontalLayout_37.addWidget(self.tool_table_save_button)
        self.tool_table_reload_button = QtWidgets.QPushButton(self.frame_13)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_table_reload_button.sizePolicy().hasHeightForWidth())
        self.tool_table_reload_button.setSizePolicy(sizePolicy)
        self.tool_table_reload_button.setMinimumSize(QtCore.QSize(140, 33))
        self.tool_table_reload_button.setMaximumSize(QtCore.QSize(140, 33))
        self.tool_table_reload_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_table_reload_button.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.tool_table_reload_button.setObjectName("tool_table_reload_button")
        self.horizontalLayout_37.addWidget(self.tool_table_reload_button)
        self.verticalLayout_20.addLayout(self.horizontalLayout_37)
        self.verticalLayout_19.addWidget(self.frame_13)
        self.horizontalLayout_20.addLayout(self.verticalLayout_19)
        self.tabWidget1.addTab(self.TOOLTABLE, "")
        self.toollibrary = QtWidgets.QWidget()
        self.toollibrary.setObjectName("toollibrary")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.toollibrary)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout()
        self.verticalLayout_15.setContentsMargins(12, 2, 2, 23)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.frame_2 = QtWidgets.QFrame(self.toollibrary)
        self.frame_2.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_15.addWidget(self.frame_2)
        self.horizontalLayout_15.addLayout(self.verticalLayout_15)
        self.tabWidget1.addTab(self.toollibrary, "")
        self.horizontalLayout_41.addWidget(self.tabWidget1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(6, 21, 10, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_10 = QtWidgets.QFrame(self.tool_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy)
        self.frame_10.setMinimumSize(QtCore.QSize(580, 590))
        self.frame_10.setMaximumSize(QtCore.QSize(580, 590))
        self.frame_10.setStyleSheet("QFrame{\n"
"border-style: none;\n"
"border-color: transparent;\n"
"background-color: transparent;\n"
"border-width: 2px;\n"
"border-radius: 6px;\n"
"}")
        self.frame_10.setObjectName("frame_10")
        self.label_43 = QtWidgets.QLabel(self.frame_10)
        self.label_43.setGeometry(QtCore.QRect(45, 78, 250, 403))
        self.label_43.setStyleSheet("image: url(:/images/atc_spindle_tool_dimensioned.png);")
        self.label_43.setText("")
        self.label_43.setPixmap(QtGui.QPixmap(":/images/atc_spindle_tool_dimensioned.png"))
        self.label_43.setScaledContents(True)
        self.label_43.setObjectName("label_43")
        self.frame_11 = QtWidgets.QFrame(self.frame_10)
        self.frame_11.setGeometry(QtCore.QRect(0, 267, 145, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy)
        self.frame_11.setMinimumSize(QtCore.QSize(100, 60))
        self.frame_11.setMaximumSize(QtCore.QSize(16777215, 58))
        self.frame_11.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-width: 2px;\n"
"    border-radius: 6px;\n"
"    color: rgb(238, 238, 236);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}")
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_98 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_98.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_98.setObjectName("horizontalLayout_98")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setSpacing(3)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_48 = QtWidgets.QLabel(self.frame_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_48.sizePolicy().hasHeightForWidth())
        self.label_48.setSizePolicy(sizePolicy)
        self.label_48.setMinimumSize(QtCore.QSize(48, 33))
        self.label_48.setMaximumSize(QtCore.QSize(48, 33))
        self.label_48.setStyleSheet("QLabel{\n"
"font: 75 13pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.label_48.setAlignment(QtCore.Qt.AlignCenter)
        self.label_48.setWordWrap(True)
        self.label_48.setObjectName("label_48")
        self.horizontalLayout_17.addWidget(self.label_48)
        self.tool_length_5 = StatusLabel(self.frame_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_length_5.sizePolicy().hasHeightForWidth())
        self.tool_length_5.setSizePolicy(sizePolicy)
        self.tool_length_5.setMinimumSize(QtCore.QSize(70, 33))
        self.tool_length_5.setMaximumSize(QtCore.QSize(70, 33))
        self.tool_length_5.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.tool_length_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tool_length_5.setObjectName("tool_length_5")
        self.horizontalLayout_17.addWidget(self.tool_length_5)
        self.horizontalLayout_98.addLayout(self.horizontalLayout_17)
        self.frame_12 = QtWidgets.QFrame(self.frame_10)
        self.frame_12.setGeometry(QtCore.QRect(30, 446, 132, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_12.sizePolicy().hasHeightForWidth())
        self.frame_12.setSizePolicy(sizePolicy)
        self.frame_12.setMinimumSize(QtCore.QSize(100, 60))
        self.frame_12.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_12.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-width: 2px;\n"
"    border-radius: 6px;\n"
"    color: rgb(238, 238, 236);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}")
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_99 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_99.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_99.setObjectName("horizontalLayout_99")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setSpacing(3)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_49 = QtWidgets.QLabel(self.frame_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_49.sizePolicy().hasHeightForWidth())
        self.label_49.setSizePolicy(sizePolicy)
        self.label_49.setMinimumSize(QtCore.QSize(35, 33))
        self.label_49.setMaximumSize(QtCore.QSize(35, 33))
        self.label_49.setStyleSheet("QLabel{\n"
"font: 75 13pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.label_49.setAlignment(QtCore.Qt.AlignCenter)
        self.label_49.setWordWrap(True)
        self.label_49.setObjectName("label_49")
        self.horizontalLayout_18.addWidget(self.label_49)
        self.tool_diameter_2 = StatusLabel(self.frame_12)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_diameter_2.sizePolicy().hasHeightForWidth())
        self.tool_diameter_2.setSizePolicy(sizePolicy)
        self.tool_diameter_2.setMinimumSize(QtCore.QSize(70, 33))
        self.tool_diameter_2.setMaximumSize(QtCore.QSize(70, 33))
        self.tool_diameter_2.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.tool_diameter_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tool_diameter_2.setObjectName("tool_diameter_2")
        self.horizontalLayout_18.addWidget(self.tool_diameter_2)
        self.horizontalLayout_99.addLayout(self.horizontalLayout_18)
        self.frame_28 = QtWidgets.QFrame(self.frame_10)
        self.frame_28.setGeometry(QtCore.QRect(4, 0, 570, 60))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_28.sizePolicy().hasHeightForWidth())
        self.frame_28.setSizePolicy(sizePolicy)
        self.frame_28.setMinimumSize(QtCore.QSize(570, 60))
        self.frame_28.setMaximumSize(QtCore.QSize(570, 58))
        self.frame_28.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-width: 2px;\n"
"    border-radius: 6px;\n"
"    color: rgb(238, 238, 236);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}")
        self.frame_28.setObjectName("frame_28")
        self.horizontalLayout_108 = QtWidgets.QHBoxLayout(self.frame_28)
        self.horizontalLayout_108.setContentsMargins(5, -1, 5, -1)
        self.horizontalLayout_108.setObjectName("horizontalLayout_108")
        self.horizontalLayout_109 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_109.setSpacing(3)
        self.horizontalLayout_109.setObjectName("horizontalLayout_109")
        self.label_56 = QtWidgets.QLabel(self.frame_28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_56.sizePolicy().hasHeightForWidth())
        self.label_56.setSizePolicy(sizePolicy)
        self.label_56.setMinimumSize(QtCore.QSize(60, 33))
        self.label_56.setMaximumSize(QtCore.QSize(60, 33))
        self.label_56.setStyleSheet("QLabel{\n"
"font: 75 13pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.label_56.setAlignment(QtCore.Qt.AlignCenter)
        self.label_56.setWordWrap(True)
        self.label_56.setObjectName("label_56")
        self.horizontalLayout_109.addWidget(self.label_56)
        self.tool_length_7 = StatusLabel(self.frame_28)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_length_7.sizePolicy().hasHeightForWidth())
        self.tool_length_7.setSizePolicy(sizePolicy)
        self.tool_length_7.setMinimumSize(QtCore.QSize(70, 33))
        self.tool_length_7.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.tool_length_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.tool_length_7.setIndent(4)
        self.tool_length_7.setObjectName("tool_length_7")
        self.horizontalLayout_109.addWidget(self.tool_length_7)
        self.horizontalLayout_108.addLayout(self.horizontalLayout_109)
        self.mdi_entry_box_4 = MDIEntry(self.frame_10)
        self.mdi_entry_box_4.setGeometry(QtCore.QRect(4, 542, 570, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdi_entry_box_4.sizePolicy().hasHeightForWidth())
        self.mdi_entry_box_4.setSizePolicy(sizePolicy)
        self.mdi_entry_box_4.setMinimumSize(QtCore.QSize(570, 40))
        self.mdi_entry_box_4.setMaximumSize(QtCore.QSize(570, 40))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mdi_entry_box_4.setFont(font)
        self.mdi_entry_box_4.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mdi_entry_box_4.setObjectName("mdi_entry_box_4")
        self.tool_length_6 = StatusLabel(self.frame_10)
        self.tool_length_6.setGeometry(QtCore.QRect(180, 227, 50, 33))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_length_6.sizePolicy().hasHeightForWidth())
        self.tool_length_6.setSizePolicy(sizePolicy)
        self.tool_length_6.setMinimumSize(QtCore.QSize(50, 33))
        self.tool_length_6.setMaximumSize(QtCore.QSize(50, 33))
        self.tool_length_6.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.tool_length_6.setAlignment(QtCore.Qt.AlignCenter)
        self.tool_length_6.setObjectName("tool_length_6")
        self.frame_17 = QtWidgets.QFrame(self.frame_10)
        self.frame_17.setGeometry(QtCore.QRect(320, 80, 250, 250))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_17.sizePolicy().hasHeightForWidth())
        self.frame_17.setSizePolicy(sizePolicy)
        self.frame_17.setMinimumSize(QtCore.QSize(250, 250))
        self.frame_17.setMaximumSize(QtCore.QSize(250, 250))
        self.frame_17.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179, 172);\n"
"    border-width: 2px;\n"
"    border-radius: 6px;\n"
"    background-color: rgb(51, 57, 59);\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}")
        self.frame_17.setObjectName("frame_17")
        self.verticalLayout_49 = QtWidgets.QVBoxLayout(self.frame_17)
        self.verticalLayout_49.setContentsMargins(6, -1, 6, 7)
        self.verticalLayout_49.setSpacing(5)
        self.verticalLayout_49.setObjectName("verticalLayout_49")
        self.horizontalLayout_78 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_78.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout_78.setSpacing(0)
        self.horizontalLayout_78.setObjectName("horizontalLayout_78")
        self.machine_column_header_7 = QtWidgets.QLabel(self.frame_17)
        self.machine_column_header_7.setMinimumSize(QtCore.QSize(0, 45))
        self.machine_column_header_7.setMaximumSize(QtCore.QSize(16777215, 45))
        self.machine_column_header_7.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179, 172);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"    background: rgb(90, 90, 90);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_7.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_7.setObjectName("machine_column_header_7")
        self.horizontalLayout_78.addWidget(self.machine_column_header_7)
        self.verticalLayout_49.addLayout(self.horizontalLayout_78)
        self.horizontalLayout_79 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_79.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_79.setContentsMargins(4, 2, 2, 2)
        self.horizontalLayout_79.setSpacing(9)
        self.horizontalLayout_79.setObjectName("horizontalLayout_79")
        self.load_spindle_tool_number_2 = VCPLineEdit(self.frame_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_spindle_tool_number_2.sizePolicy().hasHeightForWidth())
        self.load_spindle_tool_number_2.setSizePolicy(sizePolicy)
        self.load_spindle_tool_number_2.setMinimumSize(QtCore.QSize(60, 43))
        self.load_spindle_tool_number_2.setMaximumSize(QtCore.QSize(16777215, 43))
        self.load_spindle_tool_number_2.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.load_spindle_tool_number_2.setStyleSheet("font: 16pt;")
        self.load_spindle_tool_number_2.setAlignment(QtCore.Qt.AlignCenter)
        self.load_spindle_tool_number_2.setObjectName("load_spindle_tool_number_2")
        self.horizontalLayout_79.addWidget(self.load_spindle_tool_number_2)
        self.load_spindle_button_2 = SubCallButton(self.frame_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.load_spindle_button_2.sizePolicy().hasHeightForWidth())
        self.load_spindle_button_2.setSizePolicy(sizePolicy)
        self.load_spindle_button_2.setMinimumSize(QtCore.QSize(120, 45))
        self.load_spindle_button_2.setMaximumSize(QtCore.QSize(16777215, 45))
        self.load_spindle_button_2.setStyleSheet("QPushButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 16pt;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"")
        self.load_spindle_button_2.setObjectName("load_spindle_button_2")
        self.horizontalLayout_79.addWidget(self.load_spindle_button_2)
        self.verticalLayout_49.addLayout(self.horizontalLayout_79)
        self.horizontalLayout_80 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_80.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_80.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_80.setSpacing(0)
        self.horizontalLayout_80.setObjectName("horizontalLayout_80")
        self.remove_current_tool_3 = MDIButton(self.frame_17)
        self.remove_current_tool_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_current_tool_3.sizePolicy().hasHeightForWidth())
        self.remove_current_tool_3.setSizePolicy(sizePolicy)
        self.remove_current_tool_3.setMinimumSize(QtCore.QSize(130, 45))
        self.remove_current_tool_3.setMaximumSize(QtCore.QSize(16777215, 45))
        self.remove_current_tool_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.remove_current_tool_3.setStyleSheet("QPushButton {\n"
"       font: 16pt \"Bebas Kai\";\n"
"}")
        self.remove_current_tool_3.setCheckable(False)
        self.remove_current_tool_3.setAutoExclusive(True)
        self.remove_current_tool_3.setObjectName("remove_current_tool_3")
        self.horizontalLayout_80.addWidget(self.remove_current_tool_3)
        self.verticalLayout_49.addLayout(self.horizontalLayout_80)
        self.horizontalLayout_145 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_145.setContentsMargins(4, 2, 2, 2)
        self.horizontalLayout_145.setSpacing(9)
        self.horizontalLayout_145.setObjectName("horizontalLayout_145")
        self.tool_number_entry_tool_page = VCPLineEdit(self.frame_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_number_entry_tool_page.sizePolicy().hasHeightForWidth())
        self.tool_number_entry_tool_page.setSizePolicy(sizePolicy)
        self.tool_number_entry_tool_page.setMinimumSize(QtCore.QSize(60, 43))
        self.tool_number_entry_tool_page.setMaximumSize(QtCore.QSize(16777215, 43))
        self.tool_number_entry_tool_page.setSizeIncrement(QtCore.QSize(0, 40))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.tool_number_entry_tool_page.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_number_entry_tool_page.setFont(font)
        self.tool_number_entry_tool_page.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tool_number_entry_tool_page.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tool_number_entry_tool_page.setStyleSheet("font: 16pt;")
        self.tool_number_entry_tool_page.setFrame(True)
        self.tool_number_entry_tool_page.setAlignment(QtCore.Qt.AlignCenter)
        self.tool_number_entry_tool_page.setObjectName("tool_number_entry_tool_page")
        self.horizontalLayout_145.addWidget(self.tool_number_entry_tool_page)
        self.m6_tool_call_button_tool_page = SubCallButton(self.frame_17)
        self.m6_tool_call_button_tool_page.setMinimumSize(QtCore.QSize(120, 45))
        self.m6_tool_call_button_tool_page.setMaximumSize(QtCore.QSize(16777215, 45))
        self.m6_tool_call_button_tool_page.setStyleSheet("QPushButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 16pt;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"")
        self.m6_tool_call_button_tool_page.setObjectName("m6_tool_call_button_tool_page")
        self.horizontalLayout_145.addWidget(self.m6_tool_call_button_tool_page)
        self.verticalLayout_49.addLayout(self.horizontalLayout_145)
        self.frame_18 = QtWidgets.QFrame(self.frame_10)
        self.frame_18.setGeometry(QtCore.QRect(320, 360, 250, 150))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_18.sizePolicy().hasHeightForWidth())
        self.frame_18.setSizePolicy(sizePolicy)
        self.frame_18.setMinimumSize(QtCore.QSize(250, 150))
        self.frame_18.setMaximumSize(QtCore.QSize(250, 150))
        self.frame_18.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179, 172);\n"
"    border-width: 2px;\n"
"    border-radius: 6px;\n"
"    background-color: rgb(51, 57, 59);\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}")
        self.frame_18.setObjectName("frame_18")
        self.verticalLayout_53 = QtWidgets.QVBoxLayout(self.frame_18)
        self.verticalLayout_53.setContentsMargins(6, -1, 6, 6)
        self.verticalLayout_53.setSpacing(5)
        self.verticalLayout_53.setObjectName("verticalLayout_53")
        self.horizontalLayout_82 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_82.setContentsMargins(0, 2, 0, 2)
        self.horizontalLayout_82.setSpacing(0)
        self.horizontalLayout_82.setObjectName("horizontalLayout_82")
        self.machine_column_header_8 = QtWidgets.QLabel(self.frame_18)
        self.machine_column_header_8.setMinimumSize(QtCore.QSize(0, 45))
        self.machine_column_header_8.setMaximumSize(QtCore.QSize(16777215, 45))
        self.machine_column_header_8.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179, 172);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"    background: rgb(90, 90, 90);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_8.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_8.setObjectName("machine_column_header_8")
        self.horizontalLayout_82.addWidget(self.machine_column_header_8)
        self.verticalLayout_53.addLayout(self.horizontalLayout_82)
        self.horizontalLayout_100 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_100.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_100.setSpacing(0)
        self.horizontalLayout_100.setObjectName("horizontalLayout_100")
        self.tool_touch_off_button = SubCallButton(self.frame_18)
        self.tool_touch_off_button.setMinimumSize(QtCore.QSize(145, 45))
        self.tool_touch_off_button.setStyleSheet("QPushButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 16pt;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"")
        self.tool_touch_off_button.setObjectName("tool_touch_off_button")
        self.horizontalLayout_100.addWidget(self.tool_touch_off_button)
        self.verticalLayout_53.addLayout(self.horizontalLayout_100)
        self.horizontalLayout_6.addWidget(self.frame_10)
        self.horizontalLayout_41.addLayout(self.horizontalLayout_6)
        self.tabWidget.addTab(self.tool_tab, "")
        self.offsets_tab = QtWidgets.QWidget()
        self.offsets_tab.setObjectName("offsets_tab")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.offsets_tab)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setContentsMargins(0, 18, 5, 18)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_37 = QtWidgets.QFrame(self.offsets_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_37.sizePolicy().hasHeightForWidth())
        self.frame_37.setSizePolicy(sizePolicy)
        self.frame_37.setMinimumSize(QtCore.QSize(545, 500))
        self.frame_37.setMaximumSize(QtCore.QSize(545, 500))
        self.frame_37.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_37.setObjectName("frame_37")
        self.verticalLayout_39 = QtWidgets.QVBoxLayout(self.frame_37)
        self.verticalLayout_39.setContentsMargins(-1, 9, -1, 5)
        self.verticalLayout_39.setSpacing(4)
        self.verticalLayout_39.setObjectName("verticalLayout_39")
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_47.setSpacing(0)
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.offset_table = OffsetTable(self.frame_37)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.offset_table.sizePolicy().hasHeightForWidth())
        self.offset_table.setSizePolicy(sizePolicy)
        self.offset_table.setMinimumSize(QtCore.QSize(522, 428))
        self.offset_table.setMaximumSize(QtCore.QSize(522, 428))
        self.offset_table.setStyleSheet("OffsetTable,\n"
"QHeaderView {\n"
"    font: 15pt \"Bebas Kai\";\n"
"    background-color: rgb(220, 220, 220);\n"
"    color: black;\n"
"    border: none;\n"
"}\n"
"\n"
"OffsetTable {\n"
"       border-top: 8px rgb(120, 120, 120);\n"
"    border-left: 4px  rgb(120, 120, 120);\n"
"    border-bottom: 5px rgb(120, 120, 120);\n"
"    border-right: 4px rgb(120, 120, 120);\n"
"    border-radius: 5px;\n"
"    border-color: rgb(120, 120, 120);\n"
"    border-style: solid;\n"
"    background-color: rgb(120, 120, 120);\n"
"    gridline-color: rgb(203, 203, 203);\n"
"    alternate-background-color: rgb(90, 90, 90);\n"
"    color: white;\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.offset_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.offset_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.offset_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.offset_table.setAutoScroll(False)
        self.offset_table.setAutoScrollMargin(0)
        self.offset_table.setWordWrap(False)
        self.offset_table.setCornerButtonEnabled(False)
        self.offset_table.setProperty("currentRowColor", QtGui.QColor(0, 38, 255))
        self.offset_table.setObjectName("offset_table")
        self.offset_table.horizontalHeader().setCascadingSectionResizes(False)
        self.offset_table.horizontalHeader().setDefaultSectionSize(118)
        self.offset_table.horizontalHeader().setHighlightSections(False)
        self.offset_table.horizontalHeader().setMinimumSectionSize(118)
        self.offset_table.horizontalHeader().setStretchLastSection(True)
        self.offset_table.verticalHeader().setDefaultSectionSize(43)
        self.offset_table.verticalHeader().setHighlightSections(False)
        self.offset_table.verticalHeader().setMinimumSectionSize(43)
        self.offset_table.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_47.addWidget(self.offset_table)
        self.verticalLayout_39.addLayout(self.horizontalLayout_47)
        self.horizontalLayout_130 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_130.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_130.setSpacing(10)
        self.horizontalLayout_130.setObjectName("horizontalLayout_130")
        self.x_axis_button_10 = QtWidgets.QPushButton(self.frame_37)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_axis_button_10.sizePolicy().hasHeightForWidth())
        self.x_axis_button_10.setSizePolicy(sizePolicy)
        self.x_axis_button_10.setMinimumSize(QtCore.QSize(100, 33))
        self.x_axis_button_10.setMaximumSize(QtCore.QSize(150, 33))
        self.x_axis_button_10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_axis_button_10.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.x_axis_button_10.setObjectName("x_axis_button_10")
        self.horizontalLayout_130.addWidget(self.x_axis_button_10)
        self.x_axis_button_11 = QtWidgets.QPushButton(self.frame_37)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_axis_button_11.sizePolicy().hasHeightForWidth())
        self.x_axis_button_11.setSizePolicy(sizePolicy)
        self.x_axis_button_11.setMinimumSize(QtCore.QSize(100, 33))
        self.x_axis_button_11.setMaximumSize(QtCore.QSize(150, 33))
        self.x_axis_button_11.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_axis_button_11.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.x_axis_button_11.setObjectName("x_axis_button_11")
        self.horizontalLayout_130.addWidget(self.x_axis_button_11)
        self.x_axis_button_13 = QtWidgets.QPushButton(self.frame_37)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_axis_button_13.sizePolicy().hasHeightForWidth())
        self.x_axis_button_13.setSizePolicy(sizePolicy)
        self.x_axis_button_13.setMinimumSize(QtCore.QSize(100, 33))
        self.x_axis_button_13.setMaximumSize(QtCore.QSize(150, 33))
        self.x_axis_button_13.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_axis_button_13.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.x_axis_button_13.setObjectName("x_axis_button_13")
        self.horizontalLayout_130.addWidget(self.x_axis_button_13)
        self.x_axis_button_14 = QtWidgets.QPushButton(self.frame_37)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_axis_button_14.sizePolicy().hasHeightForWidth())
        self.x_axis_button_14.setSizePolicy(sizePolicy)
        self.x_axis_button_14.setMinimumSize(QtCore.QSize(100, 33))
        self.x_axis_button_14.setMaximumSize(QtCore.QSize(150, 33))
        self.x_axis_button_14.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_axis_button_14.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.x_axis_button_14.setObjectName("x_axis_button_14")
        self.horizontalLayout_130.addWidget(self.x_axis_button_14)
        self.verticalLayout_39.addLayout(self.horizontalLayout_130)
        self.verticalLayout_11.addWidget(self.frame_37)
        self.mdi_entry_box_6 = MDIEntry(self.offsets_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdi_entry_box_6.sizePolicy().hasHeightForWidth())
        self.mdi_entry_box_6.setSizePolicy(sizePolicy)
        self.mdi_entry_box_6.setMinimumSize(QtCore.QSize(540, 40))
        self.mdi_entry_box_6.setMaximumSize(QtCore.QSize(540, 40))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mdi_entry_box_6.setFont(font)
        self.mdi_entry_box_6.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mdi_entry_box_6.setObjectName("mdi_entry_box_6")
        self.verticalLayout_11.addWidget(self.mdi_entry_box_6)
        self.horizontalLayout_8.addLayout(self.verticalLayout_11)
        self.horizontalLayout_51 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_51.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_51.setSpacing(0)
        self.horizontalLayout_51.setObjectName("horizontalLayout_51")
        self.frame_15 = QtWidgets.QFrame(self.offsets_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_15.sizePolicy().hasHeightForWidth())
        self.frame_15.setSizePolicy(sizePolicy)
        self.frame_15.setMinimumSize(QtCore.QSize(650, 560))
        self.frame_15.setMaximumSize(QtCore.QSize(650, 560))
        self.frame_15.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout_33 = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout_33.setContentsMargins(-1, 5, -1, 9)
        self.verticalLayout_33.setSpacing(15)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout_12.setContentsMargins(-1, 5, -1, -1)
        self.gridLayout_12.setHorizontalSpacing(20)
        self.gridLayout_12.setVerticalSpacing(12)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.machine_column_header_4 = QtWidgets.QLabel(self.frame_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_column_header_4.sizePolicy().hasHeightForWidth())
        self.machine_column_header_4.setSizePolicy(sizePolicy)
        self.machine_column_header_4.setMinimumSize(QtCore.QSize(0, 55))
        self.machine_column_header_4.setMaximumSize(QtCore.QSize(16777215, 55))
        self.machine_column_header_4.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179,172);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    background: rgb(90, 90, 90);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_4.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_4.setObjectName("machine_column_header_4")
        self.gridLayout_12.addWidget(self.machine_column_header_4, 0, 0, 1, 5)
        self.actionbutton_g54_2 = ActionButton(self.frame_15)
        self.actionbutton_g54_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g54_2.sizePolicy().hasHeightForWidth())
        self.actionbutton_g54_2.setSizePolicy(sizePolicy)
        self.actionbutton_g54_2.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g54_2.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g54_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g54_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g54_2.setAutoExclusive(True)
        self.actionbutton_g54_2.setObjectName("actionbutton_g54_2")
        self.gridLayout_12.addWidget(self.actionbutton_g54_2, 1, 0, 1, 1)
        self.actionbutton_g55_2 = ActionButton(self.frame_15)
        self.actionbutton_g55_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g55_2.sizePolicy().hasHeightForWidth())
        self.actionbutton_g55_2.setSizePolicy(sizePolicy)
        self.actionbutton_g55_2.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g55_2.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g55_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g55_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g55_2.setAutoExclusive(True)
        self.actionbutton_g55_2.setObjectName("actionbutton_g55_2")
        self.gridLayout_12.addWidget(self.actionbutton_g55_2, 1, 1, 1, 1)
        self.actionbutton_g56_2 = ActionButton(self.frame_15)
        self.actionbutton_g56_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g56_2.sizePolicy().hasHeightForWidth())
        self.actionbutton_g56_2.setSizePolicy(sizePolicy)
        self.actionbutton_g56_2.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g56_2.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g56_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g56_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g56_2.setAutoExclusive(True)
        self.actionbutton_g56_2.setObjectName("actionbutton_g56_2")
        self.gridLayout_12.addWidget(self.actionbutton_g56_2, 1, 2, 1, 1)
        self.actionbutton_g57_2 = ActionButton(self.frame_15)
        self.actionbutton_g57_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g57_2.sizePolicy().hasHeightForWidth())
        self.actionbutton_g57_2.setSizePolicy(sizePolicy)
        self.actionbutton_g57_2.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g57_2.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g57_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g57_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g57_2.setAutoExclusive(True)
        self.actionbutton_g57_2.setObjectName("actionbutton_g57_2")
        self.gridLayout_12.addWidget(self.actionbutton_g57_2, 1, 3, 1, 1)
        self.actionbutton_g58_2 = ActionButton(self.frame_15)
        self.actionbutton_g58_2.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g58_2.sizePolicy().hasHeightForWidth())
        self.actionbutton_g58_2.setSizePolicy(sizePolicy)
        self.actionbutton_g58_2.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g58_2.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g58_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g58_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g58_2.setAutoExclusive(True)
        self.actionbutton_g58_2.setObjectName("actionbutton_g58_2")
        self.gridLayout_12.addWidget(self.actionbutton_g58_2, 1, 4, 1, 1)
        self.actionbutton_g59_4 = ActionButton(self.frame_15)
        self.actionbutton_g59_4.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g59_4.sizePolicy().hasHeightForWidth())
        self.actionbutton_g59_4.setSizePolicy(sizePolicy)
        self.actionbutton_g59_4.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g59_4.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g59_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g59_4.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g59_4.setAutoExclusive(True)
        self.actionbutton_g59_4.setObjectName("actionbutton_g59_4")
        self.gridLayout_12.addWidget(self.actionbutton_g59_4, 2, 1, 1, 1)
        self.actionbutton_g59_5 = ActionButton(self.frame_15)
        self.actionbutton_g59_5.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g59_5.sizePolicy().hasHeightForWidth())
        self.actionbutton_g59_5.setSizePolicy(sizePolicy)
        self.actionbutton_g59_5.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g59_5.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g59_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g59_5.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g59_5.setAutoExclusive(True)
        self.actionbutton_g59_5.setObjectName("actionbutton_g59_5")
        self.gridLayout_12.addWidget(self.actionbutton_g59_5, 2, 2, 1, 1)
        self.actionbutton_g59_6 = ActionButton(self.frame_15)
        self.actionbutton_g59_6.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g59_6.sizePolicy().hasHeightForWidth())
        self.actionbutton_g59_6.setSizePolicy(sizePolicy)
        self.actionbutton_g59_6.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g59_6.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g59_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g59_6.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g59_6.setAutoExclusive(True)
        self.actionbutton_g59_6.setObjectName("actionbutton_g59_6")
        self.gridLayout_12.addWidget(self.actionbutton_g59_6, 2, 3, 1, 1)
        self.actionbutton_g59_7 = ActionButton(self.frame_15)
        self.actionbutton_g59_7.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g59_7.sizePolicy().hasHeightForWidth())
        self.actionbutton_g59_7.setSizePolicy(sizePolicy)
        self.actionbutton_g59_7.setMinimumSize(QtCore.QSize(110, 38))
        self.actionbutton_g59_7.setMaximumSize(QtCore.QSize(110, 38))
        self.actionbutton_g59_7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g59_7.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g59_7.setAutoExclusive(True)
        self.actionbutton_g59_7.setObjectName("actionbutton_g59_7")
        self.gridLayout_12.addWidget(self.actionbutton_g59_7, 2, 4, 1, 1)
        self.verticalLayout_33.addLayout(self.gridLayout_12)
        self.frame_31 = QtWidgets.QFrame(self.frame_15)
        self.frame_31.setStyleSheet("QFrame{\n"
"    border: none;\n"
"}")
        self.frame_31.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_31.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_31.setObjectName("frame_31")
        self.verticalLayout_33.addWidget(self.frame_31)
        self.frame_32 = QtWidgets.QFrame(self.frame_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_32.sizePolicy().hasHeightForWidth())
        self.frame_32.setSizePolicy(sizePolicy)
        self.frame_32.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_32.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179,172);\n"
"    border-width: 2px;\n"
"    border-radius: 6px;\n"
"    background-color: rgb(90, 90, 90);\n"
"    padding: -5px;\n"
"}")
        self.frame_32.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_32.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_32.setObjectName("frame_32")
        self.verticalLayout_34 = QtWidgets.QVBoxLayout(self.frame_32)
        self.verticalLayout_34.setContentsMargins(10, -1, 11, -1)
        self.verticalLayout_34.setSpacing(5)
        self.verticalLayout_34.setObjectName("verticalLayout_34")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_7.setSpacing(13)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.axis_column_header_9 = QtWidgets.QLabel(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axis_column_header_9.sizePolicy().hasHeightForWidth())
        self.axis_column_header_9.setSizePolicy(sizePolicy)
        self.axis_column_header_9.setMinimumSize(QtCore.QSize(55, 50))
        self.axis_column_header_9.setMaximumSize(QtCore.QSize(55, 50))
        self.axis_column_header_9.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.axis_column_header_9.setAlignment(QtCore.Qt.AlignCenter)
        self.axis_column_header_9.setWordWrap(True)
        self.axis_column_header_9.setObjectName("axis_column_header_9")
        self.horizontalLayout_7.addWidget(self.axis_column_header_9)
        self.axis_column_header_10 = QtWidgets.QLabel(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axis_column_header_10.sizePolicy().hasHeightForWidth())
        self.axis_column_header_10.setSizePolicy(sizePolicy)
        self.axis_column_header_10.setMinimumSize(QtCore.QSize(45, 50))
        self.axis_column_header_10.setMaximumSize(QtCore.QSize(45, 50))
        self.axis_column_header_10.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.axis_column_header_10.setAlignment(QtCore.Qt.AlignCenter)
        self.axis_column_header_10.setWordWrap(True)
        self.axis_column_header_10.setObjectName("axis_column_header_10")
        self.horizontalLayout_7.addWidget(self.axis_column_header_10)
        self.machine_column_header_10 = QtWidgets.QLabel(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_column_header_10.sizePolicy().hasHeightForWidth())
        self.machine_column_header_10.setSizePolicy(sizePolicy)
        self.machine_column_header_10.setMinimumSize(QtCore.QSize(88, 50))
        self.machine_column_header_10.setMaximumSize(QtCore.QSize(16777215, 50))
        self.machine_column_header_10.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_10.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_10.setWordWrap(True)
        self.machine_column_header_10.setObjectName("machine_column_header_10")
        self.horizontalLayout_7.addWidget(self.machine_column_header_10)
        self.machine_column_header_11 = QtWidgets.QLabel(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_column_header_11.sizePolicy().hasHeightForWidth())
        self.machine_column_header_11.setSizePolicy(sizePolicy)
        self.machine_column_header_11.setMinimumSize(QtCore.QSize(85, 50))
        self.machine_column_header_11.setMaximumSize(QtCore.QSize(16777215, 50))
        self.machine_column_header_11.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_11.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_11.setWordWrap(True)
        self.machine_column_header_11.setObjectName("machine_column_header_11")
        self.horizontalLayout_7.addWidget(self.machine_column_header_11)
        self.machine_column_header_12 = QtWidgets.QLabel(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_column_header_12.sizePolicy().hasHeightForWidth())
        self.machine_column_header_12.setSizePolicy(sizePolicy)
        self.machine_column_header_12.setMinimumSize(QtCore.QSize(60, 50))
        self.machine_column_header_12.setMaximumSize(QtCore.QSize(16777215, 50))
        self.machine_column_header_12.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_12.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_12.setWordWrap(True)
        self.machine_column_header_12.setObjectName("machine_column_header_12")
        self.horizontalLayout_7.addWidget(self.machine_column_header_12)
        self.ref_coilumn_header_4 = QtWidgets.QLabel(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_4.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_4.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_4.setMinimumSize(QtCore.QSize(65, 50))
        self.ref_coilumn_header_4.setMaximumSize(QtCore.QSize(16777215, 50))
        self.ref_coilumn_header_4.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.ref_coilumn_header_4.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_4.setWordWrap(True)
        self.ref_coilumn_header_4.setObjectName("ref_coilumn_header_4")
        self.horizontalLayout_7.addWidget(self.ref_coilumn_header_4)
        self.machine_column_header_13 = QtWidgets.QLabel(self.frame_32)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_column_header_13.sizePolicy().hasHeightForWidth())
        self.machine_column_header_13.setSizePolicy(sizePolicy)
        self.machine_column_header_13.setMinimumSize(QtCore.QSize(65, 50))
        self.machine_column_header_13.setMaximumSize(QtCore.QSize(16777215, 50))
        self.machine_column_header_13.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.machine_column_header_13.setAlignment(QtCore.Qt.AlignCenter)
        self.machine_column_header_13.setWordWrap(True)
        self.machine_column_header_13.setObjectName("machine_column_header_13")
        self.horizontalLayout_7.addWidget(self.machine_column_header_13)
        self.verticalLayout_34.addLayout(self.horizontalLayout_7)
        self.verticalLayout_33.addWidget(self.frame_32)
        self.dro_qvboxlayout_3 = QtWidgets.QVBoxLayout()
        self.dro_qvboxlayout_3.setContentsMargins(6, 0, 6, 5)
        self.dro_qvboxlayout_3.setSpacing(15)
        self.dro_qvboxlayout_3.setObjectName("dro_qvboxlayout_3")
        self.x_axis_dro_layout_3 = QtWidgets.QHBoxLayout()
        self.x_axis_dro_layout_3.setContentsMargins(-1, 1, -1, 1)
        self.x_axis_dro_layout_3.setSpacing(12)
        self.x_axis_dro_layout_3.setObjectName("x_axis_dro_layout_3")
        self.zero_x_button_2 = MDIButton(self.frame_15)
        self.zero_x_button_2.setEnabled(False)
        self.zero_x_button_2.setMinimumSize(QtCore.QSize(55, 38))
        self.zero_x_button_2.setMaximumSize(QtCore.QSize(55, 38))
        self.zero_x_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_x_button_2.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.zero_x_button_2.setObjectName("zero_x_button_2")
        self.x_axis_dro_layout_3.addWidget(self.zero_x_button_2)
        self.axis_column_header_11 = QtWidgets.QLabel(self.frame_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axis_column_header_11.sizePolicy().hasHeightForWidth())
        self.axis_column_header_11.setSizePolicy(sizePolicy)
        self.axis_column_header_11.setMinimumSize(QtCore.QSize(45, 35))
        self.axis_column_header_11.setMaximumSize(QtCore.QSize(45, 35))
        self.axis_column_header_11.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    font: 18pt \"Bebas Kai\";\n"
"}")
        self.axis_column_header_11.setAlignment(QtCore.Qt.AlignCenter)
        self.axis_column_header_11.setObjectName("axis_column_header_11")
        self.x_axis_dro_layout_3.addWidget(self.axis_column_header_11)
        self.statuslabel_50 = StatusLabel(self.frame_15)
        self.statuslabel_50.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_50.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_50.setObjectName("statuslabel_50")
        self.x_axis_dro_layout_3.addWidget(self.statuslabel_50)
        self.statuslabel_51 = StatusLabel(self.frame_15)
        self.statuslabel_51.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_51.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_51.setObjectName("statuslabel_51")
        self.x_axis_dro_layout_3.addWidget(self.statuslabel_51)
        self.statuslabel_52 = StatusLabel(self.frame_15)
        self.statuslabel_52.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_52.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_52.setObjectName("statuslabel_52")
        self.x_axis_dro_layout_3.addWidget(self.statuslabel_52)
        self.statuslabel_53 = StatusLabel(self.frame_15)
        self.statuslabel_53.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_53.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_53.setObjectName("statuslabel_53")
        self.x_axis_dro_layout_3.addWidget(self.statuslabel_53)
        self.statuslabel_54 = StatusLabel(self.frame_15)
        self.statuslabel_54.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_54.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_54.setObjectName("statuslabel_54")
        self.x_axis_dro_layout_3.addWidget(self.statuslabel_54)
        self.dro_qvboxlayout_3.addLayout(self.x_axis_dro_layout_3)
        self.y_axis_dro_layout_3 = QtWidgets.QHBoxLayout()
        self.y_axis_dro_layout_3.setContentsMargins(-1, 1, -1, 1)
        self.y_axis_dro_layout_3.setSpacing(12)
        self.y_axis_dro_layout_3.setObjectName("y_axis_dro_layout_3")
        self.zero_y_button_2 = MDIButton(self.frame_15)
        self.zero_y_button_2.setEnabled(False)
        self.zero_y_button_2.setMinimumSize(QtCore.QSize(55, 38))
        self.zero_y_button_2.setMaximumSize(QtCore.QSize(55, 38))
        self.zero_y_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_y_button_2.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.zero_y_button_2.setObjectName("zero_y_button_2")
        self.y_axis_dro_layout_3.addWidget(self.zero_y_button_2)
        self.axis_column_header_12 = QtWidgets.QLabel(self.frame_15)
        self.axis_column_header_12.setMinimumSize(QtCore.QSize(45, 35))
        self.axis_column_header_12.setMaximumSize(QtCore.QSize(45, 35))
        self.axis_column_header_12.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    font: 18pt \"Bebas Kai\";\n"
"}")
        self.axis_column_header_12.setAlignment(QtCore.Qt.AlignCenter)
        self.axis_column_header_12.setObjectName("axis_column_header_12")
        self.y_axis_dro_layout_3.addWidget(self.axis_column_header_12)
        self.statuslabel_55 = StatusLabel(self.frame_15)
        self.statuslabel_55.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_55.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_55.setObjectName("statuslabel_55")
        self.y_axis_dro_layout_3.addWidget(self.statuslabel_55)
        self.statuslabel_56 = StatusLabel(self.frame_15)
        self.statuslabel_56.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_56.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_56.setObjectName("statuslabel_56")
        self.y_axis_dro_layout_3.addWidget(self.statuslabel_56)
        self.statuslabel_57 = StatusLabel(self.frame_15)
        self.statuslabel_57.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_57.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_57.setObjectName("statuslabel_57")
        self.y_axis_dro_layout_3.addWidget(self.statuslabel_57)
        self.statuslabel_58 = StatusLabel(self.frame_15)
        self.statuslabel_58.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_58.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_58.setObjectName("statuslabel_58")
        self.y_axis_dro_layout_3.addWidget(self.statuslabel_58)
        self.statuslabel_59 = StatusLabel(self.frame_15)
        self.statuslabel_59.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_59.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_59.setObjectName("statuslabel_59")
        self.y_axis_dro_layout_3.addWidget(self.statuslabel_59)
        self.dro_qvboxlayout_3.addLayout(self.y_axis_dro_layout_3)
        self.z_axis_dro_layout_3 = QtWidgets.QHBoxLayout()
        self.z_axis_dro_layout_3.setContentsMargins(-1, 1, -1, 1)
        self.z_axis_dro_layout_3.setSpacing(12)
        self.z_axis_dro_layout_3.setObjectName("z_axis_dro_layout_3")
        self.zero_z_button_2 = MDIButton(self.frame_15)
        self.zero_z_button_2.setEnabled(False)
        self.zero_z_button_2.setMinimumSize(QtCore.QSize(55, 38))
        self.zero_z_button_2.setMaximumSize(QtCore.QSize(55, 38))
        self.zero_z_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_z_button_2.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.zero_z_button_2.setObjectName("zero_z_button_2")
        self.z_axis_dro_layout_3.addWidget(self.zero_z_button_2)
        self.axis_column_header_13 = QtWidgets.QLabel(self.frame_15)
        self.axis_column_header_13.setMinimumSize(QtCore.QSize(45, 35))
        self.axis_column_header_13.setMaximumSize(QtCore.QSize(45, 35))
        self.axis_column_header_13.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    font: 18pt \"Bebas Kai\";\n"
"}")
        self.axis_column_header_13.setAlignment(QtCore.Qt.AlignCenter)
        self.axis_column_header_13.setObjectName("axis_column_header_13")
        self.z_axis_dro_layout_3.addWidget(self.axis_column_header_13)
        self.statuslabel_60 = StatusLabel(self.frame_15)
        self.statuslabel_60.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_60.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_60.setObjectName("statuslabel_60")
        self.z_axis_dro_layout_3.addWidget(self.statuslabel_60)
        self.statuslabel_61 = StatusLabel(self.frame_15)
        self.statuslabel_61.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_61.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_61.setObjectName("statuslabel_61")
        self.z_axis_dro_layout_3.addWidget(self.statuslabel_61)
        self.statuslabel_62 = StatusLabel(self.frame_15)
        self.statuslabel_62.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_62.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_62.setObjectName("statuslabel_62")
        self.z_axis_dro_layout_3.addWidget(self.statuslabel_62)
        self.statuslabel_63 = StatusLabel(self.frame_15)
        self.statuslabel_63.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_63.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_63.setObjectName("statuslabel_63")
        self.z_axis_dro_layout_3.addWidget(self.statuslabel_63)
        self.statuslabel_64 = StatusLabel(self.frame_15)
        self.statuslabel_64.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_64.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_64.setObjectName("statuslabel_64")
        self.z_axis_dro_layout_3.addWidget(self.statuslabel_64)
        self.dro_qvboxlayout_3.addLayout(self.z_axis_dro_layout_3)
        self.a_axis_dro_layout_3 = QtWidgets.QHBoxLayout()
        self.a_axis_dro_layout_3.setContentsMargins(-1, 1, -1, 1)
        self.a_axis_dro_layout_3.setSpacing(12)
        self.a_axis_dro_layout_3.setObjectName("a_axis_dro_layout_3")
        self.zero_a_button_2 = MDIButton(self.frame_15)
        self.zero_a_button_2.setEnabled(False)
        self.zero_a_button_2.setMinimumSize(QtCore.QSize(55, 38))
        self.zero_a_button_2.setMaximumSize(QtCore.QSize(55, 38))
        self.zero_a_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_a_button_2.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.zero_a_button_2.setObjectName("zero_a_button_2")
        self.a_axis_dro_layout_3.addWidget(self.zero_a_button_2)
        self.axis_column_header_14 = QtWidgets.QLabel(self.frame_15)
        self.axis_column_header_14.setMinimumSize(QtCore.QSize(45, 35))
        self.axis_column_header_14.setMaximumSize(QtCore.QSize(45, 35))
        self.axis_column_header_14.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    font: 18pt \"Bebas Kai\";\n"
"}")
        self.axis_column_header_14.setAlignment(QtCore.Qt.AlignCenter)
        self.axis_column_header_14.setObjectName("axis_column_header_14")
        self.a_axis_dro_layout_3.addWidget(self.axis_column_header_14)
        self.statuslabel_65 = StatusLabel(self.frame_15)
        self.statuslabel_65.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_65.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_65.setObjectName("statuslabel_65")
        self.a_axis_dro_layout_3.addWidget(self.statuslabel_65)
        self.statuslabel_66 = StatusLabel(self.frame_15)
        self.statuslabel_66.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_66.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_66.setObjectName("statuslabel_66")
        self.a_axis_dro_layout_3.addWidget(self.statuslabel_66)
        self.statuslabel_67 = StatusLabel(self.frame_15)
        self.statuslabel_67.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_67.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_67.setObjectName("statuslabel_67")
        self.a_axis_dro_layout_3.addWidget(self.statuslabel_67)
        self.statuslabel_68 = StatusLabel(self.frame_15)
        self.statuslabel_68.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_68.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_68.setObjectName("statuslabel_68")
        self.a_axis_dro_layout_3.addWidget(self.statuslabel_68)
        self.statuslabel_69 = StatusLabel(self.frame_15)
        self.statuslabel_69.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_69.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_69.setObjectName("statuslabel_69")
        self.a_axis_dro_layout_3.addWidget(self.statuslabel_69)
        self.dro_qvboxlayout_3.addLayout(self.a_axis_dro_layout_3)
        self.b_axis_dro_layout_4 = QtWidgets.QHBoxLayout()
        self.b_axis_dro_layout_4.setContentsMargins(-1, 1, -1, 1)
        self.b_axis_dro_layout_4.setSpacing(12)
        self.b_axis_dro_layout_4.setObjectName("b_axis_dro_layout_4")
        self.zero_b_button_2 = MDIButton(self.frame_15)
        self.zero_b_button_2.setEnabled(False)
        self.zero_b_button_2.setMinimumSize(QtCore.QSize(55, 38))
        self.zero_b_button_2.setMaximumSize(QtCore.QSize(55, 38))
        self.zero_b_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_b_button_2.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.zero_b_button_2.setObjectName("zero_b_button_2")
        self.b_axis_dro_layout_4.addWidget(self.zero_b_button_2)
        self.axis_column_header_15 = QtWidgets.QLabel(self.frame_15)
        self.axis_column_header_15.setMinimumSize(QtCore.QSize(45, 35))
        self.axis_column_header_15.setMaximumSize(QtCore.QSize(45, 35))
        self.axis_column_header_15.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    font: 18pt \"Bebas Kai\";\n"
"}")
        self.axis_column_header_15.setAlignment(QtCore.Qt.AlignCenter)
        self.axis_column_header_15.setObjectName("axis_column_header_15")
        self.b_axis_dro_layout_4.addWidget(self.axis_column_header_15)
        self.statuslabel_70 = StatusLabel(self.frame_15)
        self.statuslabel_70.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_70.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_70.setObjectName("statuslabel_70")
        self.b_axis_dro_layout_4.addWidget(self.statuslabel_70)
        self.statuslabel_71 = StatusLabel(self.frame_15)
        self.statuslabel_71.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_71.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_71.setObjectName("statuslabel_71")
        self.b_axis_dro_layout_4.addWidget(self.statuslabel_71)
        self.statuslabel_72 = StatusLabel(self.frame_15)
        self.statuslabel_72.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_72.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_72.setObjectName("statuslabel_72")
        self.b_axis_dro_layout_4.addWidget(self.statuslabel_72)
        self.statuslabel_73 = StatusLabel(self.frame_15)
        self.statuslabel_73.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_73.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_73.setObjectName("statuslabel_73")
        self.b_axis_dro_layout_4.addWidget(self.statuslabel_73)
        self.statuslabel_74 = StatusLabel(self.frame_15)
        self.statuslabel_74.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_74.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_74.setObjectName("statuslabel_74")
        self.b_axis_dro_layout_4.addWidget(self.statuslabel_74)
        self.dro_qvboxlayout_3.addLayout(self.b_axis_dro_layout_4)
        self.verticalLayout_33.addLayout(self.dro_qvboxlayout_3)
        self.horizontalLayout_51.addWidget(self.frame_15)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_51)
        self.horizontalLayout_131 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_131.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_131.setObjectName("horizontalLayout_131")
        self.widget_38 = QtWidgets.QWidget(self.offsets_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_38.sizePolicy().hasHeightForWidth())
        self.widget_38.setSizePolicy(sizePolicy)
        self.widget_38.setMinimumSize(QtCore.QSize(395, 560))
        self.widget_38.setMaximumSize(QtCore.QSize(395, 560))
        self.widget_38.setStyleSheet("")
        self.widget_38.setObjectName("widget_38")
        self.label_47 = QtWidgets.QLabel(self.widget_38)
        self.label_47.setGeometry(QtCore.QRect(49, 295, 200, 150))
        self.label_47.setStyleSheet("image: url(:/images/tool_probe.png);")
        self.label_47.setText("")
        self.label_47.setScaledContents(True)
        self.label_47.setObjectName("label_47")
        self.label_51 = QtWidgets.QLabel(self.widget_38)
        self.label_51.setGeometry(QtCore.QRect(-1, 0, 140, 231))
        self.label_51.setStyleSheet("image: url(:/images/atc_spindle_tool.png);")
        self.label_51.setText("")
        self.label_51.setScaledContents(True)
        self.label_51.setObjectName("label_51")
        self.frame_39 = QtWidgets.QFrame(self.widget_38)
        self.frame_39.setGeometry(QtCore.QRect(2, 454, 390, 105))
        self.frame_39.setMinimumSize(QtCore.QSize(390, 105))
        self.frame_39.setMaximumSize(QtCore.QSize(390, 105))
        self.frame_39.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_39.setObjectName("frame_39")
        self.verticalLayout_48 = QtWidgets.QVBoxLayout(self.frame_39)
        self.verticalLayout_48.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_48.setObjectName("verticalLayout_48")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setContentsMargins(5, 2, 5, 2)
        self.horizontalLayout_22.setSpacing(10)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.set_g30_1_position = SubCallButton(self.frame_39)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.set_g30_1_position.sizePolicy().hasHeightForWidth())
        self.set_g30_1_position.setSizePolicy(sizePolicy)
        self.set_g30_1_position.setMinimumSize(QtCore.QSize(280, 40))
        self.set_g30_1_position.setFocusPolicy(QtCore.Qt.NoFocus)
        self.set_g30_1_position.setStyleSheet(".SubCallButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
".SubCallButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 15pt;\n"
"}\n"
"\n"
".SubCallButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
".SubCallButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
".SubCallButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.set_g30_1_position.setObjectName("set_g30_1_position")
        self.horizontalLayout_22.addWidget(self.set_g30_1_position)
        self.verticalLayout_48.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_27 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_27.setContentsMargins(-1, -1, 8, -1)
        self.horizontalLayout_27.setSpacing(2)
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_55 = QtWidgets.QLabel(self.frame_39)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_55.sizePolicy().hasHeightForWidth())
        self.label_55.setSizePolicy(sizePolicy)
        self.label_55.setMinimumSize(QtCore.QSize(20, 33))
        self.label_55.setMaximumSize(QtCore.QSize(20, 33))
        self.label_55.setStyleSheet("QLabel{\n"
"font: 75 16pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"padding-right: 1px;\n"
"padding-left: 5px;\n"
"}")
        self.label_55.setAlignment(QtCore.Qt.AlignCenter)
        self.label_55.setObjectName("label_55")
        self.horizontalLayout_27.addWidget(self.label_55)
        self.x_tool_change_position = VCPSettingsLineEdit(self.frame_39)
        self.x_tool_change_position.setMinimumSize(QtCore.QSize(75, 33))
        self.x_tool_change_position.setMaximumSize(QtCore.QSize(16777215, 33))
        self.x_tool_change_position.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.x_tool_change_position.setStyleSheet("VCPSettingsLineEdit {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 15pt \"Bebas Kai\";\n"
"}")
        self.x_tool_change_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_tool_change_position.setReadOnly(True)
        self.x_tool_change_position.setObjectName("x_tool_change_position")
        self.horizontalLayout_27.addWidget(self.x_tool_change_position)
        self.label_57 = QtWidgets.QLabel(self.frame_39)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_57.sizePolicy().hasHeightForWidth())
        self.label_57.setSizePolicy(sizePolicy)
        self.label_57.setMinimumSize(QtCore.QSize(23, 33))
        self.label_57.setMaximumSize(QtCore.QSize(23, 33))
        self.label_57.setStyleSheet("QLabel{\n"
"font: 75 16pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"padding-right: 1px;\n"
"padding-left: 5px;\n"
"}")
        self.label_57.setAlignment(QtCore.Qt.AlignCenter)
        self.label_57.setObjectName("label_57")
        self.horizontalLayout_27.addWidget(self.label_57)
        self.y_tool_change_position = VCPSettingsLineEdit(self.frame_39)
        self.y_tool_change_position.setMinimumSize(QtCore.QSize(75, 33))
        self.y_tool_change_position.setMaximumSize(QtCore.QSize(16777215, 33))
        self.y_tool_change_position.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.y_tool_change_position.setStyleSheet("VCPSettingsLineEdit {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 15pt \"Bebas Kai\";\n"
"}")
        self.y_tool_change_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_tool_change_position.setReadOnly(True)
        self.y_tool_change_position.setObjectName("y_tool_change_position")
        self.horizontalLayout_27.addWidget(self.y_tool_change_position)
        self.label_58 = QtWidgets.QLabel(self.frame_39)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_58.sizePolicy().hasHeightForWidth())
        self.label_58.setSizePolicy(sizePolicy)
        self.label_58.setMinimumSize(QtCore.QSize(23, 33))
        self.label_58.setMaximumSize(QtCore.QSize(23, 33))
        self.label_58.setStyleSheet("QLabel{\n"
"font: 75 16pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"padding-right: 1px;\n"
"padding-left: 5px;\n"
"}")
        self.label_58.setAlignment(QtCore.Qt.AlignCenter)
        self.label_58.setObjectName("label_58")
        self.horizontalLayout_27.addWidget(self.label_58)
        self.z_tool_change_position = VCPSettingsLineEdit(self.frame_39)
        self.z_tool_change_position.setMinimumSize(QtCore.QSize(75, 33))
        self.z_tool_change_position.setMaximumSize(QtCore.QSize(16777215, 33))
        self.z_tool_change_position.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.z_tool_change_position.setStyleSheet("VCPSettingsLineEdit {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 15pt \"Bebas Kai\";\n"
"}")
        self.z_tool_change_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.z_tool_change_position.setReadOnly(True)
        self.z_tool_change_position.setObjectName("z_tool_change_position")
        self.horizontalLayout_27.addWidget(self.z_tool_change_position)
        self.verticalLayout_48.addLayout(self.horizontalLayout_27)
        self.frame_51 = QtWidgets.QFrame(self.widget_38)
        self.frame_51.setGeometry(QtCore.QRect(190, 0, 201, 281))
        self.frame_51.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}\n"
"")
        self.frame_51.setObjectName("frame_51")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_51)
        self.verticalLayout_13.setContentsMargins(6, 6, 6, 6)
        self.verticalLayout_13.setSpacing(6)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.horizontalLayout_163 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_163.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_163.setObjectName("horizontalLayout_163")
        self.label_4 = QtWidgets.QLabel(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(85, 31))
        self.label_4.setMaximumSize(QtCore.QSize(85, 31))
        self.label_4.setStyleSheet("QLabel{\n"
"font: 13pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_4.setLineWidth(0)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setIndent(0)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_163.addWidget(self.label_4)
        self.fast_probe_fr = VCPSettingsLineEdit(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fast_probe_fr.sizePolicy().hasHeightForWidth())
        self.fast_probe_fr.setSizePolicy(sizePolicy)
        self.fast_probe_fr.setMinimumSize(QtCore.QSize(75, 31))
        self.fast_probe_fr.setMaximumSize(QtCore.QSize(75, 31))
        font = QtGui.QFont()
        font.setFamily("bebas kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.fast_probe_fr.setFont(font)
        self.fast_probe_fr.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.fast_probe_fr.setStyleSheet("VCPSettingsLineEdit {\n"
"    font: 14pt \"bebas kai\"\n"
"}")
        self.fast_probe_fr.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.fast_probe_fr.setObjectName("fast_probe_fr")
        self.horizontalLayout_163.addWidget(self.fast_probe_fr)
        self.verticalLayout_13.addLayout(self.horizontalLayout_163)
        self.horizontalLayout_64 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_64.setObjectName("horizontalLayout_64")
        self.label_119 = QtWidgets.QLabel(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_119.sizePolicy().hasHeightForWidth())
        self.label_119.setSizePolicy(sizePolicy)
        self.label_119.setMinimumSize(QtCore.QSize(85, 31))
        self.label_119.setMaximumSize(QtCore.QSize(85, 31))
        self.label_119.setStyleSheet("QLabel{\n"
"font: 13pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_119.setLineWidth(0)
        self.label_119.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_119.setIndent(0)
        self.label_119.setObjectName("label_119")
        self.horizontalLayout_64.addWidget(self.label_119)
        self.slow_probe_fr = VCPSettingsLineEdit(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.slow_probe_fr.sizePolicy().hasHeightForWidth())
        self.slow_probe_fr.setSizePolicy(sizePolicy)
        self.slow_probe_fr.setMinimumSize(QtCore.QSize(75, 31))
        self.slow_probe_fr.setMaximumSize(QtCore.QSize(75, 31))
        font = QtGui.QFont()
        font.setFamily("bebas kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.slow_probe_fr.setFont(font)
        self.slow_probe_fr.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.slow_probe_fr.setStyleSheet("VCPSettingsLineEdit {\n"
"    font: 14pt \"bebas kai\"\n"
"}")
        self.slow_probe_fr.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.slow_probe_fr.setObjectName("slow_probe_fr")
        self.horizontalLayout_64.addWidget(self.slow_probe_fr)
        self.verticalLayout_13.addLayout(self.horizontalLayout_64)
        self.horizontalLayout_165 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_165.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_165.setObjectName("horizontalLayout_165")
        self.label_122 = QtWidgets.QLabel(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_122.sizePolicy().hasHeightForWidth())
        self.label_122.setSizePolicy(sizePolicy)
        self.label_122.setMinimumSize(QtCore.QSize(85, 31))
        self.label_122.setMaximumSize(QtCore.QSize(85, 31))
        self.label_122.setStyleSheet("QLabel{\n"
"font: 13pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_122.setLineWidth(0)
        self.label_122.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_122.setIndent(0)
        self.label_122.setObjectName("label_122")
        self.horizontalLayout_165.addWidget(self.label_122)
        self.z_max_travel = VCPSettingsLineEdit(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.z_max_travel.sizePolicy().hasHeightForWidth())
        self.z_max_travel.setSizePolicy(sizePolicy)
        self.z_max_travel.setMinimumSize(QtCore.QSize(75, 31))
        self.z_max_travel.setMaximumSize(QtCore.QSize(75, 31))
        font = QtGui.QFont()
        font.setFamily("bebas kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.z_max_travel.setFont(font)
        self.z_max_travel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.z_max_travel.setStyleSheet("VCPSettingsLineEdit {\n"
"    font: 14pt \"bebas kai\"\n"
"}")
        self.z_max_travel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.z_max_travel.setObjectName("z_max_travel")
        self.horizontalLayout_165.addWidget(self.z_max_travel)
        self.verticalLayout_13.addLayout(self.horizontalLayout_165)
        self.horizontalLayout_73 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_73.setObjectName("horizontalLayout_73")
        self.label_125 = QtWidgets.QLabel(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_125.sizePolicy().hasHeightForWidth())
        self.label_125.setSizePolicy(sizePolicy)
        self.label_125.setMinimumSize(QtCore.QSize(85, 31))
        self.label_125.setMaximumSize(QtCore.QSize(85, 31))
        self.label_125.setStyleSheet("QLabel{\n"
"font: 13pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_125.setLineWidth(0)
        self.label_125.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_125.setIndent(0)
        self.label_125.setObjectName("label_125")
        self.horizontalLayout_73.addWidget(self.label_125)
        self.xy_max_travel = VCPSettingsLineEdit(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xy_max_travel.sizePolicy().hasHeightForWidth())
        self.xy_max_travel.setSizePolicy(sizePolicy)
        self.xy_max_travel.setMinimumSize(QtCore.QSize(75, 31))
        self.xy_max_travel.setMaximumSize(QtCore.QSize(75, 31))
        font = QtGui.QFont()
        font.setFamily("bebas kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.xy_max_travel.setFont(font)
        self.xy_max_travel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.xy_max_travel.setStyleSheet("VCPSettingsLineEdit {\n"
"    font: 14pt \"bebas kai\"\n"
"}")
        self.xy_max_travel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xy_max_travel.setObjectName("xy_max_travel")
        self.horizontalLayout_73.addWidget(self.xy_max_travel)
        self.verticalLayout_13.addLayout(self.horizontalLayout_73)
        self.horizontalLayout_66 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_66.setObjectName("horizontalLayout_66")
        self.label_123 = QtWidgets.QLabel(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_123.sizePolicy().hasHeightForWidth())
        self.label_123.setSizePolicy(sizePolicy)
        self.label_123.setMinimumSize(QtCore.QSize(85, 31))
        self.label_123.setMaximumSize(QtCore.QSize(85, 31))
        self.label_123.setStyleSheet("QLabel{\n"
"font: 13pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_123.setLineWidth(0)
        self.label_123.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_123.setIndent(0)
        self.label_123.setObjectName("label_123")
        self.horizontalLayout_66.addWidget(self.label_123)
        self.retract_distance = VCPSettingsLineEdit(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.retract_distance.sizePolicy().hasHeightForWidth())
        self.retract_distance.setSizePolicy(sizePolicy)
        self.retract_distance.setMinimumSize(QtCore.QSize(75, 31))
        self.retract_distance.setMaximumSize(QtCore.QSize(75, 31))
        font = QtGui.QFont()
        font.setFamily("bebas kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.retract_distance.setFont(font)
        self.retract_distance.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.retract_distance.setStyleSheet("VCPSettingsLineEdit {\n"
"    font: 14pt \"bebas kai\"\n"
"}")
        self.retract_distance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.retract_distance.setObjectName("retract_distance")
        self.horizontalLayout_66.addWidget(self.retract_distance)
        self.verticalLayout_13.addLayout(self.horizontalLayout_66)
        self.horizontalLayout_72 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_72.setObjectName("horizontalLayout_72")
        self.label_124 = QtWidgets.QLabel(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_124.sizePolicy().hasHeightForWidth())
        self.label_124.setSizePolicy(sizePolicy)
        self.label_124.setMinimumSize(QtCore.QSize(85, 31))
        self.label_124.setMaximumSize(QtCore.QSize(85, 31))
        self.label_124.setStyleSheet("QLabel{\n"
"font: 13pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_124.setLineWidth(0)
        self.label_124.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_124.setIndent(0)
        self.label_124.setObjectName("label_124")
        self.horizontalLayout_72.addWidget(self.label_124)
        self.spindle_zero_height = VCPSettingsLineEdit(self.frame_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spindle_zero_height.sizePolicy().hasHeightForWidth())
        self.spindle_zero_height.setSizePolicy(sizePolicy)
        self.spindle_zero_height.setMinimumSize(QtCore.QSize(75, 31))
        self.spindle_zero_height.setMaximumSize(QtCore.QSize(75, 31))
        font = QtGui.QFont()
        font.setFamily("bebas kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.spindle_zero_height.setFont(font)
        self.spindle_zero_height.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.spindle_zero_height.setStyleSheet("VCPSettingsLineEdit {\n"
"    font: 14pt \"bebas kai\"\n"
"}")
        self.spindle_zero_height.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spindle_zero_height.setObjectName("spindle_zero_height")
        self.horizontalLayout_72.addWidget(self.spindle_zero_height)
        self.verticalLayout_13.addLayout(self.horizontalLayout_72)
        self.tool_diameter_probe_Btn = QtWidgets.QPushButton(self.widget_38)
        self.tool_diameter_probe_Btn.setGeometry(QtCore.QRect(265, 348, 125, 38))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_diameter_probe_Btn.sizePolicy().hasHeightForWidth())
        self.tool_diameter_probe_Btn.setSizePolicy(sizePolicy)
        self.tool_diameter_probe_Btn.setMinimumSize(QtCore.QSize(125, 38))
        self.tool_diameter_probe_Btn.setMaximumSize(QtCore.QSize(125, 38))
        self.tool_diameter_probe_Btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_diameter_probe_Btn.setStyleSheet("QPushButton{\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.tool_diameter_probe_Btn.setCheckable(True)
        self.tool_diameter_probe_Btn.setObjectName("tool_diameter_probe_Btn")
        self.tool_diameter_offset_Btn = QtWidgets.QPushButton(self.widget_38)
        self.tool_diameter_offset_Btn.setGeometry(QtCore.QRect(265, 295, 125, 38))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_diameter_offset_Btn.sizePolicy().hasHeightForWidth())
        self.tool_diameter_offset_Btn.setSizePolicy(sizePolicy)
        self.tool_diameter_offset_Btn.setMinimumSize(QtCore.QSize(125, 38))
        self.tool_diameter_offset_Btn.setMaximumSize(QtCore.QSize(125, 38))
        self.tool_diameter_offset_Btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_diameter_offset_Btn.setStyleSheet("QPushButton{\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.tool_diameter_offset_Btn.setCheckable(True)
        self.tool_diameter_offset_Btn.setObjectName("tool_diameter_offset_Btn")
        self.horizontalLayout_131.addWidget(self.widget_38)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_131)
        self.tabWidget.addTab(self.offsets_tab, "")
        self.probe_tab = QtWidgets.QWidget()
        self.probe_tab.setObjectName("probe_tab")
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout(self.probe_tab)
        self.horizontalLayout_43.setObjectName("horizontalLayout_43")
        self.widget_44 = QtWidgets.QWidget(self.probe_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_44.sizePolicy().hasHeightForWidth())
        self.widget_44.setSizePolicy(sizePolicy)
        self.widget_44.setMinimumSize(QtCore.QSize(530, 0))
        self.widget_44.setMaximumSize(QtCore.QSize(540, 16777215))
        self.widget_44.setStyleSheet("")
        self.widget_44.setObjectName("widget_44")
        self.verticalLayout_41 = QtWidgets.QVBoxLayout(self.widget_44)
        self.verticalLayout_41.setContentsMargins(-1, 6, 6, 9)
        self.verticalLayout_41.setObjectName("verticalLayout_41")
        self.label_81 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_81.sizePolicy().hasHeightForWidth())
        self.label_81.setSizePolicy(sizePolicy)
        self.label_81.setMinimumSize(QtCore.QSize(0, 27))
        self.label_81.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_81.setFont(font)
        self.label_81.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_81.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_81.setObjectName("label_81")
        self.verticalLayout_41.addWidget(self.label_81)
        self.widget_15 = QtWidgets.QWidget(self.widget_44)
        self.widget_15.setMinimumSize(QtCore.QSize(112, 90))
        self.widget_15.setMaximumSize(QtCore.QSize(16777215, 100))
        self.widget_15.setObjectName("widget_15")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.widget_15)
        self.verticalLayout_16.setContentsMargins(9, 0, 9, 0)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.horizontalWidget = QtWidgets.QWidget(self.widget_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget.sizePolicy().hasHeightForWidth())
        self.horizontalWidget.setSizePolicy(sizePolicy)
        self.horizontalWidget.setMinimumSize(QtCore.QSize(440, 0))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_45 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_45.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_45.setSpacing(9)
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")
        self.actionbutton_19 = ActionButton(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_19.sizePolicy().hasHeightForWidth())
        self.actionbutton_19.setSizePolicy(sizePolicy)
        self.actionbutton_19.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_19.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_19.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_19.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_19.setAutoExclusive(True)
        self.actionbutton_19.setObjectName("actionbutton_19")
        self.probepagewcsbtnGroup = QtWidgets.QButtonGroup(Form)
        self.probepagewcsbtnGroup.setObjectName("probepagewcsbtnGroup")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_19)
        self.horizontalLayout_45.addWidget(self.actionbutton_19)
        self.actionbutton_20 = ActionButton(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_20.sizePolicy().hasHeightForWidth())
        self.actionbutton_20.setSizePolicy(sizePolicy)
        self.actionbutton_20.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_20.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_20.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_20.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_20.setAutoExclusive(True)
        self.actionbutton_20.setObjectName("actionbutton_20")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_20)
        self.horizontalLayout_45.addWidget(self.actionbutton_20)
        self.actionbutton_21 = ActionButton(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_21.sizePolicy().hasHeightForWidth())
        self.actionbutton_21.setSizePolicy(sizePolicy)
        self.actionbutton_21.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_21.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_21.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_21.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_21.setAutoExclusive(True)
        self.actionbutton_21.setObjectName("actionbutton_21")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_21)
        self.horizontalLayout_45.addWidget(self.actionbutton_21)
        self.actionbutton_26 = ActionButton(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_26.sizePolicy().hasHeightForWidth())
        self.actionbutton_26.setSizePolicy(sizePolicy)
        self.actionbutton_26.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_26.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_26.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_26.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_26.setAutoExclusive(True)
        self.actionbutton_26.setObjectName("actionbutton_26")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_26)
        self.horizontalLayout_45.addWidget(self.actionbutton_26)
        self.actionbutton_24 = ActionButton(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_24.sizePolicy().hasHeightForWidth())
        self.actionbutton_24.setSizePolicy(sizePolicy)
        self.actionbutton_24.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_24.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_24.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_24.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_24.setAutoExclusive(True)
        self.actionbutton_24.setObjectName("actionbutton_24")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_24)
        self.horizontalLayout_45.addWidget(self.actionbutton_24)
        self.actionbutton_22 = ActionButton(self.horizontalWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_22.sizePolicy().hasHeightForWidth())
        self.actionbutton_22.setSizePolicy(sizePolicy)
        self.actionbutton_22.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_22.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_22.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_22.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_22.setAutoExclusive(True)
        self.actionbutton_22.setObjectName("actionbutton_22")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_22)
        self.horizontalLayout_45.addWidget(self.actionbutton_22)
        self.verticalLayout_16.addWidget(self.horizontalWidget)
        self.horizontalWidget_2 = QtWidgets.QWidget(self.widget_15)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget_2.sizePolicy().hasHeightForWidth())
        self.horizontalWidget_2.setSizePolicy(sizePolicy)
        self.horizontalWidget_2.setMinimumSize(QtCore.QSize(440, 0))
        self.horizontalWidget_2.setObjectName("horizontalWidget_2")
        self.horizontalLayout_46 = QtWidgets.QHBoxLayout(self.horizontalWidget_2)
        self.horizontalLayout_46.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_46.setSpacing(9)
        self.horizontalLayout_46.setObjectName("horizontalLayout_46")
        self.actionbutton_27 = ActionButton(self.horizontalWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_27.sizePolicy().hasHeightForWidth())
        self.actionbutton_27.setSizePolicy(sizePolicy)
        self.actionbutton_27.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_27.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_27.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_27.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_27.setAutoExclusive(True)
        self.actionbutton_27.setObjectName("actionbutton_27")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_27)
        self.horizontalLayout_46.addWidget(self.actionbutton_27)
        self.actionbutton_25 = ActionButton(self.horizontalWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_25.sizePolicy().hasHeightForWidth())
        self.actionbutton_25.setSizePolicy(sizePolicy)
        self.actionbutton_25.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_25.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_25.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_25.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_25.setAutoExclusive(True)
        self.actionbutton_25.setObjectName("actionbutton_25")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_25)
        self.horizontalLayout_46.addWidget(self.actionbutton_25)
        self.actionbutton_23 = ActionButton(self.horizontalWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_23.sizePolicy().hasHeightForWidth())
        self.actionbutton_23.setSizePolicy(sizePolicy)
        self.actionbutton_23.setMinimumSize(QtCore.QSize(75, 38))
        self.actionbutton_23.setMaximumSize(QtCore.QSize(70, 38))
        self.actionbutton_23.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_23.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_23.setAutoExclusive(True)
        self.actionbutton_23.setObjectName("actionbutton_23")
        self.probepagewcsbtnGroup.addButton(self.actionbutton_23)
        self.horizontalLayout_46.addWidget(self.actionbutton_23)
        self.probe_wco = QtWidgets.QPushButton(self.horizontalWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(156)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_wco.sizePolicy().hasHeightForWidth())
        self.probe_wco.setSizePolicy(sizePolicy)
        self.probe_wco.setMinimumSize(QtCore.QSize(118, 38))
        self.probe_wco.setMaximumSize(QtCore.QSize(16777215, 38))
        self.probe_wco.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_wco.setStyleSheet("QPushButton{\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.probe_wco.setCheckable(True)
        self.probe_wco.setChecked(True)
        self.probe_wco.setAutoExclusive(True)
        self.probe_wco.setObjectName("probe_wco")
        self.probemodeGroup = QtWidgets.QButtonGroup(Form)
        self.probemodeGroup.setObjectName("probemodeGroup")
        self.probemodeGroup.addButton(self.probe_wco)
        self.horizontalLayout_46.addWidget(self.probe_wco)
        self.probe_Position_only = QtWidgets.QPushButton(self.horizontalWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(156)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_Position_only.sizePolicy().hasHeightForWidth())
        self.probe_Position_only.setSizePolicy(sizePolicy)
        self.probe_Position_only.setMinimumSize(QtCore.QSize(118, 38))
        self.probe_Position_only.setMaximumSize(QtCore.QSize(16777215, 38))
        self.probe_Position_only.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_Position_only.setStyleSheet("QPushButton{\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.probe_Position_only.setCheckable(True)
        self.probe_Position_only.setObjectName("probe_Position_only")
        self.probemodeGroup.addButton(self.probe_Position_only)
        self.horizontalLayout_46.addWidget(self.probe_Position_only)
        self.verticalLayout_16.addWidget(self.horizontalWidget_2)
        self.verticalLayout_41.addWidget(self.widget_15)
        self.label_82 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_82.sizePolicy().hasHeightForWidth())
        self.label_82.setSizePolicy(sizePolicy)
        self.label_82.setMinimumSize(QtCore.QSize(0, 27))
        self.label_82.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_82.setFont(font)
        self.label_82.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_82.setObjectName("label_82")
        self.verticalLayout_41.addWidget(self.label_82)
        self.verticalLayout_22 = QtWidgets.QVBoxLayout()
        self.verticalLayout_22.setContentsMargins(-1, 0, 9, -1)
        self.verticalLayout_22.setSpacing(6)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.horizontalLayout_154 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_154.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_154.setObjectName("horizontalLayout_154")
        self.ref_coilumn_header_19 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_19.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_19.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_19.setStyleSheet("")
        self.ref_coilumn_header_19.setText("")
        self.ref_coilumn_header_19.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_19.setObjectName("ref_coilumn_header_19")
        self.horizontalLayout_154.addWidget(self.ref_coilumn_header_19)
        self.label_83 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_83.sizePolicy().hasHeightForWidth())
        self.label_83.setSizePolicy(sizePolicy)
        self.label_83.setMinimumSize(QtCore.QSize(140, 31))
        self.label_83.setMaximumSize(QtCore.QSize(150, 31))
        self.label_83.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_83.setLineWidth(0)
        self.label_83.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_83.setIndent(0)
        self.label_83.setObjectName("label_83")
        self.horizontalLayout_154.addWidget(self.label_83)
        self.probe_tool_number = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_tool_number.sizePolicy().hasHeightForWidth())
        self.probe_tool_number.setSizePolicy(sizePolicy)
        self.probe_tool_number.setMinimumSize(QtCore.QSize(100, 31))
        self.probe_tool_number.setMaximumSize(QtCore.QSize(100, 31))
        self.probe_tool_number.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.probe_tool_number.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.probe_tool_number.setObjectName("probe_tool_number")
        self.horizontalLayout_154.addWidget(self.probe_tool_number)
        self.label_84 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_84.sizePolicy().hasHeightForWidth())
        self.label_84.setSizePolicy(sizePolicy)
        self.label_84.setMinimumSize(QtCore.QSize(140, 31))
        self.label_84.setMaximumSize(QtCore.QSize(140, 31))
        self.label_84.setBaseSize(QtCore.QSize(140, 30))
        self.label_84.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_84.setLineWidth(0)
        self.label_84.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_84.setIndent(0)
        self.label_84.setObjectName("label_84")
        self.horizontalLayout_154.addWidget(self.label_84)
        self.step_off_width = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.step_off_width.sizePolicy().hasHeightForWidth())
        self.step_off_width.setSizePolicy(sizePolicy)
        self.step_off_width.setMinimumSize(QtCore.QSize(100, 31))
        self.step_off_width.setMaximumSize(QtCore.QSize(100, 31))
        self.step_off_width.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.step_off_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.step_off_width.setObjectName("step_off_width")
        self.horizontalLayout_154.addWidget(self.step_off_width)
        self.verticalLayout_22.addLayout(self.horizontalLayout_154)
        self.horizontalLayout_155 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_155.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_155.setObjectName("horizontalLayout_155")
        self.ref_coilumn_header_20 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_20.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_20.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_20.setStyleSheet("")
        self.ref_coilumn_header_20.setText("")
        self.ref_coilumn_header_20.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_20.setObjectName("ref_coilumn_header_20")
        self.horizontalLayout_155.addWidget(self.ref_coilumn_header_20)
        self.label_85 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_85.sizePolicy().hasHeightForWidth())
        self.label_85.setSizePolicy(sizePolicy)
        self.label_85.setMinimumSize(QtCore.QSize(140, 31))
        self.label_85.setMaximumSize(QtCore.QSize(150, 31))
        self.label_85.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_85.setLineWidth(0)
        self.label_85.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_85.setIndent(0)
        self.label_85.setObjectName("label_85")
        self.horizontalLayout_155.addWidget(self.label_85)
        self.probe_fast_fr = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_fast_fr.sizePolicy().hasHeightForWidth())
        self.probe_fast_fr.setSizePolicy(sizePolicy)
        self.probe_fast_fr.setMinimumSize(QtCore.QSize(100, 31))
        self.probe_fast_fr.setMaximumSize(QtCore.QSize(100, 31))
        self.probe_fast_fr.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.probe_fast_fr.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.probe_fast_fr.setObjectName("probe_fast_fr")
        self.horizontalLayout_155.addWidget(self.probe_fast_fr)
        self.label_86 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_86.sizePolicy().hasHeightForWidth())
        self.label_86.setSizePolicy(sizePolicy)
        self.label_86.setMinimumSize(QtCore.QSize(140, 31))
        self.label_86.setMaximumSize(QtCore.QSize(140, 31))
        self.label_86.setBaseSize(QtCore.QSize(140, 30))
        self.label_86.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_86.setLineWidth(0)
        self.label_86.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_86.setIndent(0)
        self.label_86.setObjectName("label_86")
        self.horizontalLayout_155.addWidget(self.label_86)
        self.probe_slow_fr = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_slow_fr.sizePolicy().hasHeightForWidth())
        self.probe_slow_fr.setSizePolicy(sizePolicy)
        self.probe_slow_fr.setMinimumSize(QtCore.QSize(100, 31))
        self.probe_slow_fr.setMaximumSize(QtCore.QSize(100, 31))
        self.probe_slow_fr.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.probe_slow_fr.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.probe_slow_fr.setObjectName("probe_slow_fr")
        self.horizontalLayout_155.addWidget(self.probe_slow_fr)
        self.verticalLayout_22.addLayout(self.horizontalLayout_155)
        self.horizontalLayout_156 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_156.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_156.setObjectName("horizontalLayout_156")
        self.ref_coilumn_header_21 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_21.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_21.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_21.setStyleSheet("")
        self.ref_coilumn_header_21.setText("")
        self.ref_coilumn_header_21.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_21.setObjectName("ref_coilumn_header_21")
        self.horizontalLayout_156.addWidget(self.ref_coilumn_header_21)
        self.label_87 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_87.sizePolicy().hasHeightForWidth())
        self.label_87.setSizePolicy(sizePolicy)
        self.label_87.setMinimumSize(QtCore.QSize(140, 31))
        self.label_87.setMaximumSize(QtCore.QSize(150, 31))
        self.label_87.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_87.setLineWidth(0)
        self.label_87.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_87.setIndent(0)
        self.label_87.setObjectName("label_87")
        self.horizontalLayout_156.addWidget(self.label_87)
        self.max_xy_distance = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_xy_distance.sizePolicy().hasHeightForWidth())
        self.max_xy_distance.setSizePolicy(sizePolicy)
        self.max_xy_distance.setMinimumSize(QtCore.QSize(100, 31))
        self.max_xy_distance.setMaximumSize(QtCore.QSize(100, 31))
        self.max_xy_distance.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.max_xy_distance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.max_xy_distance.setObjectName("max_xy_distance")
        self.horizontalLayout_156.addWidget(self.max_xy_distance)
        self.label_88 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_88.sizePolicy().hasHeightForWidth())
        self.label_88.setSizePolicy(sizePolicy)
        self.label_88.setMinimumSize(QtCore.QSize(140, 31))
        self.label_88.setMaximumSize(QtCore.QSize(140, 31))
        self.label_88.setBaseSize(QtCore.QSize(140, 30))
        self.label_88.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_88.setLineWidth(0)
        self.label_88.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_88.setIndent(0)
        self.label_88.setObjectName("label_88")
        self.horizontalLayout_156.addWidget(self.label_88)
        self.xy_clearance = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xy_clearance.sizePolicy().hasHeightForWidth())
        self.xy_clearance.setSizePolicy(sizePolicy)
        self.xy_clearance.setMinimumSize(QtCore.QSize(100, 31))
        self.xy_clearance.setMaximumSize(QtCore.QSize(100, 31))
        self.xy_clearance.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.xy_clearance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xy_clearance.setObjectName("xy_clearance")
        self.horizontalLayout_156.addWidget(self.xy_clearance)
        self.verticalLayout_22.addLayout(self.horizontalLayout_156)
        self.horizontalLayout_157 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_157.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_157.setObjectName("horizontalLayout_157")
        self.ref_coilumn_header_22 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_22.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_22.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_22.setStyleSheet("")
        self.ref_coilumn_header_22.setText("")
        self.ref_coilumn_header_22.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_22.setObjectName("ref_coilumn_header_22")
        self.horizontalLayout_157.addWidget(self.ref_coilumn_header_22)
        self.label_90 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_90.sizePolicy().hasHeightForWidth())
        self.label_90.setSizePolicy(sizePolicy)
        self.label_90.setMinimumSize(QtCore.QSize(140, 31))
        self.label_90.setMaximumSize(QtCore.QSize(150, 31))
        self.label_90.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_90.setLineWidth(0)
        self.label_90.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_90.setIndent(0)
        self.label_90.setObjectName("label_90")
        self.horizontalLayout_157.addWidget(self.label_90)
        self.max_z_distance = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_z_distance.sizePolicy().hasHeightForWidth())
        self.max_z_distance.setSizePolicy(sizePolicy)
        self.max_z_distance.setMinimumSize(QtCore.QSize(100, 31))
        self.max_z_distance.setMaximumSize(QtCore.QSize(100, 31))
        self.max_z_distance.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.max_z_distance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.max_z_distance.setObjectName("max_z_distance")
        self.horizontalLayout_157.addWidget(self.max_z_distance)
        self.label_91 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_91.sizePolicy().hasHeightForWidth())
        self.label_91.setSizePolicy(sizePolicy)
        self.label_91.setMinimumSize(QtCore.QSize(140, 31))
        self.label_91.setMaximumSize(QtCore.QSize(140, 31))
        self.label_91.setBaseSize(QtCore.QSize(140, 30))
        self.label_91.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_91.setLineWidth(0)
        self.label_91.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_91.setIndent(0)
        self.label_91.setObjectName("label_91")
        self.horizontalLayout_157.addWidget(self.label_91)
        self.z_clearance = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.z_clearance.sizePolicy().hasHeightForWidth())
        self.z_clearance.setSizePolicy(sizePolicy)
        self.z_clearance.setMinimumSize(QtCore.QSize(100, 31))
        self.z_clearance.setMaximumSize(QtCore.QSize(100, 31))
        self.z_clearance.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.z_clearance.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.z_clearance.setObjectName("z_clearance")
        self.horizontalLayout_157.addWidget(self.z_clearance)
        self.verticalLayout_22.addLayout(self.horizontalLayout_157)
        self.horizontalLayout_158 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_158.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_158.setObjectName("horizontalLayout_158")
        self.ref_coilumn_header_23 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_23.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_23.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_23.setStyleSheet("")
        self.ref_coilumn_header_23.setText("")
        self.ref_coilumn_header_23.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_23.setObjectName("ref_coilumn_header_23")
        self.horizontalLayout_158.addWidget(self.ref_coilumn_header_23)
        self.label_92 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_92.sizePolicy().hasHeightForWidth())
        self.label_92.setSizePolicy(sizePolicy)
        self.label_92.setMinimumSize(QtCore.QSize(140, 31))
        self.label_92.setMaximumSize(QtCore.QSize(150, 31))
        self.label_92.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_92.setLineWidth(0)
        self.label_92.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_92.setIndent(0)
        self.label_92.setObjectName("label_92")
        self.horizontalLayout_158.addWidget(self.label_92)
        self.extra_probe_depth = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.extra_probe_depth.sizePolicy().hasHeightForWidth())
        self.extra_probe_depth.setSizePolicy(sizePolicy)
        self.extra_probe_depth.setMinimumSize(QtCore.QSize(100, 31))
        self.extra_probe_depth.setMaximumSize(QtCore.QSize(100, 31))
        self.extra_probe_depth.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.extra_probe_depth.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.extra_probe_depth.setObjectName("extra_probe_depth")
        self.horizontalLayout_158.addWidget(self.extra_probe_depth)
        self.label_94 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_94.sizePolicy().hasHeightForWidth())
        self.label_94.setSizePolicy(sizePolicy)
        self.label_94.setMinimumSize(QtCore.QSize(140, 31))
        self.label_94.setMaximumSize(QtCore.QSize(140, 31))
        self.label_94.setBaseSize(QtCore.QSize(140, 30))
        self.label_94.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_94.setLineWidth(0)
        self.label_94.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_94.setIndent(0)
        self.label_94.setObjectName("label_94")
        self.horizontalLayout_158.addWidget(self.label_94)
        self.edge_width = VCPSettingsLineEdit(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edge_width.sizePolicy().hasHeightForWidth())
        self.edge_width.setSizePolicy(sizePolicy)
        self.edge_width.setMinimumSize(QtCore.QSize(100, 31))
        self.edge_width.setMaximumSize(QtCore.QSize(100, 31))
        self.edge_width.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.edge_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edge_width.setObjectName("edge_width")
        self.horizontalLayout_158.addWidget(self.edge_width)
        self.verticalLayout_22.addLayout(self.horizontalLayout_158)
        self.verticalLayout_41.addLayout(self.verticalLayout_22)
        self.widget_19 = QtWidgets.QWidget(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_19.sizePolicy().hasHeightForWidth())
        self.widget_19.setSizePolicy(sizePolicy)
        self.widget_19.setMinimumSize(QtCore.QSize(0, 33))
        self.widget_19.setMaximumSize(QtCore.QSize(16777215, 33))
        self.widget_19.setObjectName("widget_19")
        self.horizontalLayout_57 = QtWidgets.QHBoxLayout(self.widget_19)
        self.horizontalLayout_57.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_57.setSpacing(1)
        self.horizontalLayout_57.setObjectName("horizontalLayout_57")
        self.label_95 = QtWidgets.QLabel(self.widget_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_95.sizePolicy().hasHeightForWidth())
        self.label_95.setSizePolicy(sizePolicy)
        self.label_95.setMinimumSize(QtCore.QSize(0, 27))
        self.label_95.setMaximumSize(QtCore.QSize(16777215, 27))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_95.setFont(font)
        self.label_95.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-width: 2px;\n"
"    border-top-left-radius: 5px;\n"
"    border-bottom-left-radius: 5px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"    color: rgb(238, 238, 236);\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_95.setObjectName("label_95")
        self.horizontalLayout_57.addWidget(self.label_95)
        self.reset_all_data = SubCallButton(self.widget_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reset_all_data.sizePolicy().hasHeightForWidth())
        self.reset_all_data.setSizePolicy(sizePolicy)
        self.reset_all_data.setMinimumSize(QtCore.QSize(120, 27))
        self.reset_all_data.setMaximumSize(QtCore.QSize(120, 27))
        self.reset_all_data.setFocusPolicy(QtCore.Qt.NoFocus)
        self.reset_all_data.setStyleSheet(".SubCallButton{\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"    font: 14pt \"Bebas Kai\";\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}\n"
"\n"
".SubCallButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
".SubCallButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
".SubCallButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.reset_all_data.setObjectName("reset_all_data")
        self.horizontalLayout_57.addWidget(self.reset_all_data)
        self.x_data_reset1 = SubCallButton(self.widget_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_data_reset1.sizePolicy().hasHeightForWidth())
        self.x_data_reset1.setSizePolicy(sizePolicy)
        self.x_data_reset1.setMinimumSize(QtCore.QSize(110, 27))
        self.x_data_reset1.setMaximumSize(QtCore.QSize(110, 27))
        self.x_data_reset1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_data_reset1.setStyleSheet(".SubCallButton{\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"    font: 14pt \"Bebas Kai\";\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}\n"
"\n"
".SubCallButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
".SubCallButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
".SubCallButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.x_data_reset1.setObjectName("x_data_reset1")
        self.horizontalLayout_57.addWidget(self.x_data_reset1)
        self.y_data_reset1 = SubCallButton(self.widget_19)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_data_reset1.sizePolicy().hasHeightForWidth())
        self.y_data_reset1.setSizePolicy(sizePolicy)
        self.y_data_reset1.setMinimumSize(QtCore.QSize(110, 27))
        self.y_data_reset1.setMaximumSize(QtCore.QSize(110, 27))
        self.y_data_reset1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.y_data_reset1.setStyleSheet("SubCallButton{\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"    font: 14pt \"Bebas Kai\";\n"
"      background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}\n"
"\n"
".SubCallButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
".SubCallButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
".SubCallButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.y_data_reset1.setObjectName("y_data_reset1")
        self.horizontalLayout_57.addWidget(self.y_data_reset1)
        self.verticalLayout_41.addWidget(self.widget_19)
        self.verticalLayout_42 = QtWidgets.QVBoxLayout()
        self.verticalLayout_42.setContentsMargins(-1, 0, 9, 3)
        self.verticalLayout_42.setSpacing(6)
        self.verticalLayout_42.setObjectName("verticalLayout_42")
        self.horizontalLayout_160 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_160.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_160.setObjectName("horizontalLayout_160")
        self.label_108 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_108.sizePolicy().hasHeightForWidth())
        self.label_108.setSizePolicy(sizePolicy)
        self.label_108.setMinimumSize(QtCore.QSize(0, 31))
        self.label_108.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_108.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_108.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_108.setLineWidth(0)
        self.label_108.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_108.setIndent(0)
        self.label_108.setObjectName("label_108")
        self.horizontalLayout_160.addWidget(self.label_108)
        self.x_minus_probed_position = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_minus_probed_position.sizePolicy().hasHeightForWidth())
        self.x_minus_probed_position.setSizePolicy(sizePolicy)
        self.x_minus_probed_position.setMinimumSize(QtCore.QSize(80, 31))
        self.x_minus_probed_position.setMaximumSize(QtCore.QSize(80, 31))
        self.x_minus_probed_position.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.x_minus_probed_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_minus_probed_position.setObjectName("x_minus_probed_position")
        self.horizontalLayout_160.addWidget(self.x_minus_probed_position)
        self.label_98 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_98.sizePolicy().hasHeightForWidth())
        self.label_98.setSizePolicy(sizePolicy)
        self.label_98.setMinimumSize(QtCore.QSize(80, 31))
        self.label_98.setMaximumSize(QtCore.QSize(80, 31))
        self.label_98.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_98.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_98.setLineWidth(0)
        self.label_98.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_98.setIndent(0)
        self.label_98.setObjectName("label_98")
        self.horizontalLayout_160.addWidget(self.label_98)
        self.x_plus_probed_position = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_plus_probed_position.sizePolicy().hasHeightForWidth())
        self.x_plus_probed_position.setSizePolicy(sizePolicy)
        self.x_plus_probed_position.setMinimumSize(QtCore.QSize(80, 31))
        self.x_plus_probed_position.setMaximumSize(QtCore.QSize(80, 31))
        self.x_plus_probed_position.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.x_plus_probed_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_plus_probed_position.setObjectName("x_plus_probed_position")
        self.horizontalLayout_160.addWidget(self.x_plus_probed_position)
        self.label_97 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_97.sizePolicy().hasHeightForWidth())
        self.label_97.setSizePolicy(sizePolicy)
        self.label_97.setMinimumSize(QtCore.QSize(80, 31))
        self.label_97.setMaximumSize(QtCore.QSize(80, 31))
        self.label_97.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_97.setLineWidth(0)
        self.label_97.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_97.setIndent(0)
        self.label_97.setObjectName("label_97")
        self.horizontalLayout_160.addWidget(self.label_97)
        self.x_probed_width = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_probed_width.sizePolicy().hasHeightForWidth())
        self.x_probed_width.setSizePolicy(sizePolicy)
        self.x_probed_width.setMinimumSize(QtCore.QSize(80, 31))
        self.x_probed_width.setMaximumSize(QtCore.QSize(80, 31))
        self.x_probed_width.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.x_probed_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_probed_width.setObjectName("x_probed_width")
        self.horizontalLayout_160.addWidget(self.x_probed_width)
        self.verticalLayout_42.addLayout(self.horizontalLayout_160)
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.label_109 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_109.sizePolicy().hasHeightForWidth())
        self.label_109.setSizePolicy(sizePolicy)
        self.label_109.setMinimumSize(QtCore.QSize(0, 31))
        self.label_109.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_109.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_109.setLineWidth(0)
        self.label_109.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_109.setIndent(0)
        self.label_109.setObjectName("label_109")
        self.horizontalLayout_29.addWidget(self.label_109)
        self.y_minus_probed_position = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_minus_probed_position.sizePolicy().hasHeightForWidth())
        self.y_minus_probed_position.setSizePolicy(sizePolicy)
        self.y_minus_probed_position.setMinimumSize(QtCore.QSize(80, 31))
        self.y_minus_probed_position.setMaximumSize(QtCore.QSize(80, 31))
        self.y_minus_probed_position.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.y_minus_probed_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_minus_probed_position.setObjectName("y_minus_probed_position")
        self.horizontalLayout_29.addWidget(self.y_minus_probed_position)
        self.label_101 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_101.sizePolicy().hasHeightForWidth())
        self.label_101.setSizePolicy(sizePolicy)
        self.label_101.setMinimumSize(QtCore.QSize(80, 31))
        self.label_101.setMaximumSize(QtCore.QSize(80, 31))
        self.label_101.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_101.setLineWidth(0)
        self.label_101.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_101.setIndent(0)
        self.label_101.setObjectName("label_101")
        self.horizontalLayout_29.addWidget(self.label_101)
        self.y_plus_probed_position = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_plus_probed_position.sizePolicy().hasHeightForWidth())
        self.y_plus_probed_position.setSizePolicy(sizePolicy)
        self.y_plus_probed_position.setMinimumSize(QtCore.QSize(80, 31))
        self.y_plus_probed_position.setMaximumSize(QtCore.QSize(80, 31))
        self.y_plus_probed_position.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.y_plus_probed_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_plus_probed_position.setObjectName("y_plus_probed_position")
        self.horizontalLayout_29.addWidget(self.y_plus_probed_position)
        self.label_100 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_100.sizePolicy().hasHeightForWidth())
        self.label_100.setSizePolicy(sizePolicy)
        self.label_100.setMinimumSize(QtCore.QSize(80, 31))
        self.label_100.setMaximumSize(QtCore.QSize(80, 31))
        self.label_100.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_100.setLineWidth(0)
        self.label_100.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_100.setIndent(0)
        self.label_100.setObjectName("label_100")
        self.horizontalLayout_29.addWidget(self.label_100)
        self.y_probed_width = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_probed_width.sizePolicy().hasHeightForWidth())
        self.y_probed_width.setSizePolicy(sizePolicy)
        self.y_probed_width.setMinimumSize(QtCore.QSize(80, 31))
        self.y_probed_width.setMaximumSize(QtCore.QSize(80, 31))
        self.y_probed_width.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.y_probed_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_probed_width.setObjectName("y_probed_width")
        self.horizontalLayout_29.addWidget(self.y_probed_width)
        self.verticalLayout_42.addLayout(self.horizontalLayout_29)
        self.horizontalLayout_161 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_161.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_161.setObjectName("horizontalLayout_161")
        self.label_110 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_110.sizePolicy().hasHeightForWidth())
        self.label_110.setSizePolicy(sizePolicy)
        self.label_110.setMinimumSize(QtCore.QSize(0, 31))
        self.label_110.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_110.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_110.setLineWidth(0)
        self.label_110.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_110.setIndent(0)
        self.label_110.setObjectName("label_110")
        self.horizontalLayout_161.addWidget(self.label_110)
        self.z_minus_probed_position = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.z_minus_probed_position.sizePolicy().hasHeightForWidth())
        self.z_minus_probed_position.setSizePolicy(sizePolicy)
        self.z_minus_probed_position.setMinimumSize(QtCore.QSize(80, 31))
        self.z_minus_probed_position.setMaximumSize(QtCore.QSize(80, 31))
        self.z_minus_probed_position.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.z_minus_probed_position.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.z_minus_probed_position.setObjectName("z_minus_probed_position")
        self.horizontalLayout_161.addWidget(self.z_minus_probed_position)
        self.label_102 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_102.sizePolicy().hasHeightForWidth())
        self.label_102.setSizePolicy(sizePolicy)
        self.label_102.setMinimumSize(QtCore.QSize(80, 31))
        self.label_102.setMaximumSize(QtCore.QSize(80, 31))
        self.label_102.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_102.setLineWidth(0)
        self.label_102.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_102.setIndent(0)
        self.label_102.setObjectName("label_102")
        self.horizontalLayout_161.addWidget(self.label_102)
        self.averaged_diam = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.averaged_diam.sizePolicy().hasHeightForWidth())
        self.averaged_diam.setSizePolicy(sizePolicy)
        self.averaged_diam.setMinimumSize(QtCore.QSize(80, 31))
        self.averaged_diam.setMaximumSize(QtCore.QSize(80, 31))
        self.averaged_diam.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.averaged_diam.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.averaged_diam.setObjectName("averaged_diam")
        self.horizontalLayout_161.addWidget(self.averaged_diam)
        self.label_113 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_113.sizePolicy().hasHeightForWidth())
        self.label_113.setSizePolicy(sizePolicy)
        self.label_113.setMinimumSize(QtCore.QSize(80, 31))
        self.label_113.setMaximumSize(QtCore.QSize(80, 31))
        self.label_113.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_113.setLineWidth(0)
        self.label_113.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_113.setIndent(0)
        self.label_113.setObjectName("label_113")
        self.horizontalLayout_161.addWidget(self.label_113)
        self.x_center_probed = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_center_probed.sizePolicy().hasHeightForWidth())
        self.x_center_probed.setSizePolicy(sizePolicy)
        self.x_center_probed.setMinimumSize(QtCore.QSize(80, 31))
        self.x_center_probed.setMaximumSize(QtCore.QSize(80, 31))
        self.x_center_probed.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.x_center_probed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_center_probed.setObjectName("x_center_probed")
        self.horizontalLayout_161.addWidget(self.x_center_probed)
        self.verticalLayout_42.addLayout(self.horizontalLayout_161)
        self.horizontalLayout_162 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_162.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_162.setObjectName("horizontalLayout_162")
        self.label_99 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_99.sizePolicy().hasHeightForWidth())
        self.label_99.setSizePolicy(sizePolicy)
        self.label_99.setMinimumSize(QtCore.QSize(0, 31))
        self.label_99.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_99.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_99.setLineWidth(0)
        self.label_99.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_99.setIndent(0)
        self.label_99.setObjectName("label_99")
        self.horizontalLayout_162.addWidget(self.label_99)
        self.edge_delta = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edge_delta.sizePolicy().hasHeightForWidth())
        self.edge_delta.setSizePolicy(sizePolicy)
        self.edge_delta.setMinimumSize(QtCore.QSize(80, 31))
        self.edge_delta.setMaximumSize(QtCore.QSize(80, 31))
        self.edge_delta.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.edge_delta.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edge_delta.setObjectName("edge_delta")
        self.horizontalLayout_162.addWidget(self.edge_delta)
        self.label_96 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_96.sizePolicy().hasHeightForWidth())
        self.label_96.setSizePolicy(sizePolicy)
        self.label_96.setMinimumSize(QtCore.QSize(80, 31))
        self.label_96.setMaximumSize(QtCore.QSize(80, 31))
        self.label_96.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_96.setLineWidth(0)
        self.label_96.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_96.setIndent(0)
        self.label_96.setObjectName("label_96")
        self.horizontalLayout_162.addWidget(self.label_96)
        self.edge_angle = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.edge_angle.sizePolicy().hasHeightForWidth())
        self.edge_angle.setSizePolicy(sizePolicy)
        self.edge_angle.setMinimumSize(QtCore.QSize(80, 31))
        self.edge_angle.setMaximumSize(QtCore.QSize(80, 31))
        self.edge_angle.setMouseTracking(True)
        self.edge_angle.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.edge_angle.setTextFormat(QtCore.Qt.RichText)
        self.edge_angle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.edge_angle.setObjectName("edge_angle")
        self.horizontalLayout_162.addWidget(self.edge_angle)
        self.label_114 = QtWidgets.QLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_114.sizePolicy().hasHeightForWidth())
        self.label_114.setSizePolicy(sizePolicy)
        self.label_114.setMinimumSize(QtCore.QSize(80, 31))
        self.label_114.setMaximumSize(QtCore.QSize(80, 31))
        self.label_114.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_114.setLineWidth(0)
        self.label_114.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_114.setIndent(0)
        self.label_114.setObjectName("label_114")
        self.horizontalLayout_162.addWidget(self.label_114)
        self.y_center_probed = StatusLabel(self.widget_44)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_center_probed.sizePolicy().hasHeightForWidth())
        self.y_center_probed.setSizePolicy(sizePolicy)
        self.y_center_probed.setMinimumSize(QtCore.QSize(80, 31))
        self.y_center_probed.setMaximumSize(QtCore.QSize(80, 31))
        self.y_center_probed.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(134, 136, 138);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.y_center_probed.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_center_probed.setObjectName("y_center_probed")
        self.horizontalLayout_162.addWidget(self.y_center_probed)
        self.verticalLayout_42.addLayout(self.horizontalLayout_162)
        self.verticalLayout_41.addLayout(self.verticalLayout_42)
        self.mdi_entry_box_5 = MDIEntry(self.widget_44)
        self.mdi_entry_box_5.setMinimumSize(QtCore.QSize(0, 42))
        self.mdi_entry_box_5.setMaximumSize(QtCore.QSize(16777215, 42))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.mdi_entry_box_5.setFont(font)
        self.mdi_entry_box_5.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mdi_entry_box_5.setObjectName("mdi_entry_box_5")
        self.verticalLayout_41.addWidget(self.mdi_entry_box_5)
        self.horizontalLayout_43.addWidget(self.widget_44)
        self.widget_13 = QtWidgets.QWidget(self.probe_tab)
        self.widget_13.setObjectName("widget_13")
        self.verticalLayout_45 = QtWidgets.QVBoxLayout(self.widget_13)
        self.verticalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_45.setObjectName("verticalLayout_45")
        self.probe_group_select = QtWidgets.QWidget(self.widget_13)
        self.probe_group_select.setStyleSheet("QWidget {\n"
"    font: 13pt \"bebas kai\";\n"
"}")
        self.probe_group_select.setObjectName("probe_group_select")
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout(self.probe_group_select)
        self.horizontalLayout_30.setContentsMargins(20, 3, 20, 6)
        self.horizontalLayout_30.setSpacing(0)
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.outside_corners = QtWidgets.QPushButton(self.probe_group_select)
        self.outside_corners.setFocusPolicy(QtCore.Qt.NoFocus)
        self.outside_corners.setStyleSheet("QPushButton {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    color: white;\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #4e4e4e, stop: 1.0 #3a3a3a);\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-top-width: 2px;\n"
"    border-bottom-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-left-width: 2px;\n"
"    min-width: 10ex;\n"
"    min-height: 25;\n"
"    padding: 2px;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(112, 112, 238, 255), stop:0.121053 rgba(123, 123, 232, 255), stop:0.3 rgba(85, 85, 238, 255), stop:0.694737 rgba(85, 85, 238, 255), stop:0.915789 rgba(123, 123, 232, 255), stop:1 rgba(112, 112, 238, 255))\n"
"}")
        self.outside_corners.setCheckable(True)
        self.outside_corners.setChecked(True)
        self.outside_corners.setAutoExclusive(True)
        self.outside_corners.setProperty("page", 0)
        self.outside_corners.setObjectName("outside_corners")
        self.probetabGroup = QtWidgets.QButtonGroup(Form)
        self.probetabGroup.setObjectName("probetabGroup")
        self.probetabGroup.addButton(self.outside_corners)
        self.horizontalLayout_30.addWidget(self.outside_corners)
        self.inside_corners = QtWidgets.QPushButton(self.probe_group_select)
        self.inside_corners.setFocusPolicy(QtCore.Qt.NoFocus)
        self.inside_corners.setStyleSheet("QPushButton {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    color: white;\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #4e4e4e, stop: 1.0 #3a3a3a);\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-top-width: 2px;\n"
"    border-bottom-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-left-width: 1px;\n"
"    min-width: 10ex;\n"
"    min-height: 25;\n"
"    padding: 2px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(112, 112, 238, 255), stop:0.121053 rgba(123, 123, 232, 255), stop:0.3 rgba(85, 85, 238, 255), stop:0.694737 rgba(85, 85, 238, 255), stop:0.915789 rgba(123, 123, 232, 255), stop:1 rgba(112, 112, 238, 255))\n"
"}")
        self.inside_corners.setCheckable(True)
        self.inside_corners.setAutoExclusive(True)
        self.inside_corners.setProperty("page", 1)
        self.inside_corners.setObjectName("inside_corners")
        self.probetabGroup.addButton(self.inside_corners)
        self.horizontalLayout_30.addWidget(self.inside_corners)
        self.boss_and_pocket = QtWidgets.QPushButton(self.probe_group_select)
        self.boss_and_pocket.setFocusPolicy(QtCore.Qt.NoFocus)
        self.boss_and_pocket.setStyleSheet("QPushButton {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    color: white;\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #4e4e4e, stop: 1.0 #3a3a3a);\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-top-width: 2px;\n"
"    border-bottom-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-left-width: 1px;\n"
"    min-width: 10ex;\n"
"    min-height: 25;\n"
"    padding: 2px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(112, 112, 238, 255), stop:0.121053 rgba(123, 123, 232, 255), stop:0.3 rgba(85, 85, 238, 255), stop:0.694737 rgba(85, 85, 238, 255), stop:0.915789 rgba(123, 123, 232, 255), stop:1 rgba(112, 112, 238, 255))\n"
"}")
        self.boss_and_pocket.setCheckable(True)
        self.boss_and_pocket.setAutoExclusive(True)
        self.boss_and_pocket.setProperty("page", 2)
        self.boss_and_pocket.setObjectName("boss_and_pocket")
        self.probetabGroup.addButton(self.boss_and_pocket)
        self.horizontalLayout_30.addWidget(self.boss_and_pocket)
        self.ridge_and_valley = QtWidgets.QPushButton(self.probe_group_select)
        self.ridge_and_valley.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ridge_and_valley.setStyleSheet("QPushButton {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    color: white;\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #4e4e4e, stop: 1.0 #3a3a3a);\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-top-width: 2px;\n"
"    border-bottom-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-left-width: 1px;\n"
"    min-width: 10ex;\n"
"    min-height: 25;\n"
"    padding: 2px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(112, 112, 238, 255), stop:0.121053 rgba(123, 123, 232, 255), stop:0.3 rgba(85, 85, 238, 255), stop:0.694737 rgba(85, 85, 238, 255), stop:0.915789 rgba(123, 123, 232, 255), stop:1 rgba(112, 112, 238, 255))\n"
"}")
        self.ridge_and_valley.setCheckable(True)
        self.ridge_and_valley.setAutoExclusive(True)
        self.ridge_and_valley.setProperty("page", 3)
        self.ridge_and_valley.setObjectName("ridge_and_valley")
        self.probetabGroup.addButton(self.ridge_and_valley)
        self.horizontalLayout_30.addWidget(self.ridge_and_valley)
        self.rotation_angle = QtWidgets.QPushButton(self.probe_group_select)
        self.rotation_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rotation_angle.setStyleSheet("QPushButton {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    color: white;\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #4e4e4e, stop: 1.0 #3a3a3a);\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-top-width: 2px;\n"
"    border-bottom-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-left-width: 1px;\n"
"    min-width: 10ex;\n"
"    min-height: 25;\n"
"    padding: 2px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(112, 112, 238, 255), stop:0.121053 rgba(123, 123, 232, 255), stop:0.3 rgba(85, 85, 238, 255), stop:0.694737 rgba(85, 85, 238, 255), stop:0.915789 rgba(123, 123, 232, 255), stop:1 rgba(112, 112, 238, 255))\n"
"}")
        self.rotation_angle.setCheckable(True)
        self.rotation_angle.setAutoExclusive(True)
        self.rotation_angle.setProperty("page", 4)
        self.rotation_angle.setObjectName("rotation_angle")
        self.probetabGroup.addButton(self.rotation_angle)
        self.horizontalLayout_30.addWidget(self.rotation_angle)
        self.rotary_axis_2 = QtWidgets.QPushButton(self.probe_group_select)
        self.rotary_axis_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.rotary_axis_2.setStyleSheet("QPushButton {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    color: white;\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #4e4e4e, stop: 1.0 #3a3a3a);\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-top-width: 2px;\n"
"    border-bottom-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-left-width: 1px;\n"
"    min-width: 10ex;\n"
"    min-height: 25;\n"
"    padding: 2px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(112, 112, 238, 255), stop:0.121053 rgba(123, 123, 232, 255), stop:0.3 rgba(85, 85, 238, 255), stop:0.694737 rgba(85, 85, 238, 255), stop:0.915789 rgba(123, 123, 232, 255), stop:1 rgba(112, 112, 238, 255))\n"
"}")
        self.rotary_axis_2.setCheckable(True)
        self.rotary_axis_2.setAutoExclusive(True)
        self.rotary_axis_2.setProperty("page", 5)
        self.rotary_axis_2.setObjectName("rotary_axis_2")
        self.probetabGroup.addButton(self.rotary_axis_2)
        self.horizontalLayout_30.addWidget(self.rotary_axis_2)
        self.calibrate = QtWidgets.QPushButton(self.probe_group_select)
        self.calibrate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calibrate.setStyleSheet("QPushButton {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    color: white;\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #4e4e4e, stop: 1.0 #3a3a3a);\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-top-width: 2px;\n"
"    border-bottom-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-left-width: 1px;\n"
"    min-width: 10ex;\n"
"    min-height: 25;\n"
"    padding: 2px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(112, 112, 238, 255), stop:0.121053 rgba(123, 123, 232, 255), stop:0.3 rgba(85, 85, 238, 255), stop:0.694737 rgba(85, 85, 238, 255), stop:0.915789 rgba(123, 123, 232, 255), stop:1 rgba(112, 112, 238, 255))\n"
"}")
        self.calibrate.setCheckable(True)
        self.calibrate.setAutoExclusive(True)
        self.calibrate.setProperty("page", 6)
        self.calibrate.setObjectName("calibrate")
        self.probetabGroup.addButton(self.calibrate)
        self.horizontalLayout_30.addWidget(self.calibrate)
        self.probe_help = QtWidgets.QPushButton(self.probe_group_select)
        self.probe_help.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_help.setStyleSheet("QPushButton {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    color: white;\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #4e4e4e, stop: 1.0 #3a3a3a);\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-top-width: 2px;\n"
"    border-bottom-width: 2px;\n"
"    border-right-width: 2px;\n"
"    border-left-width: 1px;\n"
"    min-width: 10ex;\n"
"    min-height: 25;\n"
"    padding: 2px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 4px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 4px;\n"
"}\n"
"\n"
"QPushButton:pressed, QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(112, 112, 238, 255), stop:0.121053 rgba(123, 123, 232, 255), stop:0.3 rgba(85, 85, 238, 255), stop:0.694737 rgba(85, 85, 238, 255), stop:0.915789 rgba(123, 123, 232, 255), stop:1 rgba(112, 112, 238, 255))\n"
"}")
        self.probe_help.setCheckable(True)
        self.probe_help.setAutoExclusive(True)
        self.probe_help.setProperty("page", 7)
        self.probe_help.setObjectName("probe_help")
        self.probetabGroup.addButton(self.probe_help)
        self.horizontalLayout_30.addWidget(self.probe_help)
        self.verticalLayout_45.addWidget(self.probe_group_select)
        self.widget_11 = QtWidgets.QWidget(self.widget_13)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, 0, -1, 9)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.probe_tab_widget = QtWidgets.QStackedWidget(self.widget_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_tab_widget.sizePolicy().hasHeightForWidth())
        self.probe_tab_widget.setSizePolicy(sizePolicy)
        self.probe_tab_widget.setMinimumSize(QtCore.QSize(550, 0))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(13)
        self.probe_tab_widget.setFont(font)
        self.probe_tab_widget.setStyleSheet("")
        self.probe_tab_widget.setObjectName("probe_tab_widget")
        self.Page1 = QtWidgets.QWidget()
        self.Page1.setObjectName("Page1")
        self.horizontalLayout_1321 = QtWidgets.QHBoxLayout(self.Page1)
        self.horizontalLayout_1321.setObjectName("horizontalLayout_1321")
        self.widget_40 = QtWidgets.QWidget(self.Page1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_40.sizePolicy().hasHeightForWidth())
        self.widget_40.setSizePolicy(sizePolicy)
        self.widget_40.setMinimumSize(QtCore.QSize(465, 465))
        self.widget_40.setMaximumSize(QtCore.QSize(465, 465))
        self.widget_40.setStyleSheet("")
        self.widget_40.setObjectName("widget_40")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget_40)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.probe_back_left_top_corner = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_back_left_top_corner.sizePolicy().hasHeightForWidth())
        self.probe_back_left_top_corner.setSizePolicy(sizePolicy)
        self.probe_back_left_top_corner.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_back_left_top_corner.setFocusPolicy(QtCore.Qt.NoFocus)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/images/back_left_outside_corner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_back_left_top_corner.setIcon(icon11)
        self.probe_back_left_top_corner.setIconSize(QtCore.QSize(130, 130))
        self.probe_back_left_top_corner.setObjectName("probe_back_left_top_corner")
        self.proberoutinebtnGroup = QtWidgets.QButtonGroup(Form)
        self.proberoutinebtnGroup.setObjectName("proberoutinebtnGroup")
        self.proberoutinebtnGroup.addButton(self.probe_back_left_top_corner)
        self.gridLayout_7.addWidget(self.probe_back_left_top_corner, 0, 0, 1, 1)
        self.probe_back_right_top_corner = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_back_right_top_corner.sizePolicy().hasHeightForWidth())
        self.probe_back_right_top_corner.setSizePolicy(sizePolicy)
        self.probe_back_right_top_corner.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_back_right_top_corner.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_back_right_top_corner.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_back_right_top_corner.setStyleSheet("")
        self.probe_back_right_top_corner.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/images/back_right_outside_corner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_back_right_top_corner.setIcon(icon12)
        self.probe_back_right_top_corner.setIconSize(QtCore.QSize(130, 130))
        self.probe_back_right_top_corner.setObjectName("probe_back_right_top_corner")
        self.proberoutinebtnGroup.addButton(self.probe_back_right_top_corner)
        self.gridLayout_7.addWidget(self.probe_back_right_top_corner, 0, 4, 1, 1)
        self.probe_right_top_side = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_right_top_side.sizePolicy().hasHeightForWidth())
        self.probe_right_top_side.setSizePolicy(sizePolicy)
        self.probe_right_top_side.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_right_top_side.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_right_top_side.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_right_top_side.setStyleSheet("")
        self.probe_right_top_side.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/images/right_side_edge.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon13.addPixmap(QtGui.QPixmap(":/images/right_side_edge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_right_top_side.setIcon(icon13)
        self.probe_right_top_side.setIconSize(QtCore.QSize(130, 130))
        self.probe_right_top_side.setObjectName("probe_right_top_side")
        self.proberoutinebtnGroup.addButton(self.probe_right_top_side)
        self.gridLayout_7.addWidget(self.probe_right_top_side, 1, 4, 1, 1)
        self.probe_z_minus_wco_edge = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_z_minus_wco_edge.sizePolicy().hasHeightForWidth())
        self.probe_z_minus_wco_edge.setSizePolicy(sizePolicy)
        self.probe_z_minus_wco_edge.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_z_minus_wco_edge.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_z_minus_wco_edge.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_z_minus_wco_edge.setStyleSheet("")
        self.probe_z_minus_wco_edge.setText("")
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/images/z_top.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_z_minus_wco_edge.setIcon(icon14)
        self.probe_z_minus_wco_edge.setIconSize(QtCore.QSize(130, 130))
        self.probe_z_minus_wco_edge.setObjectName("probe_z_minus_wco_edge")
        self.proberoutinebtnGroup.addButton(self.probe_z_minus_wco_edge)
        self.gridLayout_7.addWidget(self.probe_z_minus_wco_edge, 1, 3, 1, 1)
        self.probe_front_top_side = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_front_top_side.sizePolicy().hasHeightForWidth())
        self.probe_front_top_side.setSizePolicy(sizePolicy)
        self.probe_front_top_side.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_front_top_side.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_front_top_side.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_front_top_side.setStyleSheet("")
        self.probe_front_top_side.setText("")
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/images/front_middle_edge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_front_top_side.setIcon(icon15)
        self.probe_front_top_side.setIconSize(QtCore.QSize(130, 130))
        self.probe_front_top_side.setObjectName("probe_front_top_side")
        self.proberoutinebtnGroup.addButton(self.probe_front_top_side)
        self.gridLayout_7.addWidget(self.probe_front_top_side, 2, 3, 1, 1)
        self.probe_back_top_side = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_back_top_side.sizePolicy().hasHeightForWidth())
        self.probe_back_top_side.setSizePolicy(sizePolicy)
        self.probe_back_top_side.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_back_top_side.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_back_top_side.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_back_top_side.setStyleSheet("")
        self.probe_back_top_side.setText("")
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/images/back_middle_outside_edge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_back_top_side.setIcon(icon16)
        self.probe_back_top_side.setIconSize(QtCore.QSize(130, 130))
        self.probe_back_top_side.setObjectName("probe_back_top_side")
        self.proberoutinebtnGroup.addButton(self.probe_back_top_side)
        self.gridLayout_7.addWidget(self.probe_back_top_side, 0, 3, 1, 1)
        self.probe_front_left_top_corner = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_front_left_top_corner.sizePolicy().hasHeightForWidth())
        self.probe_front_left_top_corner.setSizePolicy(sizePolicy)
        self.probe_front_left_top_corner.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_front_left_top_corner.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_front_left_top_corner.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_front_left_top_corner.setStyleSheet("")
        self.probe_front_left_top_corner.setText("")
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/images/front_left_outside_corner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_front_left_top_corner.setIcon(icon17)
        self.probe_front_left_top_corner.setIconSize(QtCore.QSize(130, 130))
        self.probe_front_left_top_corner.setObjectName("probe_front_left_top_corner")
        self.proberoutinebtnGroup.addButton(self.probe_front_left_top_corner)
        self.gridLayout_7.addWidget(self.probe_front_left_top_corner, 2, 0, 1, 1)
        self.probe_front_right_top_corner = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_front_right_top_corner.sizePolicy().hasHeightForWidth())
        self.probe_front_right_top_corner.setSizePolicy(sizePolicy)
        self.probe_front_right_top_corner.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_front_right_top_corner.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_front_right_top_corner.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_front_right_top_corner.setStyleSheet("")
        self.probe_front_right_top_corner.setText("")
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/images/front_right_outside_corner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_front_right_top_corner.setIcon(icon18)
        self.probe_front_right_top_corner.setIconSize(QtCore.QSize(130, 130))
        self.probe_front_right_top_corner.setObjectName("probe_front_right_top_corner")
        self.proberoutinebtnGroup.addButton(self.probe_front_right_top_corner)
        self.gridLayout_7.addWidget(self.probe_front_right_top_corner, 2, 4, 1, 1)
        self.probe_left_top_side = SubCallButton(self.widget_40)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_left_top_side.sizePolicy().hasHeightForWidth())
        self.probe_left_top_side.setSizePolicy(sizePolicy)
        self.probe_left_top_side.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_left_top_side.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_left_top_side.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_left_top_side.setStyleSheet("")
        self.probe_left_top_side.setText("")
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/images/left_side_edge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_left_top_side.setIcon(icon19)
        self.probe_left_top_side.setIconSize(QtCore.QSize(130, 130))
        self.probe_left_top_side.setObjectName("probe_left_top_side")
        self.proberoutinebtnGroup.addButton(self.probe_left_top_side)
        self.gridLayout_7.addWidget(self.probe_left_top_side, 1, 0, 1, 1)
        self.horizontalLayout_1321.addWidget(self.widget_40)
        self.probe_tab_widget.addWidget(self.Page1)
        self.Page2 = QtWidgets.QWidget()
        self.Page2.setObjectName("Page2")
        self.horizontalLayout_1351 = QtWidgets.QHBoxLayout(self.Page2)
        self.horizontalLayout_1351.setObjectName("horizontalLayout_1351")
        self.widget_41 = QtWidgets.QWidget(self.Page2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_41.sizePolicy().hasHeightForWidth())
        self.widget_41.setSizePolicy(sizePolicy)
        self.widget_41.setMinimumSize(QtCore.QSize(465, 465))
        self.widget_41.setMaximumSize(QtCore.QSize(465, 465))
        self.widget_41.setStyleSheet("QFrame {\n"
"    border: none;\n"
"}")
        self.widget_41.setObjectName("widget_41")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.widget_41)
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.probe_front_right_inside_corner = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_front_right_inside_corner.sizePolicy().hasHeightForWidth())
        self.probe_front_right_inside_corner.setSizePolicy(sizePolicy)
        self.probe_front_right_inside_corner.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_front_right_inside_corner.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_front_right_inside_corner.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_front_right_inside_corner.setText("")
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/images/inside_front_right_corner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_front_right_inside_corner.setIcon(icon20)
        self.probe_front_right_inside_corner.setIconSize(QtCore.QSize(125, 125))
        self.probe_front_right_inside_corner.setObjectName("probe_front_right_inside_corner")
        self.proberoutinebtnGroup.addButton(self.probe_front_right_inside_corner)
        self.gridLayout_16.addWidget(self.probe_front_right_inside_corner, 3, 4, 1, 1)
        self.probe_y_plus_wco = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_y_plus_wco.sizePolicy().hasHeightForWidth())
        self.probe_y_plus_wco.setSizePolicy(sizePolicy)
        self.probe_y_plus_wco.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_y_plus_wco.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_y_plus_wco.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_y_plus_wco.setText("")
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/images/y_plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_y_plus_wco.setIcon(icon21)
        self.probe_y_plus_wco.setIconSize(QtCore.QSize(125, 125))
        self.probe_y_plus_wco.setObjectName("probe_y_plus_wco")
        self.proberoutinebtnGroup.addButton(self.probe_y_plus_wco)
        self.gridLayout_16.addWidget(self.probe_y_plus_wco, 0, 3, 1, 1)
        self.probe_back_right_inside_corner = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_back_right_inside_corner.sizePolicy().hasHeightForWidth())
        self.probe_back_right_inside_corner.setSizePolicy(sizePolicy)
        self.probe_back_right_inside_corner.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_back_right_inside_corner.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_back_right_inside_corner.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_back_right_inside_corner.setText("")
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(":/images/inside_back_right_corner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_back_right_inside_corner.setIcon(icon22)
        self.probe_back_right_inside_corner.setIconSize(QtCore.QSize(125, 125))
        self.probe_back_right_inside_corner.setObjectName("probe_back_right_inside_corner")
        self.proberoutinebtnGroup.addButton(self.probe_back_right_inside_corner)
        self.gridLayout_16.addWidget(self.probe_back_right_inside_corner, 0, 4, 1, 1)
        self.probe_front_left_inside_corner = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_front_left_inside_corner.sizePolicy().hasHeightForWidth())
        self.probe_front_left_inside_corner.setSizePolicy(sizePolicy)
        self.probe_front_left_inside_corner.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_front_left_inside_corner.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_front_left_inside_corner.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_front_left_inside_corner.setText("")
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(":/images/inside_front_left_corner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_front_left_inside_corner.setIcon(icon23)
        self.probe_front_left_inside_corner.setIconSize(QtCore.QSize(125, 125))
        self.probe_front_left_inside_corner.setObjectName("probe_front_left_inside_corner")
        self.proberoutinebtnGroup.addButton(self.probe_front_left_inside_corner)
        self.gridLayout_16.addWidget(self.probe_front_left_inside_corner, 3, 0, 1, 1)
        self.probe_z_minus_wco_inside = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_z_minus_wco_inside.sizePolicy().hasHeightForWidth())
        self.probe_z_minus_wco_inside.setSizePolicy(sizePolicy)
        self.probe_z_minus_wco_inside.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_z_minus_wco_inside.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_z_minus_wco_inside.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_z_minus_wco_inside.setText("")
        self.probe_z_minus_wco_inside.setIcon(icon14)
        self.probe_z_minus_wco_inside.setIconSize(QtCore.QSize(125, 125))
        self.probe_z_minus_wco_inside.setObjectName("probe_z_minus_wco_inside")
        self.proberoutinebtnGroup.addButton(self.probe_z_minus_wco_inside)
        self.gridLayout_16.addWidget(self.probe_z_minus_wco_inside, 1, 3, 1, 1)
        self.probe_back_left_inside_corner = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_back_left_inside_corner.sizePolicy().hasHeightForWidth())
        self.probe_back_left_inside_corner.setSizePolicy(sizePolicy)
        self.probe_back_left_inside_corner.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_back_left_inside_corner.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_back_left_inside_corner.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_back_left_inside_corner.setText("")
        icon24 = QtGui.QIcon()
        icon24.addPixmap(QtGui.QPixmap(":/images/inside_back_left_corner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_back_left_inside_corner.setIcon(icon24)
        self.probe_back_left_inside_corner.setIconSize(QtCore.QSize(125, 125))
        self.probe_back_left_inside_corner.setObjectName("probe_back_left_inside_corner")
        self.proberoutinebtnGroup.addButton(self.probe_back_left_inside_corner)
        self.gridLayout_16.addWidget(self.probe_back_left_inside_corner, 0, 0, 1, 1)
        self.probe_x_minus_wco = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_x_minus_wco.sizePolicy().hasHeightForWidth())
        self.probe_x_minus_wco.setSizePolicy(sizePolicy)
        self.probe_x_minus_wco.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_x_minus_wco.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_x_minus_wco.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_x_minus_wco.setText("")
        icon25 = QtGui.QIcon()
        icon25.addPixmap(QtGui.QPixmap(":/images/x_minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_x_minus_wco.setIcon(icon25)
        self.probe_x_minus_wco.setIconSize(QtCore.QSize(125, 125))
        self.probe_x_minus_wco.setObjectName("probe_x_minus_wco")
        self.proberoutinebtnGroup.addButton(self.probe_x_minus_wco)
        self.gridLayout_16.addWidget(self.probe_x_minus_wco, 1, 0, 1, 1)
        self.probe_x_plus_wco = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_x_plus_wco.sizePolicy().hasHeightForWidth())
        self.probe_x_plus_wco.setSizePolicy(sizePolicy)
        self.probe_x_plus_wco.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_x_plus_wco.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_x_plus_wco.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_x_plus_wco.setText("")
        icon26 = QtGui.QIcon()
        icon26.addPixmap(QtGui.QPixmap(":/images/x_plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_x_plus_wco.setIcon(icon26)
        self.probe_x_plus_wco.setIconSize(QtCore.QSize(125, 125))
        self.probe_x_plus_wco.setObjectName("probe_x_plus_wco")
        self.proberoutinebtnGroup.addButton(self.probe_x_plus_wco)
        self.gridLayout_16.addWidget(self.probe_x_plus_wco, 1, 4, 1, 1)
        self.probe_y_minus_wco = SubCallButton(self.widget_41)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_y_minus_wco.sizePolicy().hasHeightForWidth())
        self.probe_y_minus_wco.setSizePolicy(sizePolicy)
        self.probe_y_minus_wco.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_y_minus_wco.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_y_minus_wco.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_y_minus_wco.setText("")
        icon27 = QtGui.QIcon()
        icon27.addPixmap(QtGui.QPixmap(":/images/y_minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_y_minus_wco.setIcon(icon27)
        self.probe_y_minus_wco.setIconSize(QtCore.QSize(125, 125))
        self.probe_y_minus_wco.setObjectName("probe_y_minus_wco")
        self.proberoutinebtnGroup.addButton(self.probe_y_minus_wco)
        self.gridLayout_16.addWidget(self.probe_y_minus_wco, 3, 3, 1, 1)
        self.horizontalLayout_1351.addWidget(self.widget_41)
        self.probe_tab_widget.addWidget(self.Page2)
        self.Page3 = QtWidgets.QWidget()
        self.Page3.setObjectName("Page3")
        self.horizontalLayout_138 = QtWidgets.QHBoxLayout(self.Page3)
        self.horizontalLayout_138.setObjectName("horizontalLayout_138")
        self.widget_42 = QtWidgets.QWidget(self.Page3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_42.sizePolicy().hasHeightForWidth())
        self.widget_42.setSizePolicy(sizePolicy)
        self.widget_42.setMinimumSize(QtCore.QSize(465, 461))
        self.widget_42.setMaximumSize(QtCore.QSize(465, 461))
        self.widget_42.setStyleSheet("QFrame {\n"
"    border: none;\n"
"}")
        self.widget_42.setObjectName("widget_42")
        self.gridWidget_8 = QtWidgets.QWidget(self.widget_42)
        self.gridWidget_8.setGeometry(QtCore.QRect(53, 1, 364, 364))
        self.gridWidget_8.setObjectName("gridWidget_8")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.gridWidget_8)
        self.gridLayout_10.setSpacing(10)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.probe_round_boss = SubCallButton(self.gridWidget_8)
        self.probe_round_boss.setMinimumSize(QtCore.QSize(170, 170))
        self.probe_round_boss.setMaximumSize(QtCore.QSize(170, 170))
        self.probe_round_boss.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_round_boss.setStyleSheet("")
        self.probe_round_boss.setText("")
        icon28 = QtGui.QIcon()
        icon28.addPixmap(QtGui.QPixmap(":/images/boss_round.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_round_boss.setIcon(icon28)
        self.probe_round_boss.setIconSize(QtCore.QSize(170, 170))
        self.probe_round_boss.setObjectName("probe_round_boss")
        self.proberoutinebtnGroup.addButton(self.probe_round_boss)
        self.gridLayout_10.addWidget(self.probe_round_boss, 0, 0, 1, 1)
        self.probe_round_pocket = SubCallButton(self.gridWidget_8)
        self.probe_round_pocket.setMinimumSize(QtCore.QSize(170, 170))
        self.probe_round_pocket.setMaximumSize(QtCore.QSize(170, 170))
        self.probe_round_pocket.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_round_pocket.setStyleSheet("")
        self.probe_round_pocket.setText("")
        icon29 = QtGui.QIcon()
        icon29.addPixmap(QtGui.QPixmap(":/images/round_pocket.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_round_pocket.setIcon(icon29)
        self.probe_round_pocket.setIconSize(QtCore.QSize(145, 145))
        self.probe_round_pocket.setObjectName("probe_round_pocket")
        self.proberoutinebtnGroup.addButton(self.probe_round_pocket)
        self.gridLayout_10.addWidget(self.probe_round_pocket, 0, 1, 1, 1)
        self.probe_rect_boss = SubCallButton(self.gridWidget_8)
        self.probe_rect_boss.setMinimumSize(QtCore.QSize(170, 170))
        self.probe_rect_boss.setMaximumSize(QtCore.QSize(170, 170))
        self.probe_rect_boss.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_rect_boss.setStyleSheet("")
        self.probe_rect_boss.setText("")
        icon30 = QtGui.QIcon()
        icon30.addPixmap(QtGui.QPixmap(":/images/rect_boss.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_rect_boss.setIcon(icon30)
        self.probe_rect_boss.setIconSize(QtCore.QSize(170, 170))
        self.probe_rect_boss.setObjectName("probe_rect_boss")
        self.proberoutinebtnGroup.addButton(self.probe_rect_boss)
        self.gridLayout_10.addWidget(self.probe_rect_boss, 1, 0, 1, 1)
        self.probe_rect_pocket = SubCallButton(self.gridWidget_8)
        self.probe_rect_pocket.setMinimumSize(QtCore.QSize(170, 170))
        self.probe_rect_pocket.setMaximumSize(QtCore.QSize(170, 170))
        self.probe_rect_pocket.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_rect_pocket.setStyleSheet("")
        self.probe_rect_pocket.setText("")
        icon31 = QtGui.QIcon()
        icon31.addPixmap(QtGui.QPixmap(":/images/rect_pocket.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_rect_pocket.setIcon(icon31)
        self.probe_rect_pocket.setIconSize(QtCore.QSize(145, 145))
        self.probe_rect_pocket.setObjectName("probe_rect_pocket")
        self.proberoutinebtnGroup.addButton(self.probe_rect_pocket)
        self.gridLayout_10.addWidget(self.probe_rect_pocket, 1, 1, 1, 1)
        self.frame_8 = QtWidgets.QFrame(self.widget_42)
        self.frame_8.setGeometry(QtCore.QRect(3, 392, 460, 65))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setMinimumSize(QtCore.QSize(460, 65))
        self.frame_8.setMaximumSize(QtCore.QSize(460, 65))
        self.frame_8.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-width: 2px;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}")
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_48 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_48.setObjectName("horizontalLayout_48")
        self.horizontalLayout_201 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_201.setSpacing(0)
        self.horizontalLayout_201.setObjectName("horizontalLayout_201")
        self.hint_label = QtWidgets.QLabel(self.frame_8)
        self.hint_label.setMinimumSize(QtCore.QSize(60, 40))
        self.hint_label.setMaximumSize(QtCore.QSize(60, 40))
        self.hint_label.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(191, 191, 191);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.hint_label.setAlignment(QtCore.Qt.AlignCenter)
        self.hint_label.setObjectName("hint_label")
        self.horizontalLayout_201.addWidget(self.hint_label)
        self.label_70 = QtWidgets.QLabel(self.frame_8)
        self.label_70.setMinimumSize(QtCore.QSize(50, 0))
        self.label_70.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_70.setStyleSheet("QLabel{\n"
"font: 75 15pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"padding-right: 1px;\n"
"padding-left: 5px;\n"
"}")
        self.label_70.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_70.setIndent(0)
        self.label_70.setObjectName("label_70")
        self.horizontalLayout_201.addWidget(self.label_70)
        self.diameter_hint = VCPLineEdit(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.diameter_hint.sizePolicy().hasHeightForWidth())
        self.diameter_hint.setSizePolicy(sizePolicy)
        self.diameter_hint.setMinimumSize(QtCore.QSize(80, 40))
        self.diameter_hint.setMaximumSize(QtCore.QSize(80, 40))
        self.diameter_hint.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.diameter_hint.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.diameter_hint.setObjectName("diameter_hint")
        self.horizontalLayout_201.addWidget(self.diameter_hint)
        self.label_71 = QtWidgets.QLabel(self.frame_8)
        self.label_71.setMinimumSize(QtCore.QSize(30, 0))
        self.label_71.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_71.setStyleSheet("QLabel{\n"
"font: 75 15pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"padding-right: 1px;\n"
"padding-left: 5px;\n"
"}")
        self.label_71.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_71.setIndent(0)
        self.label_71.setObjectName("label_71")
        self.horizontalLayout_201.addWidget(self.label_71)
        self.x_hint_0 = VCPLineEdit(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_hint_0.sizePolicy().hasHeightForWidth())
        self.x_hint_0.setSizePolicy(sizePolicy)
        self.x_hint_0.setMinimumSize(QtCore.QSize(80, 40))
        self.x_hint_0.setMaximumSize(QtCore.QSize(80, 40))
        self.x_hint_0.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.x_hint_0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_hint_0.setObjectName("x_hint_0")
        self.horizontalLayout_201.addWidget(self.x_hint_0)
        self.label_72 = QtWidgets.QLabel(self.frame_8)
        self.label_72.setMinimumSize(QtCore.QSize(30, 0))
        self.label_72.setMaximumSize(QtCore.QSize(30, 16777215))
        self.label_72.setStyleSheet("QLabel{\n"
"font: 75 15pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"padding-right: 1px;\n"
"padding-left: 5px;\n"
"}")
        self.label_72.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_72.setIndent(0)
        self.label_72.setObjectName("label_72")
        self.horizontalLayout_201.addWidget(self.label_72)
        self.y_hint_0 = VCPLineEdit(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_hint_0.sizePolicy().hasHeightForWidth())
        self.y_hint_0.setSizePolicy(sizePolicy)
        self.y_hint_0.setMinimumSize(QtCore.QSize(80, 40))
        self.y_hint_0.setMaximumSize(QtCore.QSize(80, 40))
        self.y_hint_0.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.y_hint_0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_hint_0.setObjectName("y_hint_0")
        self.horizontalLayout_201.addWidget(self.y_hint_0)
        self.horizontalLayout_48.addLayout(self.horizontalLayout_201)
        self.horizontalLayout_138.addWidget(self.widget_42)
        self.probe_tab_widget.addWidget(self.Page3)
        self.Page4 = QtWidgets.QWidget()
        self.Page4.setObjectName("Page4")
        self.horizontalLayout_141 = QtWidgets.QHBoxLayout(self.Page4)
        self.horizontalLayout_141.setObjectName("horizontalLayout_141")
        self.widget_43 = QtWidgets.QWidget(self.Page4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_43.sizePolicy().hasHeightForWidth())
        self.widget_43.setSizePolicy(sizePolicy)
        self.widget_43.setMinimumSize(QtCore.QSize(405, 461))
        self.widget_43.setMaximumSize(QtCore.QSize(405, 461))
        self.widget_43.setStyleSheet("")
        self.widget_43.setObjectName("widget_43")
        self.gridWidget_9 = QtWidgets.QWidget(self.widget_43)
        self.gridWidget_9.setGeometry(QtCore.QRect(23, 1, 364, 364))
        self.gridWidget_9.setObjectName("gridWidget_9")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.gridWidget_9)
        self.gridLayout_9.setSpacing(10)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.probe_valley_x = SubCallButton(self.gridWidget_9)
        self.probe_valley_x.setMinimumSize(QtCore.QSize(170, 170))
        self.probe_valley_x.setMaximumSize(QtCore.QSize(170, 170))
        self.probe_valley_x.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_valley_x.setStyleSheet("")
        self.probe_valley_x.setText("")
        icon32 = QtGui.QIcon()
        icon32.addPixmap(QtGui.QPixmap(":/images/probe_x_valley.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_valley_x.setIcon(icon32)
        self.probe_valley_x.setIconSize(QtCore.QSize(150, 150))
        self.probe_valley_x.setObjectName("probe_valley_x")
        self.proberoutinebtnGroup.addButton(self.probe_valley_x)
        self.gridLayout_9.addWidget(self.probe_valley_x, 0, 0, 1, 1)
        self.probe_valley_y = SubCallButton(self.gridWidget_9)
        self.probe_valley_y.setMinimumSize(QtCore.QSize(170, 170))
        self.probe_valley_y.setMaximumSize(QtCore.QSize(170, 170))
        self.probe_valley_y.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_valley_y.setStyleSheet("")
        self.probe_valley_y.setText("")
        icon33 = QtGui.QIcon()
        icon33.addPixmap(QtGui.QPixmap(":/images/probe_y_valley.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_valley_y.setIcon(icon33)
        self.probe_valley_y.setIconSize(QtCore.QSize(150, 150))
        self.probe_valley_y.setObjectName("probe_valley_y")
        self.proberoutinebtnGroup.addButton(self.probe_valley_y)
        self.gridLayout_9.addWidget(self.probe_valley_y, 0, 1, 1, 1)
        self.probe_ridge_x = SubCallButton(self.gridWidget_9)
        self.probe_ridge_x.setMinimumSize(QtCore.QSize(170, 170))
        self.probe_ridge_x.setMaximumSize(QtCore.QSize(170, 170))
        self.probe_ridge_x.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_ridge_x.setStyleSheet("")
        self.probe_ridge_x.setText("")
        icon34 = QtGui.QIcon()
        icon34.addPixmap(QtGui.QPixmap(":/images/probe_x_ridge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_ridge_x.setIcon(icon34)
        self.probe_ridge_x.setIconSize(QtCore.QSize(150, 150))
        self.probe_ridge_x.setObjectName("probe_ridge_x")
        self.proberoutinebtnGroup.addButton(self.probe_ridge_x)
        self.gridLayout_9.addWidget(self.probe_ridge_x, 1, 0, 1, 1)
        self.probe_ridge_y = SubCallButton(self.gridWidget_9)
        self.probe_ridge_y.setMinimumSize(QtCore.QSize(170, 170))
        self.probe_ridge_y.setMaximumSize(QtCore.QSize(170, 170))
        self.probe_ridge_y.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_ridge_y.setStyleSheet("")
        self.probe_ridge_y.setText("")
        icon35 = QtGui.QIcon()
        icon35.addPixmap(QtGui.QPixmap(":/images/probe_y_ridge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_ridge_y.setIcon(icon35)
        self.probe_ridge_y.setIconSize(QtCore.QSize(150, 150))
        self.probe_ridge_y.setObjectName("probe_ridge_y")
        self.proberoutinebtnGroup.addButton(self.probe_ridge_y)
        self.gridLayout_9.addWidget(self.probe_ridge_y, 1, 1, 1, 1)
        self.frame_9 = QtWidgets.QFrame(self.widget_43)
        self.frame_9.setGeometry(QtCore.QRect(3, 392, 400, 65))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setMinimumSize(QtCore.QSize(400, 65))
        self.frame_9.setMaximumSize(QtCore.QSize(400, 65))
        self.frame_9.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: black;\n"
"    border-width: 2px;\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}")
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_143 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_143.setObjectName("horizontalLayout_143")
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setSpacing(0)
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.hint_label_2 = QtWidgets.QLabel(self.frame_9)
        self.hint_label_2.setMinimumSize(QtCore.QSize(115, 40))
        self.hint_label_2.setMaximumSize(QtCore.QSize(115, 40))
        self.hint_label_2.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(191, 191, 191);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.hint_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.hint_label_2.setObjectName("hint_label_2")
        self.horizontalLayout_28.addWidget(self.hint_label_2)
        self.label_74 = QtWidgets.QLabel(self.frame_9)
        self.label_74.setMinimumSize(QtCore.QSize(50, 0))
        self.label_74.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_74.setStyleSheet("QLabel{\n"
"    font: 15pt \"Bebas Kai\";\n"
"    color: rgb(255, 255, 255);\n"
"    padding-right: 1px;\n"
"    padding-left: 5px;\n"
"}")
        self.label_74.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_74.setIndent(0)
        self.label_74.setObjectName("label_74")
        self.horizontalLayout_28.addWidget(self.label_74)
        self.x_hint = VCPLineEdit(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_hint.sizePolicy().hasHeightForWidth())
        self.x_hint.setSizePolicy(sizePolicy)
        self.x_hint.setMinimumSize(QtCore.QSize(80, 40))
        self.x_hint.setMaximumSize(QtCore.QSize(80, 40))
        self.x_hint.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.x_hint.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_hint.setObjectName("x_hint")
        self.horizontalLayout_28.addWidget(self.x_hint)
        self.label_75 = QtWidgets.QLabel(self.frame_9)
        self.label_75.setMinimumSize(QtCore.QSize(50, 0))
        self.label_75.setMaximumSize(QtCore.QSize(50, 16777215))
        self.label_75.setStyleSheet("QLabel{\n"
"    font: 15pt \"Bebas Kai\";\n"
"    color: rgb(255, 255, 255);\n"
"    padding-right: 1px;\n"
"    padding-left: 5px;\n"
"}")
        self.label_75.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_75.setIndent(0)
        self.label_75.setObjectName("label_75")
        self.horizontalLayout_28.addWidget(self.label_75)
        self.y_hint = VCPLineEdit(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_hint.sizePolicy().hasHeightForWidth())
        self.y_hint.setSizePolicy(sizePolicy)
        self.y_hint.setMinimumSize(QtCore.QSize(80, 40))
        self.y_hint.setMaximumSize(QtCore.QSize(80, 40))
        self.y_hint.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.y_hint.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_hint.setObjectName("y_hint")
        self.horizontalLayout_28.addWidget(self.y_hint)
        self.horizontalLayout_143.addLayout(self.horizontalLayout_28)
        self.horizontalLayout_141.addWidget(self.widget_43)
        self.probe_tab_widget.addWidget(self.Page4)
        self.Page5 = QtWidgets.QWidget()
        self.Page5.setObjectName("Page5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.Page5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.widget_16 = QtWidgets.QWidget(self.Page5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_16.sizePolicy().hasHeightForWidth())
        self.widget_16.setSizePolicy(sizePolicy)
        self.widget_16.setObjectName("widget_16")
        self.verticalLayout_26 = QtWidgets.QVBoxLayout(self.widget_16)
        self.verticalLayout_26.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_26.setSpacing(9)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.widget_45 = QtWidgets.QWidget(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_45.sizePolicy().hasHeightForWidth())
        self.widget_45.setSizePolicy(sizePolicy)
        self.widget_45.setMinimumSize(QtCore.QSize(465, 465))
        self.widget_45.setMaximumSize(QtCore.QSize(465, 465))
        self.widget_45.setStyleSheet("")
        self.widget_45.setObjectName("widget_45")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget_45)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.probe_top_left_edge_angle = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_top_left_edge_angle.sizePolicy().hasHeightForWidth())
        self.probe_top_left_edge_angle.setSizePolicy(sizePolicy)
        self.probe_top_left_edge_angle.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_top_left_edge_angle.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_top_left_edge_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_top_left_edge_angle.setStyleSheet("")
        self.probe_top_left_edge_angle.setText("")
        icon36 = QtGui.QIcon()
        icon36.addPixmap(QtGui.QPixmap(":/images/probe_top_left_edge_angle_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_top_left_edge_angle.setIcon(icon36)
        self.probe_top_left_edge_angle.setIconSize(QtCore.QSize(130, 130))
        self.probe_top_left_edge_angle.setObjectName("probe_top_left_edge_angle")
        self.proberoutinebtnGroup.addButton(self.probe_top_left_edge_angle)
        self.gridLayout_8.addWidget(self.probe_top_left_edge_angle, 2, 0, 1, 1)
        self.probe_corner_y_plus_edge_angle = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_corner_y_plus_edge_angle.sizePolicy().hasHeightForWidth())
        self.probe_corner_y_plus_edge_angle.setSizePolicy(sizePolicy)
        self.probe_corner_y_plus_edge_angle.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_corner_y_plus_edge_angle.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_corner_y_plus_edge_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_corner_y_plus_edge_angle.setStyleSheet("")
        self.probe_corner_y_plus_edge_angle.setText("")
        icon37 = QtGui.QIcon()
        icon37.addPixmap(QtGui.QPixmap(":/images/probe_corner_y_plus_edge_angle_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_corner_y_plus_edge_angle.setIcon(icon37)
        self.probe_corner_y_plus_edge_angle.setIconSize(QtCore.QSize(130, 130))
        self.probe_corner_y_plus_edge_angle.setObjectName("probe_corner_y_plus_edge_angle")
        self.proberoutinebtnGroup.addButton(self.probe_corner_y_plus_edge_angle)
        self.gridLayout_8.addWidget(self.probe_corner_y_plus_edge_angle, 3, 0, 1, 1)
        self.probe_corner_x_plus_edge_angle = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_corner_x_plus_edge_angle.sizePolicy().hasHeightForWidth())
        self.probe_corner_x_plus_edge_angle.setSizePolicy(sizePolicy)
        self.probe_corner_x_plus_edge_angle.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_corner_x_plus_edge_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        icon38 = QtGui.QIcon()
        icon38.addPixmap(QtGui.QPixmap(":/images/probe_corner_x_plus_edge_angle_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_corner_x_plus_edge_angle.setIcon(icon38)
        self.probe_corner_x_plus_edge_angle.setIconSize(QtCore.QSize(130, 130))
        self.probe_corner_x_plus_edge_angle.setObjectName("probe_corner_x_plus_edge_angle")
        self.proberoutinebtnGroup.addButton(self.probe_corner_x_plus_edge_angle)
        self.gridLayout_8.addWidget(self.probe_corner_x_plus_edge_angle, 1, 0, 1, 1)
        self.probe_corner_y_minus_edge_angle = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_corner_y_minus_edge_angle.sizePolicy().hasHeightForWidth())
        self.probe_corner_y_minus_edge_angle.setSizePolicy(sizePolicy)
        self.probe_corner_y_minus_edge_angle.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_corner_y_minus_edge_angle.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_corner_y_minus_edge_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_corner_y_minus_edge_angle.setStyleSheet("")
        self.probe_corner_y_minus_edge_angle.setText("")
        icon39 = QtGui.QIcon()
        icon39.addPixmap(QtGui.QPixmap(":/images/probe_corner_y_minus_edge_angle_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_corner_y_minus_edge_angle.setIcon(icon39)
        self.probe_corner_y_minus_edge_angle.setIconSize(QtCore.QSize(130, 130))
        self.probe_corner_y_minus_edge_angle.setObjectName("probe_corner_y_minus_edge_angle")
        self.proberoutinebtnGroup.addButton(self.probe_corner_y_minus_edge_angle)
        self.gridLayout_8.addWidget(self.probe_corner_y_minus_edge_angle, 1, 2, 1, 1)
        self.probe_z_minus_edge = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_z_minus_edge.sizePolicy().hasHeightForWidth())
        self.probe_z_minus_edge.setSizePolicy(sizePolicy)
        self.probe_z_minus_edge.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_z_minus_edge.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_z_minus_edge.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_z_minus_edge.setStyleSheet("")
        self.probe_z_minus_edge.setText("")
        icon40 = QtGui.QIcon()
        icon40.addPixmap(QtGui.QPixmap(":/images/z_top_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_z_minus_edge.setIcon(icon40)
        self.probe_z_minus_edge.setIconSize(QtCore.QSize(130, 130))
        self.probe_z_minus_edge.setObjectName("probe_z_minus_edge")
        self.proberoutinebtnGroup.addButton(self.probe_z_minus_edge)
        self.gridLayout_8.addWidget(self.probe_z_minus_edge, 2, 1, 1, 1)
        self.probe_corner_x_minus_edge_angle = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_corner_x_minus_edge_angle.sizePolicy().hasHeightForWidth())
        self.probe_corner_x_minus_edge_angle.setSizePolicy(sizePolicy)
        self.probe_corner_x_minus_edge_angle.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_corner_x_minus_edge_angle.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_corner_x_minus_edge_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_corner_x_minus_edge_angle.setStyleSheet("")
        self.probe_corner_x_minus_edge_angle.setText("")
        icon41 = QtGui.QIcon()
        icon41.addPixmap(QtGui.QPixmap(":/images/probe_corner_x_minus_edge_angle_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_corner_x_minus_edge_angle.setIcon(icon41)
        self.probe_corner_x_minus_edge_angle.setIconSize(QtCore.QSize(130, 130))
        self.probe_corner_x_minus_edge_angle.setObjectName("probe_corner_x_minus_edge_angle")
        self.proberoutinebtnGroup.addButton(self.probe_corner_x_minus_edge_angle)
        self.gridLayout_8.addWidget(self.probe_corner_x_minus_edge_angle, 3, 2, 1, 1)
        self.probe_top_right_edge_angle = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_top_right_edge_angle.sizePolicy().hasHeightForWidth())
        self.probe_top_right_edge_angle.setSizePolicy(sizePolicy)
        self.probe_top_right_edge_angle.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_top_right_edge_angle.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_top_right_edge_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_top_right_edge_angle.setStyleSheet("")
        self.probe_top_right_edge_angle.setText("")
        icon42 = QtGui.QIcon()
        icon42.addPixmap(QtGui.QPixmap(":/images/probe_top_right_edge_angle_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_top_right_edge_angle.setIcon(icon42)
        self.probe_top_right_edge_angle.setIconSize(QtCore.QSize(130, 130))
        self.probe_top_right_edge_angle.setObjectName("probe_top_right_edge_angle")
        self.proberoutinebtnGroup.addButton(self.probe_top_right_edge_angle)
        self.gridLayout_8.addWidget(self.probe_top_right_edge_angle, 2, 2, 1, 1)
        self.probe_top_back_edge_angle = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_top_back_edge_angle.sizePolicy().hasHeightForWidth())
        self.probe_top_back_edge_angle.setSizePolicy(sizePolicy)
        self.probe_top_back_edge_angle.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_top_back_edge_angle.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_top_back_edge_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_top_back_edge_angle.setStyleSheet("")
        self.probe_top_back_edge_angle.setText("")
        icon43 = QtGui.QIcon()
        icon43.addPixmap(QtGui.QPixmap(":/images/probe_top_back_edge_angle_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_top_back_edge_angle.setIcon(icon43)
        self.probe_top_back_edge_angle.setIconSize(QtCore.QSize(130, 130))
        self.probe_top_back_edge_angle.setObjectName("probe_top_back_edge_angle")
        self.proberoutinebtnGroup.addButton(self.probe_top_back_edge_angle)
        self.gridLayout_8.addWidget(self.probe_top_back_edge_angle, 1, 1, 1, 1)
        self.probe_top_front_edge_angle = SubCallButton(self.widget_45)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_top_front_edge_angle.sizePolicy().hasHeightForWidth())
        self.probe_top_front_edge_angle.setSizePolicy(sizePolicy)
        self.probe_top_front_edge_angle.setMinimumSize(QtCore.QSize(140, 140))
        self.probe_top_front_edge_angle.setMaximumSize(QtCore.QSize(140, 140))
        self.probe_top_front_edge_angle.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_top_front_edge_angle.setStyleSheet("")
        self.probe_top_front_edge_angle.setText("")
        icon44 = QtGui.QIcon()
        icon44.addPixmap(QtGui.QPixmap(":/images/probe_top_front_edge_angle_r.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_top_front_edge_angle.setIcon(icon44)
        self.probe_top_front_edge_angle.setIconSize(QtCore.QSize(130, 130))
        self.probe_top_front_edge_angle.setObjectName("probe_top_front_edge_angle")
        self.proberoutinebtnGroup.addButton(self.probe_top_front_edge_angle)
        self.gridLayout_8.addWidget(self.probe_top_front_edge_angle, 3, 1, 1, 1)
        self.verticalLayout_26.addWidget(self.widget_45)
        self.widget_17 = QtWidgets.QWidget(self.widget_16)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_17.sizePolicy().hasHeightForWidth())
        self.widget_17.setSizePolicy(sizePolicy)
        self.widget_17.setMinimumSize(QtCore.QSize(0, 42))
        self.widget_17.setMaximumSize(QtCore.QSize(16777215, 42))
        self.widget_17.setObjectName("widget_17")
        self.horizontalLayout_54 = QtWidgets.QHBoxLayout(self.widget_17)
        self.horizontalLayout_54.setContentsMargins(0, 1, 0, 1)
        self.horizontalLayout_54.setSpacing(0)
        self.horizontalLayout_54.setObjectName("horizontalLayout_54")
        self.set_wco_offset_Btn = QtWidgets.QPushButton(self.widget_17)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.set_wco_offset_Btn.sizePolicy().hasHeightForWidth())
        self.set_wco_offset_Btn.setSizePolicy(sizePolicy)
        self.set_wco_offset_Btn.setMinimumSize(QtCore.QSize(400, 38))
        self.set_wco_offset_Btn.setMaximumSize(QtCore.QSize(16777215, 38))
        self.set_wco_offset_Btn.setFocusPolicy(QtCore.Qt.NoFocus)
        self.set_wco_offset_Btn.setStyleSheet("")
        self.set_wco_offset_Btn.setCheckable(True)
        self.set_wco_offset_Btn.setChecked(False)
        self.set_wco_offset_Btn.setAutoExclusive(True)
        self.set_wco_offset_Btn.setDefault(False)
        self.set_wco_offset_Btn.setObjectName("set_wco_offset_Btn")
        self.horizontalLayout_54.addWidget(self.set_wco_offset_Btn)
        self.verticalLayout_26.addWidget(self.widget_17)
        self.horizontalLayout_4.addWidget(self.widget_16)
        self.probe_tab_widget.addWidget(self.Page5)
        self.Page6 = QtWidgets.QWidget()
        self.Page6.setObjectName("Page6")
        self.probe_tab_widget.addWidget(self.Page6)
        self.Page7 = QtWidgets.QWidget()
        self.Page7.setObjectName("Page7")
        self.horizontalLayout_55 = QtWidgets.QHBoxLayout(self.Page7)
        self.horizontalLayout_55.setObjectName("horizontalLayout_55")
        self.frame_47 = QtWidgets.QFrame(self.Page7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_47.sizePolicy().hasHeightForWidth())
        self.frame_47.setSizePolicy(sizePolicy)
        self.frame_47.setMaximumSize(QtCore.QSize(520, 520))
        self.frame_47.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(206, 209, 202);\n"
"    background-color: rgb(57, 63, 65);\n"
"    border-radius: 8px;\n"
"}\n"
"")
        self.frame_47.setObjectName("frame_47")
        self.verticalLayout_46 = QtWidgets.QVBoxLayout(self.frame_47)
        self.verticalLayout_46.setContentsMargins(9, 12, 9, 18)
        self.verticalLayout_46.setSpacing(9)
        self.verticalLayout_46.setObjectName("verticalLayout_46")
        self.horizontalLayout_61 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_61.setContentsMargins(9, 3, 9, 3)
        self.horizontalLayout_61.setSpacing(6)
        self.horizontalLayout_61.setObjectName("horizontalLayout_61")
        self.label_93 = QtWidgets.QLabel(self.frame_47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_93.sizePolicy().hasHeightForWidth())
        self.label_93.setSizePolicy(sizePolicy)
        self.label_93.setMinimumSize(QtCore.QSize(210, 30))
        self.label_93.setMaximumSize(QtCore.QSize(210, 30))
        self.label_93.setBaseSize(QtCore.QSize(140, 30))
        self.label_93.setStyleSheet("QLabel{\n"
"font: 17pt \"Bebas Kai\";\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.label_93.setLineWidth(0)
        self.label_93.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_93.setIndent(0)
        self.label_93.setObjectName("label_93")
        self.horizontalLayout_61.addWidget(self.label_93)
        self.calibration_offset = VCPSettingsLineEdit(self.frame_47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calibration_offset.sizePolicy().hasHeightForWidth())
        self.calibration_offset.setSizePolicy(sizePolicy)
        self.calibration_offset.setMinimumSize(QtCore.QSize(100, 35))
        self.calibration_offset.setMaximumSize(QtCore.QSize(100, 35))
        self.calibration_offset.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.calibration_offset.setStyleSheet("")
        self.calibration_offset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.calibration_offset.setReadOnly(False)
        self.calibration_offset.setClearButtonEnabled(False)
        self.calibration_offset.setObjectName("calibration_offset")
        self.horizontalLayout_61.addWidget(self.calibration_offset)
        self.probe_cal_reset = SubCallButton(self.frame_47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_cal_reset.sizePolicy().hasHeightForWidth())
        self.probe_cal_reset.setSizePolicy(sizePolicy)
        self.probe_cal_reset.setMinimumSize(QtCore.QSize(150, 37))
        self.probe_cal_reset.setMaximumSize(QtCore.QSize(150, 37))
        self.probe_cal_reset.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_cal_reset.setStyleSheet("SubCallButton{\n"
"    border-radius: 5px;  \n"
"    font: 15pt \"Bebas Kai\";\n"
"      background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgb(81, 86, 85), stop:0.489795 rgb(99, 102, 102), stop:0.699799 rgb(85, 88, 94), stop:0.90444 rgb(77, 84, 86), stop:0.160246 rgb(83, 84, 91), stop:1 rgb(109, 115, 118));\n"
"}\n"
"\n"
".SubCallButton:disabled {\n"
"    border-color: black;\n"
"}\n"
"\n"
".SubCallButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
".SubCallButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.probe_cal_reset.setObjectName("probe_cal_reset")
        self.horizontalLayout_61.addWidget(self.probe_cal_reset)
        self.verticalLayout_46.addLayout(self.horizontalLayout_61)
        self.horizontalLayout_60 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_60.setContentsMargins(9, 3, -1, 3)
        self.horizontalLayout_60.setSpacing(21)
        self.horizontalLayout_60.setObjectName("horizontalLayout_60")
        self.probe_cal_round_pocket = SubCallButton(self.frame_47)
        self.probe_cal_round_pocket.setMinimumSize(QtCore.QSize(150, 150))
        self.probe_cal_round_pocket.setMaximumSize(QtCore.QSize(150, 150))
        self.probe_cal_round_pocket.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_cal_round_pocket.setStatusTip("")
        self.probe_cal_round_pocket.setStyleSheet("")
        self.probe_cal_round_pocket.setText("")
        icon45 = QtGui.QIcon()
        icon45.addPixmap(QtGui.QPixmap(":/images/probe_cal_round_pocket.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_cal_round_pocket.setIcon(icon45)
        self.probe_cal_round_pocket.setIconSize(QtCore.QSize(135, 135))
        self.probe_cal_round_pocket.setObjectName("probe_cal_round_pocket")
        self.proberoutinebtnGroup.addButton(self.probe_cal_round_pocket)
        self.horizontalLayout_60.addWidget(self.probe_cal_round_pocket)
        self.probe_cal_round_boss = SubCallButton(self.frame_47)
        self.probe_cal_round_boss.setMinimumSize(QtCore.QSize(150, 150))
        self.probe_cal_round_boss.setMaximumSize(QtCore.QSize(150, 150))
        self.probe_cal_round_boss.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_cal_round_boss.setStatusTip("")
        self.probe_cal_round_boss.setStyleSheet("")
        self.probe_cal_round_boss.setText("")
        icon46 = QtGui.QIcon()
        icon46.addPixmap(QtGui.QPixmap(":/images/probe_cal_round_boss.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_cal_round_boss.setIcon(icon46)
        self.probe_cal_round_boss.setIconSize(QtCore.QSize(140, 140))
        self.probe_cal_round_boss.setAutoDefault(False)
        self.probe_cal_round_boss.setObjectName("probe_cal_round_boss")
        self.proberoutinebtnGroup.addButton(self.probe_cal_round_boss)
        self.horizontalLayout_60.addWidget(self.probe_cal_round_boss)
        self.widget_211 = QtWidgets.QWidget(self.frame_47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_211.sizePolicy().hasHeightForWidth())
        self.widget_211.setSizePolicy(sizePolicy)
        self.widget_211.setMinimumSize(QtCore.QSize(130, 150))
        self.widget_211.setMaximumSize(QtCore.QSize(130, 150))
        self.widget_211.setSizeIncrement(QtCore.QSize(0, 0))
        self.widget_211.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.widget_211.setObjectName("widget_211")
        self.formLayout_2 = QtWidgets.QFormLayout(self.widget_211)
        self.formLayout_2.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout_2.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setContentsMargins(1, 0, 1, 9)
        self.formLayout_2.setHorizontalSpacing(0)
        self.formLayout_2.setVerticalSpacing(15)
        self.formLayout_2.setObjectName("formLayout_2")
        self.hint_label_4 = QtWidgets.QLabel(self.widget_211)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hint_label_4.sizePolicy().hasHeightForWidth())
        self.hint_label_4.setSizePolicy(sizePolicy)
        self.hint_label_4.setMinimumSize(QtCore.QSize(130, 58))
        self.hint_label_4.setMaximumSize(QtCore.QSize(130, 58))
        self.hint_label_4.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.hint_label_4.setTextFormat(QtCore.Qt.RichText)
        self.hint_label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.hint_label_4.setWordWrap(True)
        self.hint_label_4.setObjectName("hint_label_4")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.hint_label_4)
        self.cal_diameter = VCPLineEdit(self.widget_211)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cal_diameter.sizePolicy().hasHeightForWidth())
        self.cal_diameter.setSizePolicy(sizePolicy)
        self.cal_diameter.setMinimumSize(QtCore.QSize(130, 35))
        self.cal_diameter.setMaximumSize(QtCore.QSize(130, 35))
        self.cal_diameter.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.cal_diameter.setStyleSheet("margin-right: 14px;\n"
"margin-left: 14px;")
        self.cal_diameter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.cal_diameter.setObjectName("cal_diameter")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cal_diameter)
        self.horizontalLayout_60.addWidget(self.widget_211)
        self.verticalLayout_46.addLayout(self.horizontalLayout_60)
        self.horizontalLayout_56 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_56.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_56.setSpacing(9)
        self.horizontalLayout_56.setObjectName("horizontalLayout_56")
        self.cal_avg_error = QtWidgets.QPushButton(self.frame_47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cal_avg_error.sizePolicy().hasHeightForWidth())
        self.cal_avg_error.setSizePolicy(sizePolicy)
        self.cal_avg_error.setMinimumSize(QtCore.QSize(165, 37))
        self.cal_avg_error.setMaximumSize(QtCore.QSize(165, 37))
        self.cal_avg_error.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cal_avg_error.setStyleSheet("")
        self.cal_avg_error.setCheckable(True)
        self.cal_avg_error.setChecked(True)
        self.cal_avg_error.setAutoExclusive(True)
        self.cal_avg_error.setObjectName("cal_avg_error")
        self.xycalbtnGroup = QtWidgets.QButtonGroup(Form)
        self.xycalbtnGroup.setObjectName("xycalbtnGroup")
        self.xycalbtnGroup.addButton(self.cal_avg_error)
        self.horizontalLayout_56.addWidget(self.cal_avg_error)
        self.cal_x_error = QtWidgets.QPushButton(self.frame_47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cal_x_error.sizePolicy().hasHeightForWidth())
        self.cal_x_error.setSizePolicy(sizePolicy)
        self.cal_x_error.setMinimumSize(QtCore.QSize(140, 37))
        self.cal_x_error.setMaximumSize(QtCore.QSize(140, 37))
        self.cal_x_error.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cal_x_error.setCheckable(True)
        self.cal_x_error.setChecked(False)
        self.cal_x_error.setAutoExclusive(True)
        self.cal_x_error.setObjectName("cal_x_error")
        self.xycalbtnGroup.addButton(self.cal_x_error)
        self.horizontalLayout_56.addWidget(self.cal_x_error)
        self.cal_y_error = QtWidgets.QPushButton(self.frame_47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cal_y_error.sizePolicy().hasHeightForWidth())
        self.cal_y_error.setSizePolicy(sizePolicy)
        self.cal_y_error.setMinimumSize(QtCore.QSize(140, 37))
        self.cal_y_error.setMaximumSize(QtCore.QSize(140, 37))
        self.cal_y_error.setFocusPolicy(QtCore.Qt.NoFocus)
        self.cal_y_error.setStyleSheet("")
        self.cal_y_error.setCheckable(True)
        self.cal_y_error.setAutoExclusive(True)
        self.cal_y_error.setObjectName("cal_y_error")
        self.xycalbtnGroup.addButton(self.cal_y_error)
        self.horizontalLayout_56.addWidget(self.cal_y_error)
        self.verticalLayout_46.addLayout(self.horizontalLayout_56)
        self.horizontalLayout_62 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_62.setContentsMargins(9, 3, -1, 6)
        self.horizontalLayout_62.setSpacing(21)
        self.horizontalLayout_62.setObjectName("horizontalLayout_62")
        self.probe_cal_square_pocket = SubCallButton(self.frame_47)
        self.probe_cal_square_pocket.setMinimumSize(QtCore.QSize(150, 150))
        self.probe_cal_square_pocket.setMaximumSize(QtCore.QSize(150, 150))
        self.probe_cal_square_pocket.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_cal_square_pocket.setStatusTip("")
        self.probe_cal_square_pocket.setStyleSheet("")
        self.probe_cal_square_pocket.setText("")
        icon47 = QtGui.QIcon()
        icon47.addPixmap(QtGui.QPixmap(":/images/probe_cal_square_pocket.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_cal_square_pocket.setIcon(icon47)
        self.probe_cal_square_pocket.setIconSize(QtCore.QSize(135, 135))
        self.probe_cal_square_pocket.setObjectName("probe_cal_square_pocket")
        self.proberoutinebtnGroup.addButton(self.probe_cal_square_pocket)
        self.horizontalLayout_62.addWidget(self.probe_cal_square_pocket)
        self.probe_cal_square_boss = SubCallButton(self.frame_47)
        self.probe_cal_square_boss.setMinimumSize(QtCore.QSize(150, 150))
        self.probe_cal_square_boss.setMaximumSize(QtCore.QSize(150, 150))
        self.probe_cal_square_boss.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_cal_square_boss.setStatusTip("")
        self.probe_cal_square_boss.setStyleSheet("")
        self.probe_cal_square_boss.setText("")
        icon48 = QtGui.QIcon()
        icon48.addPixmap(QtGui.QPixmap(":/images/probe_cal_square_boss.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.probe_cal_square_boss.setIcon(icon48)
        self.probe_cal_square_boss.setIconSize(QtCore.QSize(140, 140))
        self.probe_cal_square_boss.setObjectName("probe_cal_square_boss")
        self.proberoutinebtnGroup.addButton(self.probe_cal_square_boss)
        self.horizontalLayout_62.addWidget(self.probe_cal_square_boss)
        self.widget_18 = QtWidgets.QWidget(self.frame_47)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_18.sizePolicy().hasHeightForWidth())
        self.widget_18.setSizePolicy(sizePolicy)
        self.widget_18.setMinimumSize(QtCore.QSize(130, 150))
        self.widget_18.setMaximumSize(QtCore.QSize(130, 150))
        self.widget_18.setObjectName("widget_18")
        self.formLayout = QtWidgets.QFormLayout(self.widget_18)
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignCenter)
        self.formLayout.setContentsMargins(1, 0, 1, 9)
        self.formLayout.setVerticalSpacing(15)
        self.formLayout.setObjectName("formLayout")
        self.hint_label_3 = QtWidgets.QLabel(self.widget_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hint_label_3.sizePolicy().hasHeightForWidth())
        self.hint_label_3.setSizePolicy(sizePolicy)
        self.hint_label_3.setMinimumSize(QtCore.QSize(120, 23))
        self.hint_label_3.setMaximumSize(QtCore.QSize(130, 0))
        self.hint_label_3.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.hint_label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.hint_label_3.setObjectName("hint_label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.hint_label_3)
        self.label_103 = QtWidgets.QLabel(self.widget_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_103.sizePolicy().hasHeightForWidth())
        self.label_103.setSizePolicy(sizePolicy)
        self.label_103.setMinimumSize(QtCore.QSize(23, 31))
        self.label_103.setMaximumSize(QtCore.QSize(23, 31))
        self.label_103.setStyleSheet("QLabel{\n"
"font: 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_103.setLineWidth(0)
        self.label_103.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_103.setIndent(0)
        self.label_103.setObjectName("label_103")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_103)
        self.label_107 = QtWidgets.QLabel(self.widget_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_107.sizePolicy().hasHeightForWidth())
        self.label_107.setSizePolicy(sizePolicy)
        self.label_107.setMinimumSize(QtCore.QSize(23, 31))
        self.label_107.setMaximumSize(QtCore.QSize(23, 31))
        self.label_107.setStyleSheet("QLabel{\n"
"font: 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_107.setLineWidth(0)
        self.label_107.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_107.setIndent(0)
        self.label_107.setObjectName("label_107")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_107)
        self.x_cal_width = VCPLineEdit(self.widget_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_cal_width.sizePolicy().hasHeightForWidth())
        self.x_cal_width.setSizePolicy(sizePolicy)
        self.x_cal_width.setMinimumSize(QtCore.QSize(87, 35))
        self.x_cal_width.setMaximumSize(QtCore.QSize(87, 35))
        self.x_cal_width.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.x_cal_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.x_cal_width.setObjectName("x_cal_width")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.x_cal_width)
        self.y_cal_width = VCPLineEdit(self.widget_18)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_cal_width.sizePolicy().hasHeightForWidth())
        self.y_cal_width.setSizePolicy(sizePolicy)
        self.y_cal_width.setMinimumSize(QtCore.QSize(87, 35))
        self.y_cal_width.setMaximumSize(QtCore.QSize(87, 35))
        self.y_cal_width.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.y_cal_width.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.y_cal_width.setObjectName("y_cal_width")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.y_cal_width)
        self.horizontalLayout_62.addWidget(self.widget_18)
        self.verticalLayout_46.addLayout(self.horizontalLayout_62)
        self.horizontalLayout_55.addWidget(self.frame_47)
        self.probe_tab_widget.addWidget(self.Page7)
        self.Page8 = QtWidgets.QWidget()
        self.Page8.setObjectName("Page8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.Page8)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame = QtWidgets.QFrame(self.Page8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(520, 480))
        self.frame.setMaximumSize(QtCore.QSize(520, 480))
        self.frame.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(206, 209, 202);\n"
"    background-color: rgb(51, 57, 59);\n"
"    border-radius: 8px;\n"
"}")
        self.frame.setObjectName("frame")
        self.verticalLayout_21 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_21.setContentsMargins(3, 6, 3, 12)
        self.verticalLayout_21.setSpacing(6)
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.probe_help_widget = QtWidgets.QStackedWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_help_widget.sizePolicy().hasHeightForWidth())
        self.probe_help_widget.setSizePolicy(sizePolicy)
        self.probe_help_widget.setMinimumSize(QtCore.QSize(0, 410))
        self.probe_help_widget.setMaximumSize(QtCore.QSize(16777215, 410))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(13)
        self.probe_help_widget.setFont(font)
        self.probe_help_widget.setStyleSheet("QStackedWidget{\n"
"border: none;\n"
"background: transparent;\n"
"}")
        self.probe_help_widget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.probe_help_widget.setLineWidth(0)
        self.probe_help_widget.setObjectName("probe_help_widget")
        self.stackedWidget_4Page1 = QtWidgets.QWidget()
        self.stackedWidget_4Page1.setObjectName("stackedWidget_4Page1")
        self.horizontalLayout_146 = QtWidgets.QHBoxLayout(self.stackedWidget_4Page1)
        self.horizontalLayout_146.setObjectName("horizontalLayout_146")
        self.label_77 = QtWidgets.QLabel(self.stackedWidget_4Page1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_77.sizePolicy().hasHeightForWidth())
        self.label_77.setSizePolicy(sizePolicy)
        self.label_77.setMinimumSize(QtCore.QSize(450, 400))
        self.label_77.setMaximumSize(QtCore.QSize(450, 400))
        self.label_77.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(46, 54, 56);\n"
"    border-width: 3px;\n"
"    border-radius: 10px;\n"
"    background: rgb(245, 240, 255);\n"
"    image: url(:/images/step_off_width.png);\n"
"}")
        self.label_77.setText("")
        self.label_77.setScaledContents(True)
        self.label_77.setIndent(0)
        self.label_77.setObjectName("label_77")
        self.horizontalLayout_146.addWidget(self.label_77)
        self.probe_help_widget.addWidget(self.stackedWidget_4Page1)
        self.stackedWidget_4Page2 = QtWidgets.QWidget()
        self.stackedWidget_4Page2.setObjectName("stackedWidget_4Page2")
        self.horizontalLayout_148 = QtWidgets.QHBoxLayout(self.stackedWidget_4Page2)
        self.horizontalLayout_148.setObjectName("horizontalLayout_148")
        self.label_78 = QtWidgets.QLabel(self.stackedWidget_4Page2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_78.sizePolicy().hasHeightForWidth())
        self.label_78.setSizePolicy(sizePolicy)
        self.label_78.setMinimumSize(QtCore.QSize(500, 400))
        self.label_78.setMaximumSize(QtCore.QSize(500, 400))
        self.label_78.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(46, 54, 56);\n"
"    border-width: 3px;\n"
"    border-radius: 10px;\n"
"    background: rgb(245, 240, 255);\n"
"    image: url(:/images/extra_probe_depth.png);\n"
"}")
        self.label_78.setText("")
        self.label_78.setScaledContents(True)
        self.label_78.setAlignment(QtCore.Qt.AlignCenter)
        self.label_78.setWordWrap(True)
        self.label_78.setIndent(0)
        self.label_78.setObjectName("label_78")
        self.horizontalLayout_148.addWidget(self.label_78)
        self.probe_help_widget.addWidget(self.stackedWidget_4Page2)
        self.stackedWidget_4Page3 = QtWidgets.QWidget()
        self.stackedWidget_4Page3.setObjectName("stackedWidget_4Page3")
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout(self.stackedWidget_4Page3)
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.label_79 = QtWidgets.QLabel(self.stackedWidget_4Page3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_79.sizePolicy().hasHeightForWidth())
        self.label_79.setSizePolicy(sizePolicy)
        self.label_79.setMinimumSize(QtCore.QSize(440, 400))
        self.label_79.setMaximumSize(QtCore.QSize(440, 400))
        self.label_79.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(46, 54, 56);\n"
"    border-width: 3px;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    background: rgb(245, 240, 255);\n"
"    image: url(:/images/max_z_distance.png);\n"
"}")
        self.label_79.setText("")
        self.label_79.setScaledContents(True)
        self.label_79.setAlignment(QtCore.Qt.AlignCenter)
        self.label_79.setWordWrap(True)
        self.label_79.setIndent(0)
        self.label_79.setObjectName("label_79")
        self.horizontalLayout_39.addWidget(self.label_79)
        self.probe_help_widget.addWidget(self.stackedWidget_4Page3)
        self.stackedWidget_4Page4 = QtWidgets.QWidget()
        self.stackedWidget_4Page4.setObjectName("stackedWidget_4Page4")
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout(self.stackedWidget_4Page4)
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.label_105 = QtWidgets.QLabel(self.stackedWidget_4Page4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_105.sizePolicy().hasHeightForWidth())
        self.label_105.setSizePolicy(sizePolicy)
        self.label_105.setMinimumSize(QtCore.QSize(470, 400))
        self.label_105.setMaximumSize(QtCore.QSize(470, 400))
        self.label_105.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(46, 54, 56);\n"
"    border-width: 3px;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    background: rgb(245, 240, 255);\n"
"    image: url(:/images/max_xy_distance.png);\n"
"}")
        self.label_105.setText("")
        self.label_105.setScaledContents(True)
        self.label_105.setAlignment(QtCore.Qt.AlignCenter)
        self.label_105.setWordWrap(True)
        self.label_105.setIndent(0)
        self.label_105.setObjectName("label_105")
        self.horizontalLayout_34.addWidget(self.label_105)
        self.probe_help_widget.addWidget(self.stackedWidget_4Page4)
        self.stackedWidget_4Page5 = QtWidgets.QWidget()
        self.stackedWidget_4Page5.setObjectName("stackedWidget_4Page5")
        self.horizontalLayout_42 = QtWidgets.QHBoxLayout(self.stackedWidget_4Page5)
        self.horizontalLayout_42.setObjectName("horizontalLayout_42")
        self.label_80 = QtWidgets.QLabel(self.stackedWidget_4Page5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_80.sizePolicy().hasHeightForWidth())
        self.label_80.setSizePolicy(sizePolicy)
        self.label_80.setMinimumSize(QtCore.QSize(450, 400))
        self.label_80.setMaximumSize(QtCore.QSize(450, 400))
        self.label_80.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(46, 54, 56);\n"
"    border-width: 3px;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    background: rgb(245, 240, 255);\n"
"    image: url(:/images/z_clearance.png);\n"
"}")
        self.label_80.setText("")
        self.label_80.setScaledContents(True)
        self.label_80.setAlignment(QtCore.Qt.AlignCenter)
        self.label_80.setWordWrap(True)
        self.label_80.setIndent(0)
        self.label_80.setObjectName("label_80")
        self.horizontalLayout_42.addWidget(self.label_80)
        self.probe_help_widget.addWidget(self.stackedWidget_4Page5)
        self.stackedWidget_4Page6 = QtWidgets.QWidget()
        self.stackedWidget_4Page6.setObjectName("stackedWidget_4Page6")
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout(self.stackedWidget_4Page6)
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.label_106 = QtWidgets.QLabel(self.stackedWidget_4Page6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_106.sizePolicy().hasHeightForWidth())
        self.label_106.setSizePolicy(sizePolicy)
        self.label_106.setMinimumSize(QtCore.QSize(480, 400))
        self.label_106.setMaximumSize(QtCore.QSize(480, 400))
        self.label_106.setStyleSheet("QLabel{\n"
"    border-style: solid;\n"
"    border-color: rgb(46, 54, 56);\n"
"    border-width: 3px;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    background: rgb(245, 240, 255);\n"
"    image: url(:/images/xy_clearance.png);\n"
"}")
        self.label_106.setText("")
        self.label_106.setScaledContents(True)
        self.label_106.setAlignment(QtCore.Qt.AlignCenter)
        self.label_106.setWordWrap(True)
        self.label_106.setIndent(0)
        self.label_106.setObjectName("label_106")
        self.horizontalLayout_35.addWidget(self.label_106)
        self.probe_help_widget.addWidget(self.stackedWidget_4Page6)
        self.stackedWidget_4Page7 = QtWidgets.QWidget()
        self.stackedWidget_4Page7.setObjectName("stackedWidget_4Page7")
        self.probe_help_widget.addWidget(self.stackedWidget_4Page7)
        self.stackedWidget_4Page8 = QtWidgets.QWidget()
        self.stackedWidget_4Page8.setObjectName("stackedWidget_4Page8")
        self.probe_help_widget.addWidget(self.stackedWidget_4Page8)
        self.verticalLayout_21.addWidget(self.probe_help_widget, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.probe_help_Group_select = QtWidgets.QWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_help_Group_select.sizePolicy().hasHeightForWidth())
        self.probe_help_Group_select.setSizePolicy(sizePolicy)
        self.probe_help_Group_select.setMinimumSize(QtCore.QSize(0, 40))
        self.probe_help_Group_select.setMaximumSize(QtCore.QSize(16777215, 40))
        self.probe_help_Group_select.setStyleSheet("")
        self.probe_help_Group_select.setObjectName("probe_help_Group_select")
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout(self.probe_help_Group_select)
        self.horizontalLayout_44.setContentsMargins(70, 1, 70, 1)
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        self.probe_help_prev = QtWidgets.QPushButton(self.probe_help_Group_select)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_help_prev.sizePolicy().hasHeightForWidth())
        self.probe_help_prev.setSizePolicy(sizePolicy)
        self.probe_help_prev.setMinimumSize(QtCore.QSize(150, 37))
        self.probe_help_prev.setMaximumSize(QtCore.QSize(150, 37))
        self.probe_help_prev.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_help_prev.setStyleSheet("QPushButton{\n"
"    padding-left: 0px;\n"
"    padding-right: 0px;\n"
"    font: 13pt \"Bebas Kai\";\n"
"}")
        self.probe_help_prev.setIcon(icon9)
        self.probe_help_prev.setIconSize(QtCore.QSize(16, 16))
        self.probe_help_prev.setCheckable(False)
        self.probe_help_prev.setChecked(False)
        self.probe_help_prev.setAutoExclusive(True)
        self.probe_help_prev.setObjectName("probe_help_prev")
        self.probehelpGroup = QtWidgets.QButtonGroup(Form)
        self.probehelpGroup.setObjectName("probehelpGroup")
        self.probehelpGroup.addButton(self.probe_help_prev)
        self.horizontalLayout_44.addWidget(self.probe_help_prev)
        self.probe_help_next = QtWidgets.QPushButton(self.probe_help_Group_select)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_help_next.sizePolicy().hasHeightForWidth())
        self.probe_help_next.setSizePolicy(sizePolicy)
        self.probe_help_next.setMinimumSize(QtCore.QSize(150, 37))
        self.probe_help_next.setMaximumSize(QtCore.QSize(150, 37))
        self.probe_help_next.setFocusPolicy(QtCore.Qt.NoFocus)
        self.probe_help_next.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.probe_help_next.setStyleSheet("QPushButton{\n"
"    padding-left: 0px;\n"
"    padding-right: 0px;\n"
"    font: 13pt \"Bebas Kai\";\n"
"}")
        self.probe_help_next.setIcon(icon10)
        self.probe_help_next.setIconSize(QtCore.QSize(16, 16))
        self.probe_help_next.setCheckable(False)
        self.probe_help_next.setAutoExclusive(True)
        self.probe_help_next.setObjectName("probe_help_next")
        self.probehelpGroup.addButton(self.probe_help_next)
        self.horizontalLayout_44.addWidget(self.probe_help_next)
        self.verticalLayout_21.addWidget(self.probe_help_Group_select)
        self.horizontalLayout_5.addWidget(self.frame)
        self.probe_tab_widget.addWidget(self.Page8)
        self.verticalLayout_3.addWidget(self.probe_tab_widget)
        self.horizontalLayout_31.addLayout(self.verticalLayout_3)
        self.verticalLayout_44 = QtWidgets.QVBoxLayout()
        self.verticalLayout_44.setContentsMargins(0, 27, 9, 37)
        self.verticalLayout_44.setSpacing(0)
        self.verticalLayout_44.setObjectName("verticalLayout_44")
        self.frame1 = QtWidgets.QFrame(self.widget_11)
        self.frame1.setStyleSheet(".QFrame{\n"
"background-color: rgb(32, 36, 37);\n"
"border-radius: 8px;\n"
"}")
        self.frame1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame1.setObjectName("frame1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame1)
        self.horizontalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.vtk_probe = VTKBackPlot(self.frame1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vtk_probe.sizePolicy().hasHeightForWidth())
        self.vtk_probe.setSizePolicy(sizePolicy)
        self.vtk_probe.setFocusPolicy(QtCore.Qt.NoFocus)
        self.vtk_probe.setStyleSheet("VTKBackPlot {\n"
"    border: solid;\n"
"    border-color: white;\n"
"    border-width: 2px;\n"
"    border-radius: 8px;\n"
"}")
        self.vtk_probe.setProperty("backgroundColor", QtGui.QColor(32, 36, 37))
        self.vtk_probe.setObjectName("vtk_probe")
        self.horizontalLayout_3.addWidget(self.vtk_probe)
        self.verticalLayout_44.addWidget(self.frame1)
        self.horizontalLayout_31.addLayout(self.verticalLayout_44)
        self.verticalLayout_45.addWidget(self.widget_11)
        self.horizontalLayout_43.addWidget(self.widget_13)
        self.tabWidget.addTab(self.probe_tab, "")
        self.conversational_tab = QtWidgets.QWidget()
        self.conversational_tab.setObjectName("conversational_tab")
        self.horizontalLayout_131 = QtWidgets.QHBoxLayout(self.conversational_tab)
        self.horizontalLayout_131.setObjectName("horizontalLayout_131")
        self.operation = QtWidgets.QTabWidget(self.conversational_tab)
        self.operation.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.operation.setStyleSheet("QTabWidget QTabBar::tab{\n"
"    margin-top: 0px;\n"
"    margin-right: 0px;\n"
"    margin-bottom:0px;\n"
"    min-width: 35px;\n"
"    min-height: 100px;\n"
"    font: 15pt \"bebas kai\";\n"
"}\n"
"\n"
"QTabBar::tab:first {\n"
"    margin-top: 45px;\n"
"    border-left-width: 2px;\n"
"    border-bottom-width: 1px;\n"
"    border-right-width: 2px;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:last {\n"
"    border-left-width: 2px;\n"
"    border-top-width: 1px;\n"
"    border-right-width: 2px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    border-width: 2px;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"\n"
"")
        self.operation.setTabPosition(QtWidgets.QTabWidget.West)
        self.operation.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.operation.setObjectName("operation")
        self.holeop_tab = QtWidgets.QWidget()
        self.holeop_tab.setObjectName("holeop_tab")
        self.horizontalLayout_151 = QtWidgets.QHBoxLayout(self.holeop_tab)
        self.horizontalLayout_151.setObjectName("horizontalLayout_151")
        self.tabWidget_3 = QtWidgets.QTabWidget(self.holeop_tab)
        self.tabWidget_3.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_3.setStyleSheet("QTabWidget QTabBar::tab {\n"
"    margin-top: 5px;\n"
"    margin-right: 0px;\n"
"    min-width: 130px;\n"
"    min-height: 23px;\n"
"    font: 14pt \"bebas kai\";\n"
"}\n"
"\n"
"QTabBar::tab:first {\n"
"    margin-left: 300px;\n"
"    border-left-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-bottom-width: 2px;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:last {\n"
"    border-left-width: 1px;\n"
"    border-right-width: 2px;\n"
"    border-top-width: 2px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 4px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    border-width: 2px;\n"
"    border-radius: 4px;\n"
"}")
        self.tabWidget_3.setObjectName("tabWidget_3")
        self.spot_drill_tab = QtWidgets.QWidget()
        self.spot_drill_tab.setObjectName("spot_drill_tab")
        self.tabWidget_3.addTab(self.spot_drill_tab, "")
        self.drill_tab = QtWidgets.QWidget()
        self.drill_tab.setObjectName("drill_tab")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.drill_tab)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.widget_31 = QtWidgets.QWidget(self.drill_tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_31.sizePolicy().hasHeightForWidth())
        self.widget_31.setSizePolicy(sizePolicy)
        self.widget_31.setMinimumSize(QtCore.QSize(640, 410))
        self.widget_31.setObjectName("widget_31")
        self.label_41 = QtWidgets.QLabel(self.widget_31)
        self.label_41.setGeometry(QtCore.QRect(20, 8, 600, 401))
        self.label_41.setStyleSheet("QLabel{\n"
"    border: none;\n"
"    background: transparent;\n"
"}")
        self.label_41.setText("")
        self.label_41.setPixmap(QtGui.QPixmap(":/images/drill_dims_white.png"))
        self.label_41.setScaledContents(True)
        self.label_41.setObjectName("label_41")
        self.label_45 = QtWidgets.QLabel(self.widget_31)
        self.label_45.setGeometry(QtCore.QRect(291, 266, 60, 37))
        self.label_45.setMinimumSize(QtCore.QSize(60, 37))
        self.label_45.setMaximumSize(QtCore.QSize(60, 37))
        self.label_45.setStyleSheet("QLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_45.setText("")
        self.label_45.setAlignment(QtCore.Qt.AlignCenter)
        self.label_45.setObjectName("label_45")
        self.label_61 = QtWidgets.QLabel(self.widget_31)
        self.label_61.setGeometry(QtCore.QRect(290, 220, 61, 41))
        self.label_61.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.label_61.setAlignment(QtCore.Qt.AlignCenter)
        self.label_61.setWordWrap(True)
        self.label_61.setObjectName("label_61")
        self.label_60 = QtWidgets.QLabel(self.widget_31)
        self.label_60.setGeometry(QtCore.QRect(279, 28, 81, 41))
        self.label_60.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.label_60.setAlignment(QtCore.Qt.AlignCenter)
        self.label_60.setWordWrap(True)
        self.label_60.setObjectName("label_60")
        self.label_46 = QtWidgets.QLabel(self.widget_31)
        self.label_46.setGeometry(QtCore.QRect(474, 159, 100, 37))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_46.sizePolicy().hasHeightForWidth())
        self.label_46.setSizePolicy(sizePolicy)
        self.label_46.setMinimumSize(QtCore.QSize(100, 37))
        self.label_46.setMaximumSize(QtCore.QSize(100, 37))
        self.label_46.setStyleSheet("QLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_46.setText("")
        self.label_46.setAlignment(QtCore.Qt.AlignCenter)
        self.label_46.setObjectName("label_46")
        self.label_44 = QtWidgets.QLabel(self.widget_31)
        self.label_44.setGeometry(QtCore.QRect(269, 75, 100, 37))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_44.sizePolicy().hasHeightForWidth())
        self.label_44.setSizePolicy(sizePolicy)
        self.label_44.setMinimumSize(QtCore.QSize(100, 37))
        self.label_44.setMaximumSize(QtCore.QSize(100, 37))
        self.label_44.setStyleSheet("QLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_44.setText("")
        self.label_44.setAlignment(QtCore.Qt.AlignCenter)
        self.label_44.setObjectName("label_44")
        self.label_59 = QtWidgets.QLabel(self.widget_31)
        self.label_59.setGeometry(QtCore.QRect(473, 129, 101, 21))
        self.label_59.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.label_59.setAlignment(QtCore.Qt.AlignCenter)
        self.label_59.setObjectName("label_59")
        self.label_53 = QtWidgets.QLabel(self.widget_31)
        self.label_53.setGeometry(QtCore.QRect(66, 152, 101, 21))
        self.label_53.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.label_53.setAlignment(QtCore.Qt.AlignCenter)
        self.label_53.setObjectName("label_53")
        self.label_42 = QtWidgets.QLabel(self.widget_31)
        self.label_42.setGeometry(QtCore.QRect(66, 183, 100, 37))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_42.sizePolicy().hasHeightForWidth())
        self.label_42.setSizePolicy(sizePolicy)
        self.label_42.setMinimumSize(QtCore.QSize(100, 37))
        self.label_42.setMaximumSize(QtCore.QSize(100, 37))
        self.label_42.setStyleSheet("QLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_42.setText("")
        self.label_42.setAlignment(QtCore.Qt.AlignCenter)
        self.label_42.setObjectName("label_42")
        self.horizontalLayout_12.addWidget(self.widget_31)
        self.tabWidget_3.addTab(self.drill_tab, "")
        self.ream_tab = QtWidgets.QWidget()
        self.ream_tab.setObjectName("ream_tab")
        self.tabWidget_3.addTab(self.ream_tab, "")
        self.chamfer_tab = QtWidgets.QWidget()
        self.chamfer_tab.setObjectName("chamfer_tab")
        self.tabWidget_3.addTab(self.chamfer_tab, "")
        self.rigid_tap_tab = QtWidgets.QWidget()
        self.rigid_tap_tab.setObjectName("rigid_tap_tab")
        self.tabWidget_3.addTab(self.rigid_tap_tab, "")
        self.threadmill_tab = QtWidgets.QWidget()
        self.threadmill_tab.setObjectName("threadmill_tab")
        self.tabWidget_3.addTab(self.threadmill_tab, "")
        self.XY_tab = QtWidgets.QWidget()
        self.XY_tab.setObjectName("XY_tab")
        self.tabWidget_3.addTab(self.XY_tab, "")
        self.gcode_tab = QtWidgets.QWidget()
        self.gcode_tab.setObjectName("gcode_tab")
        self.tabWidget_3.addTab(self.gcode_tab, "")
        self.horizontalLayout_151.addWidget(self.tabWidget_3)
        self.operation.addTab(self.holeop_tab, "")
        self.facing_tab = QtWidgets.QWidget()
        self.facing_tab.setObjectName("facing_tab")
        self.horizontalLayout_49 = QtWidgets.QHBoxLayout(self.facing_tab)
        self.horizontalLayout_49.setObjectName("horizontalLayout_49")
        self.tabWidget_10 = QtWidgets.QTabWidget(self.facing_tab)
        self.tabWidget_10.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget_10.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_10.setStyleSheet("QTabWidget QTabBar::tab {\n"
"    margin-top: 5px;\n"
"    margin-right: 0px;\n"
"    min-width: 130px;\n"
"    min-height: 23px;\n"
"    font: 14pt \"bebas kai\";\n"
"}\n"
"\n"
"QTabBar::tab:first {\n"
"    margin-left: 300px;\n"
"    border-left-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-bottom-width: 2px;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:last {\n"
"    border-left-width: 1px;\n"
"    border-right-width: 2px;\n"
"    border-top-width: 2px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 4px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    border-width: 2px;\n"
"    border-radius: 4px;\n"
"}")
        self.tabWidget_10.setObjectName("tabWidget_10")
        self.widget_36 = QtWidgets.QWidget()
        self.widget_36.setObjectName("widget_36")
        self.tabWidget_10.addTab(self.widget_36, "")
        self.widget_37 = QtWidgets.QWidget()
        self.widget_37.setObjectName("widget_37")
        self.horizontalLayout_71 = QtWidgets.QHBoxLayout(self.widget_37)
        self.horizontalLayout_71.setObjectName("horizontalLayout_71")
        self.tabWidget_10.addTab(self.widget_37, "")
        self.widget_39 = QtWidgets.QWidget()
        self.widget_39.setObjectName("widget_39")
        self.tabWidget_10.addTab(self.widget_39, "")
        self.widget_46 = QtWidgets.QWidget()
        self.widget_46.setObjectName("widget_46")
        self.tabWidget_10.addTab(self.widget_46, "")
        self.widget_47 = QtWidgets.QWidget()
        self.widget_47.setObjectName("widget_47")
        self.tabWidget_10.addTab(self.widget_47, "")
        self.widget_48 = QtWidgets.QWidget()
        self.widget_48.setObjectName("widget_48")
        self.tabWidget_10.addTab(self.widget_48, "")
        self.widget_49 = QtWidgets.QWidget()
        self.widget_49.setObjectName("widget_49")
        self.tabWidget_10.addTab(self.widget_49, "")
        self.widget_50 = QtWidgets.QWidget()
        self.widget_50.setObjectName("widget_50")
        self.tabWidget_10.addTab(self.widget_50, "")
        self.horizontalLayout_49.addWidget(self.tabWidget_10)
        self.operation.addTab(self.facing_tab, "")
        self.perimeter_tab = QtWidgets.QWidget()
        self.perimeter_tab.setObjectName("perimeter_tab")
        self.horizontalLayout_63 = QtWidgets.QHBoxLayout(self.perimeter_tab)
        self.horizontalLayout_63.setObjectName("horizontalLayout_63")
        self.tabWidget_9 = QtWidgets.QTabWidget(self.perimeter_tab)
        self.tabWidget_9.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_9.setStyleSheet("QTabWidget QTabBar::tab {\n"
"    margin-top: 5px;\n"
"    margin-right: 0px;\n"
"    min-width: 130px;\n"
"    min-height: 23px;\n"
"    font: 14pt \"bebas kai\";\n"
"}\n"
"\n"
"QTabBar::tab:first {\n"
"    margin-left: 300px;\n"
"    border-left-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-bottom-width: 2px;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:last {\n"
"    border-left-width: 1px;\n"
"    border-right-width: 2px;\n"
"    border-top-width: 2px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 4px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    border-width: 2px;\n"
"    border-radius: 4px;\n"
"}")
        self.tabWidget_9.setObjectName("tabWidget_9")
        self.widget_28 = QtWidgets.QWidget()
        self.widget_28.setObjectName("widget_28")
        self.tabWidget_9.addTab(self.widget_28, "")
        self.widget_29 = QtWidgets.QWidget()
        self.widget_29.setObjectName("widget_29")
        self.horizontalLayout_70 = QtWidgets.QHBoxLayout(self.widget_29)
        self.horizontalLayout_70.setObjectName("horizontalLayout_70")
        self.tabWidget_9.addTab(self.widget_29, "")
        self.widget_30 = QtWidgets.QWidget()
        self.widget_30.setObjectName("widget_30")
        self.tabWidget_9.addTab(self.widget_30, "")
        self.widget_31 = QtWidgets.QWidget()
        self.widget_31.setObjectName("widget_31")
        self.tabWidget_9.addTab(self.widget_31, "")
        self.widget_32 = QtWidgets.QWidget()
        self.widget_32.setObjectName("widget_32")
        self.tabWidget_9.addTab(self.widget_32, "")
        self.widget_33 = QtWidgets.QWidget()
        self.widget_33.setObjectName("widget_33")
        self.tabWidget_9.addTab(self.widget_33, "")
        self.widget_34 = QtWidgets.QWidget()
        self.widget_34.setObjectName("widget_34")
        self.tabWidget_9.addTab(self.widget_34, "")
        self.widget_35 = QtWidgets.QWidget()
        self.widget_35.setObjectName("widget_35")
        self.tabWidget_9.addTab(self.widget_35, "")
        self.horizontalLayout_63.addWidget(self.tabWidget_9)
        self.operation.addTab(self.perimeter_tab, "")
        self.pockets_tab = QtWidgets.QWidget()
        self.pockets_tab.setObjectName("pockets_tab")
        self.horizontalLayout_65 = QtWidgets.QHBoxLayout(self.pockets_tab)
        self.horizontalLayout_65.setObjectName("horizontalLayout_65")
        self.tabWidget_8 = QtWidgets.QTabWidget(self.pockets_tab)
        self.tabWidget_8.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_8.setStyleSheet("QTabWidget QTabBar::tab {\n"
"    margin-top: 5px;\n"
"    margin-right: 0px;\n"
"    min-width: 130px;\n"
"    min-height: 23px;\n"
"    font: 14pt \"bebas kai\";\n"
"}\n"
"\n"
"QTabBar::tab:first {\n"
"    margin-left: 300px;\n"
"    border-left-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-bottom-width: 2px;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:last {\n"
"    border-left-width: 1px;\n"
"    border-right-width: 2px;\n"
"    border-top-width: 2px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 4px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    border-width: 2px;\n"
"    border-radius: 4px;\n"
"}")
        self.tabWidget_8.setObjectName("tabWidget_8")
        self.widget_2 = QtWidgets.QWidget()
        self.widget_2.setObjectName("widget_2")
        self.tabWidget_8.addTab(self.widget_2, "")
        self.widget_20 = QtWidgets.QWidget()
        self.widget_20.setObjectName("widget_20")
        self.horizontalLayout_69 = QtWidgets.QHBoxLayout(self.widget_20)
        self.horizontalLayout_69.setObjectName("horizontalLayout_69")
        self.tabWidget_8.addTab(self.widget_20, "")
        self.widget_22 = QtWidgets.QWidget()
        self.widget_22.setObjectName("widget_22")
        self.tabWidget_8.addTab(self.widget_22, "")
        self.widget_23 = QtWidgets.QWidget()
        self.widget_23.setObjectName("widget_23")
        self.tabWidget_8.addTab(self.widget_23, "")
        self.widget_24 = QtWidgets.QWidget()
        self.widget_24.setObjectName("widget_24")
        self.tabWidget_8.addTab(self.widget_24, "")
        self.widget_25 = QtWidgets.QWidget()
        self.widget_25.setObjectName("widget_25")
        self.tabWidget_8.addTab(self.widget_25, "")
        self.widget_26 = QtWidgets.QWidget()
        self.widget_26.setObjectName("widget_26")
        self.tabWidget_8.addTab(self.widget_26, "")
        self.widget_27 = QtWidgets.QWidget()
        self.widget_27.setObjectName("widget_27")
        self.tabWidget_8.addTab(self.widget_27, "")
        self.horizontalLayout_65.addWidget(self.tabWidget_8)
        self.operation.addTab(self.pockets_tab, "")
        self.misc_tab = QtWidgets.QWidget()
        self.misc_tab.setObjectName("misc_tab")
        self.horizontalLayout_68 = QtWidgets.QHBoxLayout(self.misc_tab)
        self.horizontalLayout_68.setObjectName("horizontalLayout_68")
        self.tabWidget_7 = QtWidgets.QTabWidget(self.misc_tab)
        self.tabWidget_7.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tabWidget_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget_7.setStyleSheet("QTabWidget QTabBar::tab {\n"
"    margin-top: 5px;\n"
"    margin-right: 0px;\n"
"    min-width: 130px;\n"
"    min-height: 23px;\n"
"    font: 14pt \"bebas kai\";\n"
"}\n"
"\n"
"QTabBar::tab:first {\n"
"    margin-left: 300px;\n"
"    border-left-width: 2px;\n"
"    border-right-width: 1px;\n"
"    border-bottom-width: 2px;\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:last {\n"
"    border-left-width: 1px;\n"
"    border-right-width: 2px;\n"
"    border-top-width: 2px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 4px;\n"
"    border-top-left-radius: 0px;\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"\n"
"QTabBar::tab:only-one {\n"
"    border-width: 2px;\n"
"    border-radius: 4px;\n"
"}")
        self.tabWidget_7.setObjectName("tabWidget_7")
        self.widget = QtWidgets.QWidget()
        self.widget.setObjectName("widget")
        self.tabWidget_7.addTab(self.widget, "")
        self.widget1 = QtWidgets.QWidget()
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_67 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_67.setObjectName("horizontalLayout_67")
        self.tabWidget_7.addTab(self.widget1, "")
        self.widget2 = QtWidgets.QWidget()
        self.widget2.setObjectName("widget2")
        self.tabWidget_7.addTab(self.widget2, "")
        self.widget3 = QtWidgets.QWidget()
        self.widget3.setObjectName("widget3")
        self.tabWidget_7.addTab(self.widget3, "")
        self.widget4 = QtWidgets.QWidget()
        self.widget4.setObjectName("widget4")
        self.tabWidget_7.addTab(self.widget4, "")
        self.widget5 = QtWidgets.QWidget()
        self.widget5.setObjectName("widget5")
        self.tabWidget_7.addTab(self.widget5, "")
        self.widget6 = QtWidgets.QWidget()
        self.widget6.setObjectName("widget6")
        self.tabWidget_7.addTab(self.widget6, "")
        self.widget7 = QtWidgets.QWidget()
        self.widget7.setObjectName("widget7")
        self.tabWidget_7.addTab(self.widget7, "")
        self.horizontalLayout_68.addWidget(self.tabWidget_7)
        self.operation.addTab(self.misc_tab, "")
        self.horizontalLayout_131.addWidget(self.operation)
        self.tabWidget.addTab(self.conversational_tab, "")
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setObjectName("settings_tab")
        self.frame_4 = QtWidgets.QFrame(self.settings_tab)
        self.frame_4.setGeometry(QtCore.QRect(950, 10, 201, 180))
        self.frame_4.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_58 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_58.setObjectName("verticalLayout_58")
        self.horizontalLayout_137 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_137.setContentsMargins(6, -1, 6, -1)
        self.horizontalLayout_137.setObjectName("horizontalLayout_137")
        self.xyz_checkbox = VCPSettingsCheckBox(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xyz_checkbox.sizePolicy().hasHeightForWidth())
        self.xyz_checkbox.setSizePolicy(sizePolicy)
        self.xyz_checkbox.setChecked(True)
        self.xyz_checkbox.setAutoExclusive(True)
        self.xyz_checkbox.setProperty("page", 0)
        self.xyz_checkbox.setObjectName("xyz_checkbox")
        self.guiaxisdisplayGroup = QtWidgets.QButtonGroup(Form)
        self.guiaxisdisplayGroup.setObjectName("guiaxisdisplayGroup")
        self.guiaxisdisplayGroup.addButton(self.xyz_checkbox)
        self.horizontalLayout_137.addWidget(self.xyz_checkbox)
        self.label_118 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_118.sizePolicy().hasHeightForWidth())
        self.label_118.setSizePolicy(sizePolicy)
        self.label_118.setMinimumSize(QtCore.QSize(120, 31))
        self.label_118.setMaximumSize(QtCore.QSize(120, 31))
        self.label_118.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_118.setLineWidth(0)
        self.label_118.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_118.setIndent(0)
        self.label_118.setObjectName("label_118")
        self.horizontalLayout_137.addWidget(self.label_118)
        self.verticalLayout_58.addLayout(self.horizontalLayout_137)
        self.horizontalLayout_139 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_139.setContentsMargins(6, -1, 6, -1)
        self.horizontalLayout_139.setObjectName("horizontalLayout_139")
        self.xyza_checkbox = VCPSettingsCheckBox(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xyza_checkbox.sizePolicy().hasHeightForWidth())
        self.xyza_checkbox.setSizePolicy(sizePolicy)
        self.xyza_checkbox.setAutoExclusive(True)
        self.xyza_checkbox.setProperty("page", 1)
        self.xyza_checkbox.setObjectName("xyza_checkbox")
        self.guiaxisdisplayGroup.addButton(self.xyza_checkbox)
        self.horizontalLayout_139.addWidget(self.xyza_checkbox)
        self.label_120 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_120.sizePolicy().hasHeightForWidth())
        self.label_120.setSizePolicy(sizePolicy)
        self.label_120.setMinimumSize(QtCore.QSize(120, 31))
        self.label_120.setMaximumSize(QtCore.QSize(120, 31))
        self.label_120.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_120.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_120.setLineWidth(0)
        self.label_120.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_120.setIndent(0)
        self.label_120.setObjectName("label_120")
        self.horizontalLayout_139.addWidget(self.label_120)
        self.verticalLayout_58.addLayout(self.horizontalLayout_139)
        self.horizontalLayout_142 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_142.setContentsMargins(6, -1, 6, -1)
        self.horizontalLayout_142.setObjectName("horizontalLayout_142")
        self.xyzab_checkbox = VCPSettingsCheckBox(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xyzab_checkbox.sizePolicy().hasHeightForWidth())
        self.xyzab_checkbox.setSizePolicy(sizePolicy)
        self.xyzab_checkbox.setAutoExclusive(True)
        self.xyzab_checkbox.setProperty("page", 2)
        self.xyzab_checkbox.setObjectName("xyzab_checkbox")
        self.guiaxisdisplayGroup.addButton(self.xyzab_checkbox)
        self.horizontalLayout_142.addWidget(self.xyzab_checkbox)
        self.label_121 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_121.sizePolicy().hasHeightForWidth())
        self.label_121.setSizePolicy(sizePolicy)
        self.label_121.setMinimumSize(QtCore.QSize(120, 31))
        self.label_121.setMaximumSize(QtCore.QSize(120, 31))
        self.label_121.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_121.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_121.setLineWidth(0)
        self.label_121.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_121.setIndent(0)
        self.label_121.setObjectName("label_121")
        self.horizontalLayout_142.addWidget(self.label_121)
        self.verticalLayout_58.addLayout(self.horizontalLayout_142)
        self.frame_5 = QtWidgets.QFrame(self.settings_tab)
        self.frame_5.setGeometry(QtCore.QRect(1160, 10, 471, 361))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_59 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_59.setObjectName("verticalLayout_59")
        self.work_column_header_6 = QtWidgets.QLabel(self.frame_5)
        self.work_column_header_6.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.work_column_header_6.sizePolicy().hasHeightForWidth())
        self.work_column_header_6.setSizePolicy(sizePolicy)
        self.work_column_header_6.setMinimumSize(QtCore.QSize(100, 25))
        self.work_column_header_6.setMaximumSize(QtCore.QSize(16777215, 25))
        self.work_column_header_6.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.work_column_header_6.setAlignment(QtCore.Qt.AlignCenter)
        self.work_column_header_6.setObjectName("work_column_header_6")
        self.verticalLayout_59.addWidget(self.work_column_header_6)
        self.horizontalLayout_170 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_170.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_170.setObjectName("horizontalLayout_170")
        self.label_127 = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_127.sizePolicy().hasHeightForWidth())
        self.label_127.setSizePolicy(sizePolicy)
        self.label_127.setMinimumSize(QtCore.QSize(140, 31))
        self.label_127.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_127.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_127.setLineWidth(0)
        self.label_127.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_127.setIndent(0)
        self.label_127.setObjectName("label_127")
        self.horizontalLayout_170.addWidget(self.label_127)
        self.activate_pogrammable_coolant = VCPSettingsLineEdit(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.activate_pogrammable_coolant.sizePolicy().hasHeightForWidth())
        self.activate_pogrammable_coolant.setSizePolicy(sizePolicy)
        self.activate_pogrammable_coolant.setMinimumSize(QtCore.QSize(100, 31))
        self.activate_pogrammable_coolant.setMaximumSize(QtCore.QSize(100, 31))
        self.activate_pogrammable_coolant.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.activate_pogrammable_coolant.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.activate_pogrammable_coolant.setObjectName("activate_pogrammable_coolant")
        self.horizontalLayout_170.addWidget(self.activate_pogrammable_coolant)
        self.verticalLayout_59.addLayout(self.horizontalLayout_170)
        self.horizontalLayout_166 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_166.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_166.setObjectName("horizontalLayout_166")
        self.label_126 = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_126.sizePolicy().hasHeightForWidth())
        self.label_126.setSizePolicy(sizePolicy)
        self.label_126.setMinimumSize(QtCore.QSize(140, 31))
        self.label_126.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_126.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_126.setLineWidth(0)
        self.label_126.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_126.setIndent(0)
        self.label_126.setObjectName("label_126")
        self.horizontalLayout_166.addWidget(self.label_126)
        self.horizontal_spindle_nozzle_dist = VCPSettingsLineEdit(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontal_spindle_nozzle_dist.sizePolicy().hasHeightForWidth())
        self.horizontal_spindle_nozzle_dist.setSizePolicy(sizePolicy)
        self.horizontal_spindle_nozzle_dist.setMinimumSize(QtCore.QSize(100, 31))
        self.horizontal_spindle_nozzle_dist.setMaximumSize(QtCore.QSize(100, 31))
        self.horizontal_spindle_nozzle_dist.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.horizontal_spindle_nozzle_dist.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.horizontal_spindle_nozzle_dist.setObjectName("horizontal_spindle_nozzle_dist")
        self.horizontalLayout_166.addWidget(self.horizontal_spindle_nozzle_dist)
        self.verticalLayout_59.addLayout(self.horizontalLayout_166)
        self.horizontalLayout_167 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_167.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_167.setObjectName("horizontalLayout_167")
        self.label_128 = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_128.sizePolicy().hasHeightForWidth())
        self.label_128.setSizePolicy(sizePolicy)
        self.label_128.setMinimumSize(QtCore.QSize(140, 31))
        self.label_128.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_128.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_128.setLineWidth(0)
        self.label_128.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_128.setIndent(0)
        self.label_128.setObjectName("label_128")
        self.horizontalLayout_167.addWidget(self.label_128)
        self.vertical_spindle_nozzle_dist = VCPSettingsLineEdit(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vertical_spindle_nozzle_dist.sizePolicy().hasHeightForWidth())
        self.vertical_spindle_nozzle_dist.setSizePolicy(sizePolicy)
        self.vertical_spindle_nozzle_dist.setMinimumSize(QtCore.QSize(100, 31))
        self.vertical_spindle_nozzle_dist.setMaximumSize(QtCore.QSize(100, 31))
        self.vertical_spindle_nozzle_dist.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.vertical_spindle_nozzle_dist.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.vertical_spindle_nozzle_dist.setObjectName("vertical_spindle_nozzle_dist")
        self.horizontalLayout_167.addWidget(self.vertical_spindle_nozzle_dist)
        self.verticalLayout_59.addLayout(self.horizontalLayout_167)
        self.horizontalLayout_171 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_171.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_171.setObjectName("horizontalLayout_171")
        self.label_132 = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_132.sizePolicy().hasHeightForWidth())
        self.label_132.setSizePolicy(sizePolicy)
        self.label_132.setMinimumSize(QtCore.QSize(140, 31))
        self.label_132.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_132.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_132.setLineWidth(0)
        self.label_132.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_132.setIndent(0)
        self.label_132.setObjectName("label_132")
        self.horizontalLayout_171.addWidget(self.label_132)
        self.pc_angle_offset = VCPSettingsLineEdit(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pc_angle_offset.sizePolicy().hasHeightForWidth())
        self.pc_angle_offset.setSizePolicy(sizePolicy)
        self.pc_angle_offset.setMinimumSize(QtCore.QSize(100, 31))
        self.pc_angle_offset.setMaximumSize(QtCore.QSize(100, 31))
        self.pc_angle_offset.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.pc_angle_offset.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pc_angle_offset.setObjectName("pc_angle_offset")
        self.horizontalLayout_171.addWidget(self.pc_angle_offset)
        self.verticalLayout_59.addLayout(self.horizontalLayout_171)
        self.horizontalLayout_168 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_168.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_168.setObjectName("horizontalLayout_168")
        self.label_130 = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_130.sizePolicy().hasHeightForWidth())
        self.label_130.setSizePolicy(sizePolicy)
        self.label_130.setMinimumSize(QtCore.QSize(140, 31))
        self.label_130.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_130.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_130.setLineWidth(0)
        self.label_130.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_130.setIndent(0)
        self.label_130.setObjectName("label_130")
        self.horizontalLayout_168.addWidget(self.label_130)
        self.pc_tool_length = StatusLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pc_tool_length.sizePolicy().hasHeightForWidth())
        self.pc_tool_length.setSizePolicy(sizePolicy)
        self.pc_tool_length.setMinimumSize(QtCore.QSize(100, 33))
        self.pc_tool_length.setMaximumSize(QtCore.QSize(100, 33))
        self.pc_tool_length.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: transparent;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.pc_tool_length.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pc_tool_length.setObjectName("pc_tool_length")
        self.horizontalLayout_168.addWidget(self.pc_tool_length)
        self.verticalLayout_59.addLayout(self.horizontalLayout_168)
        self.horizontalLayout_169 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_169.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_169.setObjectName("horizontalLayout_169")
        self.label_131 = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_131.sizePolicy().hasHeightForWidth())
        self.label_131.setSizePolicy(sizePolicy)
        self.label_131.setMinimumSize(QtCore.QSize(140, 31))
        self.label_131.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_131.setStyleSheet("QLabel{\n"
"font: 75 14pt \"Bebas Kai\";\n"
"color: white;\n"
"}")
        self.label_131.setLineWidth(0)
        self.label_131.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_131.setIndent(0)
        self.label_131.setObjectName("label_131")
        self.horizontalLayout_169.addWidget(self.label_131)
        self.coolant_final_angle = StatusLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coolant_final_angle.sizePolicy().hasHeightForWidth())
        self.coolant_final_angle.setSizePolicy(sizePolicy)
        self.coolant_final_angle.setMinimumSize(QtCore.QSize(100, 33))
        self.coolant_final_angle.setMaximumSize(QtCore.QSize(100, 33))
        self.coolant_final_angle.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: transparent;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 15pt \"Bebas Kai\";\n"
"}")
        self.coolant_final_angle.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.coolant_final_angle.setObjectName("coolant_final_angle")
        self.horizontalLayout_169.addWidget(self.coolant_final_angle)
        self.verticalLayout_59.addLayout(self.horizontalLayout_169)
        self.tabWidget.addTab(self.settings_tab, "")
        self.status_tab = QtWidgets.QWidget()
        self.status_tab.setObjectName("status_tab")
        self.frame_21 = QtWidgets.QFrame(self.status_tab)
        self.frame_21.setGeometry(QtCore.QRect(1320, 26, 290, 280))
        self.frame_21.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.verticalLayout_25 = QtWidgets.QVBoxLayout(self.frame_21)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.horizontalLayout_52 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_52.setObjectName("horizontalLayout_52")
        self.label_111 = QtWidgets.QLabel(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_111.sizePolicy().hasHeightForWidth())
        self.label_111.setSizePolicy(sizePolicy)
        self.label_111.setMinimumSize(QtCore.QSize(150, 31))
        self.label_111.setMaximumSize(QtCore.QSize(200, 31))
        self.label_111.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_111.setLineWidth(0)
        self.label_111.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_111.setIndent(0)
        self.label_111.setObjectName("label_111")
        self.horizontalLayout_52.addWidget(self.label_111)
        self.probe_mode = QtWidgets.QLineEdit(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probe_mode.sizePolicy().hasHeightForWidth())
        self.probe_mode.setSizePolicy(sizePolicy)
        self.probe_mode.setMinimumSize(QtCore.QSize(60, 31))
        self.probe_mode.setMaximumSize(QtCore.QSize(60, 31))
        self.probe_mode.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.probe_mode.setStyleSheet("")
        self.probe_mode.setFrame(False)
        self.probe_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.probe_mode.setReadOnly(True)
        self.probe_mode.setObjectName("probe_mode")
        self.horizontalLayout_52.addWidget(self.probe_mode)
        self.verticalLayout_25.addLayout(self.horizontalLayout_52)
        self.horizontalLayout_53 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_53.setObjectName("horizontalLayout_53")
        self.label_112 = QtWidgets.QLabel(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_112.sizePolicy().hasHeightForWidth())
        self.label_112.setSizePolicy(sizePolicy)
        self.label_112.setMinimumSize(QtCore.QSize(150, 31))
        self.label_112.setMaximumSize(QtCore.QSize(200, 31))
        self.label_112.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_112.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_112.setLineWidth(0)
        self.label_112.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_112.setIndent(0)
        self.label_112.setObjectName("label_112")
        self.horizontalLayout_53.addWidget(self.label_112)
        self.wco_rotation = QtWidgets.QLineEdit(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wco_rotation.sizePolicy().hasHeightForWidth())
        self.wco_rotation.setSizePolicy(sizePolicy)
        self.wco_rotation.setMinimumSize(QtCore.QSize(60, 31))
        self.wco_rotation.setMaximumSize(QtCore.QSize(60, 31))
        self.wco_rotation.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.wco_rotation.setStyleSheet("")
        self.wco_rotation.setFrame(False)
        self.wco_rotation.setAlignment(QtCore.Qt.AlignCenter)
        self.wco_rotation.setReadOnly(True)
        self.wco_rotation.setObjectName("wco_rotation")
        self.horizontalLayout_53.addWidget(self.wco_rotation)
        self.verticalLayout_25.addLayout(self.horizontalLayout_53)
        self.horizontalLayout_59 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_59.setObjectName("horizontalLayout_59")
        self.label_115 = QtWidgets.QLabel(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_115.sizePolicy().hasHeightForWidth())
        self.label_115.setSizePolicy(sizePolicy)
        self.label_115.setMinimumSize(QtCore.QSize(150, 31))
        self.label_115.setMaximumSize(QtCore.QSize(200, 31))
        self.label_115.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_115.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_115.setLineWidth(0)
        self.label_115.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_115.setIndent(0)
        self.label_115.setObjectName("label_115")
        self.horizontalLayout_59.addWidget(self.label_115)
        self.sq_cal_axis = QtWidgets.QLineEdit(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sq_cal_axis.sizePolicy().hasHeightForWidth())
        self.sq_cal_axis.setSizePolicy(sizePolicy)
        self.sq_cal_axis.setMinimumSize(QtCore.QSize(60, 31))
        self.sq_cal_axis.setMaximumSize(QtCore.QSize(60, 31))
        self.sq_cal_axis.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.sq_cal_axis.setStyleSheet("")
        self.sq_cal_axis.setFrame(False)
        self.sq_cal_axis.setAlignment(QtCore.Qt.AlignCenter)
        self.sq_cal_axis.setReadOnly(True)
        self.sq_cal_axis.setObjectName("sq_cal_axis")
        self.horizontalLayout_59.addWidget(self.sq_cal_axis)
        self.verticalLayout_25.addLayout(self.horizontalLayout_59)
        self.horizontalLayout_74 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_74.setObjectName("horizontalLayout_74")
        self.label_116 = QtWidgets.QLabel(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_116.sizePolicy().hasHeightForWidth())
        self.label_116.setSizePolicy(sizePolicy)
        self.label_116.setMinimumSize(QtCore.QSize(150, 31))
        self.label_116.setMaximumSize(QtCore.QSize(200, 31))
        self.label_116.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_116.setLineWidth(0)
        self.label_116.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_116.setIndent(0)
        self.label_116.setObjectName("label_116")
        self.horizontalLayout_74.addWidget(self.label_116)
        self.tool_diameter_probe_mode = QtWidgets.QLineEdit(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_diameter_probe_mode.sizePolicy().hasHeightForWidth())
        self.tool_diameter_probe_mode.setSizePolicy(sizePolicy)
        self.tool_diameter_probe_mode.setMinimumSize(QtCore.QSize(60, 31))
        self.tool_diameter_probe_mode.setMaximumSize(QtCore.QSize(60, 31))
        self.tool_diameter_probe_mode.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tool_diameter_probe_mode.setStyleSheet("")
        self.tool_diameter_probe_mode.setFrame(False)
        self.tool_diameter_probe_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.tool_diameter_probe_mode.setReadOnly(True)
        self.tool_diameter_probe_mode.setObjectName("tool_diameter_probe_mode")
        self.horizontalLayout_74.addWidget(self.tool_diameter_probe_mode)
        self.verticalLayout_25.addLayout(self.horizontalLayout_74)
        self.horizontalLayout_76 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_76.setObjectName("horizontalLayout_76")
        self.label_117 = QtWidgets.QLabel(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_117.sizePolicy().hasHeightForWidth())
        self.label_117.setSizePolicy(sizePolicy)
        self.label_117.setMinimumSize(QtCore.QSize(150, 31))
        self.label_117.setMaximumSize(QtCore.QSize(200, 31))
        self.label_117.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_117.setLineWidth(0)
        self.label_117.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_117.setIndent(0)
        self.label_117.setObjectName("label_117")
        self.horizontalLayout_76.addWidget(self.label_117)
        self.tool_diameter_offset_mode = QtWidgets.QLineEdit(self.frame_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_diameter_offset_mode.sizePolicy().hasHeightForWidth())
        self.tool_diameter_offset_mode.setSizePolicy(sizePolicy)
        self.tool_diameter_offset_mode.setMinimumSize(QtCore.QSize(60, 31))
        self.tool_diameter_offset_mode.setMaximumSize(QtCore.QSize(60, 31))
        self.tool_diameter_offset_mode.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tool_diameter_offset_mode.setStyleSheet("")
        self.tool_diameter_offset_mode.setFrame(False)
        self.tool_diameter_offset_mode.setAlignment(QtCore.Qt.AlignCenter)
        self.tool_diameter_offset_mode.setReadOnly(True)
        self.tool_diameter_offset_mode.setObjectName("tool_diameter_offset_mode")
        self.horizontalLayout_76.addWidget(self.tool_diameter_offset_mode)
        self.verticalLayout_25.addLayout(self.horizontalLayout_76)
        self.frame_38 = QtWidgets.QFrame(self.status_tab)
        self.frame_38.setGeometry(QtCore.QRect(11, 10, 800, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_38.sizePolicy().hasHeightForWidth())
        self.frame_38.setSizePolicy(sizePolicy)
        self.frame_38.setMinimumSize(QtCore.QSize(800, 600))
        self.frame_38.setMaximumSize(QtCore.QSize(800, 600))
        self.frame_38.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_38.setObjectName("frame_38")
        self.verticalLayout_47 = QtWidgets.QVBoxLayout(self.frame_38)
        self.verticalLayout_47.setContentsMargins(-1, 5, -1, 5)
        self.verticalLayout_47.setSpacing(6)
        self.verticalLayout_47.setObjectName("verticalLayout_47")
        self.notificationwidget = NotificationWidget(self.frame_38)
        self.notificationwidget.setStyleSheet("QLabel {\n"
"    font-family: \"Bebas Kai\";\n"
"    color: white;\n"
"    font-size: 16pt;\n"
"}\n"
"")
        self.notificationwidget.setObjectName("notificationwidget")
        self.verticalLayout_47.addWidget(self.notificationwidget)
        self.tabWidget.addTab(self.status_tab, "")
        self.verticalLayout_30.addWidget(self.tabWidget)
        self.horizontalLayout_101.addLayout(self.verticalLayout_30)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(0, -1, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget_24 = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_24.sizePolicy().hasHeightForWidth())
        self.tabWidget_24.setSizePolicy(sizePolicy)
        self.tabWidget_24.setMinimumSize(QtCore.QSize(256, 600))
        self.tabWidget_24.setMaximumSize(QtCore.QSize(256, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(15)
        self.tabWidget_24.setFont(font)
        self.tabWidget_24.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget_24.setStyleSheet("QTabWidget QTabBar::tab {\n"
"    margin-top: 2px;\n"
"    margin-bottom: 2px;\n"
"    min-width: 75px;\n"
"    min-height: 30px;\n"
"    font: 15pt \"bebas kai\";\n"
"}")
        self.tabWidget_24.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabWidget_24.setObjectName("tabWidget_24")
        self.tabWidget_24Page1 = QtWidgets.QWidget()
        self.tabWidget_24Page1.setObjectName("tabWidget_24Page1")
        self.frame_26 = QtWidgets.QFrame(self.tabWidget_24Page1)
        self.frame_26.setGeometry(QtCore.QRect(7, 26, 201, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_26.sizePolicy().hasHeightForWidth())
        self.frame_26.setSizePolicy(sizePolicy)
        self.frame_26.setMinimumSize(QtCore.QSize(201, 600))
        self.frame_26.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_26.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_26.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_26.setObjectName("frame_26")
        self.verticalLayout_32 = QtWidgets.QVBoxLayout(self.frame_26)
        self.verticalLayout_32.setContentsMargins(9, 15, 9, 12)
        self.verticalLayout_32.setSpacing(20)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.horizontalLayout_106 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_106.setObjectName("horizontalLayout_106")
        self.z_plus_jogbutton = ActionButton(self.frame_26)
        self.z_plus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.z_plus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.z_plus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.z_plus_jogbutton.setText("")
        icon49 = QtGui.QIcon()
        icon49.addPixmap(QtGui.QPixmap(":/images/z_plus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.z_plus_jogbutton.setIcon(icon49)
        self.z_plus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.z_plus_jogbutton.setObjectName("z_plus_jogbutton")
        self.horizontalLayout_106.addWidget(self.z_plus_jogbutton)
        self.verticalLayout_32.addLayout(self.horizontalLayout_106)
        self.horizontalLayout_107 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_107.setObjectName("horizontalLayout_107")
        self.z_minus_jogbutton = ActionButton(self.frame_26)
        self.z_minus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.z_minus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.z_minus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.z_minus_jogbutton.setText("")
        icon50 = QtGui.QIcon()
        icon50.addPixmap(QtGui.QPixmap(":/images/z_minus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.z_minus_jogbutton.setIcon(icon50)
        self.z_minus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.z_minus_jogbutton.setObjectName("z_minus_jogbutton")
        self.horizontalLayout_107.addWidget(self.z_minus_jogbutton)
        self.verticalLayout_32.addLayout(self.horizontalLayout_107)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setHorizontalSpacing(0)
        self.gridLayout_6.setVerticalSpacing(15)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.x_plus_jogbutton = ActionButton(self.frame_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_plus_jogbutton.sizePolicy().hasHeightForWidth())
        self.x_plus_jogbutton.setSizePolicy(sizePolicy)
        self.x_plus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.x_plus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.x_plus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_plus_jogbutton.setText("")
        icon51 = QtGui.QIcon()
        icon51.addPixmap(QtGui.QPixmap(":/images/x_plus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.x_plus_jogbutton.setIcon(icon51)
        self.x_plus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.x_plus_jogbutton.setObjectName("x_plus_jogbutton")
        self.gridLayout_6.addWidget(self.x_plus_jogbutton, 1, 2, 1, 1)
        self.x_minus_jogbutton = ActionButton(self.frame_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_minus_jogbutton.sizePolicy().hasHeightForWidth())
        self.x_minus_jogbutton.setSizePolicy(sizePolicy)
        self.x_minus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.x_minus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.x_minus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_minus_jogbutton.setText("")
        icon52 = QtGui.QIcon()
        icon52.addPixmap(QtGui.QPixmap(":/images/x_minus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.x_minus_jogbutton.setIcon(icon52)
        self.x_minus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.x_minus_jogbutton.setObjectName("x_minus_jogbutton")
        self.gridLayout_6.addWidget(self.x_minus_jogbutton, 1, 0, 1, 1)
        self.y_minus_jogbutton = ActionButton(self.frame_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_minus_jogbutton.sizePolicy().hasHeightForWidth())
        self.y_minus_jogbutton.setSizePolicy(sizePolicy)
        self.y_minus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.y_minus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.y_minus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.y_minus_jogbutton.setText("")
        icon53 = QtGui.QIcon()
        icon53.addPixmap(QtGui.QPixmap(":/images/y_minus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.y_minus_jogbutton.setIcon(icon53)
        self.y_minus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.y_minus_jogbutton.setObjectName("y_minus_jogbutton")
        self.gridLayout_6.addWidget(self.y_minus_jogbutton, 2, 1, 1, 1)
        self.y_plus_jogbutton = ActionButton(self.frame_26)
        self.y_plus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.y_plus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.y_plus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.y_plus_jogbutton.setText("")
        icon54 = QtGui.QIcon()
        icon54.addPixmap(QtGui.QPixmap(":/images/y_plus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.y_plus_jogbutton.setIcon(icon54)
        self.y_plus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.y_plus_jogbutton.setObjectName("y_plus_jogbutton")
        self.gridLayout_6.addWidget(self.y_plus_jogbutton, 0, 1, 1, 1)
        self.verticalLayout_32.addLayout(self.gridLayout_6)
        self.horizontalLayout_112 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_112.setObjectName("horizontalLayout_112")
        self.a_minus_jogbutton = ActionButton(self.frame_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.a_minus_jogbutton.sizePolicy().hasHeightForWidth())
        self.a_minus_jogbutton.setSizePolicy(sizePolicy)
        self.a_minus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.a_minus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.a_minus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.a_minus_jogbutton.setText("")
        icon55 = QtGui.QIcon()
        icon55.addPixmap(QtGui.QPixmap(":/images/a_minus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_minus_jogbutton.setIcon(icon55)
        self.a_minus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.a_minus_jogbutton.setObjectName("a_minus_jogbutton")
        self.horizontalLayout_112.addWidget(self.a_minus_jogbutton)
        self.a_plus_jogbutton = ActionButton(self.frame_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.a_plus_jogbutton.sizePolicy().hasHeightForWidth())
        self.a_plus_jogbutton.setSizePolicy(sizePolicy)
        self.a_plus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.a_plus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.a_plus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.a_plus_jogbutton.setText("")
        icon56 = QtGui.QIcon()
        icon56.addPixmap(QtGui.QPixmap(":/images/a_plus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.a_plus_jogbutton.setIcon(icon56)
        self.a_plus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.a_plus_jogbutton.setObjectName("a_plus_jogbutton")
        self.horizontalLayout_112.addWidget(self.a_plus_jogbutton)
        self.verticalLayout_32.addLayout(self.horizontalLayout_112)
        self.horizontalLayout_111 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_111.setObjectName("horizontalLayout_111")
        self.b_minus_jogbutton = ActionButton(self.frame_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_minus_jogbutton.sizePolicy().hasHeightForWidth())
        self.b_minus_jogbutton.setSizePolicy(sizePolicy)
        self.b_minus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.b_minus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.b_minus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.b_minus_jogbutton.setText("")
        icon57 = QtGui.QIcon()
        icon57.addPixmap(QtGui.QPixmap(":/images/b_minus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_minus_jogbutton.setIcon(icon57)
        self.b_minus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.b_minus_jogbutton.setObjectName("b_minus_jogbutton")
        self.horizontalLayout_111.addWidget(self.b_minus_jogbutton)
        self.b_plus_jogbutton = ActionButton(self.frame_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b_plus_jogbutton.sizePolicy().hasHeightForWidth())
        self.b_plus_jogbutton.setSizePolicy(sizePolicy)
        self.b_plus_jogbutton.setMinimumSize(QtCore.QSize(56, 56))
        self.b_plus_jogbutton.setMaximumSize(QtCore.QSize(56, 56))
        self.b_plus_jogbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.b_plus_jogbutton.setText("")
        icon58 = QtGui.QIcon()
        icon58.addPixmap(QtGui.QPixmap(":/images/b_plus_jog_button.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.b_plus_jogbutton.setIcon(icon58)
        self.b_plus_jogbutton.setIconSize(QtCore.QSize(48, 48))
        self.b_plus_jogbutton.setObjectName("b_plus_jogbutton")
        self.horizontalLayout_111.addWidget(self.b_plus_jogbutton)
        self.verticalLayout_32.addLayout(self.horizontalLayout_111)
        self.horizontalWidget1 = QtWidgets.QWidget(self.frame_26)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget1.sizePolicy().hasHeightForWidth())
        self.horizontalWidget1.setSizePolicy(sizePolicy)
        self.horizontalWidget1.setMinimumSize(QtCore.QSize(0, 42))
        self.horizontalWidget1.setMaximumSize(QtCore.QSize(16777215, 42))
        self.horizontalWidget1.setObjectName("horizontalWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(8)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.manual_mode_button = ActionButton(self.horizontalWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_mode_button.sizePolicy().hasHeightForWidth())
        self.manual_mode_button.setSizePolicy(sizePolicy)
        self.manual_mode_button.setMinimumSize(QtCore.QSize(0, 40))
        self.manual_mode_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.manual_mode_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.manual_mode_button.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.manual_mode_button.setCheckable(True)
        self.manual_mode_button.setAutoExclusive(True)
        self.manual_mode_button.setObjectName("manual_mode_button")
        self.horizontalLayout_2.addWidget(self.manual_mode_button)
        self.auto_mode_button = ActionButton(self.horizontalWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_mode_button.sizePolicy().hasHeightForWidth())
        self.auto_mode_button.setSizePolicy(sizePolicy)
        self.auto_mode_button.setMinimumSize(QtCore.QSize(0, 40))
        self.auto_mode_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.auto_mode_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.auto_mode_button.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.auto_mode_button.setCheckable(True)
        self.auto_mode_button.setAutoExclusive(True)
        self.auto_mode_button.setObjectName("auto_mode_button")
        self.horizontalLayout_2.addWidget(self.auto_mode_button)
        self.mdi_mode_button = ActionButton(self.horizontalWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdi_mode_button.sizePolicy().hasHeightForWidth())
        self.mdi_mode_button.setSizePolicy(sizePolicy)
        self.mdi_mode_button.setMinimumSize(QtCore.QSize(0, 40))
        self.mdi_mode_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.mdi_mode_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mdi_mode_button.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.mdi_mode_button.setCheckable(True)
        self.mdi_mode_button.setAutoExclusive(True)
        self.mdi_mode_button.setObjectName("mdi_mode_button")
        self.horizontalLayout_2.addWidget(self.mdi_mode_button)
        self.verticalLayout_32.addWidget(self.horizontalWidget1)
        self.label_20 = QtWidgets.QLabel(self.tabWidget_24Page1)
        self.label_20.setGeometry(QtCore.QRect(95, 4, 110, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QtCore.QSize(110, 20))
        self.label_20.setMaximumSize(QtCore.QSize(110, 20))
        self.label_20.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 14pt \"Bebas Kai\";\n"
"}")
        self.label_20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_20.setObjectName("label_20")
        self.layoutWidget_2 = QtWidgets.QWidget(self.tabWidget_24Page1)
        self.layoutWidget_2.setGeometry(QtCore.QRect(214, 0, 51, 621))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_12.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_12.setContentsMargins(-1, 2, -1, -1)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.statuslabel_15 = StatusLabel(self.layoutWidget_2)
        self.statuslabel_15.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.statuslabel_15.sizePolicy().hasHeightForWidth())
        self.statuslabel_15.setSizePolicy(sizePolicy)
        self.statuslabel_15.setMinimumSize(QtCore.QSize(40, 0))
        self.statuslabel_15.setMaximumSize(QtCore.QSize(40, 16777215))
        self.statuslabel_15.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_15.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.statuslabel_15.setWordWrap(True)
        self.statuslabel_15.setIndent(0)
        self.statuslabel_15.setProperty("statusItem", "")
        self.statuslabel_15.setObjectName("statuslabel_15")
        self.verticalLayout_12.addWidget(self.statuslabel_15)
        self.statuslabel_16 = StatusLabel(self.layoutWidget_2)
        self.statuslabel_16.setMinimumSize(QtCore.QSize(40, 0))
        self.statuslabel_16.setMaximumSize(QtCore.QSize(40, 16777215))
        self.statuslabel_16.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_16.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.statuslabel_16.setWordWrap(True)
        self.statuslabel_16.setIndent(0)
        self.statuslabel_16.setProperty("statusItem", "")
        self.statuslabel_16.setObjectName("statuslabel_16")
        self.verticalLayout_12.addWidget(self.statuslabel_16)
        self.tabWidget_24.addTab(self.tabWidget_24Page1, "")
        self.tab_17 = QtWidgets.QWidget()
        self.tab_17.setObjectName("tab_17")
        self.layoutWidget = QtWidgets.QWidget(self.tab_17)
        self.layoutWidget.setGeometry(QtCore.QRect(214, 0, 42, 621))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_9.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_9.setContentsMargins(-1, 2, -1, -1)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.statuslabel_13 = StatusLabel(self.layoutWidget)
        self.statuslabel_13.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.statuslabel_13.sizePolicy().hasHeightForWidth())
        self.statuslabel_13.setSizePolicy(sizePolicy)
        self.statuslabel_13.setMinimumSize(QtCore.QSize(40, 0))
        self.statuslabel_13.setMaximumSize(QtCore.QSize(40, 16777215))
        self.statuslabel_13.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_13.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.statuslabel_13.setWordWrap(True)
        self.statuslabel_13.setIndent(0)
        self.statuslabel_13.setProperty("statusItem", "")
        self.statuslabel_13.setObjectName("statuslabel_13")
        self.verticalLayout_9.addWidget(self.statuslabel_13)
        self.statuslabel_14 = StatusLabel(self.layoutWidget)
        self.statuslabel_14.setMinimumSize(QtCore.QSize(40, 0))
        self.statuslabel_14.setMaximumSize(QtCore.QSize(40, 16777215))
        self.statuslabel_14.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_14.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.statuslabel_14.setWordWrap(True)
        self.statuslabel_14.setIndent(0)
        self.statuslabel_14.setProperty("statusItem", "")
        self.statuslabel_14.setObjectName("statuslabel_14")
        self.verticalLayout_9.addWidget(self.statuslabel_14)
        self.label_19 = QtWidgets.QLabel(self.tab_17)
        self.label_19.setEnabled(True)
        self.label_19.setGeometry(QtCore.QRect(95, 4, 110, 20))
        self.label_19.setMinimumSize(QtCore.QSize(110, 20))
        self.label_19.setMaximumSize(QtCore.QSize(110, 20))
        self.label_19.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.frame_29 = QtWidgets.QFrame(self.tab_17)
        self.frame_29.setGeometry(QtCore.QRect(7, 26, 201, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_29.sizePolicy().hasHeightForWidth())
        self.frame_29.setSizePolicy(sizePolicy)
        self.frame_29.setMinimumSize(QtCore.QSize(201, 600))
        self.frame_29.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_29.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.verticalLayout_40 = QtWidgets.QVBoxLayout(self.frame_29)
        self.verticalLayout_40.setContentsMargins(9, 15, 9, 12)
        self.verticalLayout_40.setSpacing(12)
        self.verticalLayout_40.setObjectName("verticalLayout_40")
        self.widget_5 = QtWidgets.QWidget(self.frame_29)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy)
        self.widget_5.setMinimumSize(QtCore.QSize(171, 0))
        self.widget_5.setMaximumSize(QtCore.QSize(171, 16777215))
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout_3.setContentsMargins(2, 6, 2, 6)
        self.gridLayout_3.setSpacing(15)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.actionbutton_g58_3 = ActionButton(self.widget_5)
        self.actionbutton_g58_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g58_3.sizePolicy().hasHeightForWidth())
        self.actionbutton_g58_3.setSizePolicy(sizePolicy)
        self.actionbutton_g58_3.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g58_3.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g58_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g58_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g58_3.setAutoExclusive(True)
        self.actionbutton_g58_3.setObjectName("actionbutton_g58_3")
        self.customwcsbtnGroup = QtWidgets.QButtonGroup(Form)
        self.customwcsbtnGroup.setObjectName("customwcsbtnGroup")
        self.customwcsbtnGroup.addButton(self.actionbutton_g58_3)
        self.gridLayout_3.addWidget(self.actionbutton_g58_3, 4, 0, 1, 1)
        self.actionbutton_g59_8 = ActionButton(self.widget_5)
        self.actionbutton_g59_8.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g59_8.sizePolicy().hasHeightForWidth())
        self.actionbutton_g59_8.setSizePolicy(sizePolicy)
        self.actionbutton_g59_8.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g59_8.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g59_8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g59_8.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g59_8.setAutoExclusive(True)
        self.actionbutton_g59_8.setObjectName("actionbutton_g59_8")
        self.customwcsbtnGroup.addButton(self.actionbutton_g59_8)
        self.gridLayout_3.addWidget(self.actionbutton_g59_8, 9, 0, 1, 1)
        self.actionbutton_g54_3 = ActionButton(self.widget_5)
        self.actionbutton_g54_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g54_3.sizePolicy().hasHeightForWidth())
        self.actionbutton_g54_3.setSizePolicy(sizePolicy)
        self.actionbutton_g54_3.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g54_3.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g54_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g54_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g54_3.setAutoExclusive(True)
        self.actionbutton_g54_3.setObjectName("actionbutton_g54_3")
        self.customwcsbtnGroup.addButton(self.actionbutton_g54_3)
        self.gridLayout_3.addWidget(self.actionbutton_g54_3, 0, 0, 1, 1)
        self.actionbutton_g56_3 = ActionButton(self.widget_5)
        self.actionbutton_g56_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g56_3.sizePolicy().hasHeightForWidth())
        self.actionbutton_g56_3.setSizePolicy(sizePolicy)
        self.actionbutton_g56_3.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g56_3.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g56_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g56_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g56_3.setAutoExclusive(True)
        self.actionbutton_g56_3.setObjectName("actionbutton_g56_3")
        self.customwcsbtnGroup.addButton(self.actionbutton_g56_3)
        self.gridLayout_3.addWidget(self.actionbutton_g56_3, 2, 0, 1, 1)
        self.actionbutton_g55_3 = ActionButton(self.widget_5)
        self.actionbutton_g55_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g55_3.sizePolicy().hasHeightForWidth())
        self.actionbutton_g55_3.setSizePolicy(sizePolicy)
        self.actionbutton_g55_3.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g55_3.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g55_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g55_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g55_3.setAutoExclusive(True)
        self.actionbutton_g55_3.setObjectName("actionbutton_g55_3")
        self.customwcsbtnGroup.addButton(self.actionbutton_g55_3)
        self.gridLayout_3.addWidget(self.actionbutton_g55_3, 0, 1, 1, 1)
        self.actionbutton_g57_3 = ActionButton(self.widget_5)
        self.actionbutton_g57_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g57_3.sizePolicy().hasHeightForWidth())
        self.actionbutton_g57_3.setSizePolicy(sizePolicy)
        self.actionbutton_g57_3.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g57_3.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g57_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g57_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g57_3.setAutoExclusive(True)
        self.actionbutton_g57_3.setObjectName("actionbutton_g57_3")
        self.customwcsbtnGroup.addButton(self.actionbutton_g57_3)
        self.gridLayout_3.addWidget(self.actionbutton_g57_3, 2, 1, 1, 1)
        self.actionbutton_g59_10 = ActionButton(self.widget_5)
        self.actionbutton_g59_10.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g59_10.sizePolicy().hasHeightForWidth())
        self.actionbutton_g59_10.setSizePolicy(sizePolicy)
        self.actionbutton_g59_10.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g59_10.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g59_10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g59_10.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g59_10.setAutoExclusive(True)
        self.actionbutton_g59_10.setObjectName("actionbutton_g59_10")
        self.customwcsbtnGroup.addButton(self.actionbutton_g59_10)
        self.gridLayout_3.addWidget(self.actionbutton_g59_10, 4, 1, 1, 1)
        self.actionbutton_g59_11 = ActionButton(self.widget_5)
        self.actionbutton_g59_11.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g59_11.sizePolicy().hasHeightForWidth())
        self.actionbutton_g59_11.setSizePolicy(sizePolicy)
        self.actionbutton_g59_11.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g59_11.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g59_11.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g59_11.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g59_11.setAutoExclusive(True)
        self.actionbutton_g59_11.setObjectName("actionbutton_g59_11")
        self.customwcsbtnGroup.addButton(self.actionbutton_g59_11)
        self.gridLayout_3.addWidget(self.actionbutton_g59_11, 7, 1, 1, 1)
        self.actionbutton_g59_9 = ActionButton(self.widget_5)
        self.actionbutton_g59_9.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_g59_9.sizePolicy().hasHeightForWidth())
        self.actionbutton_g59_9.setSizePolicy(sizePolicy)
        self.actionbutton_g59_9.setMinimumSize(QtCore.QSize(75, 40))
        self.actionbutton_g59_9.setMaximumSize(QtCore.QSize(75, 40))
        self.actionbutton_g59_9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_g59_9.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_g59_9.setAutoExclusive(True)
        self.actionbutton_g59_9.setObjectName("actionbutton_g59_9")
        self.customwcsbtnGroup.addButton(self.actionbutton_g59_9)
        self.gridLayout_3.addWidget(self.actionbutton_g59_9, 7, 0, 1, 1)
        self.verticalLayout_40.addWidget(self.widget_5)
        self.label = QtWidgets.QLabel(self.frame_29)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout_40.addWidget(self.label)
        self.probesim = ProbeSim(self.frame_29)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.probesim.sizePolicy().hasHeightForWidth())
        self.probesim.setSizePolicy(sizePolicy)
        self.probesim.setMinimumSize(QtCore.QSize(0, 47))
        self.probesim.setStyleSheet("QPushButton{\n"
"    min-height: 35px;\n"
"}")
        self.probesim.setObjectName("probesim")
        self.verticalLayout_40.addWidget(self.probesim)
        self.horizontalWidget_21 = QtWidgets.QWidget(self.frame_29)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget_21.sizePolicy().hasHeightForWidth())
        self.horizontalWidget_21.setSizePolicy(sizePolicy)
        self.horizontalWidget_21.setMinimumSize(QtCore.QSize(0, 42))
        self.horizontalWidget_21.setMaximumSize(QtCore.QSize(16777215, 42))
        self.horizontalWidget_21.setObjectName("horizontalWidget_21")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalWidget_21)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(8)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.manual_mode_button_2 = ActionButton(self.horizontalWidget_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_mode_button_2.sizePolicy().hasHeightForWidth())
        self.manual_mode_button_2.setSizePolicy(sizePolicy)
        self.manual_mode_button_2.setMinimumSize(QtCore.QSize(0, 40))
        self.manual_mode_button_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.manual_mode_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.manual_mode_button_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.manual_mode_button_2.setCheckable(True)
        self.manual_mode_button_2.setAutoExclusive(True)
        self.manual_mode_button_2.setObjectName("manual_mode_button_2")
        self.horizontalLayout_9.addWidget(self.manual_mode_button_2)
        self.auto_mode_button_2 = ActionButton(self.horizontalWidget_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_mode_button_2.sizePolicy().hasHeightForWidth())
        self.auto_mode_button_2.setSizePolicy(sizePolicy)
        self.auto_mode_button_2.setMinimumSize(QtCore.QSize(0, 40))
        self.auto_mode_button_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.auto_mode_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.auto_mode_button_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.auto_mode_button_2.setCheckable(True)
        self.auto_mode_button_2.setAutoExclusive(True)
        self.auto_mode_button_2.setObjectName("auto_mode_button_2")
        self.horizontalLayout_9.addWidget(self.auto_mode_button_2)
        self.mdi_mode_button_2 = ActionButton(self.horizontalWidget_21)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdi_mode_button_2.sizePolicy().hasHeightForWidth())
        self.mdi_mode_button_2.setSizePolicy(sizePolicy)
        self.mdi_mode_button_2.setMinimumSize(QtCore.QSize(0, 40))
        self.mdi_mode_button_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.mdi_mode_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.mdi_mode_button_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.mdi_mode_button_2.setCheckable(True)
        self.mdi_mode_button_2.setAutoExclusive(True)
        self.mdi_mode_button_2.setObjectName("mdi_mode_button_2")
        self.horizontalLayout_9.addWidget(self.mdi_mode_button_2)
        self.verticalLayout_40.addWidget(self.horizontalWidget_21)
        self.tabWidget_24.addTab(self.tab_17, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.frame_46 = QtWidgets.QFrame(self.tab_2)
        self.frame_46.setGeometry(QtCore.QRect(7, 26, 201, 600))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_46.sizePolicy().hasHeightForWidth())
        self.frame_46.setSizePolicy(sizePolicy)
        self.frame_46.setMinimumSize(QtCore.QSize(201, 600))
        self.frame_46.setStyleSheet(".QFrame{\n"
"    background-color: rgb(51, 57, 59);\n"
"}")
        self.frame_46.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_46.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_46.setObjectName("frame_46")
        self.verticalLayout_43 = QtWidgets.QVBoxLayout(self.frame_46)
        self.verticalLayout_43.setContentsMargins(9, 5, 9, 12)
        self.verticalLayout_43.setSpacing(20)
        self.verticalLayout_43.setObjectName("verticalLayout_43")
        self.widget_6 = QtWidgets.QWidget(self.frame_46)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setStyleSheet("")
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_33.setContentsMargins(3, 9, 2, 6)
        self.horizontalLayout_33.setSpacing(12)
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.vtk_control_buttons_3 = QtWidgets.QWidget(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vtk_control_buttons_3.sizePolicy().hasHeightForWidth())
        self.vtk_control_buttons_3.setSizePolicy(sizePolicy)
        self.vtk_control_buttons_3.setStyleSheet("QWidget{\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton, QComboBox[editable=\"false\"],\n"
"QComboBox[editable=\"true\"]::drop-down {\n"
"    color: white;\n"
"    border-image: url(:/images/pp_border.png);\n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 14pt;\n"
"    min-height: 35px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"/*QPushButton[error=\"true\"] {\n"
"    border-color: red;\n"
"}*/\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.vtk_control_buttons_3.setObjectName("vtk_control_buttons_3")
        self.verticalLayout_151 = QtWidgets.QVBoxLayout(self.vtk_control_buttons_3)
        self.verticalLayout_151.setContentsMargins(1, 15, 0, 10)
        self.verticalLayout_151.setSpacing(9)
        self.verticalLayout_151.setObjectName("verticalLayout_151")
        self.iso_view_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iso_view_button_plot.sizePolicy().hasHeightForWidth())
        self.iso_view_button_plot.setSizePolicy(sizePolicy)
        self.iso_view_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.iso_view_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.iso_view_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.iso_view_button_plot.setStyleSheet("")
        self.iso_view_button_plot.setCheckable(False)
        self.iso_view_button_plot.setObjectName("iso_view_button_plot")
        self.plotviewGroup = QtWidgets.QButtonGroup(Form)
        self.plotviewGroup.setObjectName("plotviewGroup")
        self.plotviewGroup.addButton(self.iso_view_button_plot)
        self.verticalLayout_151.addWidget(self.iso_view_button_plot)
        self.x_view_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.x_view_button_plot.sizePolicy().hasHeightForWidth())
        self.x_view_button_plot.setSizePolicy(sizePolicy)
        self.x_view_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.x_view_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.x_view_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.x_view_button_plot.setStyleSheet("")
        self.x_view_button_plot.setCheckable(False)
        self.x_view_button_plot.setObjectName("x_view_button_plot")
        self.plotviewGroup.addButton(self.x_view_button_plot)
        self.verticalLayout_151.addWidget(self.x_view_button_plot)
        self.y_view_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.y_view_button_plot.sizePolicy().hasHeightForWidth())
        self.y_view_button_plot.setSizePolicy(sizePolicy)
        self.y_view_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.y_view_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.y_view_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.y_view_button_plot.setStyleSheet("")
        self.y_view_button_plot.setCheckable(False)
        self.y_view_button_plot.setObjectName("y_view_button_plot")
        self.plotviewGroup.addButton(self.y_view_button_plot)
        self.verticalLayout_151.addWidget(self.y_view_button_plot)
        self.z_view_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.z_view_button_plot.sizePolicy().hasHeightForWidth())
        self.z_view_button_plot.setSizePolicy(sizePolicy)
        self.z_view_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.z_view_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.z_view_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.z_view_button_plot.setStyleSheet("")
        self.z_view_button_plot.setCheckable(False)
        self.z_view_button_plot.setObjectName("z_view_button_plot")
        self.plotviewGroup.addButton(self.z_view_button_plot)
        self.verticalLayout_151.addWidget(self.z_view_button_plot)
        self.label_65 = QtWidgets.QLabel(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_65.sizePolicy().hasHeightForWidth())
        self.label_65.setSizePolicy(sizePolicy)
        self.label_65.setMinimumSize(QtCore.QSize(75, 0))
        self.label_65.setText("")
        self.label_65.setObjectName("label_65")
        self.verticalLayout_151.addWidget(self.label_65)
        self.zoom_in_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoom_in_button_plot.sizePolicy().hasHeightForWidth())
        self.zoom_in_button_plot.setSizePolicy(sizePolicy)
        self.zoom_in_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.zoom_in_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.zoom_in_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoom_in_button_plot.setStyleSheet("")
        self.zoom_in_button_plot.setCheckable(False)
        self.zoom_in_button_plot.setObjectName("zoom_in_button_plot")
        self.verticalLayout_151.addWidget(self.zoom_in_button_plot)
        self.zoom_out_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zoom_out_button_plot.sizePolicy().hasHeightForWidth())
        self.zoom_out_button_plot.setSizePolicy(sizePolicy)
        self.zoom_out_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.zoom_out_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.zoom_out_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zoom_out_button_plot.setStyleSheet("")
        self.zoom_out_button_plot.setCheckable(False)
        self.zoom_out_button_plot.setObjectName("zoom_out_button_plot")
        self.verticalLayout_151.addWidget(self.zoom_out_button_plot)
        self.label_67 = QtWidgets.QLabel(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_67.sizePolicy().hasHeightForWidth())
        self.label_67.setSizePolicy(sizePolicy)
        self.label_67.setMinimumSize(QtCore.QSize(75, 0))
        self.label_67.setText("")
        self.label_67.setObjectName("label_67")
        self.verticalLayout_151.addWidget(self.label_67)
        self.clear_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clear_button_plot.sizePolicy().hasHeightForWidth())
        self.clear_button_plot.setSizePolicy(sizePolicy)
        self.clear_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.clear_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.clear_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clear_button_plot.setStyleSheet("")
        self.clear_button_plot.setCheckable(False)
        self.clear_button_plot.setObjectName("clear_button_plot")
        self.verticalLayout_151.addWidget(self.clear_button_plot)
        self.label_68 = QtWidgets.QLabel(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_68.sizePolicy().hasHeightForWidth())
        self.label_68.setSizePolicy(sizePolicy)
        self.label_68.setMinimumSize(QtCore.QSize(75, 0))
        self.label_68.setText("")
        self.label_68.setObjectName("label_68")
        self.verticalLayout_151.addWidget(self.label_68)
        self.ortho_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ortho_button_plot.sizePolicy().hasHeightForWidth())
        self.ortho_button_plot.setSizePolicy(sizePolicy)
        self.ortho_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.ortho_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.ortho_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ortho_button_plot.setStyleSheet("")
        self.ortho_button_plot.setCheckable(True)
        self.ortho_button_plot.setChecked(True)
        self.ortho_button_plot.setAutoExclusive(True)
        self.ortho_button_plot.setObjectName("ortho_button_plot")
        self.plotorthoperspbtnGroup = QtWidgets.QButtonGroup(Form)
        self.plotorthoperspbtnGroup.setObjectName("plotorthoperspbtnGroup")
        self.plotorthoperspbtnGroup.addButton(self.ortho_button_plot)
        self.verticalLayout_151.addWidget(self.ortho_button_plot)
        self.perspective_button_plot = QtWidgets.QPushButton(self.vtk_control_buttons_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.perspective_button_plot.sizePolicy().hasHeightForWidth())
        self.perspective_button_plot.setSizePolicy(sizePolicy)
        self.perspective_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.perspective_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.perspective_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.perspective_button_plot.setStyleSheet("")
        self.perspective_button_plot.setCheckable(True)
        self.perspective_button_plot.setAutoExclusive(True)
        self.perspective_button_plot.setObjectName("perspective_button_plot")
        self.plotorthoperspbtnGroup.addButton(self.perspective_button_plot)
        self.verticalLayout_151.addWidget(self.perspective_button_plot)
        self.horizontalLayout_33.addWidget(self.vtk_control_buttons_3)
        self.widget_10 = QtWidgets.QWidget(self.widget_6)
        self.widget_10.setStyleSheet("QWidget{\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton, QComboBox[editable=\"false\"],\n"
"QComboBox[editable=\"true\"]::drop-down {\n"
"    color: white;\n"
"    border-image: url(:/images/pp_border.png);\n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 14pt;\n"
"    min-height: 35px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"/*QPushButton[error=\"true\"] {\n"
"    border-color: red;\n"
"}*/\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.widget_10.setObjectName("widget_10")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.widget_10)
        self.verticalLayout_24.setContentsMargins(0, 15, 0, 12)
        self.verticalLayout_24.setSpacing(9)
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.program_boundry_button = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.program_boundry_button.sizePolicy().hasHeightForWidth())
        self.program_boundry_button.setSizePolicy(sizePolicy)
        self.program_boundry_button.setMinimumSize(QtCore.QSize(75, 39))
        self.program_boundry_button.setMaximumSize(QtCore.QSize(85, 37))
        self.program_boundry_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.program_boundry_button.setStyleSheet("")
        self.program_boundry_button.setCheckable(True)
        self.program_boundry_button.setChecked(False)
        self.program_boundry_button.setAutoExclusive(False)
        self.program_boundry_button.setObjectName("program_boundry_button")
        self.verticalLayout_24.addWidget(self.program_boundry_button)
        self.machine_boundry_button = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_boundry_button.sizePolicy().hasHeightForWidth())
        self.machine_boundry_button.setSizePolicy(sizePolicy)
        self.machine_boundry_button.setMinimumSize(QtCore.QSize(75, 39))
        self.machine_boundry_button.setMaximumSize(QtCore.QSize(85, 37))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(14)
        self.machine_boundry_button.setFont(font)
        self.machine_boundry_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.machine_boundry_button.setStyleSheet("")
        self.machine_boundry_button.setCheckable(True)
        self.machine_boundry_button.setChecked(False)
        self.machine_boundry_button.setObjectName("machine_boundry_button")
        self.verticalLayout_24.addWidget(self.machine_boundry_button)
        self.widget_9 = QtWidgets.QWidget(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_9.sizePolicy().hasHeightForWidth())
        self.widget_9.setSizePolicy(sizePolicy)
        self.widget_9.setMinimumSize(QtCore.QSize(85, 3))
        self.widget_9.setObjectName("widget_9")
        self.verticalLayout_24.addWidget(self.widget_9)
        self.program_ticks_button = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.program_ticks_button.sizePolicy().hasHeightForWidth())
        self.program_ticks_button.setSizePolicy(sizePolicy)
        self.program_ticks_button.setMinimumSize(QtCore.QSize(75, 39))
        self.program_ticks_button.setMaximumSize(QtCore.QSize(85, 37))
        self.program_ticks_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.program_ticks_button.setStyleSheet("")
        self.program_ticks_button.setCheckable(True)
        self.program_ticks_button.setObjectName("program_ticks_button")
        self.verticalLayout_24.addWidget(self.program_ticks_button)
        self.machine_ticks_button = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_ticks_button.sizePolicy().hasHeightForWidth())
        self.machine_ticks_button.setSizePolicy(sizePolicy)
        self.machine_ticks_button.setMinimumSize(QtCore.QSize(75, 39))
        self.machine_ticks_button.setMaximumSize(QtCore.QSize(85, 37))
        self.machine_ticks_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.machine_ticks_button.setStyleSheet("")
        self.machine_ticks_button.setCheckable(True)
        self.machine_ticks_button.setObjectName("machine_ticks_button")
        self.verticalLayout_24.addWidget(self.machine_ticks_button)
        self.widget_12 = QtWidgets.QWidget(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_12.sizePolicy().hasHeightForWidth())
        self.widget_12.setSizePolicy(sizePolicy)
        self.widget_12.setMinimumSize(QtCore.QSize(85, 3))
        self.widget_12.setObjectName("widget_12")
        self.verticalLayout_24.addWidget(self.widget_12)
        self.program_labels_button = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.program_labels_button.sizePolicy().hasHeightForWidth())
        self.program_labels_button.setSizePolicy(sizePolicy)
        self.program_labels_button.setMinimumSize(QtCore.QSize(75, 39))
        self.program_labels_button.setMaximumSize(QtCore.QSize(85, 37))
        self.program_labels_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.program_labels_button.setStyleSheet("")
        self.program_labels_button.setCheckable(True)
        self.program_labels_button.setObjectName("program_labels_button")
        self.verticalLayout_24.addWidget(self.program_labels_button)
        self.machine_labels_button = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_labels_button.sizePolicy().hasHeightForWidth())
        self.machine_labels_button.setSizePolicy(sizePolicy)
        self.machine_labels_button.setMinimumSize(QtCore.QSize(75, 39))
        self.machine_labels_button.setMaximumSize(QtCore.QSize(85, 37))
        self.machine_labels_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.machine_labels_button.setStyleSheet("")
        self.machine_labels_button.setCheckable(True)
        self.machine_labels_button.setObjectName("machine_labels_button")
        self.verticalLayout_24.addWidget(self.machine_labels_button)
        self.widget_14 = QtWidgets.QWidget(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_14.sizePolicy().hasHeightForWidth())
        self.widget_14.setSizePolicy(sizePolicy)
        self.widget_14.setMinimumSize(QtCore.QSize(85, 3))
        self.widget_14.setObjectName("widget_14")
        self.verticalLayout_24.addWidget(self.widget_14)
        self.plot_grid_button = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plot_grid_button.sizePolicy().hasHeightForWidth())
        self.plot_grid_button.setSizePolicy(sizePolicy)
        self.plot_grid_button.setMinimumSize(QtCore.QSize(75, 39))
        self.plot_grid_button.setMaximumSize(QtCore.QSize(85, 37))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(14)
        self.plot_grid_button.setFont(font)
        self.plot_grid_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.plot_grid_button.setStyleSheet("")
        self.plot_grid_button.setCheckable(True)
        self.plot_grid_button.setObjectName("plot_grid_button")
        self.verticalLayout_24.addWidget(self.plot_grid_button)
        self.widget_8 = QtWidgets.QWidget(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy)
        self.widget_8.setMinimumSize(QtCore.QSize(85, 0))
        self.widget_8.setObjectName("widget_8")
        self.verticalLayout_24.addWidget(self.widget_8)
        self.program_zoom_button_plot = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.program_zoom_button_plot.sizePolicy().hasHeightForWidth())
        self.program_zoom_button_plot.setSizePolicy(sizePolicy)
        self.program_zoom_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.program_zoom_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.program_zoom_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.program_zoom_button_plot.setStyleSheet("")
        self.program_zoom_button_plot.setCheckable(False)
        self.program_zoom_button_plot.setObjectName("program_zoom_button_plot")
        self.verticalLayout_24.addWidget(self.program_zoom_button_plot)
        self.machine_zoom_button_plot = QtWidgets.QPushButton(self.widget_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.machine_zoom_button_plot.sizePolicy().hasHeightForWidth())
        self.machine_zoom_button_plot.setSizePolicy(sizePolicy)
        self.machine_zoom_button_plot.setMinimumSize(QtCore.QSize(75, 39))
        self.machine_zoom_button_plot.setMaximumSize(QtCore.QSize(85, 37))
        self.machine_zoom_button_plot.setFocusPolicy(QtCore.Qt.NoFocus)
        self.machine_zoom_button_plot.setStyleSheet("")
        self.machine_zoom_button_plot.setCheckable(False)
        self.machine_zoom_button_plot.setObjectName("machine_zoom_button_plot")
        self.verticalLayout_24.addWidget(self.machine_zoom_button_plot)
        self.horizontalLayout_33.addWidget(self.widget_10)
        self.verticalLayout_43.addWidget(self.widget_6)
        self.horizontalWidget_3 = QtWidgets.QWidget(self.frame_46)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalWidget_3.sizePolicy().hasHeightForWidth())
        self.horizontalWidget_3.setSizePolicy(sizePolicy)
        self.horizontalWidget_3.setMinimumSize(QtCore.QSize(0, 42))
        self.horizontalWidget_3.setMaximumSize(QtCore.QSize(16777215, 42))
        self.horizontalWidget_3.setObjectName("horizontalWidget_3")
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout(self.horizontalWidget_3)
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_32.setSpacing(8)
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.manual_mode_button_3 = ActionButton(self.horizontalWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manual_mode_button_3.sizePolicy().hasHeightForWidth())
        self.manual_mode_button_3.setSizePolicy(sizePolicy)
        self.manual_mode_button_3.setMinimumSize(QtCore.QSize(0, 40))
        self.manual_mode_button_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.manual_mode_button_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.manual_mode_button_3.setCheckable(True)
        self.manual_mode_button_3.setAutoExclusive(True)
        self.manual_mode_button_3.setObjectName("manual_mode_button_3")
        self.horizontalLayout_32.addWidget(self.manual_mode_button_3)
        self.auto_mode_button_3 = ActionButton(self.horizontalWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.auto_mode_button_3.sizePolicy().hasHeightForWidth())
        self.auto_mode_button_3.setSizePolicy(sizePolicy)
        self.auto_mode_button_3.setMinimumSize(QtCore.QSize(0, 40))
        self.auto_mode_button_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.auto_mode_button_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.auto_mode_button_3.setCheckable(True)
        self.auto_mode_button_3.setAutoExclusive(True)
        self.auto_mode_button_3.setObjectName("auto_mode_button_3")
        self.horizontalLayout_32.addWidget(self.auto_mode_button_3)
        self.mdi_mode_button_3 = ActionButton(self.horizontalWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mdi_mode_button_3.sizePolicy().hasHeightForWidth())
        self.mdi_mode_button_3.setSizePolicy(sizePolicy)
        self.mdi_mode_button_3.setMinimumSize(QtCore.QSize(0, 40))
        self.mdi_mode_button_3.setMaximumSize(QtCore.QSize(16777215, 40))
        self.mdi_mode_button_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.mdi_mode_button_3.setCheckable(True)
        self.mdi_mode_button_3.setAutoExclusive(True)
        self.mdi_mode_button_3.setObjectName("mdi_mode_button_3")
        self.horizontalLayout_32.addWidget(self.mdi_mode_button_3)
        self.verticalLayout_43.addWidget(self.horizontalWidget_3)
        self.layoutWidget_3 = QtWidgets.QWidget(self.tab_2)
        self.layoutWidget_3.setGeometry(QtCore.QRect(214, 0, 51, 621))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_23.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_23.setContentsMargins(-1, 2, -1, -1)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.statuslabel_17 = StatusLabel(self.layoutWidget_3)
        self.statuslabel_17.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.statuslabel_17.sizePolicy().hasHeightForWidth())
        self.statuslabel_17.setSizePolicy(sizePolicy)
        self.statuslabel_17.setMinimumSize(QtCore.QSize(40, 0))
        self.statuslabel_17.setMaximumSize(QtCore.QSize(40, 16777215))
        self.statuslabel_17.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_17.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.statuslabel_17.setWordWrap(True)
        self.statuslabel_17.setIndent(0)
        self.statuslabel_17.setProperty("statusItem", "")
        self.statuslabel_17.setObjectName("statuslabel_17")
        self.verticalLayout_23.addWidget(self.statuslabel_17)
        self.statuslabel_18 = StatusLabel(self.layoutWidget_3)
        self.statuslabel_18.setMinimumSize(QtCore.QSize(40, 0))
        self.statuslabel_18.setMaximumSize(QtCore.QSize(40, 16777215))
        self.statuslabel_18.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_18.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.statuslabel_18.setWordWrap(True)
        self.statuslabel_18.setIndent(0)
        self.statuslabel_18.setProperty("statusItem", "")
        self.statuslabel_18.setObjectName("statuslabel_18")
        self.verticalLayout_23.addWidget(self.statuslabel_18)
        self.label_104 = QtWidgets.QLabel(self.tab_2)
        self.label_104.setEnabled(True)
        self.label_104.setGeometry(QtCore.QRect(95, 4, 110, 20))
        self.label_104.setMinimumSize(QtCore.QSize(110, 20))
        self.label_104.setMaximumSize(QtCore.QSize(110, 20))
        self.label_104.setStyleSheet("QLabel{\n"
"    color: white;\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.label_104.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_104.setObjectName("label_104")
        self.tabWidget_24.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget_24)
        self.horizontalLayout_101.addLayout(self.verticalLayout)
        self.verticalLayout_31.addLayout(self.horizontalLayout_101)
        self.main_control_screen_layout_panel = QtWidgets.QHBoxLayout()
        self.main_control_screen_layout_panel.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.main_control_screen_layout_panel.setContentsMargins(12, 0, 12, -1)
        self.main_control_screen_layout_panel.setSpacing(9)
        self.main_control_screen_layout_panel.setObjectName("main_control_screen_layout_panel")
        self.main_control_qframe = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_control_qframe.sizePolicy().hasHeightForWidth())
        self.main_control_qframe.setSizePolicy(sizePolicy)
        self.main_control_qframe.setMinimumSize(QtCore.QSize(350, 340))
        self.main_control_qframe.setStyleSheet(".QFrame{\n"
"    color: rgb(46, 52, 54);\n"
"    border-style: solid;\n"
"    border-color: rgb(186, 189, 182);\n"
"    background-color: rgb(46, 52, 54);\n"
"    border-width: 2px;\n"
"    border-radius: 6px;\n"
"}")
        self.main_control_qframe.setObjectName("main_control_qframe")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.main_control_qframe)
        self.verticalLayout_28.setContentsMargins(18, 9, 18, 4)
        self.verticalLayout_28.setSpacing(6)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.horizontalLayout_92 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_92.setContentsMargins(-1, -1, -1, 4)
        self.horizontalLayout_92.setObjectName("horizontalLayout_92")
        self.actionbutton_3 = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_3.sizePolicy().hasHeightForWidth())
        self.actionbutton_3.setSizePolicy(sizePolicy)
        self.actionbutton_3.setMinimumSize(QtCore.QSize(0, 52))
        self.actionbutton_3.setMaximumSize(QtCore.QSize(16777215, 52))
        self.actionbutton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_3.setStyleSheet("QPushButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_3.setObjectName("actionbutton_3")
        self.horizontalLayout_92.addWidget(self.actionbutton_3)
        self.verticalLayout_28.addLayout(self.horizontalLayout_92)
        self.horizontalLayout_91 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_91.setObjectName("horizontalLayout_91")
        self.actionbutton_7 = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_7.sizePolicy().hasHeightForWidth())
        self.actionbutton_7.setSizePolicy(sizePolicy)
        self.actionbutton_7.setMinimumSize(QtCore.QSize(130, 42))
        self.actionbutton_7.setMaximumSize(QtCore.QSize(130, 42))
        self.actionbutton_7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_7.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_7.setObjectName("actionbutton_7")
        self.horizontalLayout_91.addWidget(self.actionbutton_7)
        self.ref_coilumn_header_13 = QtWidgets.QLabel(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_13.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_13.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_13.setStyleSheet("")
        self.ref_coilumn_header_13.setText("")
        self.ref_coilumn_header_13.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_13.setObjectName("ref_coilumn_header_13")
        self.horizontalLayout_91.addWidget(self.ref_coilumn_header_13)
        self.actionbutton_10 = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_10.sizePolicy().hasHeightForWidth())
        self.actionbutton_10.setSizePolicy(sizePolicy)
        self.actionbutton_10.setMinimumSize(QtCore.QSize(130, 42))
        self.actionbutton_10.setMaximumSize(QtCore.QSize(130, 42))
        self.actionbutton_10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_10.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_10.setCheckable(True)
        self.actionbutton_10.setObjectName("actionbutton_10")
        self.horizontalLayout_91.addWidget(self.actionbutton_10)
        self.verticalLayout_28.addLayout(self.horizontalLayout_91)
        self.horizontalLayout_90 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_90.setObjectName("horizontalLayout_90")
        self.actionbutton = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton.sizePolicy().hasHeightForWidth())
        self.actionbutton.setSizePolicy(sizePolicy)
        self.actionbutton.setMinimumSize(QtCore.QSize(130, 42))
        self.actionbutton.setMaximumSize(QtCore.QSize(130, 42))
        self.actionbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton.setObjectName("actionbutton")
        self.horizontalLayout_90.addWidget(self.actionbutton)
        self.ref_coilumn_header_14 = QtWidgets.QLabel(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_14.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_14.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_14.setStyleSheet("")
        self.ref_coilumn_header_14.setText("")
        self.ref_coilumn_header_14.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_14.setObjectName("ref_coilumn_header_14")
        self.horizontalLayout_90.addWidget(self.ref_coilumn_header_14)
        self.actionbutton_5 = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_5.sizePolicy().hasHeightForWidth())
        self.actionbutton_5.setSizePolicy(sizePolicy)
        self.actionbutton_5.setMinimumSize(QtCore.QSize(130, 42))
        self.actionbutton_5.setMaximumSize(QtCore.QSize(130, 42))
        self.actionbutton_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_5.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_5.setObjectName("actionbutton_5")
        self.horizontalLayout_90.addWidget(self.actionbutton_5)
        self.verticalLayout_28.addLayout(self.horizontalLayout_90)
        self.horizontalLayout_75 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_75.setObjectName("horizontalLayout_75")
        self.actionbutton_9 = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_9.sizePolicy().hasHeightForWidth())
        self.actionbutton_9.setSizePolicy(sizePolicy)
        self.actionbutton_9.setMinimumSize(QtCore.QSize(130, 42))
        self.actionbutton_9.setMaximumSize(QtCore.QSize(130, 42))
        self.actionbutton_9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_9.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_9.setCheckable(True)
        self.actionbutton_9.setObjectName("actionbutton_9")
        self.horizontalLayout_75.addWidget(self.actionbutton_9)
        self.ref_coilumn_header_15 = QtWidgets.QLabel(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_15.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_15.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_15.setStyleSheet("")
        self.ref_coilumn_header_15.setText("")
        self.ref_coilumn_header_15.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_15.setObjectName("ref_coilumn_header_15")
        self.horizontalLayout_75.addWidget(self.ref_coilumn_header_15)
        self.actionbutton_6 = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_6.sizePolicy().hasHeightForWidth())
        self.actionbutton_6.setSizePolicy(sizePolicy)
        self.actionbutton_6.setMinimumSize(QtCore.QSize(130, 42))
        self.actionbutton_6.setMaximumSize(QtCore.QSize(130, 42))
        self.actionbutton_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_6.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_6.setCheckable(True)
        self.actionbutton_6.setObjectName("actionbutton_6")
        self.horizontalLayout_75.addWidget(self.actionbutton_6)
        self.verticalLayout_28.addLayout(self.horizontalLayout_75)
        self.horizontalLayout_88 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_88.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_88.setObjectName("horizontalLayout_88")
        self.actionbutton_8 = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_8.sizePolicy().hasHeightForWidth())
        self.actionbutton_8.setSizePolicy(sizePolicy)
        self.actionbutton_8.setMinimumSize(QtCore.QSize(130, 42))
        self.actionbutton_8.setMaximumSize(QtCore.QSize(130, 42))
        self.actionbutton_8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_8.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_8.setCheckable(True)
        self.actionbutton_8.setObjectName("actionbutton_8")
        self.horizontalLayout_88.addWidget(self.actionbutton_8)
        self.ref_coilumn_header_17 = QtWidgets.QLabel(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_17.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_17.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_17.setStyleSheet("")
        self.ref_coilumn_header_17.setText("")
        self.ref_coilumn_header_17.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_17.setObjectName("ref_coilumn_header_17")
        self.horizontalLayout_88.addWidget(self.ref_coilumn_header_17)
        self.actionbutton_2 = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionbutton_2.sizePolicy().hasHeightForWidth())
        self.actionbutton_2.setSizePolicy(sizePolicy)
        self.actionbutton_2.setMinimumSize(QtCore.QSize(130, 42))
        self.actionbutton_2.setMaximumSize(QtCore.QSize(130, 42))
        self.actionbutton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_2.setCheckable(True)
        self.actionbutton_2.setObjectName("actionbutton_2")
        self.horizontalLayout_88.addWidget(self.actionbutton_2)
        self.verticalLayout_28.addLayout(self.horizontalLayout_88)
        self.line = QtWidgets.QFrame(self.main_control_qframe)
        self.line.setMinimumSize(QtCore.QSize(0, 2))
        self.line.setMaximumSize(QtCore.QSize(16777215, 2))
        self.line.setStyleSheet("Line{\n"
"color:rgb(186, 189, 182);\n"
"border-style: solid;\n"
"border-color: rgb(186, 189, 182);\n"
"background-color: rgb(186, 189, 182);\n"
"border-width: 1px;\n"
"border-radius: 1px;\n"
"}")
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_28.addWidget(self.line)
        self.horizontalLayout_89 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_89.setObjectName("horizontalLayout_89")
        self.power_button = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.power_button.sizePolicy().hasHeightForWidth())
        self.power_button.setSizePolicy(sizePolicy)
        self.power_button.setMinimumSize(QtCore.QSize(75, 35))
        self.power_button.setMaximumSize(QtCore.QSize(75, 35))
        self.power_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.power_button.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.power_button.setCheckable(True)
        self.power_button.setObjectName("power_button")
        self.horizontalLayout_89.addWidget(self.power_button)
        self.ref_coilumn_header_16 = QtWidgets.QLabel(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_16.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_16.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_16.setStyleSheet("")
        self.ref_coilumn_header_16.setText("")
        self.ref_coilumn_header_16.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_16.setObjectName("ref_coilumn_header_16")
        self.horizontalLayout_89.addWidget(self.ref_coilumn_header_16)
        self.widget8 = QtWidgets.QWidget(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget8.sizePolicy().hasHeightForWidth())
        self.widget8.setSizePolicy(sizePolicy)
        self.widget8.setMinimumSize(QtCore.QSize(0, 32))
        self.widget8.setMaximumSize(QtCore.QSize(16777215, 32))
        self.widget8.setObjectName("widget8")
        self.horizontalLayout_40 = QtWidgets.QHBoxLayout(self.widget8)
        self.horizontalLayout_40.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_40.setSpacing(0)
        self.horizontalLayout_40.setObjectName("horizontalLayout_40")
        self.timerhours = HalLabel(self.widget8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerhours.sizePolicy().hasHeightForWidth())
        self.timerhours.setSizePolicy(sizePolicy)
        self.timerhours.setMinimumSize(QtCore.QSize(30, 30))
        self.timerhours.setMaximumSize(QtCore.QSize(30, 30))
        self.timerhours.setStyleSheet("HalLabel {\n"
"    border-style: solid;\n"
"    border-color: silver;\n"
"    border-top-left-radius: 5px;\n"
"    border-bottom-left-radius: 5px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"    border-top-width: 1px;\n"
"    border-bottom-width: 1px;\n"
"    border-right-width: 0px;\n"
"    border-left-width: 1px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 17pt \"Bebas Kai\";\n"
"    padding-left: 5px;\n"
"}")
        self.timerhours.setAlignment(QtCore.Qt.AlignCenter)
        self.timerhours.setProperty("pinType", HalLabel.u32)
        self.timerhours.setObjectName("timerhours")
        self.horizontalLayout_40.addWidget(self.timerhours)
        self.label_2 = QtWidgets.QLabel(self.widget8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(5, 30))
        self.label_2.setMaximumSize(QtCore.QSize(5, 30))
        self.label_2.setStyleSheet("QLabel {\n"
"    border-style: solid;\n"
"    border-color: silver;\n"
"    border-radius: 0px;\n"
"    border-top-width: 1px;\n"
"    border-bottom-width: 1px;\n"
"    border-right-width: 0px;\n"
"    border-left-width: 0px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 17pt \"Bebas Kai\";\n"
"}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_40.addWidget(self.label_2)
        self.timerminutes = HalLabel(self.widget8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerminutes.sizePolicy().hasHeightForWidth())
        self.timerminutes.setSizePolicy(sizePolicy)
        self.timerminutes.setMinimumSize(QtCore.QSize(22, 30))
        self.timerminutes.setMaximumSize(QtCore.QSize(22, 30))
        self.timerminutes.setStyleSheet("HalLabel {\n"
"    border-style: solid;\n"
"    border-color: silver;\n"
"    border-width: 1px;\n"
"    border-radius: 0px;\n"
"    border-top-width: 1px;\n"
"    border-bottom-width: 1px;\n"
"    border-right-width: 0px;\n"
"    border-left-width: 0px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 17pt \"Bebas Kai\";\n"
"}")
        self.timerminutes.setAlignment(QtCore.Qt.AlignCenter)
        self.timerminutes.setProperty("pinType", HalLabel.u32)
        self.timerminutes.setObjectName("timerminutes")
        self.horizontalLayout_40.addWidget(self.timerminutes)
        self.label_3 = QtWidgets.QLabel(self.widget8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(3, 30))
        self.label_3.setMaximumSize(QtCore.QSize(3, 30))
        self.label_3.setStyleSheet("QLabel {\n"
"    border-style: solid;\n"
"    border-color: silver;\n"
"    border-radius: 0px;\n"
"    border-top-width: 1px;\n"
"    border-bottom-width: 1px;\n"
"    border-right-width: 0px;\n"
"    border-left-width: 0px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 17pt \"Bebas Kai\";\n"
"}")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_40.addWidget(self.label_3)
        self.timerseconds = HalLabel(self.widget8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timerseconds.sizePolicy().hasHeightForWidth())
        self.timerseconds.setSizePolicy(sizePolicy)
        self.timerseconds.setMinimumSize(QtCore.QSize(30, 30))
        self.timerseconds.setMaximumSize(QtCore.QSize(30, 30))
        self.timerseconds.setStyleSheet("HalLabel {\n"
"    border-style: solid;\n"
"    border-color: silver;\n"
"    border-width: 1px;\n"
"    border-top-width: 1px;\n"
"    border-bottom-width: 1px;\n"
"    border-right-width: 1px;\n"
"    border-left-width: 0px;\n"
"    border-top-left-radius: 0px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"    color: black;\n"
"    background: white;\n"
"    font: 75 17pt \"Bebas Kai\";\n"
"    padding-right: 5px;\n"
"}")
        self.timerseconds.setAlignment(QtCore.Qt.AlignCenter)
        self.timerseconds.setProperty("pinType", HalLabel.u32)
        self.timerseconds.setObjectName("timerseconds")
        self.horizontalLayout_40.addWidget(self.timerseconds)
        self.horizontalLayout_89.addWidget(self.widget8)
        self.ref_coilumn_header_18 = QtWidgets.QLabel(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_18.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_18.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_18.setStyleSheet("")
        self.ref_coilumn_header_18.setText("")
        self.ref_coilumn_header_18.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_18.setObjectName("ref_coilumn_header_18")
        self.horizontalLayout_89.addWidget(self.ref_coilumn_header_18)
        self.exit_button = ActionButton(self.main_control_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(sizePolicy)
        self.exit_button.setMinimumSize(QtCore.QSize(75, 35))
        self.exit_button.setMaximumSize(QtCore.QSize(75, 35))
        self.exit_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.exit_button.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.exit_button.setCheckable(True)
        self.exit_button.setObjectName("exit_button")
        self.horizontalLayout_89.addWidget(self.exit_button)
        self.verticalLayout_28.addLayout(self.horizontalLayout_89)
        self.main_control_screen_layout_panel.addWidget(self.main_control_qframe)
        self.tool_info_qframe = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_info_qframe.sizePolicy().hasHeightForWidth())
        self.tool_info_qframe.setSizePolicy(sizePolicy)
        self.tool_info_qframe.setMinimumSize(QtCore.QSize(230, 340))
        self.tool_info_qframe.setMaximumSize(QtCore.QSize(230, 340))
        self.tool_info_qframe.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tool_info_qframe.setStyleSheet("")
        self.tool_info_qframe.setObjectName("tool_info_qframe")
        self.verticalLayout_29 = QtWidgets.QVBoxLayout(self.tool_info_qframe)
        self.verticalLayout_29.setContentsMargins(12, 9, 12, 3)
        self.verticalLayout_29.setSpacing(10)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.horizontalLayout_96 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_96.setSpacing(9)
        self.horizontalLayout_96.setObjectName("horizontalLayout_96")
        self.frame_27 = QtWidgets.QFrame(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_27.sizePolicy().hasHeightForWidth())
        self.frame_27.setSizePolicy(sizePolicy)
        self.frame_27.setMinimumSize(QtCore.QSize(0, 38))
        self.frame_27.setMaximumSize(QtCore.QSize(16777215, 38))
        self.frame_27.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179,172);\n"
"    border-width: 1px;\n"
"    border-radius: 4px;\n"
"    background-color: rgb(90, 90, 90);\n"
"    padding: -5px;\n"
"}")
        self.frame_27.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_27.setObjectName("frame_27")
        self.horizontalLayout_105 = QtWidgets.QHBoxLayout(self.frame_27)
        self.horizontalLayout_105.setContentsMargins(0, 0, 1, 0)
        self.horizontalLayout_105.setSpacing(0)
        self.horizontalLayout_105.setObjectName("horizontalLayout_105")
        self.ref_coilumn_header_3 = QtWidgets.QLabel(self.frame_27)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_coilumn_header_3.sizePolicy().hasHeightForWidth())
        self.ref_coilumn_header_3.setSizePolicy(sizePolicy)
        self.ref_coilumn_header_3.setMinimumSize(QtCore.QSize(15, 36))
        self.ref_coilumn_header_3.setMaximumSize(QtCore.QSize(15, 36))
        self.ref_coilumn_header_3.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.ref_coilumn_header_3.setAlignment(QtCore.Qt.AlignCenter)
        self.ref_coilumn_header_3.setIndent(0)
        self.ref_coilumn_header_3.setObjectName("ref_coilumn_header_3")
        self.horizontalLayout_105.addWidget(self.ref_coilumn_header_3)
        self.tool_number_entry_main_panel = VCPLineEdit(self.frame_27)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_number_entry_main_panel.sizePolicy().hasHeightForWidth())
        self.tool_number_entry_main_panel.setSizePolicy(sizePolicy)
        self.tool_number_entry_main_panel.setMinimumSize(QtCore.QSize(55, 0))
        self.tool_number_entry_main_panel.setMaximumSize(QtCore.QSize(55, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 84, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.HighlightedText, brush)
        self.tool_number_entry_main_panel.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.tool_number_entry_main_panel.setFont(font)
        self.tool_number_entry_main_panel.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.tool_number_entry_main_panel.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.tool_number_entry_main_panel.setStyleSheet("font: 17pt;")
        self.tool_number_entry_main_panel.setFrame(True)
        self.tool_number_entry_main_panel.setAlignment(QtCore.Qt.AlignCenter)
        self.tool_number_entry_main_panel.setObjectName("tool_number_entry_main_panel")
        self.horizontalLayout_105.addWidget(self.tool_number_entry_main_panel)
        self.horizontalLayout_96.addWidget(self.frame_27)
        self.m6_tool_call_button_main_panel = SubCallButton(self.tool_info_qframe)
        self.m6_tool_call_button_main_panel.setMinimumSize(QtCore.QSize(70, 40))
        self.m6_tool_call_button_main_panel.setMaximumSize(QtCore.QSize(16777215, 40))
        self.m6_tool_call_button_main_panel.setStyleSheet("QPushButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
"QPushButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 16pt;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
"QPushButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"")
        self.m6_tool_call_button_main_panel.setObjectName("m6_tool_call_button_main_panel")
        self.horizontalLayout_96.addWidget(self.m6_tool_call_button_main_panel)
        self.verticalLayout_29.addLayout(self.horizontalLayout_96)
        self.horizontalLayout_104 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_104.setSpacing(9)
        self.horizontalLayout_104.setObjectName("horizontalLayout_104")
        self.G43 = MDIButton(self.tool_info_qframe)
        self.G43.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.G43.sizePolicy().hasHeightForWidth())
        self.G43.setSizePolicy(sizePolicy)
        self.G43.setMinimumSize(QtCore.QSize(0, 40))
        self.G43.setMaximumSize(QtCore.QSize(16777215, 40))
        self.G43.setFocusPolicy(QtCore.Qt.NoFocus)
        self.G43.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.G43.setCheckable(True)
        self.G43.setAutoExclusive(True)
        self.G43.setObjectName("G43")
        self.horizontalLayout_104.addWidget(self.G43)
        self.G49 = MDIButton(self.tool_info_qframe)
        self.G49.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.G49.sizePolicy().hasHeightForWidth())
        self.G49.setSizePolicy(sizePolicy)
        self.G49.setMinimumSize(QtCore.QSize(0, 40))
        self.G49.setMaximumSize(QtCore.QSize(16777215, 40))
        self.G49.setFocusPolicy(QtCore.Qt.NoFocus)
        self.G49.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.G49.setCheckable(True)
        self.G49.setAutoExclusive(True)
        self.G49.setObjectName("G49")
        self.horizontalLayout_104.addWidget(self.G49)
        self.verticalLayout_29.addLayout(self.horizontalLayout_104)
        self.horizontalLayout_94 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_94.setContentsMargins(-1, -1, 0, -1)
        self.horizontalLayout_94.setSpacing(5)
        self.horizontalLayout_94.setObjectName("horizontalLayout_94")
        self.work_column_header_4 = QtWidgets.QLabel(self.tool_info_qframe)
        self.work_column_header_4.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.work_column_header_4.sizePolicy().hasHeightForWidth())
        self.work_column_header_4.setSizePolicy(sizePolicy)
        self.work_column_header_4.setMinimumSize(QtCore.QSize(60, 33))
        self.work_column_header_4.setMaximumSize(QtCore.QSize(60, 33))
        self.work_column_header_4.setStyleSheet("QLabel{   \n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.work_column_header_4.setAlignment(QtCore.Qt.AlignCenter)
        self.work_column_header_4.setWordWrap(True)
        self.work_column_header_4.setIndent(0)
        self.work_column_header_4.setObjectName("work_column_header_4")
        self.horizontalLayout_94.addWidget(self.work_column_header_4)
        self.tool_length = StatusLabel(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_length.sizePolicy().hasHeightForWidth())
        self.tool_length.setSizePolicy(sizePolicy)
        self.tool_length.setMinimumSize(QtCore.QSize(0, 33))
        self.tool_length.setMaximumSize(QtCore.QSize(16777215, 33))
        self.tool_length.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 17pt \"Bebas Kai\";\n"
"}")
        self.tool_length.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tool_length.setObjectName("tool_length")
        self.horizontalLayout_94.addWidget(self.tool_length)
        self.statuslabel_8 = StatusLabel(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_8.sizePolicy().hasHeightForWidth())
        self.statuslabel_8.setSizePolicy(sizePolicy)
        self.statuslabel_8.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_8.setObjectName("statuslabel_8")
        self.horizontalLayout_94.addWidget(self.statuslabel_8)
        self.verticalLayout_29.addLayout(self.horizontalLayout_94)
        self.horizontalLayout_93 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_93.setSpacing(5)
        self.horizontalLayout_93.setObjectName("horizontalLayout_93")
        self.work_column_header_5 = QtWidgets.QLabel(self.tool_info_qframe)
        self.work_column_header_5.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.work_column_header_5.sizePolicy().hasHeightForWidth())
        self.work_column_header_5.setSizePolicy(sizePolicy)
        self.work_column_header_5.setMinimumSize(QtCore.QSize(60, 33))
        self.work_column_header_5.setMaximumSize(QtCore.QSize(60, 33))
        self.work_column_header_5.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}\n"
"")
        self.work_column_header_5.setAlignment(QtCore.Qt.AlignCenter)
        self.work_column_header_5.setWordWrap(True)
        self.work_column_header_5.setIndent(0)
        self.work_column_header_5.setObjectName("work_column_header_5")
        self.horizontalLayout_93.addWidget(self.work_column_header_5)
        self.tool_diameter = StatusLabel(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tool_diameter.sizePolicy().hasHeightForWidth())
        self.tool_diameter.setSizePolicy(sizePolicy)
        self.tool_diameter.setMinimumSize(QtCore.QSize(0, 33))
        self.tool_diameter.setMaximumSize(QtCore.QSize(16777215, 33))
        self.tool_diameter.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 17pt \"Bebas Kai\";\n"
"}")
        self.tool_diameter.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tool_diameter.setObjectName("tool_diameter")
        self.horizontalLayout_93.addWidget(self.tool_diameter)
        self.statuslabel_11 = StatusLabel(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_11.sizePolicy().hasHeightForWidth())
        self.statuslabel_11.setSizePolicy(sizePolicy)
        self.statuslabel_11.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_11.setObjectName("statuslabel_11")
        self.horizontalLayout_93.addWidget(self.statuslabel_11)
        self.verticalLayout_29.addLayout(self.horizontalLayout_93)
        self.horizontalLayout_95 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_95.setSpacing(9)
        self.horizontalLayout_95.setObjectName("horizontalLayout_95")
        self.go_to_zero_button_2 = SubCallButton(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go_to_zero_button_2.sizePolicy().hasHeightForWidth())
        self.go_to_zero_button_2.setSizePolicy(sizePolicy)
        self.go_to_zero_button_2.setMinimumSize(QtCore.QSize(0, 40))
        self.go_to_zero_button_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.go_to_zero_button_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.go_to_zero_button_2.setStyleSheet(".SubCallButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
".SubCallButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 15pt;\n"
"}\n"
"\n"
".SubCallButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
".SubCallButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
".SubCallButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.go_to_zero_button_2.setObjectName("go_to_zero_button_2")
        self.horizontalLayout_95.addWidget(self.go_to_zero_button_2)
        self.go_to_g30_button = SubCallButton(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go_to_g30_button.sizePolicy().hasHeightForWidth())
        self.go_to_g30_button.setSizePolicy(sizePolicy)
        self.go_to_g30_button.setMinimumSize(QtCore.QSize(0, 40))
        self.go_to_g30_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.go_to_g30_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.go_to_g30_button.setStyleSheet(".SubCallButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
".SubCallButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 15pt;\n"
"}\n"
"\n"
".SubCallButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
".SubCallButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
".SubCallButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.go_to_g30_button.setObjectName("go_to_g30_button")
        self.horizontalLayout_95.addWidget(self.go_to_g30_button)
        self.verticalLayout_29.addLayout(self.horizontalLayout_95)
        self.line_7 = QtWidgets.QFrame(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_7.sizePolicy().hasHeightForWidth())
        self.line_7.setSizePolicy(sizePolicy)
        self.line_7.setMinimumSize(QtCore.QSize(0, 2))
        self.line_7.setMaximumSize(QtCore.QSize(16777215, 2))
        self.line_7.setStyleSheet("Line{\n"
"color:rgb(186, 189, 182);\n"
"border-style: solid;\n"
"border-color: rgb(186, 189, 182);\n"
"background-color: rgb(186, 189, 182);\n"
"border-width: 1px;\n"
"border-radius: 1px;\n"
"}")
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.verticalLayout_29.addWidget(self.line_7)
        self.horizontalLayout_97 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_97.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_97.setSpacing(9)
        self.horizontalLayout_97.setObjectName("horizontalLayout_97")
        self.go_to_home_button = SubCallButton(self.tool_info_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go_to_home_button.sizePolicy().hasHeightForWidth())
        self.go_to_home_button.setSizePolicy(sizePolicy)
        self.go_to_home_button.setMinimumSize(QtCore.QSize(0, 40))
        self.go_to_home_button.setMaximumSize(QtCore.QSize(16777215, 40))
        self.go_to_home_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.go_to_home_button.setStyleSheet(".SubCallButton {\n"
"    color: white;    \n"
"    border-color: black;\n"
"    border-style: solid;\n"
"    border-radius: 5px;\n"
"    border-width: 2px;\n"
"    background: qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(213, 218, 216, 255), stop:0.169312 rgba(82, 82, 83, 255), stop:0.328042 rgba(72, 70, 73, 255), stop:0.492063 rgba(78, 77, 79, 255), stop:0.703704 rgba(72, 70, 73, 255), stop:0.86 rgba(82, 82, 83, 255), stop:1 rgba(213, 218, 216, 255));\n"
"}\n"
"\n"
".SubCallButton {\n"
"    font-family: \"Bebas Kai\";\n"
"    font-size: 15pt;\n"
"}\n"
"\n"
".SubCallButton:disabled {\n"
"    border-color: gray;\n"
"}\n"
"\n"
".SubCallButton:hover {\n"
"    background:  qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                     stop: 0 #A19E9E, stop: 1.0 #5C5959);\n"
"}\n"
"\n"
".SubCallButton:pressed {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked[option=\"true\"] {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}\n"
"\n"
".SubCallButton:checked {\n"
"    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(85, 85, 238, 255), stop:0.544974 rgba(90, 91, 239, 255), stop:1 rgba(126, 135, 243, 255));\n"
"}")
        self.go_to_home_button.setObjectName("go_to_home_button")
        self.horizontalLayout_97.addWidget(self.go_to_home_button)
        self.verticalLayout_29.addLayout(self.horizontalLayout_97)
        self.main_control_screen_layout_panel.addWidget(self.tool_info_qframe)
        self.gui_axis_display_widget = VCPStackedWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gui_axis_display_widget.sizePolicy().hasHeightForWidth())
        self.gui_axis_display_widget.setSizePolicy(sizePolicy)
        self.gui_axis_display_widget.setMinimumSize(QtCore.QSize(486, 340))
        self.gui_axis_display_widget.setMaximumSize(QtCore.QSize(486, 340))
        self.gui_axis_display_widget.setStyleSheet("VCPStackedWidget{\n"
"    padding-left: 6px;\n"
"    padding-right: 6px;\n"
"    padding-top: -1px;\n"
"    padding-bottom:-1px;\n"
"    background-color: rgb(46, 52, 54);\n"
"    border-style: solid;\n"
"    border-color: rgb(186, 189, 182);\n"
"    border-width: 2px;\n"
"    border-radius: 6px;\n"
"}")
        self.gui_axis_display_widget.setObjectName("gui_axis_display_widget")
        self.xyz = QtWidgets.QWidget()
        self.xyz.setObjectName("xyz")
        self.verticalLayout_51 = QtWidgets.QVBoxLayout(self.xyz)
        self.verticalLayout_51.setObjectName("verticalLayout_51")
        self.widget_51 = QtWidgets.QWidget(self.xyz)
        self.widget_51.setObjectName("widget_51")
        self.verticalLayout_55 = QtWidgets.QVBoxLayout(self.widget_51)
        self.verticalLayout_55.setContentsMargins(0, 6, 0, 2)
        self.verticalLayout_55.setSpacing(19)
        self.verticalLayout_55.setObjectName("verticalLayout_55")
        self.horizontalLayout_81 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_81.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_81.setSpacing(8)
        self.horizontalLayout_81.setObjectName("horizontalLayout_81")
        self.frame_42 = QtWidgets.QFrame(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_42.sizePolicy().hasHeightForWidth())
        self.frame_42.setSizePolicy(sizePolicy)
        self.frame_42.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_42.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_42.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179,172);\n"
"    border-width: 1px;\n"
"    border-radius: 4px;\n"
"    background-color: rgb(90, 90, 90);\n"
"    padding: -5px;\n"
"}")
        self.frame_42.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_42.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_42.setObjectName("frame_42")
        self.horizontalLayout_136 = QtWidgets.QHBoxLayout(self.frame_42)
        self.horizontalLayout_136.setContentsMargins(15, -1, 20, -1)
        self.horizontalLayout_136.setSpacing(8)
        self.horizontalLayout_136.setObjectName("horizontalLayout_136")
        self.statuslabel_21 = StatusLabel(self.frame_42)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_21.sizePolicy().hasHeightForWidth())
        self.statuslabel_21.setSizePolicy(sizePolicy)
        self.statuslabel_21.setMinimumSize(QtCore.QSize(60, 17))
        self.statuslabel_21.setMaximumSize(QtCore.QSize(60, 17))
        self.statuslabel_21.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"    padding-left: 1px;\n"
"    padding-right: 20px;\n"
"}")
        self.statuslabel_21.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_21.setObjectName("statuslabel_21")
        self.horizontalLayout_136.addWidget(self.statuslabel_21)
        self.statuslabel_20 = StatusLabel(self.frame_42)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_20.sizePolicy().hasHeightForWidth())
        self.statuslabel_20.setSizePolicy(sizePolicy)
        self.statuslabel_20.setMinimumSize(QtCore.QSize(100, 17))
        self.statuslabel_20.setMaximumSize(QtCore.QSize(100, 17))
        self.statuslabel_20.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"    padding-left: 6px;\n"
"}")
        self.statuslabel_20.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_20.setObjectName("statuslabel_20")
        self.horizontalLayout_136.addWidget(self.statuslabel_20)
        self.work_column_header_8 = QtWidgets.QLabel(self.frame_42)
        self.work_column_header_8.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.work_column_header_8.sizePolicy().hasHeightForWidth())
        self.work_column_header_8.setSizePolicy(sizePolicy)
        self.work_column_header_8.setMinimumSize(QtCore.QSize(100, 17))
        self.work_column_header_8.setMaximumSize(QtCore.QSize(100, 17))
        self.work_column_header_8.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.work_column_header_8.setAlignment(QtCore.Qt.AlignCenter)
        self.work_column_header_8.setObjectName("work_column_header_8")
        self.horizontalLayout_136.addWidget(self.work_column_header_8)
        self.dtg_column_header_3 = QtWidgets.QLabel(self.frame_42)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtg_column_header_3.sizePolicy().hasHeightForWidth())
        self.dtg_column_header_3.setSizePolicy(sizePolicy)
        self.dtg_column_header_3.setMinimumSize(QtCore.QSize(100, 17))
        self.dtg_column_header_3.setMaximumSize(QtCore.QSize(100, 17))
        self.dtg_column_header_3.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.dtg_column_header_3.setAlignment(QtCore.Qt.AlignCenter)
        self.dtg_column_header_3.setObjectName("dtg_column_header_3")
        self.horizontalLayout_136.addWidget(self.dtg_column_header_3)
        self.statuslabel_22 = StatusLabel(self.frame_42)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_22.sizePolicy().hasHeightForWidth())
        self.statuslabel_22.setSizePolicy(sizePolicy)
        self.statuslabel_22.setMinimumSize(QtCore.QSize(40, 17))
        self.statuslabel_22.setMaximumSize(QtCore.QSize(40, 17))
        self.statuslabel_22.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"    padding-left: 6px;\n"
"}")
        self.statuslabel_22.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_22.setObjectName("statuslabel_22")
        self.horizontalLayout_136.addWidget(self.statuslabel_22)
        self.horizontalLayout_81.addWidget(self.frame_42)
        self.verticalLayout_55.addLayout(self.horizontalLayout_81)
        self.x_axis_dro_layout_4 = QtWidgets.QHBoxLayout()
        self.x_axis_dro_layout_4.setContentsMargins(1, 1, 1, 1)
        self.x_axis_dro_layout_4.setSpacing(7)
        self.x_axis_dro_layout_4.setObjectName("x_axis_dro_layout_4")
        self.zero_x_button_5 = MDIButton(self.widget_51)
        self.zero_x_button_5.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_x_button_5.sizePolicy().hasHeightForWidth())
        self.zero_x_button_5.setSizePolicy(sizePolicy)
        self.zero_x_button_5.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_x_button_5.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_x_button_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_x_button_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.zero_x_button_5.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        icon59 = QtGui.QIcon()
        icon59.addPixmap(QtGui.QPixmap(":/images/zero.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.zero_x_button_5.setIcon(icon59)
        self.zero_x_button_5.setIconSize(QtCore.QSize(20, 20))
        self.zero_x_button_5.setObjectName("zero_x_button_5")
        self.x_axis_dro_layout_4.addWidget(self.zero_x_button_5)
        self.statuslabel_101 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_101.sizePolicy().hasHeightForWidth())
        self.statuslabel_101.setSizePolicy(sizePolicy)
        self.statuslabel_101.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_101.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_101.setFont(font)
        self.statuslabel_101.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_101.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_101.setObjectName("statuslabel_101")
        self.x_axis_dro_layout_4.addWidget(self.statuslabel_101)
        self.statuslabel_102 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_102.sizePolicy().hasHeightForWidth())
        self.statuslabel_102.setSizePolicy(sizePolicy)
        self.statuslabel_102.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_102.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_102.setFont(font)
        self.statuslabel_102.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_102.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_102.setObjectName("statuslabel_102")
        self.x_axis_dro_layout_4.addWidget(self.statuslabel_102)
        self.statuslabel_103 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_103.sizePolicy().hasHeightForWidth())
        self.statuslabel_103.setSizePolicy(sizePolicy)
        self.statuslabel_103.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_103.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_103.setFont(font)
        self.statuslabel_103.setMouseTracking(True)
        self.statuslabel_103.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_103.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_103.setObjectName("statuslabel_103")
        self.x_axis_dro_layout_4.addWidget(self.statuslabel_103)
        self.axisactionbutton_13 = ActionButton(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_13.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_13.setSizePolicy(sizePolicy)
        self.axisactionbutton_13.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_13.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_13.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_13.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_13.setObjectName("axisactionbutton_13")
        self.x_axis_dro_layout_4.addWidget(self.axisactionbutton_13)
        self.verticalLayout_55.addLayout(self.x_axis_dro_layout_4)
        self.y_axis_dro_layout_4 = QtWidgets.QHBoxLayout()
        self.y_axis_dro_layout_4.setContentsMargins(1, 1, 1, 1)
        self.y_axis_dro_layout_4.setSpacing(7)
        self.y_axis_dro_layout_4.setObjectName("y_axis_dro_layout_4")
        self.zero_y_button_5 = MDIButton(self.widget_51)
        self.zero_y_button_5.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_y_button_5.sizePolicy().hasHeightForWidth())
        self.zero_y_button_5.setSizePolicy(sizePolicy)
        self.zero_y_button_5.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_y_button_5.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_y_button_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_y_button_5.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_y_button_5.setIcon(icon59)
        self.zero_y_button_5.setIconSize(QtCore.QSize(20, 20))
        self.zero_y_button_5.setObjectName("zero_y_button_5")
        self.y_axis_dro_layout_4.addWidget(self.zero_y_button_5)
        self.statuslabel_92 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_92.sizePolicy().hasHeightForWidth())
        self.statuslabel_92.setSizePolicy(sizePolicy)
        self.statuslabel_92.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_92.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_92.setFont(font)
        self.statuslabel_92.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_92.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_92.setObjectName("statuslabel_92")
        self.y_axis_dro_layout_4.addWidget(self.statuslabel_92)
        self.statuslabel_93 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_93.sizePolicy().hasHeightForWidth())
        self.statuslabel_93.setSizePolicy(sizePolicy)
        self.statuslabel_93.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_93.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_93.setFont(font)
        self.statuslabel_93.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_93.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_93.setObjectName("statuslabel_93")
        self.y_axis_dro_layout_4.addWidget(self.statuslabel_93)
        self.statuslabel_94 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_94.sizePolicy().hasHeightForWidth())
        self.statuslabel_94.setSizePolicy(sizePolicy)
        self.statuslabel_94.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_94.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_94.setFont(font)
        self.statuslabel_94.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_94.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_94.setObjectName("statuslabel_94")
        self.y_axis_dro_layout_4.addWidget(self.statuslabel_94)
        self.axisactionbutton_10 = ActionButton(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_10.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_10.setSizePolicy(sizePolicy)
        self.axisactionbutton_10.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_10.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_10.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_10.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_10.setObjectName("axisactionbutton_10")
        self.y_axis_dro_layout_4.addWidget(self.axisactionbutton_10)
        self.verticalLayout_55.addLayout(self.y_axis_dro_layout_4)
        self.z_axis_dro_layout_4 = QtWidgets.QHBoxLayout()
        self.z_axis_dro_layout_4.setContentsMargins(1, 1, 1, 1)
        self.z_axis_dro_layout_4.setSpacing(7)
        self.z_axis_dro_layout_4.setObjectName("z_axis_dro_layout_4")
        self.zero_z_button_5 = MDIButton(self.widget_51)
        self.zero_z_button_5.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_z_button_5.sizePolicy().hasHeightForWidth())
        self.zero_z_button_5.setSizePolicy(sizePolicy)
        self.zero_z_button_5.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_z_button_5.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_z_button_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_z_button_5.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_z_button_5.setIcon(icon59)
        self.zero_z_button_5.setIconSize(QtCore.QSize(20, 20))
        self.zero_z_button_5.setObjectName("zero_z_button_5")
        self.z_axis_dro_layout_4.addWidget(self.zero_z_button_5)
        self.statuslabel_95 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_95.sizePolicy().hasHeightForWidth())
        self.statuslabel_95.setSizePolicy(sizePolicy)
        self.statuslabel_95.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_95.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_95.setFont(font)
        self.statuslabel_95.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_95.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_95.setObjectName("statuslabel_95")
        self.z_axis_dro_layout_4.addWidget(self.statuslabel_95)
        self.statuslabel_96 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_96.sizePolicy().hasHeightForWidth())
        self.statuslabel_96.setSizePolicy(sizePolicy)
        self.statuslabel_96.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_96.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_96.setFont(font)
        self.statuslabel_96.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_96.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_96.setObjectName("statuslabel_96")
        self.z_axis_dro_layout_4.addWidget(self.statuslabel_96)
        self.statuslabel_97 = StatusLabel(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_97.sizePolicy().hasHeightForWidth())
        self.statuslabel_97.setSizePolicy(sizePolicy)
        self.statuslabel_97.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_97.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_97.setFont(font)
        self.statuslabel_97.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_97.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_97.setObjectName("statuslabel_97")
        self.z_axis_dro_layout_4.addWidget(self.statuslabel_97)
        self.axisactionbutton_11 = ActionButton(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_11.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_11.setSizePolicy(sizePolicy)
        self.axisactionbutton_11.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_11.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_11.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_11.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_11.setObjectName("axisactionbutton_11")
        self.z_axis_dro_layout_4.addWidget(self.axisactionbutton_11)
        self.verticalLayout_55.addLayout(self.z_axis_dro_layout_4)
        self.horizontalLayout_102 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_102.setContentsMargins(3, 1, 3, 1)
        self.horizontalLayout_102.setSpacing(20)
        self.horizontalLayout_102.setObjectName("horizontalLayout_102")
        self.zero_all_button_4 = MDIButton(self.widget_51)
        self.zero_all_button_4.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_all_button_4.sizePolicy().hasHeightForWidth())
        self.zero_all_button_4.setSizePolicy(sizePolicy)
        self.zero_all_button_4.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_all_button_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.zero_all_button_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_all_button_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.zero_all_button_4.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.zero_all_button_4.setIconSize(QtCore.QSize(20, 20))
        self.zero_all_button_4.setObjectName("zero_all_button_4")
        self.horizontalLayout_102.addWidget(self.zero_all_button_4)
        self.ref_all_button_4 = ActionButton(self.widget_51)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_all_button_4.sizePolicy().hasHeightForWidth())
        self.ref_all_button_4.setSizePolicy(sizePolicy)
        self.ref_all_button_4.setMinimumSize(QtCore.QSize(62, 40))
        self.ref_all_button_4.setMaximumSize(QtCore.QSize(16777215, 40))
        self.ref_all_button_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ref_all_button_4.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.ref_all_button_4.setObjectName("ref_all_button_4")
        self.horizontalLayout_102.addWidget(self.ref_all_button_4)
        self.verticalLayout_55.addLayout(self.horizontalLayout_102)
        self.verticalLayout_51.addWidget(self.widget_51)
        self.gui_axis_display_widget.addWidget(self.xyz)
        self.xyza = QtWidgets.QWidget()
        self.xyza.setObjectName("xyza")
        self.verticalLayout_54 = QtWidgets.QVBoxLayout(self.xyza)
        self.verticalLayout_54.setObjectName("verticalLayout_54")
        self.widget_52 = QtWidgets.QWidget(self.xyza)
        self.widget_52.setObjectName("widget_52")
        self.verticalLayout_56 = QtWidgets.QVBoxLayout(self.widget_52)
        self.verticalLayout_56.setContentsMargins(0, 6, 0, 2)
        self.verticalLayout_56.setSpacing(5)
        self.verticalLayout_56.setObjectName("verticalLayout_56")
        self.horizontalLayout_77 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_77.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_77.setSpacing(8)
        self.horizontalLayout_77.setObjectName("horizontalLayout_77")
        self.frame_43 = QtWidgets.QFrame(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_43.sizePolicy().hasHeightForWidth())
        self.frame_43.setSizePolicy(sizePolicy)
        self.frame_43.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_43.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_43.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179,172);\n"
"    border-width: 1px;\n"
"    border-radius: 4px;\n"
"    background-color: rgb(90, 90, 90);\n"
"    padding: -5px;\n"
"}")
        self.frame_43.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_43.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_43.setObjectName("frame_43")
        self.horizontalLayout_144 = QtWidgets.QHBoxLayout(self.frame_43)
        self.horizontalLayout_144.setContentsMargins(15, -1, 20, -1)
        self.horizontalLayout_144.setSpacing(8)
        self.horizontalLayout_144.setObjectName("horizontalLayout_144")
        self.statuslabel_23 = StatusLabel(self.frame_43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_23.sizePolicy().hasHeightForWidth())
        self.statuslabel_23.setSizePolicy(sizePolicy)
        self.statuslabel_23.setMinimumSize(QtCore.QSize(60, 17))
        self.statuslabel_23.setMaximumSize(QtCore.QSize(60, 17))
        self.statuslabel_23.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"    padding-left: 1px;\n"
"    padding-right: 20px;\n"
"}")
        self.statuslabel_23.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_23.setObjectName("statuslabel_23")
        self.horizontalLayout_144.addWidget(self.statuslabel_23)
        self.statuslabel_24 = StatusLabel(self.frame_43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_24.sizePolicy().hasHeightForWidth())
        self.statuslabel_24.setSizePolicy(sizePolicy)
        self.statuslabel_24.setMinimumSize(QtCore.QSize(100, 17))
        self.statuslabel_24.setMaximumSize(QtCore.QSize(100, 17))
        self.statuslabel_24.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"    padding-left: 6px;\n"
"}")
        self.statuslabel_24.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_24.setObjectName("statuslabel_24")
        self.horizontalLayout_144.addWidget(self.statuslabel_24)
        self.work_column_header_9 = QtWidgets.QLabel(self.frame_43)
        self.work_column_header_9.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.work_column_header_9.sizePolicy().hasHeightForWidth())
        self.work_column_header_9.setSizePolicy(sizePolicy)
        self.work_column_header_9.setMinimumSize(QtCore.QSize(100, 17))
        self.work_column_header_9.setMaximumSize(QtCore.QSize(100, 17))
        self.work_column_header_9.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.work_column_header_9.setAlignment(QtCore.Qt.AlignCenter)
        self.work_column_header_9.setObjectName("work_column_header_9")
        self.horizontalLayout_144.addWidget(self.work_column_header_9)
        self.dtg_column_header_4 = QtWidgets.QLabel(self.frame_43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtg_column_header_4.sizePolicy().hasHeightForWidth())
        self.dtg_column_header_4.setSizePolicy(sizePolicy)
        self.dtg_column_header_4.setMinimumSize(QtCore.QSize(100, 17))
        self.dtg_column_header_4.setMaximumSize(QtCore.QSize(100, 17))
        self.dtg_column_header_4.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.dtg_column_header_4.setAlignment(QtCore.Qt.AlignCenter)
        self.dtg_column_header_4.setObjectName("dtg_column_header_4")
        self.horizontalLayout_144.addWidget(self.dtg_column_header_4)
        self.statuslabel_25 = StatusLabel(self.frame_43)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_25.sizePolicy().hasHeightForWidth())
        self.statuslabel_25.setSizePolicy(sizePolicy)
        self.statuslabel_25.setMinimumSize(QtCore.QSize(40, 17))
        self.statuslabel_25.setMaximumSize(QtCore.QSize(40, 17))
        self.statuslabel_25.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"    padding-left: 6px;\n"
"}")
        self.statuslabel_25.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_25.setObjectName("statuslabel_25")
        self.horizontalLayout_144.addWidget(self.statuslabel_25)
        self.horizontalLayout_77.addWidget(self.frame_43)
        self.verticalLayout_56.addLayout(self.horizontalLayout_77)
        self.x_axis_dro_layout_2 = QtWidgets.QHBoxLayout()
        self.x_axis_dro_layout_2.setContentsMargins(1, 1, 1, 1)
        self.x_axis_dro_layout_2.setSpacing(7)
        self.x_axis_dro_layout_2.setObjectName("x_axis_dro_layout_2")
        self.zero_x_button_4 = MDIButton(self.widget_52)
        self.zero_x_button_4.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_x_button_4.sizePolicy().hasHeightForWidth())
        self.zero_x_button_4.setSizePolicy(sizePolicy)
        self.zero_x_button_4.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_x_button_4.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_x_button_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_x_button_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.zero_x_button_4.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_x_button_4.setIcon(icon59)
        self.zero_x_button_4.setIconSize(QtCore.QSize(20, 20))
        self.zero_x_button_4.setObjectName("zero_x_button_4")
        self.x_axis_dro_layout_2.addWidget(self.zero_x_button_4)
        self.statuslabel_89 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_89.sizePolicy().hasHeightForWidth())
        self.statuslabel_89.setSizePolicy(sizePolicy)
        self.statuslabel_89.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_89.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_89.setFont(font)
        self.statuslabel_89.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_89.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_89.setObjectName("statuslabel_89")
        self.x_axis_dro_layout_2.addWidget(self.statuslabel_89)
        self.statuslabel_90 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_90.sizePolicy().hasHeightForWidth())
        self.statuslabel_90.setSizePolicy(sizePolicy)
        self.statuslabel_90.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_90.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_90.setFont(font)
        self.statuslabel_90.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_90.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_90.setObjectName("statuslabel_90")
        self.x_axis_dro_layout_2.addWidget(self.statuslabel_90)
        self.statuslabel_91 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_91.sizePolicy().hasHeightForWidth())
        self.statuslabel_91.setSizePolicy(sizePolicy)
        self.statuslabel_91.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_91.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_91.setFont(font)
        self.statuslabel_91.setMouseTracking(True)
        self.statuslabel_91.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_91.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_91.setObjectName("statuslabel_91")
        self.x_axis_dro_layout_2.addWidget(self.statuslabel_91)
        self.axisactionbutton_9 = ActionButton(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_9.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_9.setSizePolicy(sizePolicy)
        self.axisactionbutton_9.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_9.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_9.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_9.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_9.setObjectName("axisactionbutton_9")
        self.x_axis_dro_layout_2.addWidget(self.axisactionbutton_9)
        self.verticalLayout_56.addLayout(self.x_axis_dro_layout_2)
        self.y_axis_dro_layout_2 = QtWidgets.QHBoxLayout()
        self.y_axis_dro_layout_2.setContentsMargins(1, 1, 1, 1)
        self.y_axis_dro_layout_2.setSpacing(7)
        self.y_axis_dro_layout_2.setObjectName("y_axis_dro_layout_2")
        self.zero_y_button_4 = MDIButton(self.widget_52)
        self.zero_y_button_4.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_y_button_4.sizePolicy().hasHeightForWidth())
        self.zero_y_button_4.setSizePolicy(sizePolicy)
        self.zero_y_button_4.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_y_button_4.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_y_button_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_y_button_4.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_y_button_4.setIcon(icon59)
        self.zero_y_button_4.setIconSize(QtCore.QSize(20, 20))
        self.zero_y_button_4.setObjectName("zero_y_button_4")
        self.y_axis_dro_layout_2.addWidget(self.zero_y_button_4)
        self.statuslabel_80 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_80.sizePolicy().hasHeightForWidth())
        self.statuslabel_80.setSizePolicy(sizePolicy)
        self.statuslabel_80.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_80.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_80.setFont(font)
        self.statuslabel_80.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_80.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_80.setObjectName("statuslabel_80")
        self.y_axis_dro_layout_2.addWidget(self.statuslabel_80)
        self.statuslabel_81 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_81.sizePolicy().hasHeightForWidth())
        self.statuslabel_81.setSizePolicy(sizePolicy)
        self.statuslabel_81.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_81.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_81.setFont(font)
        self.statuslabel_81.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_81.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_81.setObjectName("statuslabel_81")
        self.y_axis_dro_layout_2.addWidget(self.statuslabel_81)
        self.statuslabel_82 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_82.sizePolicy().hasHeightForWidth())
        self.statuslabel_82.setSizePolicy(sizePolicy)
        self.statuslabel_82.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_82.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_82.setFont(font)
        self.statuslabel_82.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_82.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_82.setObjectName("statuslabel_82")
        self.y_axis_dro_layout_2.addWidget(self.statuslabel_82)
        self.axisactionbutton_5 = ActionButton(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_5.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_5.setSizePolicy(sizePolicy)
        self.axisactionbutton_5.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_5.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_5.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_5.setObjectName("axisactionbutton_5")
        self.y_axis_dro_layout_2.addWidget(self.axisactionbutton_5)
        self.verticalLayout_56.addLayout(self.y_axis_dro_layout_2)
        self.z_axis_dro_layout_2 = QtWidgets.QHBoxLayout()
        self.z_axis_dro_layout_2.setContentsMargins(1, 1, 1, 1)
        self.z_axis_dro_layout_2.setSpacing(7)
        self.z_axis_dro_layout_2.setObjectName("z_axis_dro_layout_2")
        self.zero_z_button_4 = MDIButton(self.widget_52)
        self.zero_z_button_4.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_z_button_4.sizePolicy().hasHeightForWidth())
        self.zero_z_button_4.setSizePolicy(sizePolicy)
        self.zero_z_button_4.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_z_button_4.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_z_button_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_z_button_4.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_z_button_4.setIcon(icon59)
        self.zero_z_button_4.setIconSize(QtCore.QSize(20, 20))
        self.zero_z_button_4.setObjectName("zero_z_button_4")
        self.z_axis_dro_layout_2.addWidget(self.zero_z_button_4)
        self.statuslabel_83 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_83.sizePolicy().hasHeightForWidth())
        self.statuslabel_83.setSizePolicy(sizePolicy)
        self.statuslabel_83.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_83.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_83.setFont(font)
        self.statuslabel_83.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_83.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_83.setObjectName("statuslabel_83")
        self.z_axis_dro_layout_2.addWidget(self.statuslabel_83)
        self.statuslabel_84 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_84.sizePolicy().hasHeightForWidth())
        self.statuslabel_84.setSizePolicy(sizePolicy)
        self.statuslabel_84.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_84.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_84.setFont(font)
        self.statuslabel_84.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_84.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_84.setObjectName("statuslabel_84")
        self.z_axis_dro_layout_2.addWidget(self.statuslabel_84)
        self.statuslabel_85 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_85.sizePolicy().hasHeightForWidth())
        self.statuslabel_85.setSizePolicy(sizePolicy)
        self.statuslabel_85.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_85.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_85.setFont(font)
        self.statuslabel_85.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_85.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_85.setObjectName("statuslabel_85")
        self.z_axis_dro_layout_2.addWidget(self.statuslabel_85)
        self.axisactionbutton_7 = ActionButton(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_7.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_7.setSizePolicy(sizePolicy)
        self.axisactionbutton_7.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_7.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_7.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_7.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_7.setObjectName("axisactionbutton_7")
        self.z_axis_dro_layout_2.addWidget(self.axisactionbutton_7)
        self.verticalLayout_56.addLayout(self.z_axis_dro_layout_2)
        self.a_axis_dro_layout_2 = QtWidgets.QHBoxLayout()
        self.a_axis_dro_layout_2.setContentsMargins(1, 1, 1, 1)
        self.a_axis_dro_layout_2.setSpacing(7)
        self.a_axis_dro_layout_2.setObjectName("a_axis_dro_layout_2")
        self.zero_a_button_4 = MDIButton(self.widget_52)
        self.zero_a_button_4.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_a_button_4.sizePolicy().hasHeightForWidth())
        self.zero_a_button_4.setSizePolicy(sizePolicy)
        self.zero_a_button_4.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_a_button_4.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_a_button_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_a_button_4.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_a_button_4.setIcon(icon59)
        self.zero_a_button_4.setIconSize(QtCore.QSize(20, 20))
        self.zero_a_button_4.setObjectName("zero_a_button_4")
        self.a_axis_dro_layout_2.addWidget(self.zero_a_button_4)
        self.statuslabel_86 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_86.sizePolicy().hasHeightForWidth())
        self.statuslabel_86.setSizePolicy(sizePolicy)
        self.statuslabel_86.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_86.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_86.setFont(font)
        self.statuslabel_86.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_86.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_86.setObjectName("statuslabel_86")
        self.a_axis_dro_layout_2.addWidget(self.statuslabel_86)
        self.statuslabel_87 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_87.sizePolicy().hasHeightForWidth())
        self.statuslabel_87.setSizePolicy(sizePolicy)
        self.statuslabel_87.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_87.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_87.setFont(font)
        self.statuslabel_87.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_87.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_87.setObjectName("statuslabel_87")
        self.a_axis_dro_layout_2.addWidget(self.statuslabel_87)
        self.statuslabel_88 = StatusLabel(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_88.sizePolicy().hasHeightForWidth())
        self.statuslabel_88.setSizePolicy(sizePolicy)
        self.statuslabel_88.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_88.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_88.setFont(font)
        self.statuslabel_88.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_88.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_88.setObjectName("statuslabel_88")
        self.a_axis_dro_layout_2.addWidget(self.statuslabel_88)
        self.axisactionbutton_8 = ActionButton(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_8.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_8.setSizePolicy(sizePolicy)
        self.axisactionbutton_8.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_8.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_8.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_8.setObjectName("axisactionbutton_8")
        self.a_axis_dro_layout_2.addWidget(self.axisactionbutton_8)
        self.verticalLayout_56.addLayout(self.a_axis_dro_layout_2)
        self.horizontalLayout_140 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_140.setContentsMargins(3, 3, 3, 1)
        self.horizontalLayout_140.setSpacing(20)
        self.horizontalLayout_140.setObjectName("horizontalLayout_140")
        self.zero_all_button_5 = MDIButton(self.widget_52)
        self.zero_all_button_5.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_all_button_5.sizePolicy().hasHeightForWidth())
        self.zero_all_button_5.setSizePolicy(sizePolicy)
        self.zero_all_button_5.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_all_button_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.zero_all_button_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_all_button_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.zero_all_button_5.setStyleSheet("MDIButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.zero_all_button_5.setIconSize(QtCore.QSize(20, 20))
        self.zero_all_button_5.setObjectName("zero_all_button_5")
        self.horizontalLayout_140.addWidget(self.zero_all_button_5)
        self.ref_all_button_5 = ActionButton(self.widget_52)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_all_button_5.sizePolicy().hasHeightForWidth())
        self.ref_all_button_5.setSizePolicy(sizePolicy)
        self.ref_all_button_5.setMinimumSize(QtCore.QSize(62, 40))
        self.ref_all_button_5.setMaximumSize(QtCore.QSize(16777215, 40))
        self.ref_all_button_5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ref_all_button_5.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.ref_all_button_5.setObjectName("ref_all_button_5")
        self.horizontalLayout_140.addWidget(self.ref_all_button_5)
        self.verticalLayout_56.addLayout(self.horizontalLayout_140)
        self.verticalLayout_54.addWidget(self.widget_52)
        self.gui_axis_display_widget.addWidget(self.xyza)
        self.xyzab = QtWidgets.QWidget()
        self.xyzab.setObjectName("xyzab")
        self.verticalLayout_57 = QtWidgets.QVBoxLayout(self.xyzab)
        self.verticalLayout_57.setObjectName("verticalLayout_57")
        self.widget_53 = QtWidgets.QWidget(self.xyzab)
        self.widget_53.setObjectName("widget_53")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_53)
        self.verticalLayout_4.setContentsMargins(0, 6, 0, 1)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_58 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_58.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_58.setSpacing(7)
        self.horizontalLayout_58.setObjectName("horizontalLayout_58")
        self.zero_all_button = MDIButton(self.widget_53)
        self.zero_all_button.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_all_button.sizePolicy().hasHeightForWidth())
        self.zero_all_button.setSizePolicy(sizePolicy)
        self.zero_all_button.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_all_button.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_all_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_all_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.zero_all_button.setStyleSheet("MDIButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.zero_all_button.setIcon(icon59)
        self.zero_all_button.setIconSize(QtCore.QSize(20, 20))
        self.zero_all_button.setObjectName("zero_all_button")
        self.horizontalLayout_58.addWidget(self.zero_all_button)
        self.frame_25 = QtWidgets.QFrame(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_25.sizePolicy().hasHeightForWidth())
        self.frame_25.setSizePolicy(sizePolicy)
        self.frame_25.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_25.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_25.setStyleSheet(".QFrame{\n"
"    border-style: solid;\n"
"    border-color: rgb(176, 179,172);\n"
"    border-width: 1px;\n"
"    border-radius: 4px;\n"
"    background-color: rgb(90, 90, 90);\n"
"    padding: -5px;\n"
"}")
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.horizontalLayout_103 = QtWidgets.QHBoxLayout(self.frame_25)
        self.horizontalLayout_103.setContentsMargins(5, -1, 7, -1)
        self.horizontalLayout_103.setSpacing(8)
        self.horizontalLayout_103.setObjectName("horizontalLayout_103")
        self.statuslabel_12 = StatusLabel(self.frame_25)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_12.sizePolicy().hasHeightForWidth())
        self.statuslabel_12.setSizePolicy(sizePolicy)
        self.statuslabel_12.setMinimumSize(QtCore.QSize(100, 17))
        self.statuslabel_12.setMaximumSize(QtCore.QSize(100, 17))
        self.statuslabel_12.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"    padding-left: 6px;\n"
"}")
        self.statuslabel_12.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_12.setObjectName("statuslabel_12")
        self.horizontalLayout_103.addWidget(self.statuslabel_12)
        self.work_column_header_2 = QtWidgets.QLabel(self.frame_25)
        self.work_column_header_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.work_column_header_2.sizePolicy().hasHeightForWidth())
        self.work_column_header_2.setSizePolicy(sizePolicy)
        self.work_column_header_2.setMinimumSize(QtCore.QSize(100, 17))
        self.work_column_header_2.setMaximumSize(QtCore.QSize(100, 17))
        self.work_column_header_2.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.work_column_header_2.setAlignment(QtCore.Qt.AlignCenter)
        self.work_column_header_2.setObjectName("work_column_header_2")
        self.horizontalLayout_103.addWidget(self.work_column_header_2)
        self.dtg_column_header = QtWidgets.QLabel(self.frame_25)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dtg_column_header.sizePolicy().hasHeightForWidth())
        self.dtg_column_header.setSizePolicy(sizePolicy)
        self.dtg_column_header.setMinimumSize(QtCore.QSize(100, 17))
        self.dtg_column_header.setMaximumSize(QtCore.QSize(100, 17))
        self.dtg_column_header.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 16pt \"Bebas Kai\";\n"
"}")
        self.dtg_column_header.setAlignment(QtCore.Qt.AlignCenter)
        self.dtg_column_header.setObjectName("dtg_column_header")
        self.horizontalLayout_103.addWidget(self.dtg_column_header)
        self.horizontalLayout_58.addWidget(self.frame_25)
        self.ref_all_button = ActionButton(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ref_all_button.sizePolicy().hasHeightForWidth())
        self.ref_all_button.setSizePolicy(sizePolicy)
        self.ref_all_button.setMinimumSize(QtCore.QSize(62, 40))
        self.ref_all_button.setMaximumSize(QtCore.QSize(62, 40))
        self.ref_all_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.ref_all_button.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.ref_all_button.setObjectName("ref_all_button")
        self.horizontalLayout_58.addWidget(self.ref_all_button)
        self.verticalLayout_4.addLayout(self.horizontalLayout_58)
        self.x_axis_dro_layout = QtWidgets.QHBoxLayout()
        self.x_axis_dro_layout.setContentsMargins(1, 1, 1, 1)
        self.x_axis_dro_layout.setSpacing(7)
        self.x_axis_dro_layout.setObjectName("x_axis_dro_layout")
        self.zero_x_button_3 = MDIButton(self.widget_53)
        self.zero_x_button_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_x_button_3.sizePolicy().hasHeightForWidth())
        self.zero_x_button_3.setSizePolicy(sizePolicy)
        self.zero_x_button_3.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_x_button_3.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_x_button_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_x_button_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.zero_x_button_3.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_x_button_3.setIcon(icon59)
        self.zero_x_button_3.setIconSize(QtCore.QSize(20, 20))
        self.zero_x_button_3.setObjectName("zero_x_button_3")
        self.x_axis_dro_layout.addWidget(self.zero_x_button_3)
        self.statuslabel_40 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_40.sizePolicy().hasHeightForWidth())
        self.statuslabel_40.setSizePolicy(sizePolicy)
        self.statuslabel_40.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_40.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_40.setFont(font)
        self.statuslabel_40.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_40.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_40.setObjectName("statuslabel_40")
        self.x_axis_dro_layout.addWidget(self.statuslabel_40)
        self.statuslabel_45 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_45.sizePolicy().hasHeightForWidth())
        self.statuslabel_45.setSizePolicy(sizePolicy)
        self.statuslabel_45.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_45.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_45.setFont(font)
        self.statuslabel_45.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_45.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_45.setObjectName("statuslabel_45")
        self.x_axis_dro_layout.addWidget(self.statuslabel_45)
        self.statuslabel_75 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_75.sizePolicy().hasHeightForWidth())
        self.statuslabel_75.setSizePolicy(sizePolicy)
        self.statuslabel_75.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_75.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_75.setFont(font)
        self.statuslabel_75.setMouseTracking(True)
        self.statuslabel_75.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_75.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_75.setObjectName("statuslabel_75")
        self.x_axis_dro_layout.addWidget(self.statuslabel_75)
        self.axisactionbutton_6 = ActionButton(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_6.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_6.setSizePolicy(sizePolicy)
        self.axisactionbutton_6.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_6.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_6.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_6.setObjectName("axisactionbutton_6")
        self.x_axis_dro_layout.addWidget(self.axisactionbutton_6)
        self.verticalLayout_4.addLayout(self.x_axis_dro_layout)
        self.y_axis_dro_layout = QtWidgets.QHBoxLayout()
        self.y_axis_dro_layout.setContentsMargins(1, 1, 1, 1)
        self.y_axis_dro_layout.setSpacing(7)
        self.y_axis_dro_layout.setObjectName("y_axis_dro_layout")
        self.zero_y_button_3 = MDIButton(self.widget_53)
        self.zero_y_button_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_y_button_3.sizePolicy().hasHeightForWidth())
        self.zero_y_button_3.setSizePolicy(sizePolicy)
        self.zero_y_button_3.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_y_button_3.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_y_button_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_y_button_3.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_y_button_3.setIcon(icon59)
        self.zero_y_button_3.setIconSize(QtCore.QSize(20, 20))
        self.zero_y_button_3.setObjectName("zero_y_button_3")
        self.y_axis_dro_layout.addWidget(self.zero_y_button_3)
        self.statuslabel_41 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_41.sizePolicy().hasHeightForWidth())
        self.statuslabel_41.setSizePolicy(sizePolicy)
        self.statuslabel_41.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_41.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_41.setFont(font)
        self.statuslabel_41.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_41.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_41.setObjectName("statuslabel_41")
        self.y_axis_dro_layout.addWidget(self.statuslabel_41)
        self.statuslabel_46 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_46.sizePolicy().hasHeightForWidth())
        self.statuslabel_46.setSizePolicy(sizePolicy)
        self.statuslabel_46.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_46.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_46.setFont(font)
        self.statuslabel_46.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_46.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_46.setObjectName("statuslabel_46")
        self.y_axis_dro_layout.addWidget(self.statuslabel_46)
        self.statuslabel_76 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_76.sizePolicy().hasHeightForWidth())
        self.statuslabel_76.setSizePolicy(sizePolicy)
        self.statuslabel_76.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_76.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_76.setFont(font)
        self.statuslabel_76.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_76.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_76.setObjectName("statuslabel_76")
        self.y_axis_dro_layout.addWidget(self.statuslabel_76)
        self.axisactionbutton_3 = ActionButton(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_3.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_3.setSizePolicy(sizePolicy)
        self.axisactionbutton_3.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_3.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_3.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_3.setObjectName("axisactionbutton_3")
        self.y_axis_dro_layout.addWidget(self.axisactionbutton_3)
        self.verticalLayout_4.addLayout(self.y_axis_dro_layout)
        self.z_axis_dro_layout = QtWidgets.QHBoxLayout()
        self.z_axis_dro_layout.setContentsMargins(1, 1, 1, -1)
        self.z_axis_dro_layout.setSpacing(7)
        self.z_axis_dro_layout.setObjectName("z_axis_dro_layout")
        self.zero_z_button_3 = MDIButton(self.widget_53)
        self.zero_z_button_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_z_button_3.sizePolicy().hasHeightForWidth())
        self.zero_z_button_3.setSizePolicy(sizePolicy)
        self.zero_z_button_3.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_z_button_3.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_z_button_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_z_button_3.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_z_button_3.setIcon(icon59)
        self.zero_z_button_3.setIconSize(QtCore.QSize(20, 20))
        self.zero_z_button_3.setObjectName("zero_z_button_3")
        self.z_axis_dro_layout.addWidget(self.zero_z_button_3)
        self.statuslabel_42 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_42.sizePolicy().hasHeightForWidth())
        self.statuslabel_42.setSizePolicy(sizePolicy)
        self.statuslabel_42.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_42.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_42.setFont(font)
        self.statuslabel_42.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_42.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_42.setObjectName("statuslabel_42")
        self.z_axis_dro_layout.addWidget(self.statuslabel_42)
        self.statuslabel_47 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_47.sizePolicy().hasHeightForWidth())
        self.statuslabel_47.setSizePolicy(sizePolicy)
        self.statuslabel_47.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_47.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_47.setFont(font)
        self.statuslabel_47.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_47.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_47.setObjectName("statuslabel_47")
        self.z_axis_dro_layout.addWidget(self.statuslabel_47)
        self.statuslabel_77 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_77.sizePolicy().hasHeightForWidth())
        self.statuslabel_77.setSizePolicy(sizePolicy)
        self.statuslabel_77.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_77.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_77.setFont(font)
        self.statuslabel_77.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_77.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_77.setObjectName("statuslabel_77")
        self.z_axis_dro_layout.addWidget(self.statuslabel_77)
        self.axisactionbutton = ActionButton(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton.sizePolicy().hasHeightForWidth())
        self.axisactionbutton.setSizePolicy(sizePolicy)
        self.axisactionbutton.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton.setObjectName("axisactionbutton")
        self.z_axis_dro_layout.addWidget(self.axisactionbutton)
        self.verticalLayout_4.addLayout(self.z_axis_dro_layout)
        self.a_axis_dro_layout = QtWidgets.QHBoxLayout()
        self.a_axis_dro_layout.setContentsMargins(1, 1, 1, 1)
        self.a_axis_dro_layout.setSpacing(7)
        self.a_axis_dro_layout.setObjectName("a_axis_dro_layout")
        self.zero_a_button_3 = MDIButton(self.widget_53)
        self.zero_a_button_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_a_button_3.sizePolicy().hasHeightForWidth())
        self.zero_a_button_3.setSizePolicy(sizePolicy)
        self.zero_a_button_3.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_a_button_3.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_a_button_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_a_button_3.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_a_button_3.setIcon(icon59)
        self.zero_a_button_3.setIconSize(QtCore.QSize(20, 20))
        self.zero_a_button_3.setObjectName("zero_a_button_3")
        self.a_axis_dro_layout.addWidget(self.zero_a_button_3)
        self.statuslabel_43 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_43.sizePolicy().hasHeightForWidth())
        self.statuslabel_43.setSizePolicy(sizePolicy)
        self.statuslabel_43.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_43.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_43.setFont(font)
        self.statuslabel_43.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_43.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_43.setObjectName("statuslabel_43")
        self.a_axis_dro_layout.addWidget(self.statuslabel_43)
        self.statuslabel_48 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_48.sizePolicy().hasHeightForWidth())
        self.statuslabel_48.setSizePolicy(sizePolicy)
        self.statuslabel_48.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_48.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_48.setFont(font)
        self.statuslabel_48.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_48.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_48.setObjectName("statuslabel_48")
        self.a_axis_dro_layout.addWidget(self.statuslabel_48)
        self.statuslabel_78 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_78.sizePolicy().hasHeightForWidth())
        self.statuslabel_78.setSizePolicy(sizePolicy)
        self.statuslabel_78.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_78.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_78.setFont(font)
        self.statuslabel_78.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_78.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_78.setObjectName("statuslabel_78")
        self.a_axis_dro_layout.addWidget(self.statuslabel_78)
        self.axisactionbutton_2 = ActionButton(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_2.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_2.setSizePolicy(sizePolicy)
        self.axisactionbutton_2.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_2.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_2.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_2.setObjectName("axisactionbutton_2")
        self.a_axis_dro_layout.addWidget(self.axisactionbutton_2)
        self.verticalLayout_4.addLayout(self.a_axis_dro_layout)
        self.b_axis_dro_layout = QtWidgets.QHBoxLayout()
        self.b_axis_dro_layout.setContentsMargins(1, 1, 1, 1)
        self.b_axis_dro_layout.setSpacing(7)
        self.b_axis_dro_layout.setObjectName("b_axis_dro_layout")
        self.zero_b_button_3 = MDIButton(self.widget_53)
        self.zero_b_button_3.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zero_b_button_3.sizePolicy().hasHeightForWidth())
        self.zero_b_button_3.setSizePolicy(sizePolicy)
        self.zero_b_button_3.setMinimumSize(QtCore.QSize(60, 40))
        self.zero_b_button_3.setMaximumSize(QtCore.QSize(60, 40))
        self.zero_b_button_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.zero_b_button_3.setStyleSheet("MDIButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.zero_b_button_3.setIcon(icon59)
        self.zero_b_button_3.setIconSize(QtCore.QSize(20, 20))
        self.zero_b_button_3.setObjectName("zero_b_button_3")
        self.b_axis_dro_layout.addWidget(self.zero_b_button_3)
        self.statuslabel_44 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_44.sizePolicy().hasHeightForWidth())
        self.statuslabel_44.setSizePolicy(sizePolicy)
        self.statuslabel_44.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_44.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_44.setFont(font)
        self.statuslabel_44.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_44.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_44.setObjectName("statuslabel_44")
        self.b_axis_dro_layout.addWidget(self.statuslabel_44)
        self.statuslabel_49 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_49.sizePolicy().hasHeightForWidth())
        self.statuslabel_49.setSizePolicy(sizePolicy)
        self.statuslabel_49.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_49.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_49.setFont(font)
        self.statuslabel_49.setStyleSheet("StatusLabel{\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"    padding-right: 2px;\n"
"}\n"
"\n"
"StatusLabel[style=\"unhomed\"]{\n"
"   color: red;\n"
"}\n"
"\n"
"StatusLabel[style=\"homing\"]{\n"
"   color: rgb(196, 160, 0);\n"
"}")
        self.statuslabel_49.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_49.setObjectName("statuslabel_49")
        self.b_axis_dro_layout.addWidget(self.statuslabel_49)
        self.statuslabel_79 = StatusLabel(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_79.sizePolicy().hasHeightForWidth())
        self.statuslabel_79.setSizePolicy(sizePolicy)
        self.statuslabel_79.setMinimumSize(QtCore.QSize(100, 35))
        self.statuslabel_79.setMaximumSize(QtCore.QSize(100, 35))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(17)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.statuslabel_79.setFont(font)
        self.statuslabel_79.setStyleSheet("StatusLabel{\n"
"    border-style: transparant;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    padding-right: 2px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_79.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_79.setObjectName("statuslabel_79")
        self.b_axis_dro_layout.addWidget(self.statuslabel_79)
        self.axisactionbutton_4 = ActionButton(self.widget_53)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.axisactionbutton_4.sizePolicy().hasHeightForWidth())
        self.axisactionbutton_4.setSizePolicy(sizePolicy)
        self.axisactionbutton_4.setMinimumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_4.setMaximumSize(QtCore.QSize(62, 40))
        self.axisactionbutton_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.axisactionbutton_4.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"}")
        self.axisactionbutton_4.setObjectName("axisactionbutton_4")
        self.b_axis_dro_layout.addWidget(self.axisactionbutton_4)
        self.verticalLayout_4.addLayout(self.b_axis_dro_layout)
        self.verticalLayout_57.addWidget(self.widget_53)
        self.gui_axis_display_widget.addWidget(self.xyzab)
        self.main_control_screen_layout_panel.addWidget(self.gui_axis_display_widget)
        self.main_override_tool_qframe = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_override_tool_qframe.sizePolicy().hasHeightForWidth())
        self.main_override_tool_qframe.setSizePolicy(sizePolicy)
        self.main_override_tool_qframe.setMinimumSize(QtCore.QSize(370, 340))
        self.main_override_tool_qframe.setFocusPolicy(QtCore.Qt.NoFocus)
        self.main_override_tool_qframe.setStyleSheet(".QFrame{\n"
"    padding-left: 7px;\n"
"    padding-right: 7px;\n"
"}")
        self.main_override_tool_qframe.setObjectName("main_override_tool_qframe")
        self.gridLayout = QtWidgets.QGridLayout(self.main_override_tool_qframe)
        self.gridLayout.setContentsMargins(-1, 11, -1, 2)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(13)
        self.gridLayout.setObjectName("gridLayout")
        self.statuslabel = StatusLabel(self.main_override_tool_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel.sizePolicy().hasHeightForWidth())
        self.statuslabel.setSizePolicy(sizePolicy)
        self.statuslabel.setMinimumSize(QtCore.QSize(55, 36))
        self.statuslabel.setMaximumSize(QtCore.QSize(55, 36))
        self.statuslabel.setToolTipDuration(-3)
        self.statuslabel.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel.setLineWidth(0)
        self.statuslabel.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel.setIndent(0)
        self.statuslabel.setObjectName("statuslabel")
        self.gridLayout.addWidget(self.statuslabel, 2, 1, 1, 1)
        self.actionslider_4 = ActionSlider(self.main_override_tool_qframe)
        self.actionslider_4.setMinimumSize(QtCore.QSize(0, 50))
        self.actionslider_4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionslider_4.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 #66e, stop: 1 #bbf);\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 #bbf, stop: 1 #55f);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: rgb(235, 235, 235);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #777;\n"
"border-color: rgba(40, 40, 40, 255);\n"
"width: 40px;\n"
"margin-top: -13px;\n"
"margin-bottom: -13px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #444;\n"
"border-color: rgb(241, 239, 237);\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.actionslider_4.setOrientation(QtCore.Qt.Horizontal)
        self.actionslider_4.setObjectName("actionslider_4")
        self.gridLayout.addWidget(self.actionslider_4, 5, 0, 1, 1)
        self.statuslabel_2 = StatusLabel(self.main_override_tool_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_2.sizePolicy().hasHeightForWidth())
        self.statuslabel_2.setSizePolicy(sizePolicy)
        self.statuslabel_2.setMinimumSize(QtCore.QSize(55, 36))
        self.statuslabel_2.setMaximumSize(QtCore.QSize(55, 36))
        self.statuslabel_2.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_2.setLineWidth(0)
        self.statuslabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_2.setIndent(0)
        self.statuslabel_2.setObjectName("statuslabel_2")
        self.gridLayout.addWidget(self.statuslabel_2, 4, 1, 1, 1)
        self.statuslabel_3 = StatusLabel(self.main_override_tool_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_3.sizePolicy().hasHeightForWidth())
        self.statuslabel_3.setSizePolicy(sizePolicy)
        self.statuslabel_3.setMinimumSize(QtCore.QSize(55, 36))
        self.statuslabel_3.setMaximumSize(QtCore.QSize(55, 36))
        self.statuslabel_3.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_3.setLineWidth(0)
        self.statuslabel_3.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_3.setIndent(0)
        self.statuslabel_3.setObjectName("statuslabel_3")
        self.gridLayout.addWidget(self.statuslabel_3, 5, 1, 1, 1)
        self.work_column_header_3 = QtWidgets.QLabel(self.main_override_tool_qframe)
        self.work_column_header_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.work_column_header_3.sizePolicy().hasHeightForWidth())
        self.work_column_header_3.setSizePolicy(sizePolicy)
        self.work_column_header_3.setMinimumSize(QtCore.QSize(65, 40))
        self.work_column_header_3.setMaximumSize(QtCore.QSize(65, 40))
        self.work_column_header_3.setStyleSheet("QLabel{\n"
"color: white;\n"
"border-style: solid;\n"
"border-color: rgb(176, 179,172);\n"
"border-width: 1px;\n"
"border-radius: 4px;\n"
"background-color: rgb(90, 90, 90);\n"
"font: 13pt \"Bebas Kai\";\n"
"}")
        self.work_column_header_3.setLineWidth(0)
        self.work_column_header_3.setAlignment(QtCore.Qt.AlignCenter)
        self.work_column_header_3.setWordWrap(False)
        self.work_column_header_3.setIndent(0)
        self.work_column_header_3.setObjectName("work_column_header_3")
        self.gridLayout.addWidget(self.work_column_header_3, 0, 2, 1, 1)
        self.loadmeter = LoadMeter(self.main_override_tool_qframe)
        self.loadmeter.setMinimumSize(QtCore.QSize(0, 25))
        self.loadmeter.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setFamily("Bebas Kai")
        font.setPointSize(14)
        self.loadmeter.setFont(font)
        self.loadmeter.setStyleSheet("")
        self.loadmeter.setMaximum(150)
        self.loadmeter.setProperty("value", 150)
        self.loadmeter.setProperty("barGradient", ['0.0, 170, 170, 236', '0.63, 85, 85, 238', '0.65, 171, 171, 158', '0.79, 227, 237, 106', '0.84, 219, 124, 55', '1.0, 209, 0, 0'])
        self.loadmeter.setObjectName("loadmeter")
        self.gridLayout.addWidget(self.loadmeter, 0, 0, 1, 2)
        self.max_vel_slider = StatusLabel(self.main_override_tool_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.max_vel_slider.sizePolicy().hasHeightForWidth())
        self.max_vel_slider.setSizePolicy(sizePolicy)
        self.max_vel_slider.setMinimumSize(QtCore.QSize(55, 36))
        self.max_vel_slider.setMaximumSize(QtCore.QSize(55, 36))
        self.max_vel_slider.setToolTipDuration(-1)
        self.max_vel_slider.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 14pt \"Bebas Kai\";\n"
"}")
        self.max_vel_slider.setLineWidth(0)
        self.max_vel_slider.setAlignment(QtCore.Qt.AlignCenter)
        self.max_vel_slider.setIndent(0)
        self.max_vel_slider.setObjectName("max_vel_slider")
        self.gridLayout.addWidget(self.max_vel_slider, 1, 1, 1, 1)
        self.actionslider = ActionSlider(self.main_override_tool_qframe)
        self.actionslider.setMinimumSize(QtCore.QSize(0, 50))
        self.actionslider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionslider.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 #66e, stop: 1 #bbf);\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 #bbf, stop: 1 #55f);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: rgb(235, 235, 235);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #777;\n"
"border-color: rgba(40, 40, 40, 255);\n"
"width: 40px;\n"
"margin-top: -13px;\n"
"margin-bottom: -13px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #444;\n"
"border-color: rgb(241, 239, 237);\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.actionslider.setOrientation(QtCore.Qt.Horizontal)
        self.actionslider.setObjectName("actionslider")
        self.gridLayout.addWidget(self.actionslider, 4, 0, 1, 1)
        self.actionbutton_28 = ActionButton(self.main_override_tool_qframe)
        self.actionbutton_28.setMinimumSize(QtCore.QSize(65, 40))
        self.actionbutton_28.setMaximumSize(QtCore.QSize(65, 40))
        self.actionbutton_28.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_28.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_28.setObjectName("actionbutton_28")
        self.gridLayout.addWidget(self.actionbutton_28, 4, 2, 1, 1)
        self.actionslider_2 = ActionSlider(self.main_override_tool_qframe)
        self.actionslider_2.setMinimumSize(QtCore.QSize(0, 50))
        self.actionslider_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionslider_2.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 #66e, stop: 1 #bbf);\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 #bbf, stop: 1 #55f);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: rgb(235, 235, 235);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #777;\n"
"border-color: rgba(40, 40, 40, 255);\n"
"width: 40px;\n"
"margin-top: -13px;\n"
"margin-bottom: -13px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #444;\n"
"border-color: rgb(241, 239, 237);\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.actionslider_2.setMaximum(100)
        self.actionslider_2.setOrientation(QtCore.Qt.Horizontal)
        self.actionslider_2.setObjectName("actionslider_2")
        self.gridLayout.addWidget(self.actionslider_2, 2, 0, 1, 1)
        self.actionslider_3 = ActionSlider(self.main_override_tool_qframe)
        self.actionslider_3.setMinimumSize(QtCore.QSize(0, 50))
        self.actionslider_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionslider_3.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 #66e, stop: 1 #bbf);\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 #bbf, stop: 1 #55f);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: rgb(235, 235, 235);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #777;\n"
"border-color: rgba(40, 40, 40, 255);\n"
"width: 40px;\n"
"margin-top: -13px;\n"
"margin-bottom: -13px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #444;\n"
"border-color: rgb(241, 239, 237);\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.actionslider_3.setOrientation(QtCore.Qt.Horizontal)
        self.actionslider_3.setObjectName("actionslider_3")
        self.gridLayout.addWidget(self.actionslider_3, 1, 0, 1, 1)
        self.actionbutton_29 = ActionButton(self.main_override_tool_qframe)
        self.actionbutton_29.setMinimumSize(QtCore.QSize(65, 40))
        self.actionbutton_29.setMaximumSize(QtCore.QSize(65, 40))
        self.actionbutton_29.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_29.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_29.setObjectName("actionbutton_29")
        self.gridLayout.addWidget(self.actionbutton_29, 2, 2, 1, 1)
        self.actionbutton_30 = ActionButton(self.main_override_tool_qframe)
        self.actionbutton_30.setMinimumSize(QtCore.QSize(65, 40))
        self.actionbutton_30.setMaximumSize(QtCore.QSize(65, 40))
        self.actionbutton_30.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_30.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_30.setObjectName("actionbutton_30")
        self.gridLayout.addWidget(self.actionbutton_30, 1, 2, 1, 1)
        self.actionbutton_31 = ActionButton(self.main_override_tool_qframe)
        self.actionbutton_31.setMinimumSize(QtCore.QSize(65, 40))
        self.actionbutton_31.setMaximumSize(QtCore.QSize(65, 40))
        self.actionbutton_31.setFocusPolicy(QtCore.Qt.NoFocus)
        self.actionbutton_31.setStyleSheet("QPushButton {\n"
"       font: 14pt \"Bebas Kai\";\n"
"}")
        self.actionbutton_31.setObjectName("actionbutton_31")
        self.gridLayout.addWidget(self.actionbutton_31, 5, 2, 1, 1)
        self.main_control_screen_layout_panel.addWidget(self.main_override_tool_qframe)
        self.jog_and_spindle_qframe = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jog_and_spindle_qframe.sizePolicy().hasHeightForWidth())
        self.jog_and_spindle_qframe.setSizePolicy(sizePolicy)
        self.jog_and_spindle_qframe.setMinimumSize(QtCore.QSize(380, 340))
        self.jog_and_spindle_qframe.setMaximumSize(QtCore.QSize(380, 16777215))
        self.jog_and_spindle_qframe.setFocusPolicy(QtCore.Qt.NoFocus)
        self.jog_and_spindle_qframe.setStyleSheet("")
        self.jog_and_spindle_qframe.setObjectName("jog_and_spindle_qframe")
        self.verticalLayout_27 = QtWidgets.QVBoxLayout(self.jog_and_spindle_qframe)
        self.verticalLayout_27.setContentsMargins(15, 10, 15, 3)
        self.verticalLayout_27.setSpacing(12)
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.horizontalLayout_83 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_83.setSpacing(16)
        self.horizontalLayout_83.setObjectName("horizontalLayout_83")
        self.jogincrement = JogIncrementWidget(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jogincrement.sizePolicy().hasHeightForWidth())
        self.jogincrement.setSizePolicy(sizePolicy)
        self.jogincrement.setMinimumSize(QtCore.QSize(0, 42))
        self.jogincrement.setMaximumSize(QtCore.QSize(16777215, 42))
        self.jogincrement.setStyleSheet("QPushButton {\n"
"       font: 15pt \"Bebas Kai\";\n"
"\n"
"}\n"
"\n"
"")
        self.jogincrement.setProperty("diameter", 0)
        self.jogincrement.setObjectName("jogincrement")
        self.horizontalLayout_83.addWidget(self.jogincrement)
        self.verticalLayout_27.addLayout(self.horizontalLayout_83)
        self.horizontalLayout_84 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_84.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_84.setSpacing(15)
        self.horizontalLayout_84.setObjectName("horizontalLayout_84")
        self.settings_slider = VCPSettingsSlider(self.jog_and_spindle_qframe)
        self.settings_slider.setMinimumSize(QtCore.QSize(0, 50))
        self.settings_slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.settings_slider.setStyleSheet("QSlider::groove:horizontal {\n"
"border: 1px solid #bbb;\n"
"background: white;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal {\n"
"background: qlineargradient(x1: 0, y1: 0,    x2: 0, y2: 1,\n"
"    stop: 0 #66e, stop: 1 #bbf);\n"
"background: qlineargradient(x1: 0, y1: 0.2, x2: 1, y2: 1,\n"
"    stop: 0 #bbf, stop: 1 #55f);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal {\n"
"background: rgb(235, 235, 235);\n"
"border: 1px solid #777;\n"
"height: 20px;\n"
"border-radius: 3px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #777;\n"
"border-color: rgba(40, 40, 40, 255);\n"
"width: 40px;\n"
"margin-top: -13px;\n"
"margin-bottom: -13px;\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:hover {\n"
"background: qlineargradient(spread:reflect, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:0.1 rgba(60, 60, 60, 255), stop:0.21 rgba(60, 60, 60, 255), stop:0.25 rgba(255, 255, 255, 255), stop:0.29 rgba(60, 60, 60, 255), stop:0.46 rgba(60, 60, 60, 255), stop:0.5 rgba(255, 255, 255, 255), stop:0.54 rgba(60, 60, 60, 255), stop:0.71 rgba(60, 60, 60, 255), stop:0.75 rgba(255, 255, 255, 255), stop:0.79 rgba(60, 60, 60, 255), stop:0.9 rgba(60, 60, 60, 255), stop:1 rgba(255, 255, 255, 255));\n"
"border: 1px solid #444;\n"
"border-color: rgb(241, 239, 237);\n"
"border-radius: 4px;\n"
"}\n"
"\n"
"QSlider::sub-page:horizontal:disabled {\n"
"background: #bbb;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::add-page:horizontal:disabled {\n"
"background: #eee;\n"
"border-color: #999;\n"
"}\n"
"\n"
"QSlider::handle:horizontal:disabled {\n"
"background: #eee;\n"
"border: 1px solid #aaa;\n"
"border-radius: 4px;\n"
"}")
        self.settings_slider.setMinimum(0)
        self.settings_slider.setMaximum(100)
        self.settings_slider.setProperty("value", 50)
        self.settings_slider.setSliderPosition(50)
        self.settings_slider.setOrientation(QtCore.Qt.Horizontal)
        self.settings_slider.setObjectName("settings_slider")
        self.horizontalLayout_84.addWidget(self.settings_slider)
        self.fr_override_dro_2 = StatusLabel(self.jog_and_spindle_qframe)
        self.fr_override_dro_2.setMinimumSize(QtCore.QSize(48, 38))
        self.fr_override_dro_2.setMaximumSize(QtCore.QSize(48, 38))
        self.fr_override_dro_2.setStyleSheet("StatusLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 75 15pt \"Bebas Kai\";\n"
"}")
        self.fr_override_dro_2.setAlignment(QtCore.Qt.AlignCenter)
        self.fr_override_dro_2.setObjectName("fr_override_dro_2")
        self.horizontalLayout_84.addWidget(self.fr_override_dro_2)
        self.verticalLayout_27.addLayout(self.horizontalLayout_84)
        self.horizontalLayout_85 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_85.setSpacing(0)
        self.horizontalLayout_85.setObjectName("horizontalLayout_85")
        self.statuslabel_6 = StatusLabel(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_6.sizePolicy().hasHeightForWidth())
        self.statuslabel_6.setSizePolicy(sizePolicy)
        self.statuslabel_6.setMinimumSize(QtCore.QSize(105, 38))
        self.statuslabel_6.setMaximumSize(QtCore.QSize(105, 38))
        self.statuslabel_6.setStyleSheet("QLabel {\n"
"    border-style: solid;\n"
"    border-color: rgb(96, 96, 97);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"    background: rgb(86, 86, 87);\n"
"    font: 50 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_6.setObjectName("statuslabel_6")
        self.horizontalLayout_85.addWidget(self.statuslabel_6)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_85.addItem(spacerItem)
        self.frame_30 = QtWidgets.QFrame(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_30.sizePolicy().hasHeightForWidth())
        self.frame_30.setSizePolicy(sizePolicy)
        self.frame_30.setMaximumSize(QtCore.QSize(16777215, 38))
        self.frame_30.setStyleSheet("QFrame {\n"
"    border: none;\n"
"}")
        self.frame_30.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_30.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_30.setLineWidth(0)
        self.frame_30.setObjectName("frame_30")
        self.horizontalLayout_110 = QtWidgets.QHBoxLayout(self.frame_30)
        self.horizontalLayout_110.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_110.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_110.setSpacing(0)
        self.horizontalLayout_110.setObjectName("horizontalLayout_110")
        self.rpm_label_3 = QtWidgets.QLabel(self.frame_30)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rpm_label_3.sizePolicy().hasHeightForWidth())
        self.rpm_label_3.setSizePolicy(sizePolicy)
        self.rpm_label_3.setMaximumSize(QtCore.QSize(16777215, 30))
        self.rpm_label_3.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.rpm_label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.rpm_label_3.setWordWrap(False)
        self.rpm_label_3.setIndent(0)
        self.rpm_label_3.setObjectName("rpm_label_3")
        self.horizontalLayout_110.addWidget(self.rpm_label_3)
        self.rpm_label_4 = QtWidgets.QLabel(self.frame_30)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rpm_label_4.sizePolicy().hasHeightForWidth())
        self.rpm_label_4.setSizePolicy(sizePolicy)
        self.rpm_label_4.setMinimumSize(QtCore.QSize(5, 30))
        self.rpm_label_4.setMaximumSize(QtCore.QSize(5, 16777215))
        self.rpm_label_4.setStyleSheet("QLabel{\n"
"    border: none;\n"
"    color: rgb(238, 238, 236);\n"
"    background: transparent;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.rpm_label_4.setText("")
        self.rpm_label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.rpm_label_4.setWordWrap(True)
        self.rpm_label_4.setIndent(0)
        self.rpm_label_4.setObjectName("rpm_label_4")
        self.horizontalLayout_110.addWidget(self.rpm_label_4)
        self.statuslabel_10 = StatusLabel(self.frame_30)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_10.sizePolicy().hasHeightForWidth())
        self.statuslabel_10.setSizePolicy(sizePolicy)
        self.statuslabel_10.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_10.setAlignment(QtCore.Qt.AlignCenter)
        self.statuslabel_10.setIndent(0)
        self.statuslabel_10.setProperty("fromat", "")
        self.statuslabel_10.setObjectName("statuslabel_10")
        self.horizontalLayout_110.addWidget(self.statuslabel_10)
        self.work_column_header_7 = QtWidgets.QLabel(self.frame_30)
        self.work_column_header_7.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.work_column_header_7.sizePolicy().hasHeightForWidth())
        self.work_column_header_7.setSizePolicy(sizePolicy)
        self.work_column_header_7.setMaximumSize(QtCore.QSize(16777215, 30))
        self.work_column_header_7.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.work_column_header_7.setAlignment(QtCore.Qt.AlignCenter)
        self.work_column_header_7.setWordWrap(False)
        self.work_column_header_7.setIndent(0)
        self.work_column_header_7.setObjectName("work_column_header_7")
        self.horizontalLayout_110.addWidget(self.work_column_header_7)
        self.horizontalLayout_85.addWidget(self.frame_30)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_85.addItem(spacerItem1)
        self.statuslabel_7 = StatusLabel(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_7.sizePolicy().hasHeightForWidth())
        self.statuslabel_7.setSizePolicy(sizePolicy)
        self.statuslabel_7.setMinimumSize(QtCore.QSize(105, 38))
        self.statuslabel_7.setMaximumSize(QtCore.QSize(105, 38))
        self.statuslabel_7.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_7.setObjectName("statuslabel_7")
        self.horizontalLayout_85.addWidget(self.statuslabel_7)
        self.verticalLayout_27.addLayout(self.horizontalLayout_85)
        self.line_2 = QtWidgets.QFrame(self.jog_and_spindle_qframe)
        self.line_2.setMinimumSize(QtCore.QSize(0, 2))
        self.line_2.setMaximumSize(QtCore.QSize(16777215, 2))
        self.line_2.setStyleSheet("Line{\n"
"color:rgb(186, 189, 182);\n"
"border-style: solid;\n"
"border-color: rgb(186, 189, 182);\n"
"background-color: rgb(186, 189, 182);\n"
"border-width: 1px;\n"
"border-radius: 1px;\n"
"}")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_27.addWidget(self.line_2)
        self.horizontalLayout_87 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_87.setSpacing(0)
        self.horizontalLayout_87.setObjectName("horizontalLayout_87")
        self.statuslabel_5 = StatusLabel(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_5.sizePolicy().hasHeightForWidth())
        self.statuslabel_5.setSizePolicy(sizePolicy)
        self.statuslabel_5.setMinimumSize(QtCore.QSize(105, 38))
        self.statuslabel_5.setMaximumSize(QtCore.QSize(105, 38))
        self.statuslabel_5.setStyleSheet("QLabel {\n"
"    border-style: solid;\n"
"    border-color: rgb(96, 96, 97);\n"
"    border-width: 2px;\n"
"    border-radius: 5px;\n"
"    color: white;\n"
"    background: rgb(86, 86, 87);\n"
"    font: 50 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_5.setObjectName("statuslabel_5")
        self.horizontalLayout_87.addWidget(self.statuslabel_5)
        self.rpm_label = QtWidgets.QLabel(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rpm_label.sizePolicy().hasHeightForWidth())
        self.rpm_label.setSizePolicy(sizePolicy)
        self.rpm_label.setMaximumSize(QtCore.QSize(16777215, 38))
        self.rpm_label.setStyleSheet("QLabel{\n"
"    color: rgb(238, 238, 236);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.rpm_label.setAlignment(QtCore.Qt.AlignCenter)
        self.rpm_label.setWordWrap(False)
        self.rpm_label.setIndent(0)
        self.rpm_label.setObjectName("rpm_label")
        self.horizontalLayout_87.addWidget(self.rpm_label)
        self.statuslabel_9 = StatusLabel(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statuslabel_9.sizePolicy().hasHeightForWidth())
        self.statuslabel_9.setSizePolicy(sizePolicy)
        self.statuslabel_9.setMinimumSize(QtCore.QSize(105, 38))
        self.statuslabel_9.setMaximumSize(QtCore.QSize(105, 38))
        self.statuslabel_9.setStyleSheet("QLabel {\n"
"    border-style: transparent;\n"
"    border-color: rgb(235, 235, 235);\n"
"    border-width: 1px;\n"
"    border-radius: 5px;\n"
"    color: black;\n"
"    background: rgb(235, 235, 235);\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.statuslabel_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.statuslabel_9.setObjectName("statuslabel_9")
        self.horizontalLayout_87.addWidget(self.statuslabel_9)
        self.verticalLayout_27.addLayout(self.horizontalLayout_87)
        self.horizontalLayout_86 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_86.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_86.setSpacing(0)
        self.horizontalLayout_86.setObjectName("horizontalLayout_86")
        self.spindle_rev_button = ActionButton(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spindle_rev_button.sizePolicy().hasHeightForWidth())
        self.spindle_rev_button.setSizePolicy(sizePolicy)
        self.spindle_rev_button.setMinimumSize(QtCore.QSize(100, 42))
        self.spindle_rev_button.setMaximumSize(QtCore.QSize(100, 42))
        self.spindle_rev_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.spindle_rev_button.setStyleSheet("QPushButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.spindle_rev_button.setIcon(icon7)
        self.spindle_rev_button.setIconSize(QtCore.QSize(18, 18))
        self.spindle_rev_button.setProperty("option", True)
        self.spindle_rev_button.setObjectName("spindle_rev_button")
        self.horizontalLayout_86.addWidget(self.spindle_rev_button)
        self.spindle_stop_button = ActionButton(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spindle_stop_button.sizePolicy().hasHeightForWidth())
        self.spindle_stop_button.setSizePolicy(sizePolicy)
        self.spindle_stop_button.setMinimumSize(QtCore.QSize(90, 42))
        self.spindle_stop_button.setMaximumSize(QtCore.QSize(90, 42))
        self.spindle_stop_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.spindle_stop_button.setStyleSheet("QPushButton {\n"
"       font: 17pt \"Bebas Kai\";\n"
"}")
        self.spindle_stop_button.setProperty("option", True)
        self.spindle_stop_button.setObjectName("spindle_stop_button")
        self.horizontalLayout_86.addWidget(self.spindle_stop_button)
        self.spindle_fwd_button = ActionButton(self.jog_and_spindle_qframe)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spindle_fwd_button.sizePolicy().hasHeightForWidth())
        self.spindle_fwd_button.setSizePolicy(sizePolicy)
        self.spindle_fwd_button.setMinimumSize(QtCore.QSize(100, 42))
        self.spindle_fwd_button.setMaximumSize(QtCore.QSize(100, 42))
        self.spindle_fwd_button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.spindle_fwd_button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.spindle_fwd_button.setStyleSheet("QPushButton {\n"
"    text-align: right;\n"
"    padding-right: 22px;\n"
"    font: 17pt \"Bebas Kai\";\n"
"}")
        self.spindle_fwd_button.setIcon(icon8)
        self.spindle_fwd_button.setIconSize(QtCore.QSize(18, 18))
        self.spindle_fwd_button.setProperty("option", True)
        self.spindle_fwd_button.setObjectName("spindle_fwd_button")
        self.horizontalLayout_86.addWidget(self.spindle_fwd_button)
        self.verticalLayout_27.addLayout(self.horizontalLayout_86)
        self.main_control_screen_layout_panel.addWidget(self.jog_and_spindle_qframe)
        self.verticalLayout_31.addLayout(self.main_control_screen_layout_panel)
        Form.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(Form)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1918, 27))
        self.menuBar.setMinimumSize(QtCore.QSize(0, 25))
        self.menuBar.setStyleSheet("QMenuBar {\n"
"color: white;\n"
"background: rgb(118, 122, 124);\n"
"font: 11pt bebas kai;\n"
"}")
        self.menuBar.setObjectName("menuBar")
        self.menuExit = QtWidgets.QMenu(self.menuBar)
        self.menuExit.setObjectName("menuExit")
        self.menuRecentFiles = QtWidgets.QMenu(self.menuExit)
        self.menuRecentFiles.setObjectName("menuRecentFiles")
        self.menuMachine = QtWidgets.QMenu(self.menuBar)
        self.menuMachine.setObjectName("menuMachine")
        self.menuHoming = QtWidgets.QMenu(self.menuMachine)
        self.menuHoming.setObjectName("menuHoming")
        self.menuCooling = QtWidgets.QMenu(self.menuMachine)
        self.menuCooling.setObjectName("menuCooling")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        Form.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(Form)
        self.statusBar.setObjectName("statusBar")
        Form.setStatusBar(self.statusBar)
        self.actionExit = QtWidgets.QAction(Form)
        self.actionExit.setObjectName("actionExit")
        self.actionOpen = QtWidgets.QAction(Form)
        self.actionOpen.setObjectName("actionOpen")
        self.actionClose = QtWidgets.QAction(Form)
        self.actionClose.setObjectName("actionClose")
        self.actionReload = QtWidgets.QAction(Form)
        self.actionReload.setObjectName("actionReload")
        self.actionSave_As = QtWidgets.QAction(Form)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionHome_X = QtWidgets.QAction(Form)
        self.actionHome_X.setObjectName("actionHome_X")
        self.actionHome_Y = QtWidgets.QAction(Form)
        self.actionHome_Y.setObjectName("actionHome_Y")
        self.actionHome_Z = QtWidgets.QAction(Form)
        self.actionHome_Z.setObjectName("actionHome_Z")
        self.action_EmergencyStop_toggle = QtWidgets.QAction(Form)
        self.action_EmergencyStop_toggle.setObjectName("action_EmergencyStop_toggle")
        self.action_MachinePower_toggle = QtWidgets.QAction(Form)
        self.action_MachinePower_toggle.setProperty("_axis", 2)
        self.action_MachinePower_toggle.setObjectName("action_MachinePower_toggle")
        self.actionHome_All = QtWidgets.QAction(Form)
        self.actionHome_All.setObjectName("actionHome_All")
        self.actionRun_Program = QtWidgets.QAction(Form)
        self.actionRun_Program.setObjectName("actionRun_Program")
        self.actionFile1 = QtWidgets.QAction(Form)
        self.actionFile1.setObjectName("actionFile1")
        self.actionReport_Actual_Position = QtWidgets.QAction(Form)
        self.actionReport_Actual_Position.setCheckable(True)
        self.actionReport_Actual_Position.setObjectName("actionReport_Actual_Position")
        self.actionTest = QtWidgets.QAction(Form)
        self.actionTest.setObjectName("actionTest")
        self.action_Mist_toggle = QtWidgets.QAction(Form)
        self.action_Mist_toggle.setCheckable(True)
        self.action_Mist_toggle.setObjectName("action_Mist_toggle")
        self.action_Flood_toggle = QtWidgets.QAction(Form)
        self.action_Flood_toggle.setCheckable(True)
        self.action_Flood_toggle.setObjectName("action_Flood_toggle")
        self.menuRecentFiles.addAction(self.actionFile1)
        self.menuExit.addAction(self.actionOpen)
        self.menuExit.addAction(self.menuRecentFiles.menuAction())
        self.menuExit.addAction(self.actionReload)
        self.menuExit.addAction(self.actionClose)
        self.menuExit.addAction(self.actionSave_As)
        self.menuExit.addSeparator()
        self.menuExit.addAction(self.actionExit)
        self.menuHoming.addAction(self.actionHome_All)
        self.menuHoming.addAction(self.actionHome_X)
        self.menuHoming.addAction(self.actionHome_Y)
        self.menuHoming.addAction(self.actionHome_Z)
        self.menuCooling.addAction(self.action_Mist_toggle)
        self.menuCooling.addAction(self.action_Flood_toggle)
        self.menuMachine.addAction(self.action_EmergencyStop_toggle)
        self.menuMachine.addAction(self.action_MachinePower_toggle)
        self.menuMachine.addSeparator()
        self.menuMachine.addAction(self.actionRun_Program)
        self.menuMachine.addAction(self.menuHoming.menuAction())
        self.menuMachine.addAction(self.menuCooling.menuAction())
        self.menuView.addAction(self.actionReport_Actual_Position)
        self.menuView.addAction(self.actionTest)
        self.menuBar.addAction(self.menuExit.menuAction())
        self.menuBar.addAction(self.menuMachine.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(7)
        self.file_viewer_widget.setCurrentIndex(0)
        self.tabWidget1.setCurrentIndex(0)
        self.probe_tab_widget.setCurrentIndex(0)
        self.probe_help_widget.setCurrentIndex(0)
        self.operation.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(1)
        self.tabWidget_10.setCurrentIndex(2)
        self.tabWidget_9.setCurrentIndex(2)
        self.tabWidget_8.setCurrentIndex(2)
        self.tabWidget_7.setCurrentIndex(0)
        self.tabWidget_24.setCurrentIndex(1)
        self.gui_axis_display_widget.setCurrentIndex(0)
        self.main_delete_item_button.clicked.connect(self.filesystemtable.deleteItem)
        self.main_folder_up_button.clicked.connect(self.filesystemtable.viewParentDirectory)
        self.main_new_folder_button.clicked.connect(self.filesystemtable.newFolder)
        self.device_new_folder_button.clicked.connect(self.filesystemtable_2.newFolder)
        self.copy_from_usb_2.clicked.connect(self.filesystemtable_2.doFileTransfer)
        self.device_delete_item_button.clicked.connect(self.filesystemtable_2.deleteItem)
        self.main_new_file_button.clicked.connect(self.filesystemtable.newFile)
        self.copy_to_usb_2.clicked.connect(self.filesystemtable.doFileTransfer)
        self.device_folder_up_button.clicked.connect(self.filesystemtable_2.viewParentDirectory)
        self.filesystemtable_2.transferFileRequest['QString'].connect(self.filesystemtable.transferFile)
        self.main_load_gcode_button.clicked.connect(self.filesystemtable.loadSelectedFile)
        self.filesystemtable.transferFileRequest['QString'].connect(self.filesystemtable_2.transferFile)
        self.filesystemtable.gcodeFileSelected['bool'].connect(self.main_load_gcode_button.setEnabled)
        self.device_new_file_button.clicked.connect(self.filesystemtable_2.newFile)
        self.tool_table_delete_button.clicked.connect(self.tableWidget_2.deleteSelectedTool)
        self.machine_labels_button.toggled['bool'].connect(self.vtk.toggleMachineLabels)
        self.tool_table_save_button.clicked.connect(self.tableWidget_2.saveToolTable)
        self.y_view_button.clicked.connect(self.vtk.setViewY)
        self.tool_table_reload_button.clicked.connect(self.tableWidget_2.loadToolTable)
        self.zoom_in_button.clicked.connect(self.vtk.zoomIn)
        self.tool_table_add_tool_button.clicked.connect(self.tableWidget_2.addTool)
        self.x_view_button.clicked.connect(self.vtk.setViewX)
        self.iso_view_button.clicked.connect(self.vtk.setViewP)
        self.path_button.clicked.connect(self.vtk.setViewPath)
        self.z_view_button.clicked.connect(self.vtk.setViewZ)
        self.clear_button.clicked.connect(self.vtk.clearLivePlot)
        self.program_boundry_button.clicked['bool'].connect(self.vtk_probe.toggleProgramBounds)
        self.machine_boundry_button.toggled['bool'].connect(self.vtk.toggleMachineBounds)
        self.zoom_out_button.clicked.connect(self.vtk.zoomOut)
        self.program_boundry_button.toggled['bool'].connect(self.vtk.toggleProgramBounds)
        self.machine_ticks_button.toggled['bool'].connect(self.vtk.toggleMachineTicks)
        self.program_ticks_button.toggled['bool'].connect(self.vtk.toggleProgramTicks)
        self.program_labels_button.toggled['bool'].connect(self.vtk.toggleProgramLabels)
        self.perspective_button.clicked.connect(self.vtk.setViewPersp)
        self.ortho_button.clicked.connect(self.vtk.setViewOrtho)
        self.iso_view_button_plot.clicked.connect(self.vtk.setViewP)
        self.plot_grid_button.clicked['bool'].connect(self.vtk.showGrid)
        self.y_view_button_plot.clicked.connect(self.vtk.setViewY)
        self.zoom_out_button_plot.clicked.connect(self.vtk.zoomOut)
        self.x_view_button_plot.clicked.connect(self.vtk.setViewX)
        self.zoom_in_button_plot.clicked.connect(self.vtk.zoomIn)
        self.ortho_button_plot.clicked.connect(self.vtk.setViewOrtho)
        self.clear_button_plot.clicked.connect(self.vtk.clearLivePlot)
        self.machine_zoom_button_plot.clicked.connect(self.vtk.setViewMachine)
        self.perspective_button_plot.clicked.connect(self.vtk.setViewPersp)
        self.program_zoom_button_plot.clicked.connect(self.vtk.printView)
        self.perspective_button_plot.clicked.connect(self.vtk_probe.setViewPersp)
        self.iso_view_button_plot.clicked.connect(self.vtk_probe.setViewP)
        self.x_view_button_plot.clicked.connect(self.vtk_probe.setViewX)
        self.y_view_button_plot.clicked.connect(self.vtk_probe.setViewY)
        self.zoom_in_button_plot.clicked.connect(self.vtk_probe.zoomIn)
        self.zoom_out_button_plot.clicked.connect(self.vtk_probe.zoomOut)
        self.clear_button_plot.clicked.connect(self.vtk_probe.clearLivePlot)
        self.ortho_button_plot.clicked.connect(self.vtk_probe.setViewOrtho)
        self.machine_ticks_button.clicked['bool'].connect(self.vtk_probe.toggleMachineTicks)
        self.plot_grid_button.clicked['bool'].connect(self.vtk_probe.showGrid)
        self.machine_labels_button.clicked['bool'].connect(self.vtk_probe.toggleMachineLabels)
        self.machine_boundry_button.clicked['bool'].connect(self.vtk_probe.toggleMachineBounds)
        self.program_ticks_button.clicked['bool'].connect(self.vtk_probe.toggleProgramTicks)
        self.program_labels_button.clicked['bool'].connect(self.vtk_probe.toggleProgramLabels)
        self.z_view_button_plot.clicked.connect(self.vtk.setViewZ)
        self.main_rename_item_button.clicked.connect(self.filesystemtable.rename)
        self.program_zoom_button_plot.clicked.connect(self.vtk_probe.printView)
        self.machine_zoom_button_plot.clicked.connect(self.vtk_probe.setViewMachine)
        self.z_view_button_plot.clicked.connect(self.vtk_probe.setViewZ)
        self.device_rename_item_button.clicked.connect(self.filesystemtable_2.rename)
        self.filesystemtable.filePreviewText['QString'].connect(self.gcodeeditor_2.setText)
        self.find_replace_button.clicked.connect(self.gcodeeditor_2.find_replace)
        self.save_as_button.clicked.connect(self.gcodeeditor_2.saveAs)
        self.edit_gcode_button.clicked['bool'].connect(self.gcodeeditor_2.setEditable)
        self.save_button.clicked.connect(self.gcodeeditor_2.save)
        self.filesystemtable.fileNamePreviewText['QString'].connect(self.file_absolute_path.setText)
        self.filesystemtable.fileNamePreviewText['QString'].connect(self.gcodeeditor_2.setFilename)
        self.x_axis_button_10.clicked.connect(self.offset_table.deleteSelectedOffset)
        self.x_axis_button_11.clicked.connect(self.offset_table.clearOffsetTable)
        self.x_axis_button_13.clicked.connect(self.offset_table.saveOffsetTable)
        self.x_axis_button_14.clicked.connect(self.offset_table.loadOffsetTable)
        self.removabledevicecombobox.currentIndexChanged['QString'].connect(self.filesystemtable_2.setRootPath)
        self.removabledevicecombobox.usbPresent['bool'].connect(self.device_eject_usb_button.setEnabled)
        self.device_eject_usb_button.clicked['bool'].connect(self.removabledevicecombobox.ejectDevice)
        self.load_spindle_tool_number.returnPressed.connect(self.load_spindle_button.click)
        self.load_spindle_tool_number_2.returnPressed.connect(self.load_spindle_button_2.click)
        self.tool_number_entry_main_panel.returnPressed.connect(self.m6_tool_call_button_main_panel.click)
        self.tool_number_entry_atc_page.returnPressed.connect(self.m6_tool_call_button_atc_page.click)
        self.tool_number_entry_tool_page.returnPressed.connect(self.m6_tool_call_button_tool_page.click)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Probe Basic"))
        self.mdi_entry_box.setPlaceholderText(_translate("Form", "MDI"))
        self.iso_view_button.setText(_translate("Form", "ISO VIEW"))
        self.x_view_button.setText(_translate("Form", "X View"))
        self.y_view_button.setText(_translate("Form", "Y View"))
        self.z_view_button.setText(_translate("Form", "Z View"))
        self.pan_button.setText(_translate("Form", "PAN"))
        self.zoom_in_button.setText(_translate("Form", "ZOOM +"))
        self.zoom_out_button.setText(_translate("Form", "ZOOM -"))
        self.program_zoom_button.setText(_translate("Form", "PGM EXT"))
        self.machine_zoom_button.setText(_translate("Form", "MCH EXT"))
        self.path_button.setText(_translate("Form", "PATH"))
        self.clear_button.setText(_translate("Form", "CLEAR"))
        self.ortho_button.setText(_translate("Form", "ORTHO"))
        self.perspective_button.setText(_translate("Form", "PSPECT"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.main_tab), _translate("Form", "MAIN"))
        self.device_folder_up_button.setText(_translate("Form", "  FOLDER UP"))
        self.device_eject_usb_button.setText(_translate("Form", "EJECT USB"))
        self.device_delete_item_button.setText(_translate("Form", " DELETE"))
        self.device_new_file_button.setText(_translate("Form", " NEW FILE"))
        self.device_new_folder_button.setText(_translate("Form", " NEW FOLDER"))
        self.device_rename_item_button.setText(_translate("Form", "RENAME"))
        self.copy_from_usb_2.setText(_translate("Form", "COPY\n"
"FROM\n"
"  USB"))
        self.copy_to_usb_2.setText(_translate("Form", "COPY\n"
"TO\n"
"USB"))
        self.main_folder_up_button.setText(_translate("Form", "  FOLDER UP"))
        self.main_load_gcode_button.setText(_translate("Form", "LOAD G-CODE"))
        self.main_delete_item_button.setText(_translate("Form", " DELETE"))
        self.main_new_file_button.setText(_translate("Form", " NEW FILE"))
        self.main_new_folder_button.setText(_translate("Form", " NEW FOLDER"))
        self.main_rename_item_button.setText(_translate("Form", "RENAME"))
        self.gcode_editor_button.setText(_translate("Form", "GCODE EDITOR"))
        self.setup_viewer_button.setText(_translate("Form", "SETUP VIEWER"))
        self.edit_gcode_button.setText(_translate("Form", "EDIT G-CODE"))
        self.find_replace_button.setText(_translate("Form", "FIND/REPLACE"))
        self.save_button.setText(_translate("Form", "SAVE"))
        self.save_as_button.setText(_translate("Form", "SAVE AS"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.file_tab), _translate("Form", "FILE"))
        self.machine_column_header_9.setText(_translate("Form", "ATC MANUAL CONTROL PANEL"))
        self.insert_atc_tool.setText(_translate("Form", "INSERT"))
        self.delete_all_atc_tools.setText(_translate("Form", "DELETE ALL"))
        self.delete_single_tool.setText(_translate("Form", "DELETE"))
        self.subcallbutton_9.setText(_translate("Form", " ATC REV"))
        self.subcallbutton_9.setProperty("MDICommand", _translate("Form", "m11"))
        self.subcallbutton_3.setText(_translate("Form", " ATC FWD "))
        self.subcallbutton_3.setProperty("MDICommand", _translate("Form", "m12"))
        self.subcallbutton_11.setText(_translate("Form", " ATC RETRACT"))
        self.subcallbutton_11.setProperty("MDICommand", _translate("Form", "m22"))
        self.subcallbutton_5.setText(_translate("Form", " ATC EXTEND "))
        self.subcallbutton_5.setProperty("MDICommand", _translate("Form", "m21"))
        self.subcallbutton_16.setText(_translate("Form", "DRAWBAR LOOSE"))
        self.subcallbutton_16.setProperty("MDICommand", _translate("Form", "M64 P2"))
        self.subcallbutton_6.setText(_translate("Form", "DRAWBAR TIGHT"))
        self.subcallbutton_6.setProperty("MDICommand", _translate("Form", "M65 P2"))
        self.m01_break_button_10.setText(_translate("Form", "SET TC POSITION"))
        self.m01_break_button_27.setText(_translate("Form", "AIR BLAST"))
        self.reference_carousel.setText(_translate("Form", "REF CAROUSEL"))
        self.reference_carousel.setProperty("MDICommand", _translate("Form", "m13"))
        self.m01_break_button_14.setText(_translate("Form", "+ +"))
        self.m01_break_button_15.setText(_translate("Form", "- -"))
        self.mdi_entry_box_3.setPlaceholderText(_translate("Form", "MDI"))
        self.tool_length_10.setText(_translate("Form", "No Tool Loaded"))
        self.tool_length_10.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?remark\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Tool Comment\"}]"))
        self.tool_length_10.setProperty("format", _translate("Form", "{:.3f}"))
        self.loaded_spindle_tool_number.setText(_translate("Form", "T0"))
        self.loaded_spindle_tool_number.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:tool_in_spindle?text\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\'T\' + ch[0]\", \"name\": \"current tool\"}]"))
        self.loaded_spindle_tool_number.setProperty("format", _translate("Form", "{:.3f}"))
        self.loaded_spindle_tool_number.setProperty("statusItem", _translate("Form", "tool_offset.3"))
        self.machine_column_header_3.setText(_translate("Form", "ATC AUTOMATIC CONTROL PANEL"))
        self.load_spindle_tool_number.setPlaceholderText(_translate("Form", "0"))
        self.load_spindle_tool_number.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?tool_number\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"str(0)\", \"name\": \"update tool num\"}, {\"channels\": [{\"url\": \"status:task_state?text\", \"trigger\": true}, {\"url\": \"status:interp_state?text\", \"trigger\": true}], \"property\": \"Enable\", \"expression\": \"ch[0] == \'On\' and ch[1] == \'Idle\'\", \"name\": \"enable/disable\"}]"))
        self.load_spindle_button.setText(_translate("Form", "LOAD SPINDLE"))
        self.load_spindle_button.setProperty("filename", _translate("Form", "load_spindle_safety.ngc"))
        self.remove_current_tool.setText(_translate("Form", "UNLOAD SPINDLE"))
        self.remove_current_tool.setProperty("rules", _translate("Form", "[]"))
        self.remove_current_tool.setProperty("MDICommand", _translate("Form", "M61 Q0 G49 #5210 = 0"))
        self.subcallbutton_12.setText(_translate("Form", " ATC REV"))
        self.subcallbutton_12.setProperty("MDICommand", _translate("Form", "m12"))
        self.subcallbutton_4.setText(_translate("Form", " ATC FWD "))
        self.subcallbutton_4.setProperty("MDICommand", _translate("Form", "m11"))
        self.store_tool_in_spindle.setText(_translate("Form", "Store Tool IN CAROUSEL"))
        self.store_tool_in_spindle.setProperty("filename", _translate("Form", "store_tool_in_carousel.ngc"))
        self.tool_number_entry_atc_page.setText(_translate("Form", "0"))
        self.tool_number_entry_atc_page.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?tool_number\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"str(ch[0])\", \"name\": \"update tool num\"}, {\"channels\": [{\"url\": \"status:task_state?text\", \"trigger\": true}, {\"url\": \"status:interp_state?text\", \"trigger\": true}], \"property\": \"Enable\", \"expression\": \"ch[0] == \'On\' and ch[1] == \'Idle\'\", \"name\": \"enable/disable\"}]"))
        self.m6_tool_call_button_atc_page.setText(_translate("Form", "M6 G43"))
        self.m6_tool_call_button_atc_page.setProperty("filename", _translate("Form", "m6_tool_call_atc_page.ngc"))
        self.machine_column_header_2.setText(_translate("Form", "ELECTRONIC TOOL SETTER"))
        self.m01_break_button_24.setText(_translate("Form", "TOUCH OFF ENTIRE CAROUSEL"))
        self.m01_break_button_25.setText(_translate("Form", "TOUCH OFF CURRENT TOOL"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.atc_tab), _translate("Form", "ATC"))
        self.tableWidget_2.setProperty("displayColumns", _translate("Form", "TPZDR"))
        self.tool_table_delete_button.setText(_translate("Form", "DELETE"))
        self.tool_table_add_tool_button.setText(_translate("Form", "ADD TOOL"))
        self.tool_table_import_tool_button.setText(_translate("Form", "IMPORT TOOL"))
        self.tool_table_export_tool_button.setText(_translate("Form", "EXPORT TOOL"))
        self.tool_table_save_button.setText(_translate("Form", "SAVE TABLE"))
        self.tool_table_reload_button.setText(_translate("Form", "RELOAD TABLE"))
        self.tabWidget1.setTabText(self.tabWidget1.indexOf(self.TOOLTABLE), _translate("Form", "TOOL TABLE"))
        self.tabWidget1.setTabText(self.tabWidget1.indexOf(self.toollibrary), _translate("Form", "TOOL LIBRARY"))
        self.label_48.setText(_translate("Form", "TOOL LENGTH"))
        self.tool_length_5.setText(_translate("Form", "0.0000"))
        self.tool_length_5.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?z_offset\", \"trigger\": true}, {\"url\": \"status:linear_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0]) if ch[1] == \'in\' else \\\"{:.4f}\\\".format(ch[0])\", \"name\": \"Tool Length\"}]"))
        self.tool_length_5.setProperty("format", _translate("Form", "{:.3f}"))
        self.label_49.setText(_translate("Form", "DIAM"))
        self.tool_diameter_2.setText(_translate("Form", "0.0000"))
        self.tool_diameter_2.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?diameter\", \"trigger\": true}, {\"url\": \"status:linear_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0]) if ch[1] == \'in\' else \\\"{:.4f}\\\".format(ch[0])\", \"name\": \"Tool Diameter\"}]"))
        self.tool_diameter_2.setProperty("format", _translate("Form", "{:.3f}"))
        self.label_56.setText(_translate("Form", "COMMENT"))
        self.tool_length_7.setText(_translate("Form", "No Tool Loaded"))
        self.tool_length_7.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?remark\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Tool Comment\"}]"))
        self.tool_length_7.setProperty("format", _translate("Form", "{:.3f}"))
        self.mdi_entry_box_4.setPlaceholderText(_translate("Form", "MDI"))
        self.tool_length_6.setText(_translate("Form", "T0"))
        self.tool_length_6.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:tool_in_spindle?text\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\'T\' + ch[0]\", \"name\": \"current tool\"}]"))
        self.tool_length_6.setProperty("format", _translate("Form", "{:.3f}"))
        self.machine_column_header_7.setText(_translate("Form", "TOOL CHANGE PANEL"))
        self.load_spindle_tool_number_2.setPlaceholderText(_translate("Form", "0"))
        self.load_spindle_tool_number_2.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?tool_number\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"str(0)\", \"name\": \"update tool num\"}, {\"channels\": [{\"url\": \"status:task_state?text\", \"trigger\": true}, {\"url\": \"status:interp_state?text\", \"trigger\": true}], \"property\": \"Enable\", \"expression\": \"ch[0] == \'On\' and ch[1] == \'Idle\'\", \"name\": \"enable/disable\"}]"))
        self.load_spindle_button_2.setText(_translate("Form", "LOAD SPINDLE"))
        self.load_spindle_button_2.setProperty("filename", _translate("Form", "load_spindle_safety_2.ngc"))
        self.remove_current_tool_3.setText(_translate("Form", "UNLOAD SPINDLE"))
        self.remove_current_tool_3.setProperty("rules", _translate("Form", "[]"))
        self.remove_current_tool_3.setProperty("MDICommand", _translate("Form", "M61 Q0 G49 #5210 = 0"))
        self.tool_number_entry_tool_page.setText(_translate("Form", "0"))
        self.tool_number_entry_tool_page.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?tool_number\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"str(ch[0])\", \"name\": \"update tool num\"}, {\"channels\": [{\"url\": \"status:task_state?text\", \"trigger\": true}, {\"url\": \"status:interp_state?text\", \"trigger\": true}], \"property\": \"Enable\", \"expression\": \"ch[0] == \'On\' and ch[1] == \'Idle\'\", \"name\": \"enable/disable\"}]"))
        self.m6_tool_call_button_tool_page.setText(_translate("Form", "M6 G43"))
        self.m6_tool_call_button_tool_page.setProperty("filename", _translate("Form", "m6_tool_call_tool_page.ngc"))
        self.machine_column_header_8.setText(_translate("Form", "ELECTRONIC TOOL SETTER"))
        self.tool_touch_off_button.setText(_translate("Form", "TOUCH OFF CURRENT TOOL"))
        self.tool_touch_off_button.setProperty("filename", _translate("Form", "tool_touch_off.ngc"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tool_tab), _translate("Form", "          TOOL          "))
        self.offset_table.setProperty("displayColumns", _translate("Form", "XYZR"))
        self.x_axis_button_10.setText(_translate("Form", "CLEAR SELECTED"))
        self.x_axis_button_11.setText(_translate("Form", "CLEAR ALL"))
        self.x_axis_button_13.setText(_translate("Form", "SAVE TABLE"))
        self.x_axis_button_14.setText(_translate("Form", "RELOAD TABLE"))
        self.mdi_entry_box_6.setPlaceholderText(_translate("Form", "MDI"))
        self.machine_column_header_4.setText(_translate("Form", "WORK COORDINATE OFFSETS"))
        self.actionbutton_g54_2.setText(_translate("Form", "G54"))
        self.actionbutton_g54_2.setProperty("actionName", _translate("Form", "machine.set-work-coord:G54"))
        self.actionbutton_g55_2.setText(_translate("Form", "G55"))
        self.actionbutton_g55_2.setProperty("actionName", _translate("Form", "machine.set-work-coord:G55"))
        self.actionbutton_g56_2.setText(_translate("Form", "G56"))
        self.actionbutton_g56_2.setProperty("actionName", _translate("Form", "machine.set-work-coord:G56"))
        self.actionbutton_g57_2.setText(_translate("Form", "G57"))
        self.actionbutton_g57_2.setProperty("actionName", _translate("Form", "machine.set-work-coord:G57"))
        self.actionbutton_g58_2.setText(_translate("Form", "G58"))
        self.actionbutton_g58_2.setProperty("actionName", _translate("Form", "machine.set-work-coord:G58"))
        self.actionbutton_g59_4.setText(_translate("Form", "G59"))
        self.actionbutton_g59_4.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59"))
        self.actionbutton_g59_5.setText(_translate("Form", "G59.1"))
        self.actionbutton_g59_5.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.1"))
        self.actionbutton_g59_6.setText(_translate("Form", "G59.2"))
        self.actionbutton_g59_6.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.2"))
        self.actionbutton_g59_7.setText(_translate("Form", "G59.3"))
        self.actionbutton_g59_7.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.3"))
        self.axis_column_header_9.setText(_translate("Form", "SET TO ZERO"))
        self.axis_column_header_10.setText(_translate("Form", "AXIS"))
        self.machine_column_header_10.setText(_translate("Form", "WC CURRENT POSITION"))
        self.machine_column_header_11.setText(_translate("Form", "MACHINE\n"
"COORDS"))
        self.machine_column_header_12.setText(_translate("Form", "WC\n"
"OFFSET"))
        self.ref_coilumn_header_4.setText(_translate("Form", "G52/G92\n"
"OFFSET"))
        self.machine_column_header_13.setText(_translate("Form", "TOOL\n"
"OFFSET"))
        self.zero_x_button_2.setText(_translate("Form", "ZERO"))
        self.zero_x_button_2.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_x_button_2.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} X0.0"))
        self.axis_column_header_11.setText(_translate("Form", "X"))
        self.statuslabel_50.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_51.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:position\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_52.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g5x_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_53.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g92_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_54.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:tool_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][0])\", \"name\": \"New Rule\"}]"))
        self.zero_y_button_2.setText(_translate("Form", "ZERO"))
        self.zero_y_button_2.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_y_button_2.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} Y0.0"))
        self.axis_column_header_12.setText(_translate("Form", "Y"))
        self.statuslabel_55.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_56.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:position\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][1])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_57.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g5x_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][1])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_58.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g92_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][1])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_59.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:tool_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][1])\", \"name\": \"New Rule\"}]"))
        self.zero_z_button_2.setText(_translate("Form", "ZERO"))
        self.zero_z_button_2.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_z_button_2.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} Z0.0"))
        self.axis_column_header_13.setText(_translate("Form", "Z"))
        self.statuslabel_60.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_61.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:position\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][2])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_62.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g5x_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][2])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_63.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g92_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][2])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_64.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:tool_offset\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][2])\", \"name\": \"tool offset\"}]"))
        self.zero_a_button_2.setText(_translate("Form", "ZERO"))
        self.zero_a_button_2.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_a_button_2.setProperty("MDICommand", _translate("Form", "G10 L2 P{ch[0]} A0.0"))
        self.axis_column_header_14.setText(_translate("Form", "A"))
        self.statuslabel_65.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?axis=a\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_66.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:position\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][3])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_67.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g92_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][3])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_68.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g5x_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][3])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_69.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:tool_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][3])\", \"name\": \"New Rule\"}]"))
        self.zero_b_button_2.setText(_translate("Form", "ZERO"))
        self.zero_b_button_2.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_b_button_2.setProperty("MDICommand", _translate("Form", "G10 L2 P{ch[0]} B0.0"))
        self.axis_column_header_15.setText(_translate("Form", "B"))
        self.statuslabel_70.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?axis=b\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_71.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:position\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][4])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_72.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g92_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][4])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_73.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:g5x_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][4])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_74.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"tuple\", \"url\": \"status:tool_offset\"}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0][4])\", \"name\": \"New Rule\"}]"))
        self.set_g30_1_position.setText(_translate("Form", "SET TOOL TOUCH OFF POSITION"))
        self.set_g30_1_position.setProperty("filename", _translate("Form", "set_g30_position.ngc"))
        self.label_55.setText(_translate("Form", "X"))
        self.x_tool_change_position.setPlaceholderText(_translate("Form", "0.0000"))
        self.x_tool_change_position.setProperty("rules", _translate("Form", "[]"))
        self.x_tool_change_position.setProperty("settingName", _translate("Form", "tool-change-position.x-tool-change-position"))
        self.x_tool_change_position.setProperty("textFormat", _translate("Form", "{:6.4f}"))
        self.label_57.setText(_translate("Form", "Y"))
        self.y_tool_change_position.setPlaceholderText(_translate("Form", "0.0000"))
        self.y_tool_change_position.setProperty("rules", _translate("Form", "[]"))
        self.y_tool_change_position.setProperty("settingName", _translate("Form", "tool-change-position.y-tool-change-position"))
        self.y_tool_change_position.setProperty("textFormat", _translate("Form", "{:6.4f}"))
        self.label_58.setText(_translate("Form", "Z"))
        self.z_tool_change_position.setPlaceholderText(_translate("Form", "0.0000"))
        self.z_tool_change_position.setProperty("rules", _translate("Form", "[]"))
        self.z_tool_change_position.setProperty("settingName", _translate("Form", "tool-change-position.z-tool-change-position"))
        self.z_tool_change_position.setProperty("textFormat", _translate("Form", "{:6.4f}"))
        self.label_4.setText(_translate("Form", "FAST PROBE FR"))
        self.fast_probe_fr.setPlaceholderText(_translate("Form", "0.0"))
        self.fast_probe_fr.setProperty("settingName", _translate("Form", "tool-setter-probe.fast-probe-fr"))
        self.fast_probe_fr.setProperty("textFormat", _translate("Form", "{:0.1f}"))
        self.label_119.setText(_translate("Form", "SLOW PROBE FR"))
        self.slow_probe_fr.setPlaceholderText(_translate("Form", "0.0"))
        self.slow_probe_fr.setProperty("settingName", _translate("Form", "tool-setter-probe.slow-probe-fr"))
        self.slow_probe_fr.setProperty("textFormat", _translate("Form", "{:0.1f}"))
        self.label_122.setText(_translate("Form", "Z MAX TRAVEL"))
        self.z_max_travel.setPlaceholderText(_translate("Form", "0.0000"))
        self.z_max_travel.setProperty("settingName", _translate("Form", "tool-setter-probe.z-max-travel"))
        self.z_max_travel.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_125.setText(_translate("Form", "XY MAX TRAVEL"))
        self.xy_max_travel.setPlaceholderText(_translate("Form", "0.0000"))
        self.xy_max_travel.setProperty("settingName", _translate("Form", "tool-setter-probe.xy-max-travel"))
        self.xy_max_travel.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_123.setText(_translate("Form", "RETRACT DIST"))
        self.retract_distance.setPlaceholderText(_translate("Form", "0.0000"))
        self.retract_distance.setProperty("settingName", _translate("Form", "tool-setter-probe.retract-distance"))
        self.retract_distance.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_124.setText(_translate("Form", "SPINDLE ZERO"))
        self.spindle_zero_height.setPlaceholderText(_translate("Form", "0.0000"))
        self.spindle_zero_height.setProperty("settingName", _translate("Form", "tool-setter-probe.spindle-nose-height"))
        self.spindle_zero_height.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.tool_diameter_probe_Btn.setText(_translate("Form", "TOOL DIAM PROBE"))
        self.tool_diameter_probe_Btn.setProperty("checkedAction", _translate("Form", "1"))
        self.tool_diameter_offset_Btn.setStatusTip(_translate("Form", "Tool Diameter Offset: offsets the X Axis during touch off by the tool\'s radius distance, this puts the tool edge over the center of the tool setter.  Very useful for touching off Facemills!"))
        self.tool_diameter_offset_Btn.setText(_translate("Form", "TOOL DIAM OFFSET"))
        self.tool_diameter_offset_Btn.setProperty("checkedAction", _translate("Form", "1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.offsets_tab), _translate("Form", "OFFSETS"))
        self.label_81.setText(_translate("Form", " WORK OFFSETS"))
        self.actionbutton_19.setText(_translate("Form", "G54"))
        self.actionbutton_19.setProperty("actionName", _translate("Form", "machine.set-work-coord:G54"))
        self.actionbutton_20.setText(_translate("Form", "G55"))
        self.actionbutton_20.setProperty("actionName", _translate("Form", "machine.set-work-coord:G55"))
        self.actionbutton_21.setText(_translate("Form", "G56"))
        self.actionbutton_21.setProperty("actionName", _translate("Form", "machine.set-work-coord:G56"))
        self.actionbutton_26.setText(_translate("Form", "G57"))
        self.actionbutton_26.setProperty("actionName", _translate("Form", "machine.set-work-coord:G57"))
        self.actionbutton_24.setText(_translate("Form", "G58"))
        self.actionbutton_24.setProperty("actionName", _translate("Form", "machine.set-work-coord:G58"))
        self.actionbutton_22.setText(_translate("Form", "G59"))
        self.actionbutton_22.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59"))
        self.actionbutton_27.setText(_translate("Form", "G59.1"))
        self.actionbutton_27.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.1"))
        self.actionbutton_25.setText(_translate("Form", "G59.2"))
        self.actionbutton_25.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.2"))
        self.actionbutton_23.setText(_translate("Form", "G59.3"))
        self.actionbutton_23.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.3"))
        self.probe_wco.setText(_translate("Form", "PROBE WCO"))
        self.probe_wco.setProperty("checkedAction", _translate("Form", "0"))
        self.probe_Position_only.setText(_translate("Form", "PROBE POS\'N"))
        self.probe_Position_only.setProperty("checkedAction", _translate("Form", "1"))
        self.label_82.setText(_translate("Form", " Probing Parameters"))
        self.label_83.setText(_translate("Form", "Probe Tool #:"))
        self.probe_tool_number.setPlaceholderText(_translate("Form", "0"))
        self.probe_tool_number.setProperty("settingName", _translate("Form", "probe-parameters.probe-tool-number"))
        self.probe_tool_number.setProperty("textFormat", _translate("Form", "{:0.0f}"))
        self.label_84.setText(_translate("Form", "Step Off Width:"))
        self.step_off_width.setPlaceholderText(_translate("Form", "0.0000"))
        self.step_off_width.setProperty("settingName", _translate("Form", "probe-parameters.step-off-width"))
        self.step_off_width.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_85.setText(_translate("Form", "PROBE FAST FDRATE:"))
        self.probe_fast_fr.setPlaceholderText(_translate("Form", "0.0"))
        self.probe_fast_fr.setProperty("settingName", _translate("Form", "probe-parameters.probe-fast-fr"))
        self.probe_fast_fr.setProperty("textFormat", _translate("Form", "{:0.1f}"))
        self.label_86.setText(_translate("Form", "PROBE SLOW FDRATE:"))
        self.probe_slow_fr.setPlaceholderText(_translate("Form", "0.0"))
        self.probe_slow_fr.setProperty("settingName", _translate("Form", "probe-parameters.probe-slow-fr"))
        self.probe_slow_fr.setProperty("textFormat", _translate("Form", "{:0.1f}"))
        self.label_87.setText(_translate("Form", "Max X/Y Distance:"))
        self.max_xy_distance.setPlaceholderText(_translate("Form", "0.0000"))
        self.max_xy_distance.setProperty("settingName", _translate("Form", "probe-parameters.max-xy-distance"))
        self.max_xy_distance.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_88.setText(_translate("Form", "X/Y Clearance:"))
        self.xy_clearance.setPlaceholderText(_translate("Form", "0.0000"))
        self.xy_clearance.setProperty("settingName", _translate("Form", "probe-parameters.xy-clearance"))
        self.xy_clearance.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_90.setText(_translate("Form", "Max Z Distance:"))
        self.max_z_distance.setPlaceholderText(_translate("Form", "0.0000"))
        self.max_z_distance.setProperty("settingName", _translate("Form", "probe-parameters.max-z-distance"))
        self.max_z_distance.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_91.setText(_translate("Form", "Z Clearance:"))
        self.z_clearance.setPlaceholderText(_translate("Form", "0.0000"))
        self.z_clearance.setProperty("settingName", _translate("Form", "probe-parameters.z-clearance"))
        self.z_clearance.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_92.setText(_translate("Form", "Extra Probe Depth:"))
        self.extra_probe_depth.setPlaceholderText(_translate("Form", "0.0000"))
        self.extra_probe_depth.setProperty("settingName", _translate("Form", "probe-parameters.extra-probe-depth"))
        self.extra_probe_depth.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_94.setText(_translate("Form", "EDGE WIDTH:"))
        self.edge_width.setPlaceholderText(_translate("Form", "0.0000"))
        self.edge_width.setProperty("settingName", _translate("Form", "probe-parameters.edge-width"))
        self.edge_width.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_95.setText(_translate("Form", " Probe Results"))
        self.reset_all_data.setText(_translate("Form", "RESET ALL DATA"))
        self.reset_all_data.setProperty("filename", _translate("Form", "reset_all_data.ngc"))
        self.x_data_reset1.setText(_translate("Form", "X DATA RESET"))
        self.x_data_reset1.setProperty("filename", _translate("Form", "x_data_reset.ngc"))
        self.y_data_reset1.setText(_translate("Form", "Y DATA RESET"))
        self.y_data_reset1.setProperty("filename", _translate("Form", "y_data_reset.ngc"))
        self.label_108.setText(_translate("Form", "X- PROBED:"))
        self.x_minus_probed_position.setText(_translate("Form", "0.0000"))
        self.x_minus_probed_position.setProperty("rules", _translate("Form", "[]"))
        self.x_minus_probed_position.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_98.setText(_translate("Form", "X+ PROBED:"))
        self.x_plus_probed_position.setText(_translate("Form", "0.0000"))
        self.x_plus_probed_position.setProperty("rules", _translate("Form", "[]"))
        self.x_plus_probed_position.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_97.setText(_translate("Form", "X WIDTH:"))
        self.x_probed_width.setText(_translate("Form", "0.0000"))
        self.x_probed_width.setProperty("rules", _translate("Form", "[]"))
        self.x_probed_width.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_109.setText(_translate("Form", "Y- PROBED:"))
        self.y_minus_probed_position.setText(_translate("Form", "0.0000"))
        self.y_minus_probed_position.setProperty("rules", _translate("Form", "[]"))
        self.y_minus_probed_position.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_101.setText(_translate("Form", "Y+ PROBED:"))
        self.y_plus_probed_position.setText(_translate("Form", "0.0000"))
        self.y_plus_probed_position.setProperty("rules", _translate("Form", "[]"))
        self.y_plus_probed_position.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_100.setText(_translate("Form", "Y WIDTH:"))
        self.y_probed_width.setText(_translate("Form", "0.0000"))
        self.y_probed_width.setProperty("rules", _translate("Form", "[]"))
        self.y_probed_width.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_110.setText(_translate("Form", "Z- PROBED:"))
        self.z_minus_probed_position.setText(_translate("Form", "0.0000"))
        self.z_minus_probed_position.setProperty("rules", _translate("Form", "[]"))
        self.z_minus_probed_position.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_102.setText(_translate("Form", "DIAM:"))
        self.averaged_diam.setText(_translate("Form", "0.0000"))
        self.averaged_diam.setProperty("rules", _translate("Form", "[]"))
        self.averaged_diam.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_113.setText(_translate("Form", "X CENTER:"))
        self.x_center_probed.setText(_translate("Form", "0.0000"))
        self.x_center_probed.setProperty("rules", _translate("Form", "[]"))
        self.x_center_probed.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_99.setText(_translate("Form", "<html><head/><body><p>EDGE DELTA:</p></body></html>"))
        self.edge_delta.setText(_translate("Form", "0.0000"))
        self.edge_delta.setProperty("rules", _translate("Form", "[]"))
        self.edge_delta.setProperty("format", _translate("Form", "{:6.4f}"))
        self.label_96.setText(_translate("Form", "EDGE ANGLE:"))
        self.edge_angle.setText(_translate("Form", "0.0000"))
        self.edge_angle.setProperty("rules", _translate("Form", "[]"))
        self.edge_angle.setProperty("format", _translate("Form", "{:6.4f}"))
        self.edge_angle.setProperty("expression", _translate("Form", "val"))
        self.label_114.setText(_translate("Form", "Y CENTER:"))
        self.y_center_probed.setText(_translate("Form", "0.0000"))
        self.y_center_probed.setProperty("rules", _translate("Form", "[]"))
        self.y_center_probed.setProperty("format", _translate("Form", "{:6.4f}"))
        self.mdi_entry_box_5.setPlaceholderText(_translate("Form", "MDI"))
        self.outside_corners.setText(_translate("Form", "OUTSIDE CORNERS"))
        self.inside_corners.setText(_translate("Form", "INSIDE CORNERS"))
        self.boss_and_pocket.setText(_translate("Form", "BOSS AND POCKET"))
        self.ridge_and_valley.setText(_translate("Form", "RIDGE AND VALLEY"))
        self.rotation_angle.setText(_translate("Form", "EDGE ANGLE"))
        self.rotary_axis_2.setText(_translate("Form", "ROTARY AXIS"))
        self.calibrate.setText(_translate("Form", "CALIBRATE"))
        self.probe_help.setText(_translate("Form", "PROBE HELP"))
        self.probe_back_left_top_corner.setProperty("filename", _translate("Form", "probe_back_left_top_corner.ngc"))
        self.probe_back_right_top_corner.setProperty("filename", _translate("Form", "probe_back_right_top_corner.ngc"))
        self.probe_right_top_side.setProperty("filename", _translate("Form", "probe_right_top_side.ngc"))
        self.probe_z_minus_wco_edge.setProperty("filename", _translate("Form", "probe_z_minus_wco.ngc"))
        self.probe_front_top_side.setProperty("filename", _translate("Form", "probe_front_top_side.ngc"))
        self.probe_back_top_side.setProperty("filename", _translate("Form", "probe_back_top_side.ngc"))
        self.probe_front_left_top_corner.setProperty("filename", _translate("Form", "probe_front_left_top_corner.ngc"))
        self.probe_front_right_top_corner.setProperty("filename", _translate("Form", "probe_front_right_top_corner.ngc"))
        self.probe_left_top_side.setProperty("filename", _translate("Form", "probe_left_top_side.ngc"))
        self.probe_front_right_inside_corner.setProperty("filename", _translate("Form", "probe_front_right_inside_corner.ngc"))
        self.probe_y_plus_wco.setProperty("filename", _translate("Form", "probe_y_plus_wco.ngc"))
        self.probe_back_right_inside_corner.setProperty("filename", _translate("Form", "probe_back_right_inside_corner.ngc"))
        self.probe_front_left_inside_corner.setProperty("filename", _translate("Form", "probe_front_left_inside_corner.ngc"))
        self.probe_z_minus_wco_inside.setProperty("filename", _translate("Form", "probe_z_minus_wco.ngc"))
        self.probe_back_left_inside_corner.setProperty("filename", _translate("Form", "probe_back_left_inside_corner.ngc"))
        self.probe_x_minus_wco.setProperty("filename", _translate("Form", "probe_x_minus_wco.ngc"))
        self.probe_x_plus_wco.setProperty("filename", _translate("Form", "probe_x_plus_wco.ngc"))
        self.probe_y_minus_wco.setProperty("filename", _translate("Form", "probe_y_minus_wco.ngc"))
        self.probe_round_boss.setProperty("filename", _translate("Form", "probe_round_boss.ngc"))
        self.probe_round_pocket.setProperty("filename", _translate("Form", "probe_round_pocket.ngc"))
        self.probe_rect_boss.setProperty("filename", _translate("Form", "probe_rect_boss.ngc"))
        self.probe_rect_pocket.setProperty("filename", _translate("Form", "probe_rect_pocket.ngc"))
        self.hint_label.setText(_translate("Form", "HINT"))
        self.label_70.setText(_translate("Form", "DIAM:"))
        self.diameter_hint.setPlaceholderText(_translate("Form", "0.0000"))
        self.label_71.setText(_translate("Form", "X :"))
        self.x_hint_0.setPlaceholderText(_translate("Form", "0.0000"))
        self.label_72.setText(_translate("Form", "Y :"))
        self.y_hint_0.setPlaceholderText(_translate("Form", "0.0000"))
        self.probe_valley_x.setProperty("filename", _translate("Form", "probe_valley_x.ngc"))
        self.probe_valley_y.setProperty("filename", _translate("Form", "probe_valley_y.ngc"))
        self.probe_ridge_x.setProperty("filename", _translate("Form", "probe_ridge_x.ngc"))
        self.probe_ridge_y.setProperty("filename", _translate("Form", "probe_ridge_y.ngc"))
        self.hint_label_2.setText(_translate("Form", "HINT"))
        self.label_74.setText(_translate("Form", "X :"))
        self.x_hint.setPlaceholderText(_translate("Form", "0.0000"))
        self.label_75.setText(_translate("Form", "Y :"))
        self.y_hint.setPlaceholderText(_translate("Form", "0.0000"))
        self.probe_top_left_edge_angle.setProperty("filename", _translate("Form", "probe_top_left_edge_angle.ngc"))
        self.probe_corner_y_plus_edge_angle.setProperty("filename", _translate("Form", "probe_corner_y_plus_edge_angle.ngc"))
        self.probe_corner_x_plus_edge_angle.setProperty("filename", _translate("Form", "probe_corner_x_plus_edge_angle.ngc"))
        self.probe_corner_y_minus_edge_angle.setProperty("filename", _translate("Form", "probe_corner_y_minus_edge_angle.ngc"))
        self.probe_z_minus_edge.setProperty("filename", _translate("Form", "probe_z_minus_wco.ngc"))
        self.probe_corner_x_minus_edge_angle.setProperty("filename", _translate("Form", "probe_corner_x_minus_edge_angle.ngc"))
        self.probe_top_right_edge_angle.setProperty("filename", _translate("Form", "probe_top_right_edge_angle.ngc"))
        self.probe_top_back_edge_angle.setProperty("filename", _translate("Form", "probe_top_back_edge_angle.ngc"))
        self.probe_top_front_edge_angle.setProperty("filename", _translate("Form", "probe_top_front_edge_angle.ngc"))
        self.set_wco_offset_Btn.setText(_translate("Form", "SET WCO ROTATION FOR ANGLE PROBE OPERATIONS"))
        self.label_93.setText(_translate("Form", "PROBE CALIBRATION OFFSET:"))
        self.calibration_offset.setPlaceholderText(_translate("Form", "0.000000"))
        self.calibration_offset.setProperty("rules", _translate("Form", "[]"))
        self.calibration_offset.setProperty("settingName", _translate("Form", "touch-probe.calibration-offset"))
        self.calibration_offset.setProperty("textFormat", _translate("Form", "{:8.6f}"))
        self.probe_cal_reset.setText(_translate("Form", "PROBE CAL RESET"))
        self.probe_cal_reset.setProperty("filename", _translate("Form", "probe_cal_reset.ngc"))
        self.probe_cal_round_pocket.setProperty("filename", _translate("Form", "probe_cal_round_pocket.ngc"))
        self.probe_cal_round_boss.setProperty("filename", _translate("Form", "probe_cal_round_boss.ngc"))
        self.hint_label_4.setText(_translate("Form", "<html><head/><body><p align=\"center\">CALIBRATION</p><p align=\"center\">DIAMETER</p></body></html>"))
        self.cal_diameter.setPlaceholderText(_translate("Form", "0.0000"))
        self.cal_avg_error.setText(_translate("Form", "CAL ON AVG XY ERROR"))
        self.cal_avg_error.setProperty("checkedAction", _translate("Form", "0"))
        self.cal_x_error.setText(_translate("Form", "CAL ON X ERROR"))
        self.cal_x_error.setProperty("checkedAction", _translate("Form", "1"))
        self.cal_y_error.setText(_translate("Form", "CAL ON Y ERROR"))
        self.cal_y_error.setProperty("checkedAction", _translate("Form", "2"))
        self.probe_cal_square_pocket.setProperty("filename", _translate("Form", "probe_cal_square_pocket.ngc"))
        self.probe_cal_square_boss.setProperty("filename", _translate("Form", "probe_cal_square_boss.ngc"))
        self.hint_label_3.setText(_translate("Form", "CALIBRATION WIDTH"))
        self.label_103.setText(_translate("Form", "X :"))
        self.label_107.setText(_translate("Form", "Y :"))
        self.x_cal_width.setPlaceholderText(_translate("Form", "0.0000"))
        self.y_cal_width.setPlaceholderText(_translate("Form", "0.0000"))
        self.probe_help_prev.setText(_translate("Form", "      PREV PAGE       "))
        self.probe_help_next.setText(_translate("Form", "            NEXT PAGE"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.probe_tab), _translate("Form", "PROBING"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.spot_drill_tab), _translate("Form", "SPOT DRILL"))
        self.label_61.setText(_translate("Form", "TIP ANGLE"))
        self.label_60.setText(_translate("Form", "HOLE DIAMETER"))
        self.label_59.setText(_translate("Form", "DIAM DEPTH"))
        self.label_53.setText(_translate("Form", "Z DEPTH"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.drill_tab), _translate("Form", "DRILL"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.ream_tab), _translate("Form", "REAM"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.chamfer_tab), _translate("Form", "CHAMFER"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.rigid_tap_tab), _translate("Form", "RIGID TAP"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.threadmill_tab), _translate("Form", "THREAD MILL"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.XY_tab), _translate("Form", "XY COORD"))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.gcode_tab), _translate("Form", "GENERATE G CODE"))
        self.operation.setTabText(self.operation.indexOf(self.holeop_tab), _translate("Form", "   HOLE OPS   "))
        self.operation.setTabText(self.operation.indexOf(self.facing_tab), _translate("Form", "FACING"))
        self.operation.setTabText(self.operation.indexOf(self.perimeter_tab), _translate("Form", "PERIMETER"))
        self.operation.setTabText(self.operation.indexOf(self.pockets_tab), _translate("Form", "POCKETS"))
        self.operation.setTabText(self.operation.indexOf(self.misc_tab), _translate("Form", "MISC"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.conversational_tab), _translate("Form", "CONVERSATIONAL"))
        self.xyz_checkbox.setProperty("settingName", _translate("Form", "axis-display.xyz-checkbox"))
        self.label_118.setText(_translate("Form", "3 AXIS INTERFACE"))
        self.xyza_checkbox.setProperty("settingName", _translate("Form", "axis-display.xyza-checkbox"))
        self.label_120.setText(_translate("Form", "4 AXIS INTERFACE"))
        self.xyzab_checkbox.setProperty("settingName", _translate("Form", "axis-display.xyzab-checkbox"))
        self.label_121.setText(_translate("Form", "5 AXIS INTERFACE"))
        self.work_column_header_6.setText(_translate("Form", "PROGRAMMED COOLANT CONSTANTS"))
        self.label_127.setText(_translate("Form", "ACTIVATE PROGRAMMABLE COOLANT = 1"))
        self.activate_pogrammable_coolant.setPlaceholderText(_translate("Form", "0"))
        self.activate_pogrammable_coolant.setProperty("settingName", _translate("Form", "programmable-coolant.active"))
        self.activate_pogrammable_coolant.setProperty("textFormat", _translate("Form", "{:0.0f}"))
        self.label_126.setText(_translate("Form", "SPINDLE CENTERLINE TO NOZZLE CENTERLINE DISTANCE"))
        self.horizontal_spindle_nozzle_dist.setPlaceholderText(_translate("Form", "0.0000"))
        self.horizontal_spindle_nozzle_dist.setProperty("settingName", _translate("Form", "programmable-coolant.spindle-to-nozzle-dist"))
        self.horizontal_spindle_nozzle_dist.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_128.setText(_translate("Form", "NOZZLE CENTERLINE TO SPINDLE GAUGE LINE"))
        self.vertical_spindle_nozzle_dist.setPlaceholderText(_translate("Form", "0.0000"))
        self.vertical_spindle_nozzle_dist.setProperty("settingName", _translate("Form", "programmable-coolant.gaugeline-to-nozzle-dist"))
        self.vertical_spindle_nozzle_dist.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_132.setText(_translate("Form", "NOZZLE ANGLE OFFSET"))
        self.pc_angle_offset.setPlaceholderText(_translate("Form", "0.0"))
        self.pc_angle_offset.setProperty("settingName", _translate("Form", "programmable-coolant.pc-angle-offset"))
        self.pc_angle_offset.setProperty("textFormat", _translate("Form", "{:0.4f}"))
        self.label_130.setText(_translate("Form", "TOOL LENGTH OFFSET"))
        self.pc_tool_length.setText(_translate("Form", "0.0000"))
        self.pc_tool_length.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?z_offset\", \"trigger\": true}, {\"url\": \"status:linear_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0]) if ch[1] == \'in\' else \\\"{:.4f}\\\".format(ch[0])\", \"name\": \"Tool Length\"}]"))
        self.pc_tool_length.setProperty("format", _translate("Form", "{:.3f}"))
        self.pc_tool_length.setProperty("statusItem", _translate("Form", "tool_offset.3"))
        self.label_131.setText(_translate("Form", "CALCULATED NOZZLE ANGLE"))
        self.coolant_final_angle.setText(_translate("Form", "0.0000"))
        self.coolant_final_angle.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?z_offset\", \"trigger\": true}, {\"url\": \"status:linear_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0]) if ch[1] == \'in\' else \\\"{:.4f}\\\".format(ch[0])\", \"name\": \"Tool Length\"}]"))
        self.coolant_final_angle.setProperty("format", _translate("Form", "{:.3f}"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings_tab), _translate("Form", "SETTINGS"))
        self.label_111.setText(_translate("Form", "PROBE POS/WCO MODE"))
        self.probe_mode.setText(_translate("Form", "0"))
        self.label_112.setText(_translate("Form", "WCO ROTATION MODE"))
        self.wco_rotation.setText(_translate("Form", "0"))
        self.label_115.setText(_translate("Form", "X and Y CAL AXIS SELECTION"))
        self.sq_cal_axis.setText(_translate("Form", "0"))
        self.label_116.setText(_translate("Form", "TOOL DIAMETER PROBE"))
        self.tool_diameter_probe_mode.setText(_translate("Form", "0"))
        self.label_117.setText(_translate("Form", "TOOL DIAM OFFSET TOUCH OFF"))
        self.tool_diameter_offset_mode.setText(_translate("Form", "0"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.status_tab), _translate("Form", "STATUS"))
        self.z_plus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:z,pos"))
        self.z_minus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:z,neg"))
        self.x_plus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:x,pos"))
        self.x_minus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:x,neg"))
        self.y_minus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:y,neg"))
        self.y_plus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:y,pos"))
        self.a_minus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:a,neg"))
        self.a_plus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:a,pos"))
        self.b_minus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:b,neg"))
        self.b_plus_jogbutton.setProperty("actionName", _translate("Form", "machine.jog.axis:b,pos"))
        self.manual_mode_button.setText(_translate("Form", "MAN"))
        self.manual_mode_button.setProperty("actionName", _translate("Form", "machine.mode.manual"))
        self.auto_mode_button.setText(_translate("Form", "AUTO"))
        self.auto_mode_button.setProperty("actionName", _translate("Form", "machine.mode.auto"))
        self.mdi_mode_button.setText(_translate("Form", "MDI"))
        self.mdi_mode_button.setProperty("actionName", _translate("Form", "machine.mode.mdi"))
        self.label_20.setText(_translate("Form", "MACHINE STATUS:"))
        self.statuslabel_15.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"str\", \"url\": \"status:gcodes?text\"}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Active Codes\"}]"))
        self.statuslabel_16.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"str\", \"url\": \"status:mcodes?text\"}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Active Mcodes\"}]"))
        self.tabWidget_24.setTabText(self.tabWidget_24.indexOf(self.tabWidget_24Page1), _translate("Form", "JOG"))
        self.statuslabel_13.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"str\", \"url\": \"status:gcodes?text\"}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Active Codes\"}]"))
        self.statuslabel_14.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"str\", \"url\": \"status:mcodes?text\"}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Active Mcodes\"}]"))
        self.label_19.setText(_translate("Form", "MACHINE STATUS:"))
        self.actionbutton_g58_3.setText(_translate("Form", "G58"))
        self.actionbutton_g58_3.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G58\' in ch[0]\", \"name\": \"g58_offset_status\"}]"))
        self.actionbutton_g58_3.setProperty("actionName", _translate("Form", "machine.set-work-coord:G58"))
        self.actionbutton_g59_8.setText(_translate("Form", "G59.3"))
        self.actionbutton_g59_8.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G59.3\' in ch[0]\", \"name\": \"g59_3_offset_status\"}]"))
        self.actionbutton_g59_8.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.3"))
        self.actionbutton_g54_3.setText(_translate("Form", "G54"))
        self.actionbutton_g54_3.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:current_line?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \" \'m2, M2, m02, M02, m30, M30\' in ch[0]\", \"name\": \"g54_offset_status\"}]"))
        self.actionbutton_g54_3.setProperty("actionName", _translate("Form", "machine.set-work-coord:G54"))
        self.actionbutton_g56_3.setText(_translate("Form", "G56"))
        self.actionbutton_g56_3.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G56\' in ch[0]\", \"name\": \"g56_offset_status\"}]"))
        self.actionbutton_g56_3.setProperty("actionName", _translate("Form", "machine.set-work-coord:G56"))
        self.actionbutton_g55_3.setText(_translate("Form", "G55"))
        self.actionbutton_g55_3.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G55\' in ch[0]\", \"name\": \"g55_offset_status\"}]"))
        self.actionbutton_g55_3.setProperty("actionName", _translate("Form", "machine.set-work-coord:G55"))
        self.actionbutton_g57_3.setText(_translate("Form", "G57"))
        self.actionbutton_g57_3.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G57\' in ch[0]\", \"name\": \"g57_offset_status\"}]"))
        self.actionbutton_g57_3.setProperty("actionName", _translate("Form", "machine.set-work-coord:G57"))
        self.actionbutton_g59_10.setText(_translate("Form", "G59"))
        self.actionbutton_g59_10.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G59\' in ch[0]\", \"name\": \"g59_offset_status\"}]"))
        self.actionbutton_g59_10.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59"))
        self.actionbutton_g59_11.setText(_translate("Form", "G59.2"))
        self.actionbutton_g59_11.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G59.2\' in ch[0]\", \"name\": \"g59_2_offset_status\"}]"))
        self.actionbutton_g59_11.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.2"))
        self.actionbutton_g59_9.setText(_translate("Form", "G59.1"))
        self.actionbutton_g59_9.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?string\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G59.1\' in ch[0]\", \"name\": \"g59_1_offset_status\"}]"))
        self.actionbutton_g59_9.setProperty("actionName", _translate("Form", "machine.set-work-coord:G59.1"))
        self.manual_mode_button_2.setText(_translate("Form", "MAN"))
        self.manual_mode_button_2.setProperty("actionName", _translate("Form", "machine.mode.manual"))
        self.auto_mode_button_2.setText(_translate("Form", "AUTO"))
        self.auto_mode_button_2.setProperty("actionName", _translate("Form", "machine.mode.auto"))
        self.mdi_mode_button_2.setText(_translate("Form", "MDI"))
        self.mdi_mode_button_2.setProperty("actionName", _translate("Form", "machine.mode.mdi"))
        self.tabWidget_24.setTabText(self.tabWidget_24.indexOf(self.tab_17), _translate("Form", "CUSTOM"))
        self.iso_view_button_plot.setText(_translate("Form", "ISO VIEW"))
        self.x_view_button_plot.setText(_translate("Form", "X View"))
        self.y_view_button_plot.setText(_translate("Form", "Y View"))
        self.z_view_button_plot.setText(_translate("Form", "Z View"))
        self.zoom_in_button_plot.setText(_translate("Form", "ZOOM +"))
        self.zoom_out_button_plot.setText(_translate("Form", "ZOOM -"))
        self.clear_button_plot.setText(_translate("Form", "CLEAR"))
        self.ortho_button_plot.setText(_translate("Form", "ORTHO"))
        self.perspective_button_plot.setText(_translate("Form", "PSPECT"))
        self.program_boundry_button.setText(_translate("Form", "PRG BDRY"))
        self.machine_boundry_button.setText(_translate("Form", "MCH BDRY"))
        self.program_ticks_button.setText(_translate("Form", "PGM TICKS"))
        self.machine_ticks_button.setText(_translate("Form", "MCH TICKS"))
        self.program_labels_button.setText(_translate("Form", "PGM LABEL"))
        self.machine_labels_button.setText(_translate("Form", "MCH LABEL"))
        self.plot_grid_button.setText(_translate("Form", "PLOT GRID"))
        self.program_zoom_button_plot.setText(_translate("Form", "PGM EXTS"))
        self.machine_zoom_button_plot.setText(_translate("Form", "MCH EXTS"))
        self.manual_mode_button_3.setText(_translate("Form", "MAN"))
        self.manual_mode_button_3.setProperty("actionName", _translate("Form", "machine.mode.manual"))
        self.auto_mode_button_3.setText(_translate("Form", "AUTO"))
        self.auto_mode_button_3.setProperty("actionName", _translate("Form", "machine.mode.auto"))
        self.mdi_mode_button_3.setText(_translate("Form", "MDI"))
        self.mdi_mode_button_3.setProperty("actionName", _translate("Form", "machine.mode.mdi"))
        self.statuslabel_17.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"str\", \"url\": \"status:gcodes?text\"}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Active Codes\"}]"))
        self.statuslabel_18.setProperty("rules", _translate("Form", "[{\"channels\": [{\"trigger\": true, \"type\": \"str\", \"url\": \"status:mcodes?text\"}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Active Mcodes\"}]"))
        self.label_104.setText(_translate("Form", "MACHINE STATUS:"))
        self.tabWidget_24.setTabText(self.tabWidget_24.indexOf(self.tab_2), _translate("Form", "PLOT"))
        self.actionbutton_3.setText(_translate("Form", "CYCLE START"))
        self.actionbutton_3.setProperty("actionName", _translate("Form", "program.run"))
        self.actionbutton_7.setText(_translate("Form", "RUN FM HERE"))
        self.actionbutton_7.setProperty("actionName", _translate("Form", "program.run-from-line"))
        self.actionbutton_10.setText(_translate("Form", "FEED HOLD"))
        self.actionbutton_10.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:interp_state?text\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"ch[0] == \'Paused\'\", \"name\": \"check when paused\"}]"))
        self.actionbutton_10.setProperty("actionName", _translate("Form", "program.pause"))
        self.actionbutton.setText(_translate("Form", "SINGLE BLOCK"))
        self.actionbutton.setProperty("actionName", _translate("Form", "program.step"))
        self.actionbutton_5.setText(_translate("Form", "STOP"))
        self.actionbutton_5.setProperty("actionName", _translate("Form", "program.abort"))
        self.actionbutton_9.setText(_translate("Form", "Flood"))
        self.actionbutton_9.setProperty("actionName", _translate("Form", "coolant.flood.toggle"))
        self.actionbutton_6.setText(_translate("Form", "BLOCK DELETE"))
        self.actionbutton_6.setProperty("actionName", _translate("Form", "program.block-delete.toggle"))
        self.actionbutton_8.setText(_translate("Form", "Mist"))
        self.actionbutton_8.setProperty("actionName", _translate("Form", "coolant.mist.toggle"))
        self.actionbutton_2.setText(_translate("Form", "M01 BREAK"))
        self.actionbutton_2.setProperty("actionName", _translate("Form", "program.optional-stop.toggle"))
        self.power_button.setText(_translate("Form", "POWER"))
        self.power_button.setProperty("actionName", _translate("Form", "machine.power.toggle"))
        self.timerhours.setText(_translate("Form", "00"))
        self.timerhours.setProperty("textFormat", _translate("Form", "%02d"))
        self.label_2.setText(_translate("Form", ":"))
        self.timerminutes.setText(_translate("Form", "00"))
        self.timerminutes.setProperty("textFormat", _translate("Form", "%02d"))
        self.label_3.setText(_translate("Form", ":"))
        self.timerseconds.setText(_translate("Form", "00"))
        self.timerseconds.setProperty("textFormat", _translate("Form", "%02d"))
        self.exit_button.setText(_translate("Form", "E-STOP"))
        self.exit_button.setProperty("actionName", _translate("Form", "machine.estop.toggle"))
        self.ref_coilumn_header_3.setText(_translate("Form", "  T"))
        self.tool_number_entry_main_panel.setText(_translate("Form", "0"))
        self.tool_number_entry_main_panel.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?tool_number\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"str(ch[0])\", \"name\": \"update tool num\"}, {\"channels\": [{\"url\": \"status:task_state?text\", \"trigger\": true}, {\"url\": \"status:interp_state?text\", \"trigger\": true}], \"property\": \"Enable\", \"expression\": \"ch[0] == \'On\' and ch[1] == \'Idle\'\", \"name\": \"enable/disable\"}]"))
        self.m6_tool_call_button_main_panel.setText(_translate("Form", "M6 G43"))
        self.m6_tool_call_button_main_panel.setProperty("filename", _translate("Form", "m6_tool_call_main_panel.ngc"))
        self.G43.setText(_translate("Form", "G43"))
        self.G43.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?text\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G43\' in ch[0]\", \"name\": \"G43\"}, {\"channels\": [{\"url\": \"status:tool_in_spindle\", \"trigger\": false}, {\"url\": \"status:interp_state\", \"trigger\": true}, {\"url\": \"status:homed\", \"trigger\": true}], \"property\": \"Enable\", \"expression\": \"ch[0] != 0\", \"name\": \"disable if no tool loaded\"}]"))
        self.G43.setProperty("MDICommand", _translate("Form", "G43"))
        self.G49.setText(_translate("Form", "G49"))
        self.G49.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:gcodes?text\", \"trigger\": true}], \"property\": \"Checked\", \"expression\": \"\'G49\' in ch[0]\", \"name\": \"G49\"}]"))
        self.G49.setProperty("MDICommand", _translate("Form", "G49"))
        self.work_column_header_4.setText(_translate("Form", "LENGTH"))
        self.tool_length.setText(_translate("Form", "0.0000"))
        self.tool_length.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?z_offset\", \"trigger\": true}, {\"url\": \"status:linear_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0]) if ch[1] == \'in\' else \\\"{:.4f}\\\".format(ch[0])\", \"name\": \"Tool Length\"}]"))
        self.tool_length.setProperty("format", _translate("Form", "{:.3f}"))
        self.tool_length.setProperty("statusItem", _translate("Form", "tool_offset.3"))
        self.statuslabel_8.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:linear_units?text\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"str\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"ch[0]\",\n"
"        \"name\": \"Units\",\n"
"        \"property\": \"Text\"\n"
"    }\n"
"]"))
        self.work_column_header_5.setText(_translate("Form", "DIAM"))
        self.tool_diameter.setText(_translate("Form", "0.0000"))
        self.tool_diameter.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"tooltable:current_tool?diameter\", \"trigger\": true}, {\"url\": \"status:linear_units?text\", \"trigger\": false}], \"property\": \"Text\", \"expression\": \"\\\"{:.4f}\\\".format(ch[0]) if ch[1] == \'in\' else \\\"{:.4f}\\\".format(ch[0])\", \"name\": \"Tool Diameter\"}]"))
        self.tool_diameter.setProperty("format", _translate("Form", "{:.3f}"))
        self.tool_diameter.setProperty("statusItem", _translate("Form", "tool_offset.3"))
        self.statuslabel_11.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:linear_units?text\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Units\"}]"))
        self.go_to_zero_button_2.setText(_translate("Form", "GO TO ZERO"))
        self.go_to_zero_button_2.setProperty("filename", _translate("Form", "go_to_zero.ngc"))
        self.go_to_g30_button.setText(_translate("Form", "GO TO G30"))
        self.go_to_g30_button.setProperty("filename", _translate("Form", "go_to_g30.ngc"))
        self.go_to_home_button.setText(_translate("Form", "GO TO HOME"))
        self.go_to_home_button.setProperty("filename", _translate("Form", "go_to_home.ngc"))
        self.gui_axis_display_widget.setProperty("settingName", _translate("Form", "axis_display_setting"))
        self.statuslabel_21.setText(_translate("Form", "AXIS"))
        self.statuslabel_21.setProperty("rules", _translate("Form", "[]"))
        self.statuslabel_20.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:g5x_index?text\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0] + \' WORK\'\\n\", \"name\": \"WCS Header\"}]"))
        self.work_column_header_8.setText(_translate("Form", "MACHINE"))
        self.dtg_column_header_3.setText(_translate("Form", "DTG"))
        self.statuslabel_22.setText(_translate("Form", "REF"))
        self.statuslabel_22.setProperty("rules", _translate("Form", "[]"))
        self.zero_x_button_5.setText(_translate("Form", "X"))
        self.zero_x_button_5.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_x_button_5.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} X0.0"))
        self.statuslabel_101.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_102.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_102.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.0.homed\", \"trigger\": true}, {\"url\": \"status:joint.0.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_103.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_13.setText(_translate("Form", "REF X"))
        self.axisactionbutton_13.setProperty("actionName", _translate("Form", "machine.home.axis:x"))
        self.zero_y_button_5.setText(_translate("Form", "Y"))
        self.zero_y_button_5.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_y_button_5.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} Y0.0"))
        self.statuslabel_92.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_93.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_93.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.1.homed\", \"trigger\": true}, {\"url\": \"status:joint.1.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_94.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_10.setText(_translate("Form", "REF Y"))
        self.axisactionbutton_10.setProperty("actionName", _translate("Form", "machine.home.axis:y"))
        self.zero_z_button_5.setText(_translate("Form", "Z"))
        self.zero_z_button_5.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_z_button_5.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} Z0.0"))
        self.statuslabel_95.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_96.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_96.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.2.homed\", \"trigger\": true}, {\"url\": \"status:joint.2.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_97.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_11.setText(_translate("Form", "REF Z"))
        self.axisactionbutton_11.setProperty("actionName", _translate("Form", "machine.home.axis:z"))
        self.zero_all_button_4.setText(_translate("Form", "ZERO ALL"))
        self.zero_all_button_4.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_all_button_4.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} X0.0 Y0.0 Z0.0"))
        self.ref_all_button_4.setText(_translate("Form", "REF ALL"))
        self.ref_all_button_4.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:all_axes_homed\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\'HOMED\' if ch[0] else \'REF ALL\'\", \"name\": \"reference_all\"}]"))
        self.ref_all_button_4.setProperty("actionName", _translate("Form", "machine.home.all"))
        self.statuslabel_23.setText(_translate("Form", "AXIS"))
        self.statuslabel_23.setProperty("rules", _translate("Form", "[]"))
        self.statuslabel_24.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:g5x_index?text\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0] + \' WORK\'\\n\", \"name\": \"WCS Header\"}]"))
        self.work_column_header_9.setText(_translate("Form", "MACHINE"))
        self.dtg_column_header_4.setText(_translate("Form", "DTG"))
        self.statuslabel_25.setText(_translate("Form", "REF"))
        self.statuslabel_25.setProperty("rules", _translate("Form", "[]"))
        self.zero_x_button_4.setText(_translate("Form", "X"))
        self.zero_x_button_4.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_x_button_4.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} X0.0"))
        self.statuslabel_89.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_90.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_90.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.0.homed\", \"trigger\": true}, {\"url\": \"status:joint.0.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_91.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_9.setText(_translate("Form", "REF X"))
        self.axisactionbutton_9.setProperty("actionName", _translate("Form", "machine.home.axis:x"))
        self.zero_y_button_4.setText(_translate("Form", "Y"))
        self.zero_y_button_4.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_y_button_4.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} Y0.0"))
        self.statuslabel_80.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_81.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_81.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.1.homed\", \"trigger\": true}, {\"url\": \"status:joint.1.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_82.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_5.setText(_translate("Form", "REF Y"))
        self.axisactionbutton_5.setProperty("actionName", _translate("Form", "machine.home.axis:y"))
        self.zero_z_button_4.setText(_translate("Form", "Z"))
        self.zero_z_button_4.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_z_button_4.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} Z0.0"))
        self.statuslabel_83.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_84.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_84.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.2.homed\", \"trigger\": true}, {\"url\": \"status:joint.2.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_85.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_7.setText(_translate("Form", "REF Z"))
        self.axisactionbutton_7.setProperty("actionName", _translate("Form", "machine.home.axis:z"))
        self.zero_a_button_4.setText(_translate("Form", "A"))
        self.zero_a_button_4.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_a_button_4.setProperty("MDICommand", _translate("Form", "G10 L2 P{ch[0]} A0.0"))
        self.statuslabel_86.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=a\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_87.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_87.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=a\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.3.homed\", \"trigger\": true}, {\"url\": \"status:joint.3.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_88.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=a\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_8.setText(_translate("Form", "REF A"))
        self.axisactionbutton_8.setProperty("actionName", _translate("Form", "machine.home.axis:a"))
        self.zero_all_button_5.setText(_translate("Form", "ZERO ALL"))
        self.zero_all_button_5.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_all_button_5.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} X0.0 Y0.0 Z0.0"))
        self.ref_all_button_5.setText(_translate("Form", "REF ALL"))
        self.ref_all_button_5.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:all_axes_homed\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\'HOMED\' if ch[0] else \'REF ALL\'\", \"name\": \"reference_all\"}]"))
        self.ref_all_button_5.setProperty("actionName", _translate("Form", "machine.home.all"))
        self.zero_all_button.setText(_translate("Form", "ALL"))
        self.zero_all_button.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_all_button.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} X0.0 Y0.0 Z0.0"))
        self.statuslabel_12.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:g5x_index?text\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0] + \' WORK\'\\n\", \"name\": \"WCS Header\"}]"))
        self.work_column_header_2.setText(_translate("Form", "MACHINE"))
        self.dtg_column_header.setText(_translate("Form", "DTG"))
        self.ref_all_button.setText(_translate("Form", "REF ALL"))
        self.ref_all_button.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:all_axes_homed\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\'HOMED\' if ch[0] else \'REF ALL\'\", \"name\": \"reference_all\"}]"))
        self.ref_all_button.setProperty("actionName", _translate("Form", "machine.home.all"))
        self.zero_x_button_3.setText(_translate("Form", "X"))
        self.zero_x_button_3.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_x_button_3.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} X0.0"))
        self.statuslabel_40.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_45.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_45.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.0.homed\", \"trigger\": true}, {\"url\": \"status:joint.0.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_75.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=x\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_6.setText(_translate("Form", "REF X"))
        self.axisactionbutton_6.setProperty("actionName", _translate("Form", "machine.home.axis:x"))
        self.zero_y_button_3.setText(_translate("Form", "Y"))
        self.zero_y_button_3.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_y_button_3.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} Y0.0"))
        self.statuslabel_41.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_46.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_46.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.1.homed\", \"trigger\": true}, {\"url\": \"status:joint.1.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_76.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=y\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_3.setText(_translate("Form", "REF Y"))
        self.axisactionbutton_3.setProperty("actionName", _translate("Form", "machine.home.axis:y"))
        self.zero_z_button_3.setText(_translate("Form", "Z"))
        self.zero_z_button_3.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_z_button_3.setProperty("MDICommand", _translate("Form", "G10 L20 P{ch[0]} Z0.0"))
        self.statuslabel_42.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_47.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_47.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.2.homed\", \"trigger\": true}, {\"url\": \"status:joint.2.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_77.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=z\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton.setText(_translate("Form", "REF Z"))
        self.axisactionbutton.setProperty("actionName", _translate("Form", "machine.home.axis:z"))
        self.zero_a_button_3.setText(_translate("Form", "A"))
        self.zero_a_button_3.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_a_button_3.setProperty("MDICommand", _translate("Form", "G10 L2 P{ch[0]} A0.0"))
        self.statuslabel_43.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=a\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_48.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_48.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=a\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.3.homed\", \"trigger\": true}, {\"url\": \"status:joint.3.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_78.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=a\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_2.setText(_translate("Form", "REF A"))
        self.axisactionbutton_2.setProperty("actionName", _translate("Form", "machine.home.axis:a"))
        self.zero_b_button_3.setText(_translate("Form", "B"))
        self.zero_b_button_3.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:g5x_index\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"int\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\",\n"
"        \"name\": \"G5x Index\",\n"
"        \"property\": \"None\"\n"
"    }\n"
"]"))
        self.zero_b_button_3.setProperty("MDICommand", _translate("Form", "G10 L2 P{ch[0]} B0.0"))
        self.statuslabel_44.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:rel?string&axis=b\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.statuslabel_49.setProperty("style", _translate("Form", "unhomed"))
        self.statuslabel_49.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:abs?string&axis=b\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"axis position\"}, {\"channels\": [{\"url\": \"status:joint.4.homed\", \"trigger\": true}, {\"url\": \"status:joint.4.homing\", \"trigger\": true}], \"property\": \"Style Class\", \"expression\": \"\\\"homed\\\" if ch[0] else \\\"homing\\\" if ch[1] else \\\"unhomed\\\"\", \"name\": \"homing indicator\"}]"))
        self.statuslabel_79.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"position:dtg?string&axis=b\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"REL axis position\"}]"))
        self.axisactionbutton_4.setText(_translate("Form", "REF B"))
        self.axisactionbutton_4.setProperty("actionName", _translate("Form", "machine.home.axis:b"))
        self.statuslabel.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:feedrate\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"float\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\'{:.0%}\'.format(ch[0])\",\n"
"        \"name\": \"New Rule\",\n"
"        \"property\": \"Text\"\n"
"    }\n"
"]"))
        self.actionslider_4.setProperty("actionName", _translate("Form", "machine.rapid-override.set"))
        self.statuslabel_2.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:spindle.0.override\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\'{:.0%}\'.format(ch[0])\", \"name\": \"New Rule\"}]"))
        self.statuslabel_3.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:rapidrate\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"float\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\'{:.0%}\'.format(ch[0])\",\n"
"        \"name\": \"New Rule\",\n"
"        \"property\": \"Text\"\n"
"    }\n"
"]"))
        self.work_column_header_3.setText(_translate("Form", "SPINDLE\n"
"LOAD"))
        self.max_vel_slider.setProperty("rules", _translate("Form", "[\n"
"    {\n"
"        \"channels\": [\n"
"            {\n"
"                \"url\": \"status:max_velocity\",\n"
"                \"trigger\": true,\n"
"                \"type\": \"float\"\n"
"            }\n"
"        ],\n"
"        \"expression\": \"\'{:.0f}\'.format(ch[0] * 60)\",\n"
"        \"name\": \"New Rule\",\n"
"        \"property\": \"Text\"\n"
"    }\n"
"]"))
        self.actionslider.setProperty("actionName", _translate("Form", "spindle.override"))
        self.actionbutton_28.setText(_translate("Form", "S 100%"))
        self.actionbutton_28.setProperty("actionName", _translate("Form", "spindle.override.reset"))
        self.actionslider_2.setProperty("actionName", _translate("Form", "machine.feed-override.set"))
        self.actionslider_3.setProperty("actionName", _translate("Form", "machine.max-velocity.set"))
        self.actionbutton_29.setText(_translate("Form", "F 100%"))
        self.actionbutton_29.setProperty("actionName", _translate("Form", "machine.feed-override.reset"))
        self.actionbutton_30.setText(_translate("Form", "V 100%"))
        self.actionbutton_30.setProperty("actionName", _translate("Form", "machine.max-velocity.reset"))
        self.actionbutton_31.setText(_translate("Form", "R 100%"))
        self.actionbutton_31.setProperty("actionName", _translate("Form", "machine.rapid-override.reset"))
        self.settings_slider.setProperty("settingName", _translate("Form", "machine.jog.linear-speed-percentage"))
        self.fr_override_dro_2.setText(_translate("Form", "30%"))
        self.fr_override_dro_2.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"settings:machine.jog.linear-speed-percentage\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"%s%%\\\" % ch[0]\", \"name\": \"New Rule\"}]"))
        self.statuslabel_6.setText(_translate("Form", "0.0"))
        self.statuslabel_6.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:current_vel\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\'%.1f\' % (ch[0] * 60)\", \"name\": \"cur vel\"}]"))
        self.statuslabel_6.setProperty("format", _translate("Form", "{:.1f}"))
        self.rpm_label_3.setText(_translate("Form", "FEEDRATE"))
        self.statuslabel_10.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:program_units?text\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"ch[0]\", \"name\": \"Linear Units\"}]"))
        self.work_column_header_7.setText(_translate("Form", "/M"))
        self.statuslabel_7.setText(_translate("Form", "0.0"))
        self.statuslabel_7.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:settings\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\'%.1f\' % ch[0][1]\", \"name\": \"F Word\"}]"))
        self.statuslabel_7.setProperty("format", _translate("Form", "{:1f}"))
        self.statuslabel_5.setText(_translate("Form", "0"))
        self.statuslabel_5.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:spindle.0.speed\", \"trigger\": true}, {\"url\": \"status:spindle.0.override\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"\\\"{:.0f}\\\".format(ch[0] * ch[1])\", \"name\": \"Speed\"}]"))
        self.statuslabel_5.setProperty("format", _translate("Form", "{:.0f}"))
        self.rpm_label.setText(_translate("Form", "SPINDLE RPM"))
        self.statuslabel_9.setText(_translate("Form", "0.0"))
        self.statuslabel_9.setProperty("rules", _translate("Form", "[{\"channels\": [{\"url\": \"status:settings?speed\", \"trigger\": true}], \"property\": \"Text\", \"expression\": \"str( ch[0] )\", \"name\": \"S Word\"}]"))
        self.statuslabel_9.setProperty("format", _translate("Form", "{:.0f}"))
        self.spindle_rev_button.setText(_translate("Form", "REV"))
        self.spindle_rev_button.setProperty("actionName", _translate("Form", "spindle.reverse"))
        self.spindle_stop_button.setText(_translate("Form", "STOP"))
        self.spindle_stop_button.setProperty("actionName", _translate("Form", "spindle.off"))
        self.spindle_fwd_button.setText(_translate("Form", "FWD"))
        self.spindle_fwd_button.setProperty("actionName", _translate("Form", "spindle.forward"))
        self.menuExit.setTitle(_translate("Form", "File"))
        self.menuRecentFiles.setTitle(_translate("Form", "Recent &Files"))
        self.menuMachine.setTitle(_translate("Form", "Machine"))
        self.menuHoming.setTitle(_translate("Form", "Homing"))
        self.menuCooling.setTitle(_translate("Form", "Cooling"))
        self.menuView.setTitle(_translate("Form", "View"))
        self.actionExit.setText(_translate("Form", "Exit"))
        self.actionOpen.setText(_translate("Form", "&Open ..."))
        self.actionOpen.setShortcut(_translate("Form", "O"))
        self.actionClose.setText(_translate("Form", "Close"))
        self.actionReload.setText(_translate("Form", "&Reload"))
        self.actionReload.setShortcut(_translate("Form", "Ctrl+R"))
        self.actionSave_As.setText(_translate("Form", "Save As ..."))
        self.actionHome_X.setText(_translate("Form", "Home &X"))
        self.actionHome_Y.setText(_translate("Form", "Home &Y"))
        self.actionHome_Z.setText(_translate("Form", "Home &Z"))
        self.action_EmergencyStop_toggle.setText(_translate("Form", "Toggle E-stop"))
        self.action_EmergencyStop_toggle.setShortcut(_translate("Form", "F1"))
        self.action_MachinePower_toggle.setText(_translate("Form", "Machine Power"))
        self.action_MachinePower_toggle.setShortcut(_translate("Form", "F2"))
        self.actionHome_All.setText(_translate("Form", "Home All"))
        self.actionRun_Program.setText(_translate("Form", "Run Program"))
        self.actionRun_Program.setShortcut(_translate("Form", "R"))
        self.actionFile1.setText(_translate("Form", "File1"))
        self.actionReport_Actual_Position.setText(_translate("Form", "Report Actual Position"))
        self.actionTest.setText(_translate("Form", "Test"))
        self.action_Mist_toggle.setText(_translate("Form", "Mist On"))
        self.action_Mist_toggle.setShortcut(_translate("Form", "F7"))
        self.action_Flood_toggle.setText(_translate("Form", "Flood On"))
        self.action_Flood_toggle.setShortcut(_translate("Form", "F8"))

from PyQt5 import QtQuickWidgets
from qtpyvcp.widgets.button_widgets.action_button import ActionButton
from qtpyvcp.widgets.button_widgets.mdi_button import MDIButton
from qtpyvcp.widgets.button_widgets.subcall_button import SubCallButton
from qtpyvcp.widgets.containers.stack import VCPStackedWidget
from qtpyvcp.widgets.display_widgets.atc_widget.atc import DynATC
from qtpyvcp.widgets.display_widgets.load_meter import LoadMeter
from qtpyvcp.widgets.display_widgets.notification_widget import NotificationWidget
from qtpyvcp.widgets.display_widgets.status_label import StatusLabel
from qtpyvcp.widgets.display_widgets.vtk_backplot.vtk_backplot import VTKBackPlot
from qtpyvcp.widgets.form_widgets.main_window import VCPMainWindow
from qtpyvcp.widgets.hal_widgets.hal_label import HalLabel
from qtpyvcp.widgets.input_widgets.action_slider import ActionSlider
from qtpyvcp.widgets.input_widgets.file_system import FileSystemTable, RemovableDeviceComboBox
from qtpyvcp.widgets.input_widgets.gcode_editor import GcodeEditor
from qtpyvcp.widgets.input_widgets.jog_increment import JogIncrementWidget
from qtpyvcp.widgets.input_widgets.line_edit import VCPLineEdit
from qtpyvcp.widgets.input_widgets.mdientry_widget import MDIEntry
from qtpyvcp.widgets.input_widgets.offset_table import OffsetTable
from qtpyvcp.widgets.input_widgets.probesim_widget import ProbeSim
from qtpyvcp.widgets.input_widgets.recent_file_combobox import RecentFileComboBox
from qtpyvcp.widgets.input_widgets.setting_slider import VCPSettingsCheckBox, VCPSettingsLineEdit, VCPSettingsSlider
from qtpyvcp.widgets.input_widgets.tool_table import ToolTable
import probe_basic_rc
