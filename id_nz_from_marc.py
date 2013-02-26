
import re

from marc import MarcSQLite, get_id_from_record


REGEX = re.compile(r'new zealand|maori', re.IGNORECASE)

m = MarcSQLite('results/non_google.20111101_01.db')

with open('results/non_google_nz.txt', 'w') as f_id:

    with m:
        for r in m.get_all_records():
            matches = []
            for field in r.subjects():
                try:
                    subj = field.get_subfields('a')[0]
                    found = REGEX.findall(subj)
                    matches += found
                except IndexError:
                    pass
            if matches:
                f_id.write("{}\n".format(get_id_from_record(r)))