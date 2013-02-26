


def file_id_iter(fname, mode='r'):
    """ Iterator over stripped lines in a file."""
    with open(fname, mode) as f:
        for line in f:
            yield line.strip()