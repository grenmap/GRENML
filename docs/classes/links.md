# Link

## Inherits: [GRENMLObject](base.md#grenmlobject)

## Overview

A representation of a connection between 2 locations of the network.

A Link is used to connect 2 Nodes and determine connections between Institutions
and the topology of various RENs. 

## Initialization

A Link can be initialized with the following fields.

    Link(id=None, name=None, short_name=None owners=[], nodes=[], lifetime_start=None, lifetime_end=None)

And can be implemented in the following forms:

    from grenml.models import Link
    Link('ID', 'NAME')
    Link(name='NAME', owners=['Inst'], nodes=['Node 1', 'Node 2'])
    
    from grenml import GRENMLManager
    manager = GRENMLManager()
    manager.add_institution(id='INST_ID', name='INST')
    manager.add_node(id='node id', name='NAME', owners=['INST_ID'])
    manager.add_node(id='node 2 id', name='NAME2')
    manager.add_link(name='link', owners=['INST_ID'], nodes=['node id', 'node 2 id'])

## Attributes

### id: String : REQUIRED
The unique identifier for the Link. Cannot be the same value as another 
Link in the topology.

#### Default: 
If no ID is provided, a UUID will automatically be generated for the ID.

### name: String : REQUIRED
The full name of the Link.

### owners: List[[Institution](institutions.md)\]
A list of all Institutions that have equipment/peering at this node

### nodes: List[[Node](nodes.md)\] : REQUIRED
A list of Nodes that this link connects.

NOTE: The nodes attribute MUST have 2 unique entries in order to pass validation.

### lifetime_start: String

The time when the Link was put in service. See [Lifetime start](base.md#lifetime_start:_string)
for more information.

### lifetime_end: String

The time when the Link was discontinued or is set to be discontinued. 
See [Lifetime end](base.md#lifetime_end:_string) for more information.

### version: Datetime
The version of the Node. If added, it must be a datetime value of when
the Node was created or last edited in ISO format.

### additional_properties
Additional keyword arguments that are added to the Link as additional properties.

See [GRENMLObject additional_properties](base.md#additional_properties) for
more information and uses.

## Functions

### match
#### Arguments: (**kwargs)
#### Returns: True or False

Compares the [Attributes](#attributes) of the Link instance to all of the given 
arguments, and returning True if they match.

See the GRENMLObject [match](base.md#match) for options that can be used 
with the attributes.

### add_property
#### Arguments: (attr, value)

Get the [additional_properties](#additional_properties) from the current Link, add the value to the property selected.

See [GRENMLObject add_property](base.md#add_property) for more information.

### del_property
#### Arguments: (attr, value=None)

Remove the value from the Link's [additional_properties](#additional_properties), or delete that property if no value is given.

See [GRENMLObject del_property](base.md#del_property) for more information.
