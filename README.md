# link extractor and archive

A link extractor and archive

To run install simply clone this repo or check the release page then do the following in a virtual environment inside linux

``
pip install -r requirments.txt
``

When everything is installed run

``
python extractor.py --weburl [weburl]
``

then use

``
python archive.py
``

To run the HTML website:

do the above

then run

    python app.py

The website can only extract links for now, no archival sadly as I'm still trying to figure stuff out, much cleaner on extraction tho.

Be sure you have a links.txt and it's curated to what you want archived on archive.ph
You may edit the time for archival; check the code inside `archive.py` under `time.sleep` 10 seconds is the default but you may change it to something longer.

Feel free to try this on the website spacejam:

https://www.spacejam.com/1996/
