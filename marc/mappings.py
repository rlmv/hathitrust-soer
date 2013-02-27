
from collections import Counter

from records import normalize_year, normalize_subject

def map_publication_years(records):
    """ Map the publication years of a collection into a dictionary. 

    This will produce year:number pairs, which relates the number of
    documents published in a given year to that year. Years are integers.

    Args: 
    -collection :  an iterator over pymarc Record objects.
    """

    mapping = Counter()

    for r in records:
        year = r.pubyear()
        norm_year = normalize_year(year)
        mapping[norm_year] += 1

    return mapping


def map_subjects(records):
    """ Map subjects of the collection into a dictionary.

        I `believe` this is the best way to implement this, and that
        subject names always live in the 'a' subfield. 

        Should the keys be lowercased? 
    """

    mapping = Counter()

    for r in records:
        for f in r.subjects():
            try:
                subj = f.get_subfields('a')[0]
                subj = normalize_subject(subj)
                mapping[subj] += 1
            except IndexError:
                pass

    return mapping