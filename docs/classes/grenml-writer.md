# GRENML Writer

## Overview

The GRENML Writer will provide the ability to write generated XML to a
veriety of outputs.

## Example Usage

To use the API, first make an instantiation of a GRENML manager, then populate
it with the data that should be written. Then instantiate a writer, passing in
the manager into the constructor. Finally, call the desired api endpoint.

    from grenml.write import GRENMLWriter()

    writer = GRENMLWriter(manager)
    
    # Use one of the methods provided by the API

    # To write to a pre-defined stream
    writer.write_stream(stream)
    
    # To return a string with the XML
    writer.write_string()

    # To write to a file
    writer.write_file('validation/example.XML')


## Initialization

The GRENMLWriter does not take any arguments upon initialization:

    from grenml.write import GRENMLWriter
    writer = GRENMLWriter()

## Functions

### write_stream
#### Arguments: (stream)
Takes a stream and writes a GRENML topology to it. This allows for the user
to provide a stream directly for use of transporting the written XML to an
external location.

##### stream
An IOStream to write the output to.

### write_string

Takes the grenml manager and writes the topology to a string, then returns it.

### write_file
#### Arguments: (file)

Opens a file write stream at the given location and writes the manager to the
file location. Of the file already exists, this will overwrite the file with
the new information.

##### file
The file location to write the output to
