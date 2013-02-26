
import argparse
from string import lower

from marc import MarcSQLite, get_id_from_record


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('MARCDB',
                        help='MarcSQLite database from which to retrieve records.')
    parser.add_argument('TERM',
                        nargs='+',
                        help='Terms signalling positive identification.')
    parser.add_argument('--out', 
                        help='Optional file to write output to.')

    args = parser.parse_args()
    print args

    terms = [lower(s) for s in args.TERM]

    m = MarcSQLite(args.MARCDB)

    with open(args.out, 'w') as f_id:

        with m:
            for r in m.get_all_records():
                matches = []
                for field in r.subjects():
                    try:
                        subj = lower(field.get_subfields('a')[0])   
                        for term in terms:
                            if term in subj:
                                matches.append(subj)
                    except IndexError:
                        pass
                if matches:
                    id_ = get_id_from_record(r)
                    print id_
                    f_id.write("{}\n".format(id_))