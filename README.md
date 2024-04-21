# KiCAD plugin for QIHE PnP machines. "Ki-QIHE"
QIHE PnP Coords Processor for KiCAD
The QIHE PnP Coords Processor is a plugin for KiCAD designed to automate the creation of coordinate files for QIHE pick-and-place machines. This plugin simplifies the process of setting up manufacturing files for your PCB designs, enhancing the efficiency of your production line.

**Features**

- Layer Selection: Choose between top, bottom, or both layers for generating coordinates.
- Component Mapping: Define custom mappings for components to specific feeders and nozzles.
- Prefix Management: Set custom file prefixes for the generated coordinate files.
- Log Verbosity Control: Adjust the level of detail in the plugin's logs to suit your needs.
- Direct Mapping File Editing: Open and edit the component mapping file directly through the plugin interface.

**Installation**

1. Download the Plugin:
- Navigate to the Releases section of this repository and download the latest version.
2. Install the Plugin in KiCAD:
Restart KiCAD to load the plugin.

**Usage**

Once installed, the QIHE PnP Coords Processor can be accessed from plugins toolbar in KiCAD.

**Main Interface**

- Generate COORDS Button: Initiates the coordinate file generation process for selected layers.
- Top/Bottom Checkboxes: Select whether to generate coordinates for the top layer, bottom layer, or both.
- Top/Bottom Layer Prefix: Set custom prefixes for the generated files to help identify them easily.

**Advanced Settings**

- Mapping File Location: Choose where to save the component mapping file - either in the plugin folder or the PCB project folder.
- Log Verbosity: Select the level of log detail from minimal (0) to detailed debug information (3).

**Editing the Component Mapping File**

- Edit Button: Opens the component mapping file in your system's default text editor, allowing you to make changes directly.

**Contributing**

Contributions are welcome! Please feel free to submit pull requests, or file issues for bugs, feature requests, and suggestions through the GitHub Issues page.

**Support**

If you encounter any problems or have questions about using the plugin, please check the Wiki or file an issue.

**License**

This project is licensed under the MIT License - see the LICENSE file for details.

**Acknowledgments**

Thanks to all contributors who have helped test, refine, and extend the functionality of this plugin.
