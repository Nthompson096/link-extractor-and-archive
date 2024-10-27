# link-extractor-and-archive

A link extractor and archive

To run simply install the following in a virtual environment inside linux

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

Be sure you have a links.txt and it's curated to what you want archived on archive.ph
You may edit the time for archival; check the code inside `archive.py` under `time.sleep` 60 seconds is the default but you may change it to something smaller.

Feel free to try this on the website spacejam:

https://www.spacejam.com/1996/
