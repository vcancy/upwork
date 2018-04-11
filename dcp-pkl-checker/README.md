# upwork

https://www.upwork.com/jobs/~01fe3365c61e2a8142

Hi, I duplicate Digital Cinema Packages (DCP) and need a script that can scrape the XML file and look for the hashes of the files in the DCP and checks them for errors.

The script must be able to show the progress when its checking the hashes (the files can be in the 100s of GB), so need to have visual cues that it is running.

The script must also output a CSV file after completion to indicate which files have passed or failed the SHA1 checksum.

Explanation of the checksum in DCP: https://kubanaltan.wordpress.com/2013/01/16/checking-sha1-checksum-of-mxf-files-in-a-dcp/

Attached is an example of the PKL XML file in the DCP which contains the hashes of the files. All PKL files are named as PKL*.xml

## Installation

Requirements :

Python :

- Should work on python 2.7 and python 3.3+

- Tested on : python 2.7, python 3.6

dependencies:

- lxml==4.2.1

- six==1.11.0

- xmltodict==0.11.0

Install dependencies from PyPI package 

```
pip install -r requirements.txt

```

## Usage:

````
python pklchecker.py -i <dcp path> -o <outputfile>

````