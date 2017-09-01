# Python3 Package Manager
_As if cargo + npm had a baby_

### Introducing PPM!
 - Download modules and libraries from PyPI, GitHub, anywhere!
 - A built-in setup utility for developing projects.
 
 - Easy installation for mac and linux (windows installer coming soon).
 - Create setup.py automatically
 - License generator with four major licenses available.
 
### Using PPM.

|Command|Function|
|:-----:|:------:|
|```$ python3 install_mac.py```|Installs PPM.|

|Command|Function|
|:-----:|:------:|
|```$ ppm new --bin [program name]```|Creates a new program in the current directory.|
|```$ ppm new --lib [library/module name]```|Creates a new library/module in the current directory.|
|```$ ppm run [optional file name]```|Runs the specified file, or the projects main.py file if no arguments are specified.|
|```$ ppm install [package name]```|Uses PIP to install a package from the PyPI - NOTE: temporary dependency, will be removed soon.|
|```$ ppm add --license [mit/apache/gpl]```|Creates a LICENSE.txt in the current folder, creates a default copyright statement if no license is specified.|
|```$ ppm add --setup```|Creates a setup.py file in the current directory.|

### Notes and Dependencies.
 - Certain PPM functions require Git to be used. If Git isn't installed, PPM will raise an error message and ask you to install Git.
 - PPM is a package manager built for Python 3.


### Development.
PPM is currently being prototyped in Python3, however there will shortly be a compiled release built in Rust. If you want to help development, feel free to "muck in" and help out.
