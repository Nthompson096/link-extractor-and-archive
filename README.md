# link extractor and archive

Included both a GUI and a CLI variant of this script:

To run both install simply clone this repo or check the release page then do the following in a virtual environment inside linux


    pip install -r requirments.txt


When everything is installed run


    python extractor.py --weburl [weburl]


for the GUI

    python extractor-gui.py


# Features of the GUI not present in CLI

* Save funtion as JSON
* log
* cleaner extraction

Example from spacejam

    https://www.spacejam.com/1996/cmp/pressbox/pressboxframes.html
    https://www.spacejam.com/1996/cmp/jamcentral/jamcentralframes.html
    https://www.spacejam.com/1996/cmp/bball/bballframes.html
    https://www.spacejam.com/1996/cmp/tunes/tunesframes.html
    https://www.spacejam.com/1996/cmp/lineup/lineupframes.html
    https://www.spacejam.com/1996/cmp/jump/jumpframes.html
    https://www.spacejam.com/1996/cmp/junior/juniorframes.html
    https://shop.looneytunes.com/spacejam96?utm_source=SpaceJam1996&utm_medium=Website&utm_campaign=Theatrical2021
    https://www.spacejam.com/1996/cmp/souvenirs/souvenirsframes.html
    https://www.spacejam.com/1996/cmp/sitemap.html
    https://www.spacejam.com/1996/cmp/behind/behindframes.html
    https://policies.warnerbros.com/privacy/
    http://policies.warnerbros.com/terms/en-us/
    http://policies.warnerbros.com/terms/en-us/#accessibility
    https://policies.warnerbros.com/privacy/en-us/#adchoices

Used to be all broken up as

    https://www.spacejam.com/1996/
    cmp/pressbox/pressboxframes.html
    cmp/jamcentral/jamcentralframes.html
    cmp/bball/bballframes.html

* exclusion of URLS in extraction based on user input

Be sure you have tkinter installed on your system.

![image](https://github.com/user-attachments/assets/e49f5d1d-247a-4310-b315-d24f36fb92d1)


# Archive Tool


    python archive.py --file

Be sure you have a links.txt and it's curated to what you want archived on archive.ph
You may edit the time for archival; check the code inside `archive.py` under `time.sleep` 10 seconds is the default but you may change it to something longer.

Uses archive.ph as an archive service to archive everything, wayback machine will rate limit.

for a single link use

    python archive.py --url

Feel free to try this on the website spacejam:

https://www.spacejam.com/1996/
