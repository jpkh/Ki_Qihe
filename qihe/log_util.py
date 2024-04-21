##########################################################
#
# Script: log_util.py
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
import traceback

def log_message(message, log_type='INFO'):
    plugin_dir = os.path.dirname(os.path.realpath(__file__))
    log_file = os.path.join(plugin_dir, 'save_restore_error.log')
    try:
        with open(log_file, 'a') as f:
            if log_type == 'ERROR':
                f.write("ERROR: {}\n".format(message))
                traceback.print_exc(file=f)
            else:
                f.write("{}: {}\n".format(log_type, message))
    except Exception as log_error:
        print(f"Failed to log error: {log_error}")
        print(message)
        traceback.print_exc()  # Print to standard output as a last resort
