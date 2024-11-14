# link extractor and archive

Included both a GUI and a CLI variant of this script:

To run both install simply clone this repo or check the release page then do the following in a virtual environment inside linux


    pip install -r requirments.txt


When everything is installed run


    python extractor.py --weburl [weburl]


for the GUI

    python extractor-gui.py


# Features of the GUI not present in CLI

* Save funtion
* log
* cleaner extraction
* exclusion of URLS in extraction based on user input

![image](https://github.com/user-attachments/assets/f5440c48-0511-458e-8586-7294c85d0da7)


# Archive Tool


    python archive.py --file

Be sure you have a links.txt and it's curated to what you want archived on archive.ph
You may edit the time for archival; check the code inside `archive.py` under `time.sleep` 10 seconds is the default but you may change it to something longer.

Uses archive.ph as an archive service to archive everything, wayback machine will rate limit.

for a single link use

    python archive.py --url

Feel free to try this on the website spacejam:

https://www.spacejam.com/1996/
