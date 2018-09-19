# JeeJuh Downloader

These scripts can be used to download all of the links for a download page provided from a JeeJuh.com purchase. The scripts are written in both Python and Powershell to provide flexibility for Windows/Linux/OSX platforms.

### Prerequisites

Python version is written in Py2 with compatability for Py3. The Powershell script requires a minimum version of Powershell 3. You can verify your installed versions:

#### Python
```
python --version
```
#### Powershell
```
$PSVersionTable.PSVersion
```

### Installing

Powershell script requires nothing extra. The Python requirements can be installed with pip. If you need to install pip on your platform, use easy_install.

```
sudo easy_install pip
pip install -r requirements.txt
```

## Running the script

Using either the Python or Powershell versions, the provided URL parameter **must be enclosed in quotes**. The `output` parameters are optional. If not set, files are saved in folders of the current working directory.

#### Python
```
./jeejuh-dl.py <URL> [-O directory]
```

#### Powershell
```
./jeejuh-dl.ps1 -Url <URL> [-Output directory]
```
