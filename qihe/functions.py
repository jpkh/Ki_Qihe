##########################################################
#
# Script: functions.py
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

import pcbnew  # type: ignore
import os
import wx
import json


def get_user_options_file_path():
    boardFilePath = pcbnew.GetBoard().GetFileName()
    return os.path.join(os.path.dirname(boardFilePath), optionsFileName)


def load_user_options(default_options):
    try:
        with open(get_user_options_file_path(), "r") as f:
            user_options = json.load(f)
    except FileNotFoundError:
        user_options = default_options
    except json.JSONDecodeError:
        user_options = default_options

    # merge the user options with the default options
    options = default_options.copy()
    options.update(user_options)
    return options


def save_user_options(options):
    try:
        with open(get_user_options_file_path(), "w") as f:
            json.dump(options, f)
    except FileNotFoundError:
        wx.MessageBox("Error saving user options",
                      "Error",
                      wx.OK | wx.ICON_ERROR)
    except Exception as e:
        wx.MessageBox(f"Error saving user options: {str(e)}",
                      "Error",
                      wx.OK | wx.ICON_ERROR)


# Create a default mapping file if it does not exist
# or if the FORCEMAPPING flag is set
def create_default_mapping_file(filename, log_activity):
    default_content = """######################################
# Component Mapping for QIHE PnP machine
#
# For more information on how to edit this file, visit:
# https://github.com/jpkh/ki_qihe
#
# Contact: [Use GitHub issues for questions and suggestions]
#
# This file defines mappings for component placement and special instructions.
# Each line follows one of these formats:
#
# Component Mapping Line:
#   1 or 2, Feeder ID, Component Name(s)
#   - '1 or 2' specifies the nozzle number.
#   - 'Feeder ID' is the feeder location, formatted as Lxx or Bxx
#      (e.g., L1, B12).
#   - 'Component Name(s)' are the names of components, separated by colons (:).
#     These names should match the component values in the PCB design.
#   Example: 1, L1, 0n1:100nF:100nf:0.1uF:0.1uf
#
# Exclude Line:
#   E, , Regex Pattern(s)
#   - 'E' indicates this line specifies components to exclude.
#   - 'Regex Pattern(s)' are patterns to match components to be excluded,
#      separated by colons (:).
#   Example: E, , NC:TP
#
# Priority Line:
#   P, , Regex Pattern(s)
#   - 'P' indicates this line specifies priority components.
#   - 'Regex Pattern(s)' are patterns to match priority components,
#      separated by colons (:).
#   Example: P, , FIDUCIAL:TESTPOINT
#
"""
    try:
        with open(filename, "w") as file:
            file.write(default_content)
            log_activity(f"Default mapping file created: {filename}")
    except Exception as e:
        log_activity(f"Failed to create default mapping file: {e}")
        raise
