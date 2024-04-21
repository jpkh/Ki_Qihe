##########################################################
#
# Script: config.py
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

# Empty placeholders for the output file names
output_file_top = ""
output_file_bottom = ""

# mapping_location = 0  # Default to plugin folder
# mapping_file_name = "component_mapping.txt"

have_separator = True

def_optionsFileName = 'ki-qihe-options.json'
def_top_fileext = 'TOP-COORDS'
def_bottom_fileext = 'BOTTOM-COORDS'
def_log_verbosity = 0
def_log_file = 'save_restore_error.log'
def_log_type = 'INFO'
def_mapping_location = 0
def_have_separator = False
def_output_file_top = ""
def_output_file_bottom = ""
def_CompopentMapping = "component_mapping.txt"
def_version = "1.0"
def_date = "2024-04-07"
