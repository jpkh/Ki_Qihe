##########################################################
#
# Script: __init__.py
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


from .log_util import log_message

try:
    from .main import Plugin
    plugin = Plugin()
    plugin.register()
except Exception as e:
    log_message("Error initializing plugin: {}".format(repr(e)), log_type='ERROR')
