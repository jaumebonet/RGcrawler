RGcrawler
=========

A crawler for [ResearchGate](http://researchgate.net).

ResearchGate is a scientific social network that displays the publications, ciations
and statistics of a given author.  
This crawler is prepared to create, given an author ID, a set of authors and publications [JSON files](http://www.json.org) that can be easily exported into any programming language to further analyse.  

Questions
---------
**How can I install it?**  
You'll need ``python2.7`` and a UNIX based system (not tested in Windows).  
As this is mostly focused on self usage and I don't want to screw with your system,
I would recommend to install it in a python virtual environment (you can find a small
guide on how to work with virtual enviroments [here](http://docs.python-guide.org/en/latest/dev/virtualenvs/)), but that's up to you...

```bash
cd project_folder
virtualenv venv
source venv/bin/activate
pip install git+git://github.com/jaumebonet/RGcrawler.git@master --process-dependency-links --allow-all-external --trusted-host github.com
```
This should do the trick. Remember that you'll need to call
```bash 
source venv/bin/activate
```
every time before running the script and 
```bash
deactivate
```
after finishing it...

**How can I run it?**  
The only thing you need to type is:
```bash
python -m RGcrawler --authorID <author_id>
```

**Where can I find the autor id?**  
When you look to one of your featured publications, the author id is the number that
appears before your name in your name's link in the author list.

**Would this work with multiple authors?**  
Yes, you can create a script that queries multiple authors calling the program multiple times. If a called author is co-author with a previous called one, some of the data will be retrieved from the files and not requested online.

**Can I be bloqued from RG?**  
No idea. Scrapping is not something web apps like. This is just a fix waiting for RG to release an API. If you query too many pages you might be bloqued for a while (that is, for example, what Google Scholar does), but I´ve never reached that limit with my (small) tests.

**Why some authors are not recognised when I can see them in my browser?**
Well. Some authors have they profile configured in such a way that you can't actually see their profile unless you are logged to ResearchGate. I'm sure the identification cookies can be loaded so that it will look like you are connected, but I´m not going to get into this right now. But... you know... feel free to fork and build upon this!!

**Will the library be updated regularly?**  
I'm basically using this to (semi)automatically update my CV. Thus, I cannot say. Of course, anybody is more than welcomed to fork and better this (there is soo much that can be improved!). Keep in mind that a scrapper totally depends on the web app layout, which means that any change in RG can invalidate the whole thing... just FYI.

