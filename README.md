# Fabriek Scraper

This program creates several CSV files with data from all movies currently scheduled 
on the website of art-house cinema 'De Fabriek' in Zaandam, The Netherlands: http://www.de-fabriek.nl. 

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

#### Install on Mac

##### Installeer een virtuele omgeving
https://docs.python.org/3/tutorial/venv.html#tut-venv 

###### Creëer een virtuele omgeving
python -m venv tutorial-env

###### Activeer de virtuele omgeving
source tutorial-env/bin/activate

###### Deactiveer de virtuele omgeving
deactivate

##### Installeer xcode (in gewone omgeving)
Installeer xcode in de gewone terminal omgeving (niet in de virtuele omgeving)
```
xcode-select --install
```
De virtuele omgeving maakt er dan gebruik van

##### Installeer homebrew
https://brew.sh/

##### Installeer git
brew git

##### Installeer python
https://www.python.org/downloads/macos/ 

##### Installeer pip
Normaal zit dat al erin als je python installeert
```
python get-pip.py
```

##### Installeer de code van fabriekscraper
```
git clone https://github.com/EelcoA/fabriekscraper
``` 
Draai fabriekscraper
```
cd fabriekscraper
python3 start.py
```

###### Foutmelding lzma
Krijg je deze foutmelding: 
builtins.ModuleNotFoundError: No module named '_lzma'

oplossing https://debuglab.net/2024/05/06/modulenotfounderror-no-module-named-_lzma-when-building-python-using-pyenv-on-macos/ 

Install xz (this contains liblzma library)
```
brew install xz
```
Reinstall Python specifying some necessary flags
vraag de versie van python op
```
$ python  - -version (op de terminal geen spatie tussen - maar google docs maakt hier 1 streep van)
Python 3.12.2
```
```
env LDFLAGS="-L/usr/local/opt/xz/lib" CFLAGS="-I/usr/local/opt/xz/include" pyenv install <version>
env LDFLAGS="-L/usr/local/opt/xz/lib" CFLAGS="-I/usr/local/opt/xz/include" pyenv install 3.12.2 
```
probeer het nu weer te doen




#### Install on windows (volgens mijn niet nodig, gewoon python installeren)
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
Output is saved in the output directory. Three files are created:

1. file with movies, with data as found on the website
2. file with same data, sorted on date/time
3. file with the data as expected by the import function for Wordpress Event Manager,
contains fields:
    - event_start_date
    - event_start_time
    - event_end_date
    - event_end_time (start-time + length + 'trailer-minutes' (default '10'))
    - event_name
    - event_slug
    - post_content
    - location ('filmtheater-de-fabriek')
    - category ('film')

The value for the last 2 fields and the 'trailer-minutes' can be set in settings.py
4. file with film agenda text per day 

#### Errors
A know error situation occurs when not all information can be found (e.g. no title).
This is checked by counting the number of start times, titles, url's and ticket-buttons. 
These should be the same. If not, an error is displayed for the user with the date where it occurs.
No movies are added then, because it is not know which title belongs to which time etc.
Of course I could improve this, but for the moment this is it ;-)

Example error message:
```
ERROR: Het verwerken van de gegevens van dag 2020-11-07 is niet goed gegaan. Check de films van die dag!
```
This is what caused it, a movie without title:

![Image](doc/Fabriek_movie_without_name_example.jpg?raw=true)

How to solve this? Contact De Fabriek (075 6311993, or info@de-fabriek.nl) and make them correct it!
    
#### Author
- Eelco Aartsen
- eelco@aesset.nl
- AESSET IT - The Netherlands
- www.aesset.nl


