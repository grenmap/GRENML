# Coding Conventions Guidelines

## Python

[PEP8](https://www.python.org/dev/peps/pep-0008/) except where noted below.



 - 99-char lines except Docstrings (72 chars), and except:
     * don't break long URLs in comments
     * translated strings, for better compatibility with makemessages
 - 4-space indents ("soft tabs" i.e. spaces, not hard tab characters)
 - double-indent line continuations
 - indented blocks usually preferred over line continuations
 - Python objects destined for output to JSON may use either underscore_delimited properties
   or hyphen-delimited properties; ideally, they're the former in Python and then run through
   a simple translation function prior to output to a client via JSON
 - do not capitalize acronyms & abbreviations in variables, properties, attributes, arguments,
   parameters; capitalize them in class names, e.g.:
   * my_id = ID(name='Joe', pin=encode('1234'))

## Language

 - all code should be crafted in English
 - log/debugging code, error messages, and other internal- or dev-only strings should
   be in English
  