# De Fabriek - filmcrawler

This program creates several CSV files containing all movies currently scheduled 
on the website of art-house cinema 'De Fabriek', address http://www.de-fabriek.nl. 

#### Dependencies
The program is written in python3 (3.6.9) using the scrapy webcrawling framework. So to use this
program, first install:

* Python 3 (see https://www.python.org/downloads/)
* Scrapy (2.1.0)

An easy way to install the dependencies:
```
pip3 install Scrapy
```

After that, download Fabriek-crawler and run it:

#### How to run this?
Go into the fabriek-crawler directory and type:
```
python3 start.py
```

#### Output
Output is saved in the output/ directory. Three files are created:

1. file with movies, data as found on the website
2. sorted version of 1
3. data as expected by the import function for Wordpress Event Manager,
contains fields:
    - event_start_date
    - event_start_time
    - event_end_date
    - event_end_time
    - event_name
    - event_slug
    - post_content
    - location (for the moment, fixed value is 'filmtheater-de-fabriek-2')
    - category (for the moment, fixed value os 'film')
    
    
#### Author
- Eelco Aartsen
- eelco@aesset.nl
- AESSET IT - The Neteherlands
- www.aeset.nl


