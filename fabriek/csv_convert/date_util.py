import datetime

def datum_naar_nederlandse_tekst(datum_string):
    """
    Zet een datumstring in het formaat 'yyyy-mm-dd' om naar een Nederlandse tekstuele datum.
    Handelt ook None, lege strings en foutieve formaten af.

    Args:
        datum_string (str): De datumstring in het formaat 'yyyy-mm-dd'.

    Returns:
        str: De datum in Nederlandse tekst, of None als de input ongeldig is.
    """

    if datum_string is None or not datum_string.strip():
        return None

    try:
        datum_object = datetime.datetime.strptime(datum_string, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Ongeldig datumformaat. Gebruik yyyy-mm-dd.")

    # Datumstring omzetten naar een datetime-object
    datum_object = datetime.datetime.strptime(datum_string, '%Y-%m-%d')

    # Maanden als woorden
    maanden = ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
               'juli', 'augustus', 'september', 'oktober', 'november', 'december']

    # Dag, maand en jaar uit het datetime-object halen
    dag = datum_object.day
    maand = maanden[datum_object.month - 1]
    jaar = datum_object.year

    # Nederlandse datumstring samenstellen
    nederlandse_datum = f"{dag} {maand} {jaar}"

    return nederlandse_datum