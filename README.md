# Fabriek Scraper

This program creates several CSV files containing all movies currently scheduled 
on the website of art-house cinema 'De Fabriek', address http://www.de-fabriek.nl. 

#### Dependencies
The program is written in python3 (3.6.9) using the scrapy web crawling framework. So to use this
program, first install:

* Python 3 (see https://www.python.org/downloads/)
* Scrapy (2.1.0)

#### Install on linux

An easy way to install the dependencies:
```
pip3 install Scrapy
```

#### Install on windows
```
1. Install Miniconda
2. Add to path:
    1. C:\Users\your-user-name\miniconda3\Scripts
    2. C:\Users\your-user-name\miniconda3
    3. C:\Users\your-user-name\miniconda3\Library\bin
```

#### Download 
After that, download fabriekscraper and, e.g. by using git:
```
git clone https://github.com/EelcoA/fabriekscraper.git
```

#### How to run this?
Go into the fabriekscraper directory and type:
```
python3 start.py
```

#### Output
Output is saved in the output/ directory. Three files are created:

1. file with movies, with data as found on the website
2. a file with same data, sorted on date/time
3. a file with the data as expected by the import function for Wordpress Event Manager,
contains fields:
    - event_start_date
    - event_start_time
    - event_end_date
    - event_end_time
    - event_name
    - event_slug
    - post_content
    - location ('filmtheater-de-fabriek-2')
    - category ('film')

last 2 values can be changed in settings.py
    
#### Author
- Eelco Aartsen
- eelco@aesset.nl
- AESSET IT - The Neteherlands
- www.aeset.nl


