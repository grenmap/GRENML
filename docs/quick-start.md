# Quick Start

The GRENML library is designed to allow a streamlined process to convert
network data into GRENML XML data. This tutorial only covers a basic use
of the library. See the [Document Index](index.md) for the full documentation.

## Development Setup

Install [flake8](https://flake8.pycqa.org) and [pytest](https://docs.pytest.org). We use them for linting and running unit tests.

You might want to create a virtual environment for working with the GRENML library.

A virtual environment is a Python installation separate from the system-wide Python. You should create one before working on the DAIR tools. See "[Creating and using virtual environments](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)".

## Exporting your Data

### Getting Started

For ease of use, we supply a [Manager](classes/manager.md) for making
the topology. To start, import the library and create a manager, passing the name of the Topology to the Manager.

    import grenml
    
    manager = grenml.GRENMLManager('Example Topology')
   
### Adding Data
   
#### Adding Institutions

When creating a topology, organizations (referred to 
going forward as [Institutions](classes/institutions.md)) that have 
an effect on your topology need to be added, and the primary owner of 
the topology should be set as the Institution using the library.

Here are a few ways to create an Institution and add it to the topology:

    # The manager will auto create an Institution from your parameters and provide the ID created
    
    institution_ids = []
    
    # An Institution can be created using positional arguments (id, name, short_name, institution_type, longitude, latitude, altitude, unlocode, address, version) with additional key word arguments
    inst_id = manager.add_institution('example id', 'name example', institution_type='Connected Institution')
    institution_ids.append(inst_id)

    # An Institution can be created directly
    from grenml.models import Institution
    institution = Institution(name='Other example', longitude=0, latitude=0)
    manager.add_institution(institution)
    institution_ids.append(institution.id)
    
    # Multiple Institutions can be created at once and provide a list of IDs
    institution_ids += manager.add_institutions([
        ['ANOTHER_ID', 'Example name', 'short name', 'connected institution', 0, 0],
        {'name': 'Another name', 'longitude': 0, 'latitude': 0},
        Institution(name='inst_name', longitude=0, latitude=0),
    ])

NOTE: An Institution, preferably the organization using this library, 
should be labeled as the owner of the topology. This Institution will be considered
to own each node and link listed in the topology. 

NOTE: The Topology will always have at least 1 Institution with the ID 'global,' type 'global,' and name 'GRENML.'
This Institution is used to denote a global organization and is used to determine a location for connection has
global reach or use.

NOTE: See [Object IDs](classes/base.md#Object IDs) for more information on how IDs are generated.

To set the topology owner, add the key word argument `primary_owner` to any of the
single Institution additions above.

    manager.add_institution('ID', 'NAME', longitude=0, latitude=0, primary_owner=True)
    manager.add_institution(Institution(name='NAME', longitude=0, latitude=0), primary_owner=True)
    
WARNING: The primary_owner is a single value and will be overridden if multiple
Institutions are labeled as the primary owner.

A primary owners can also be set to an already created Institution using the Institution's ID.
(Must be an Institution that has already been added to the topology)

    inst_id = manager.add_institution(name='Some RAN', institution_type='ran', longitude=0, latitude=0)
    manager.set_primary_owner(inst_id)

#### Adding Nodes

Once the Institutions have been added, locations of connectivity (PoPs,
Data centres, Internet Exchanges, etc.) can be added. These locations will
be referred as [Nodes](classes/nodes.md) going forward.

When a Node is added to the Topology, the Topology's primary owner will be
added to the Node's owners list.

Here are a few ways to create a Node:
    
    # Create a node. The primary owner will automatically assigned
    node_ids = []
    
    # A node can be created using the positional arguments (id, name, short_name, owners, longitude, latitude, altitude, unlocode, address, lifetime_start, lifetime_end, version) with additional key word arguments
    node_id = manager.add_node(name='Some Town', longitude=0, latitude=0)
    node_ids.append(node_id)
    
    # Create a node with an owner. The primary owner will be added to the Node's owners
    nodes_id = manager.add_node(name='another town', owners=institution_ids[0], longitude=0, latitude=0)
    node_ids.append(node_id)
    
    # Can also have owners be a list of IDs
    nodes_id = manager.add_node(name='another town', owners=[institution_ids[0], institution_ids[2]], longitude=0, latitude=0)
    node_ids.append(node_id)
    
    from grenml.models import Node
    node = Node(id='my ID', name='data centre', owners=institution_ids[0], longitude=0, latitude=0)
    manager.add_node(node)
    mode_ids.append(node.id)

    # Multiple Nodes can be added at once
    node_ids += manager.add_nodes(
        ['id', 'node', 'N', [institution_ids[0]], 0, 0],
        {'name': 'node name', 'longitude': 0, 'latitude': 0},
        Node('id', 'name', [], 0, 0),
    )

#### Adding Links

With the Nodes added to the Topology, connections between those Nodes can be
added to represent the full connected Topology. These connections are referred to as 
[Links](classes/links.md) going forward.

When a Link is added to the Topology, the Topology's primary owner will be
added to the Link's owners list.

A Link must have 2 Nodes attached to it for it to be accepted by validation.

There are a few ways to create a link:

    # Create a link. The primary owner will automatically assigned
    # A link can be created using the positional arguments (id, name, short_name, owners, nodes, lifetime_start, lifetime_end, version) with additional key word arguments
    manager.add_link(name='Some Town', nodes=['node id 1', 'node id 2'])
    
    # Create a link with an owner. The primary owner will be added to the Link's owners
    manager.add_link(name='another town', owners=institution_ids[0], nodes=[node_ids[0], node_ids[1]])
    
    # Can also have owners be a list of IDs
    manager.add_link(name='another town', owners=[institution_ids[0], institution_ids[1]], nodes=[node_ids[0], mode_ids[2]])

    from grenml.models import Node
    link = Link(id='my ID', name='data centre', owners=institution_ids[0], nodes=[node_ids[0], mode_ids[2]])
    manager.add_link(link)

    # Multiple Nodes can be added at once
    manager.add_nodes(
        ['id', 'link', 'L', institution_ids[0], [node_ids[1], mode_ids[2]]],
        {'name': 'node name', 'nodes': [node_ids[0], mode_ids[1]]},
        Link('id', 'name', [], [node_ids[0], mode_ids[2]]),
    )

### Exporting Data

After the data has been added to a manager object, there are a few ways to export
the data as shown from the [GRENMLWriter](classes/grenml-writer.md) class. The manager contains
functions to directly output the data to an XML output.

    # To write to a file, supply a string with the location of the file to write to
    manager.write_to_file('file_to_write_to.xml')
    
    # Write the XML to a string in memory
    output_string = manager.write_to_string()
    
    # Write to a given output stream. This is the recommended option if you're not writing to a file
    with open('some_file.xml') as file:
        manager.write_to_stream(file)

NOTE: With each write function, the manager performs validation and raises an error if any data is invalid.

## Importing Data

### Reading in Data

To import data from a GRENML XML file, a [GRENMLParser](developmet/grenml-parser.md) class is supplied.

The GRENMLParser class can be used in a few different ways, each way produces a GRENMLManager object with all the data 
collected from the input loaded into it.

Here's a few examples of using the GRENMLParser:

    from grenml.parse import GRENMLParser
    
    parser = GRENMLParser()
    
    # Import from a stream
    with open('grenml_example.xml', 'rb') as file:
        manager = parser.parse_byte_stream(file)
    
    # Import from a file
    manager = parser.parse_file('example_grenml.xml')
    
    # Parse data from a string
    input_string = '''
        <?xml version="1.0" encoding="utf-8"?>
        <grenml:Topology id="5ef3e130-d671-4cec-a8f9-24bed50c961c" xmlns:grenml="http://schemas.ogf.org/nml/2020/01/grenml"
                         xmlns:nml="http://schemas.ogf.org/nml/2013/05/base#"
                         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                         xsi:schemaLocation="http://schemas.ogf.org/nml/2020/01/grenml validation/grenml.xsd http://schemas.ogf.org/nml/2013/05/base# validation/nmlbase.xsd">
            <grenml:name>Example Topology</grenml:name>
            <grenml:owner>3c83c486-fa5e-46d3-b26e-94c9dcbd2493</grenml:owner>
            <grenml:Institution id="urn:ogf:networking:global">
                <grenml:name>GREN</grenml:name>
                <grenml:type>global</grenml:type>
            </grenml:Institution>
            <grenml:Institution id="3c83c486-fa5e-46d3-b26e-94c9dcbd2493">
                <grenml:name>Example Institution</grenml:name>
                <grenml:type>connected institution</grenml:type>
            </grenml:Institution>
        </grenml:Topology>
    '''
    manager = parser.parse_string(input_string)
    
### Searching Data

The GRENMLManager provides the ability to search the data that has been loaded in through the use
of get_< model name> functions. Passing key word arguments into the function allows for getting a single model object or multiple 
objects that match the provided arguments. See the [GRENObject match](classes/base.md#match) for information on the options for the get functions.

Here are a few examples of common queries:

    # Searching for an Institution by name
    inst = manager.get_institution(name='Example Institution')
    
    # Searching for all Nodes that are owned by a certain Institution
    inst_nodes = manager.get_nodes(owners_contains=inst)
    
    # Searching for all links that are owned by an institution and connected to a certain node
    inst_node_links = manager.get_links(owners_contains=inst, nodes_contains=inst_nodes[0])
    
    
    
    
