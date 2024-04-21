##########################################################
#
# Script: main.py
# Author: Jani Hirvinen aka jpkh
# Contact: [Use GitHub issues for questions and suggestions]
# Repository: https://github.com/jpkh/ki_qihe
#
# Date: 2024-04-07
# Version: 1.0
#
# Description:
# This script handles the generation of machine-readable files for QIHE PnP machines
# based on the PCB design data provided.
#
# Works:
#  - Windows/Cywin
#  - Linux
#  - MacOS
#

import os
import wx
import pcbnew  # type: ignore
import json
import webbrowser  # Import to handle URL opening
import subprocess  # For exit text file
import sys

from .qihe import QiHeProcess
from .log_util import log_message
from .functions import create_default_mapping_file
from .config import (
    def_optionsFileName,
    def_top_fileext,
    def_bottom_fileext,
    def_have_separator,
    def_CompopentMapping,
    def_version,
    def_date
)


class KiQIHEMain(wx.Frame):
    def __init__(self):
        wx.Dialog.__init__(
            self,
            None,
            id=wx.ID_ANY,
            title="QIHE PnP Coords Processor",
            pos=wx.DefaultPosition,
            size=wx.Size(800, 500),  # Adjusted size for better layout
            style=wx.DEFAULT_DIALOG_STYLE,
        )

        icon = wx.Icon(os.path.join(os.path.dirname(__file__), "icon.png"))
        self.SetIcon(icon)
        self.SetBackgroundColour(wx.LIGHT_GREY)
        self.SetSizeHints(wx.Size(800, 500), wx.DefaultSize)

        # Top-level sizer
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Left panel setup (main controls)
        leftPanel = wx.Panel(self)
        leftSizer = wx.BoxSizer(wx.VERTICAL)

        # Generate button
        self.mGenerateButton = wx.Button(leftPanel, label="Generate COORDS", size=wx.Size(600, 60))
        self.mGenerateButton.SetToolTip("Click to generate coordinate files for selected layers")

        # Layers selection and file prefixes in a frame
        layersPanel = wx.StaticBoxSizer(wx.VERTICAL, leftPanel, "Layers to include and file prefixes:")
        layerCheckSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.chkTop = wx.CheckBox(leftPanel, label="Top")
        self.chkTop.SetToolTip("Generate coordinates for the top layer")
        self.chkBottom = wx.CheckBox(leftPanel, label="Bottom")
        self.chkBottom.SetToolTip("Generate coordinates for the bottom layer")

        layerCheckSizer.Add(self.chkTop, 0, wx.RIGHT, 10)
        layerCheckSizer.Add(self.chkBottom, 0, wx.RIGHT, 5)

        prefixSizer = wx.FlexGridSizer(2, 2, 5, 5)
        prefixSizer.AddGrowableCol(1)
        self.txtTopPrefixLabel = wx.StaticText(leftPanel, label="Top Layer Prefix:")
        self.txtTopPrefix = wx.TextCtrl(leftPanel, value=def_top_fileext, size=(180, 25))
        self.txtTopPrefix.SetToolTip("Prefix for the top layer coordinate file")
        self.txtBottomPrefixLabel = wx.StaticText(leftPanel, label="Bottom Layer Prefix:")
        self.txtBottomPrefix = wx.TextCtrl(leftPanel, value=def_bottom_fileext, size=(180, 25))
        self.txtBottomPrefix.SetToolTip("Prefix for the bottom layer coordinate file")
        prefixSizer.AddMany([
            (self.txtTopPrefixLabel, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.txtTopPrefix, 1, wx.EXPAND),
            (self.txtBottomPrefixLabel, 0, wx.ALIGN_CENTER_VERTICAL),
            (self.txtBottomPrefix, 1, wx.EXPAND)
        ])
        layersPanel.Add(layerCheckSizer, 0, wx.ALL, 5)
        layersPanel.Add(prefixSizer, 1, wx.EXPAND | wx.ALL, 5)

        # Activity log in a frame
        logPanel = wx.StaticBoxSizer(wx.VERTICAL, leftPanel, "Activity LOG:")

        self.mLogTextCtrl = wx.TextCtrl(leftPanel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=wx.Size(600, 150))
        logPanel.Add(self.mLogTextCtrl, 1, wx.EXPAND | wx.ALL, 5)

        # Log verbosity settings under the activity log
        verbosityPanel = wx.BoxSizer(wx.HORIZONTAL)
        verbosityLabel = wx.StaticText(leftPanel, label="Log Verbosity:")
        self.verbosityRadioButtons = [
            wx.RadioButton(leftPanel, label="0", style=wx.RB_GROUP),
            wx.RadioButton(leftPanel, label="1"),
            wx.RadioButton(leftPanel, label="2"),
            wx.RadioButton(leftPanel, label="3")
        ]

        verbosityToolTips = [
            "Minimal logging: Only essential information will be logged.",
            "Normal logging: Regular activity and important events will be logged.",
            "Verbose logging: Detailed logging of normal and important events.",
            "Debug logging: All possible details including debugging information will be logged."
        ]

        verbosityPanel.Add(verbosityLabel, 0, wx.RIGHT, 5)
        for btn, tip in zip(self.verbosityRadioButtons, verbosityToolTips):
            btn.SetToolTip(tip)
            verbosityPanel.Add(btn, 0, wx.RIGHT, 5)

        # Add verbosity panel below the log panel
        logPanel.Add(verbosityPanel, 0, wx.TOP | wx.EXPAND, 10)

        # Mapping file location with text box
        mappingPanel = wx.StaticBoxSizer(wx.HORIZONTAL, leftPanel, "Mapping File Location:")
        self.radioBox = wx.RadioBox(
            leftPanel, choices=["Plugin folder", "PCB folder"],
            majorDimension=1, style=wx.RA_SPECIFY_ROWS
        )

        # Create a horizontal sizer for the filename label, text control, and edit button
        mappingNameSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.txtMappingFileNameLabel = wx.StaticText(leftPanel, label="Name:")
        self.txtMappingFileName = wx.TextCtrl(leftPanel, value=def_CompopentMapping, size=(180, -1))
        self.txtMappingFileName.SetToolTip("Name of the component mapping file")

        self.editButton = wx.Button(leftPanel, label="Edit", size=(70, -1))
        self.editButton.SetForegroundColour(wx.Colour('blue'))

        # Add to sizer with alignment flags
        mappingNameSizer.Add(self.txtMappingFileNameLabel, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=5)
        mappingNameSizer.Add(self.txtMappingFileName, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL)
        mappingNameSizer.Add(self.editButton, flag=wx.ALIGN_CENTER_VERTICAL)

        # Bind the edit button click event
        self.editButton.Bind(wx.EVT_BUTTON, self.onEditMappingFile)

        # Add the radio box and the filename sizer to the mapping panel
        mappingPanel.Add(self.radioBox, 0, wx.ALL | wx.EXPAND, 5)
        mappingPanel.Add(mappingNameSizer, 1, wx.EXPAND | wx.ALL, 5)

        # Add controls to left sizer
        leftSizer.Add(self.mGenerateButton, 0, wx.ALL, 5)
        leftSizer.Add(mappingPanel, 0, wx.EXPAND | wx.ALL, 5)
        leftSizer.Add(layersPanel, 0, wx.EXPAND | wx.ALL, 5)
        leftSizer.Add(logPanel, 1, wx.EXPAND | wx.ALL, 5)
        leftPanel.SetSizer(leftSizer)

        # Right panel setup (action buttons)
        rightPanel = wx.Panel(self)
        actionsPanel = wx.StaticBoxSizer(wx.VERTICAL, rightPanel, "Actions:")
        self.ACT_BTN_1 = wx.Button(rightPanel, label="Gen Mapping", size=wx.Size(100, 25))
        self.ACT_BTN_1.SetToolTip("Force generate the default mapping file. USE WITH CAUTION!")
        # self.ACT_BTN_2 = wx.Button(rightPanel, label="Button 1", size=wx.Size(100, 25))
        # self.ACT_BTN_3 = wx.Button(rightPanel, label="Button 2", size=wx.Size(100, 25))
        self.ACT_BTN_4 = wx.Button(rightPanel, label="Save Options", size=wx.Size(100, 25))
        self.ACT_BTN_4.SetToolTip("Save the current settings to the options file.")

        # Adding buttons and the reminder text to the actions panel
        actionsPanel.Add(self.ACT_BTN_1, 0, wx.ALL, 5)
        # actionsPanel.Add(self.ACT_BTN_2, 0, wx.ALL, 5)
        # actionsPanel.Add(self.ACT_BTN_3, 0, wx.ALL, 5)
        actionsPanel.Add(self.ACT_BTN_4, 0, wx.ALL, 5)

        # Author information
        AuthorPanel = wx.StaticBoxSizer(wx.VERTICAL, rightPanel, "Author:")
        authorInfo = f"Jani Hirvinen\nTampere\nFinland\n(c)2024\nVersion: {def_version}\nDate: {def_date}\n"
        authorText = wx.StaticText(rightPanel, label=authorInfo)
        PluginLink = wx.StaticText(rightPanel, label="Ki-QIHE@GitHub")
        PluginLink.SetForegroundColour('blue')
        PluginLink.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        PluginLink.Bind(wx.EVT_LEFT_DOWN, self.onPluginLinkClick)

        AuthorPanel.Add(authorText, 0, wx.ALL, 5)
        AuthorPanel.Add(PluginLink, 0, wx.ALL, 5)

        # Layout for right panel
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer.Add(actionsPanel, 0, wx.EXPAND | wx.ALL, 5)
        # This spacer panel pushes the author information to the bottom
        rightSizer.Add(wx.Panel(rightPanel), 1, wx.EXPAND)
        rightSizer.Add(AuthorPanel, 0, wx.EXPAND | wx.ALL, 5)

        rightPanel.SetSizer(rightSizer)
        rightPanel.Layout()  # Update layout to apply changes

        # Combine left and right panels in the main sizer
        mainSizer.Add(leftPanel, 1, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(rightPanel, 0, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(mainSizer)
        self.Layout()
        self.Centre(wx.BOTH)
        self.loadingSettings = False

        # Bind events
        self.mGenerateButton.Bind(wx.EVT_BUTTON, self.onGenerateButtonClick)
        self.ACT_BTN_1.Bind(wx.EVT_BUTTON, self.onForceMappingButtonClick)
        self.ACT_BTN_4.Bind(wx.EVT_BUTTON, self.onSaveOptionsButtonClick)
        self.editButton.Bind(wx.EVT_BUTTON, self.onEditMappingFile)

        # Bind events to settings controls to trigger the save reminder
        self.bindSettingsEvents()

        # Load settings after all controls are created
        self.load_settings()
        self.log_activity(f"KiCAD QIHE v{def_version} / {def_date} plugin loaded successfully.")

    def onEditMappingFile(self, event):
        # Log activity
        # self.log_activity("Attempting to edit mapping file...")

        # Determine the base directory based on radio box selection
        if self.radioBox.GetSelection() == 0:
            base_path = os.path.dirname(os.path.realpath(__file__))  # Plugin folder
        else:
            base_path = os.path.dirname(pcbnew.GetBoard().GetFileName())  # PCB folder

        # Combine the base path with the filename from the text control
        filepath = os.path.join(base_path, self.txtMappingFileName.GetValue())

        # Log the calculated file path
        # self.log_activity(f"Calculated file path: {filepath}")

        # Check if the file exists
        if not os.path.isfile(filepath):
            self.log_activity("File does not exist: " + filepath)
            self.log_activity("Please create a mapping file first. Click \"Gen Mapping\" button first and/or.")
            self.log_activity("check mapping file location selector and file name.")
            return  # Exit if file doesn't exist

        # Try to open the file in the default editor
        try:
            if sys.platform.startswith('win'):
                os.startfile(filepath, 'edit')  # 'edit' should work on Windows
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', filepath])  # macOS
            else:
                subprocess.run(['xdg-open', filepath])  # Linux and others
            self.log_activity("File opened for editing: " + filepath)
        except Exception as e:
            self.log_activity(f"Failed to open file: {str(e)}")

    # Event handler for the window close event
    def onClose(self, event):
        self.Destroy()  # Ensure the frame is destroyed properly
        event.Skip()

    # Bind events to settings controls to trigger the save reminder
    def bindSettingsEvents(self):
        """Bind events to trigger changes."""
        self.radioBox.Bind(wx.EVT_RADIOBOX, self.onSettingChanged)
        self.txtMappingFileName.Bind(wx.EVT_TEXT, self.onSettingChanged)
        self.chkTop.Bind(wx.EVT_CHECKBOX, self.onSettingChanged)
        self.chkBottom.Bind(wx.EVT_CHECKBOX, self.onSettingChanged)
        self.txtTopPrefix.Bind(wx.EVT_TEXT, self.onSettingChanged)
        self.txtBottomPrefix.Bind(wx.EVT_TEXT, self.onSettingChanged)
        for btn in self.verbosityRadioButtons:
            btn.Bind(wx.EVT_RADIOBUTTON, self.onSettingChanged)

    # Event handler to show the save reminder text
    def onSettingChanged(self, event):
        if not self.loadingSettings:
            self.ACT_BTN_4.SetLabel("Save Changes")
            self.ACT_BTN_4.SetForegroundColour(wx.Colour('red'))
            self.Layout()  # Update the layout to reflect the changes

    # Append a message to the log text control
    def log_activity(self, message):
        """Append a message to the specified wx.TextCtrl."""
        wx.CallAfter(self.mLogTextCtrl.AppendText, message + "\n")

    # Event handler to open the plugin homepage in the default browser
    def onPluginLinkClick(self, event):
        """ Event handler to open the plugin homepage in the default browser """
        webbrowser.open('https://github.com/jpkh/ki_qihe', new=2, autoraise=True)

    # Event handler for the Generate button
    def onGenerateButtonClick(self, event):
        print("Generate button clicked")
        self.log_activity("Generate button was clicked.")  # Ensure this shows in the GUI
        mapping_location = self.radioBox.GetSelection()  # 0 for Plugin folder, 1 for PCB folder
        options = {"mapping_location": mapping_location,
                   'process_top_layer': self.chkTop.IsChecked(),
                   'process_bottom_layer': self.chkBottom.IsChecked(),
                   'verbosity_level': self.get_verbosity_level(),  # Add verbosity level to options
                   'mapping_file_name': self.txtMappingFileName.GetValue(),
                   'top_fileext': self.txtTopPrefix.GetValue(),
                   'bottom_fileext': self.txtBottomPrefix.GetValue()
                   }

        qihe_thread = QiHeProcess(options=options, log_activity=self.log_activity)
        qihe_thread.start()  # Make sure this line is executed

    # Event handler for the Force Mapping button
    def onForceMappingButtonClick(self, event):
        mapping_location = self.radioBox.GetSelection()  # 0 for Plugin folder, 1 for PCB folder
        mapping_file_name = self.txtMappingFileName.GetValue()
        if mapping_location == 0:
            path = os.path.dirname(os.path.realpath(__file__))
        else:
            path = os.path.dirname(pcbnew.GetBoard().GetFileName())
        filename = os.path.join(path, mapping_file_name)
        try:
            create_default_mapping_file(filename, self.log_activity)
            # self.mLogTextCtrl.AppendText(
            #    f"Default mapping file created successfully at: {filename}\n")
        except Exception as e:
            error_message = f"Error creating mapping file: {str(e)}"
            self.mLogTextCtrl.AppendText(error_message + "\n")
            log_message(error_message, log_type="ERROR")

    # Event handler for the Save Options button
    def onSaveOptionsButtonClick(self, event):
        """Handle the save options button click."""
        self.log_activity("Save options button clicked.")
        self.save_settings()
        self.ACT_BTN_4.SetLabel("Save Options")
        self.ACT_BTN_4.SetForegroundColour(wx.BLACK)  # Reset color to black after saving
        self.Layout()  # Update the layout to reflect the changes

    # Get the path to the settings file in the plugin directory
    @staticmethod
    def get_settings_file_path():
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        settings_file = os.path.join(plugin_dir, def_optionsFileName)
        return settings_file

    # Load settings from a JSON file in the plugin directory
    def load_settings(self):
        self.loadingSettings = True
        settings_file = self.get_settings_file_path()
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
            self.apply_settings(settings)
        except FileNotFoundError:
            # print("Settings file not found, creating default settings.")
            self.create_default_settings()
        except Exception as e:
            log_message(f"Error loading settings: {repr(e)}", log_type="ERROR")
        finally:
            self.loadingSettings = False

    # Create default settings if the settings file is not found
    def create_default_settings(self):
        default_settings = {"mapping_location": 0,
                            "process_top_layer": True,
                            "process_bottom_layer": True,
                            "top_fileext": def_top_fileext,
                            "bottom_fileext": def_bottom_fileext,
                            "log_verbosity": 0,
                            "have_separator": def_have_separator,
                            "CompopentMapping": def_CompopentMapping}

        self.apply_settings(default_settings)
        self.save_settings()

    # Get the selected verbosity level from the radio buttons
    def get_verbosity_level(self):
        for i, button in enumerate(self.verbosityRadioButtons):
            if button.GetValue():  # Check if this radio button is selected
                return i
        return 0  # Default to 0 if none are selected (should not happen if one is always selected)

    # Save settings to a JSON file in the plugin directory
    def save_settings(self):
        settings_file = self.get_settings_file_path()
        log_message(f"Attempting to save settings to: {settings_file}", log_type="DEBUG")

        # Debug each setting retrieval to catch errors
        try:
            mapping_location = self.radioBox.GetSelection()
            top_layer = self.chkTop.IsChecked()
            bottom_layer = self.chkBottom.IsChecked()
            top_prefix = self.txtTopPrefix.GetValue()
            bottom_prefix = self.txtBottomPrefix.GetValue()
            # verbosity = self.get_verbosity_level(),  # Use the new method here
            componentMapping = self.txtMappingFileName.GetValue()

            verbosity_level = self.get_verbosity_level()
            log_message(f"Current verbosity level: {verbosity_level}", log_type="DEBUG")  # Debug message

            settings = {
                "mapping_location": mapping_location,
                "process_top_layer": top_layer,
                "process_bottom_layer": bottom_layer,
                "top_layer_prefix": top_prefix,
                "bottom_layer_prefix": bottom_prefix,
                "log_verbosity": verbosity_level,
                "ComponentMapping": componentMapping
            }

            log_message(f"Settings to be saved: {settings}", log_type="DEBUG")

            with open(settings_file, "w") as f:
                json.dump(settings, f, indent=4)  # Use indent for readability
            log_message(f"Settings saved successfully to: {settings_file}", log_type="INFO")
            self.log_activity("Settings saved successfully.")
        except Exception as e:
            error_msg = f"Error saving settings: {str(e)}"
            log_message(error_msg, log_type="ERROR")
            self.log_activity(error_msg)

    # Apply settings to the GUI controls
    def apply_settings(self, settings):
        try:
            self.radioBox.SetSelection(settings["mapping_location"])
            self.chkTop.SetValue(settings.get("process_top_layer", True))
            self.chkBottom.SetValue(settings.get("process_bottom_layer", True))

            self.txtTopPrefix.SetValue(settings.get("top_layer_prefix", def_top_fileext))
            self.txtBottomPrefix.SetValue(settings.get("bottom_layer_prefix", def_bottom_fileext))

            # Safely update the verbosity radio box selection
            verbosity_level = int(settings.get("log_verbosity", 0))
            log_message(f"Applying verbosity level: {verbosity_level}", log_type="DEBUG")
            if 0 <= verbosity_level < len(self.verbosityRadioButtons):
                self.verbosityRadioButtons[verbosity_level].SetValue(True)

        except KeyError as e:
            log_message(f"Missing key in settings: {repr(e)}", log_type="ERROR")
        except Exception as e:
            log_message(f"Error applying settings: {repr(e)}", log_type="ERROR")


# Plugin definition
class Plugin(pcbnew.ActionPlugin):
    def __init__(self):
        self.name = "QiHe SMD Coords Toolkit"
        self.category = "Manufacturing"
        self.description = "Toolkit to create QIHE PnP machine coordinate files from the PCB"
        self.show_toolbar_button = True
        self.icon_file_name = os.path.join(os.path.dirname(__file__), "icon.png")
        self.frame = None  # keep track of the open window

    def Run(self):
        if not self.frame or not self.frame.IsShown():
            self.frame = KiQIHEMain()
            self.frame.Show()
        else:
            self.frame.Raise()  # Brings the existing window to the front if already opened

# End main.py
