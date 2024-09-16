import csv
from dataclasses import dataclass
from typing import IO
from typing import List

from fabriek.csv_convert import event_helper
from fabriek.csv_convert.date_util import datum_naar_nederlandse_tekst


@dataclass
class Event:
    datum: str
    tijd: str
    titel: str
    taal: str
    genre: str
    speelduur: str
    cast: str
    synopsis: str
    beschrijving_incl_HTML: str
    ticket_url: str
    film_url: str


def create_event_object(row):
    # get all fields out of the List
    datum = row[0]
    tijd = row[1]
    titel = row[2]
    taal = row[3]
    genre = row[4]
    speelduur = row[5]
    cast = row[6]
    synopsis = row[7]
    beschrijving_incl_HTML = row[8]
    ticket_url = row[9]
    film_url = row[10]

    if not event_helper.is_valid_date_string(datum):
        raise ValueError("\"datum bevat geen of geen geldige waarde: " + ("Leeg" if datum is None else datum) + "\"")
    event_start_date = datum

    if not event_helper.is_valid_begintijd(tijd):
        raise ValueError("\"tijd bevat geen, of geen geldige waarde: " + ("Leeg" if tijd is None else tijd) + "\"")
    event_start_time = tijd + ":00"

    event_name = titel
    post_excerpt = event_helper.clean_text_from_HTML_and_other_shit(synopsis)
    post_content = beschrijving_incl_HTML + "<br>" + \
                   "<br>" + \
                   event_helper.to_strong("Gesproken taal: ") + taal + "<br>" + \
                   event_helper.to_strong("Genre: ") + genre + "<br>" + \
                   event_helper.to_strong("Speelduur: ") + speelduur + "<br>" + \
                   event_helper.to_strong("Cast: ") + cast + "<br>" + \
                   "<br>" + \
                   '<a href=\'' + film_url + '\'>' + film_url + '</a>'

    event_row = [datum,
                 tijd,
                 titel,
                 taal,
                 genre,
                 speelduur,
                 cast,
                 post_excerpt,
                 post_content,
                 ticket_url,
                 film_url,
                ]

    event = Event(*event_row)
    return event

def create_orkaan_agenda_file(input_file: IO, output_file: IO):

    output_file.write("======================================\n")
    output_file.write("ORKAAN AGENDA - FILMTHEATER DE FABRIEK\n")
    output_file.write("======================================\n")

    new_day = True
    old_day = ''

    with input_file as input_file:
        reader = csv.reader(input_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        line_count = 0
        for row in reader:
            if line_count != 0:
                try:
                    event = create_event_object(row)
                    if old_day != event.datum:
                        new_day = True

                    if new_day:
                        if old_day != '':
                            output_file.write('\n')
                            output_file.write('Voor tickets en beschrijvingen, ga naar De Fabriek\n')
                        output_file.write('\n')
                        output_file.write('\n')
                        output_file.write(f'<strong>Vandaag in De Fabriek - {datum_naar_nederlandse_tekst(event.datum)}</strong>\n')
                        output_file.write('\n')
                        old_day = event.datum
                        new_day = False

                    output_file.write(f'{event.tijd}   {event.titel}\n')
                except ValueError as e:
                    msg = "Foutieve data van de website, regel " + str(line_count) + ", fout= " + str(e)
                    output_file.write(msg + "\n")
            line_count += 1

        if old_day != '':
            output_file.write('\n')
            output_file.write('Voor tickets en beschrijvingen, ga naar De Fabriek\n')

    output_file.close()