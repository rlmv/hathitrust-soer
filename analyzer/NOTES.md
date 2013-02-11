

MARC:
    we're using pymarc.
    http://takhteyev.org/courses/11W/inf1005/pymarcdoc/

    Quite simple: pass a file name to parse_xml_to_array(f), and it returns a list of parsed marc structures, which is an iterable of field dictionaries (?).fo

Bugs:
    field.get_subfields() raises an Exception if the field is a Control field
        - AttributeError, cause subfields not set.

    Do a .is_control_field() before accessing ... well, anything.
