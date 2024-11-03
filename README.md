# StormworksCompilerGUI
Basic GUI app to simplify Stormworks modding asset compiling.

## App Usage Instructions
This app is designed to work with Stormworks' provided modding SDK. To use it, the app executable must be placed in the same directory as the SDK files, typically located at `Steam\steamapps\common\Stormworks\sdk`. This app helps users compile modding assets by generating and executing the necessary PowerShell commands based on selected compile settings.

Do note that this app is designed to work with Windows-based systems (as it relies on PowerShell, functionality on other systems are not tested), and requires users to have the Stormworks modding SDK.

## Building
To build the app from the source code, ensure you have Python 3.x installed on your system, along with the required libraries. The needed libraries are listed on the first lines in `StormworksCompileGUI.pyw`. You can use the provided `BUILD.bat` script to automate the building process using PyInstaller. This method requires you to have the [`pyinstaller`](https://pyinstaller.org/en/stable/) package installed. Alternatively, you can build the app with your own method and configurations.

### Library Requirements
- Python 3.x
- PyInstaller (for BUILD.bat)
- CustomTkinter

## License
This project is distributed under the MIT License - see [LICENSE](https://github.com/CruzerBlade9369/StormworksCompilerGUI/blob/main/LICENSE) for more details.
