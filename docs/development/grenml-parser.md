# GRENML Parsing

## API

The GRENML Parser will return a GRENML Manager populated with the data
read from the provided xml. The API provided in parse.py allows for 3 options
when providing xml:

### parse_byte_stream

Takes a stream and streams the data through the parser. This allows for the user
to provide a stream directly from an HTTP GET call to parse the xml without
keeping it in memory.

### parse_string

Takes an xml string and converts it into a stream to pass into the stream funcion.
Should generally be avoided in favor of streams when possible.

### parse_file

Opens a file read stream at the given location and sends it through the parser.

## Example Usage

To use the API, first make an instantiation of the parser and then call
the appropriate API endpoint. The manager contained within the parser should
then be populated with the data read from the input source

    parser = GRENMLParser()
    
    # Use one of the methods provided by the API

    # To parse a pre-defined stream
    manager = parser.parse_byte_stream(stream)
    
    # To parse a string
    manager = parser.parse_string(string)

    # To parse a file
    manager = parser.parse_file('validation/example.xml')
