# Node

## Inherits: [GRENMLObject](base.md#grenmlobject), [Location](base.md#location), [Lifetime](base.md#lifetime)

## Overview

A representation of a physical location in the network.

A Node can be a PoP (Point of Presence), data centre, or any other location
where Institutions connect to one another.

## Initialization

A Node can be initialized with the following fields.

    Node(id=None, name=None, short_name=None, owners=[], longitude=None, latitude=None, altitude=None, unlocode=None, address=None, lifetime_start=None, lifetime_end=None, version=None, **kwargs)

And can be implemented in the following forms:

    from grenml.models import Node, Institution
    Node('ID', 'NAME')
    Node(name='NAME', owners=['INST'])
    
    from grenml import GRENMLManager
    manager = GRENMLManager()
    manager.add_institution(id='INST_ID', name='INST')
    manager.add_node(name='NAME', owners=['INST_ID'])  # This will automatically create a Node and link it to the Institution

## Attributes

### id: String : REQUIRED
The unique identifier for the Node. Cannot be the same value as another 
Node in the topology.

#### Default: 

If no ID is provided, a UUID will automatically be generated for the ID.

### name: String : REQUIRED

The full name of the Node.

### short_name: String

The short name of the Institution.

### owners: List[[Institution](institutions.md)\] : REQUIRED
A list of all Institutions that have equipment/peering at this Node

### longitude: float : REQUIRED

The longitude co-ordinate of the Node. The value must be between 180 and -180.

### latitude: float : REQUIRED

The latitude co-ordinate of the Node. The value must be between 90 and -90.

### altitude: float

The altitude of the Node.

### unlocode: string

The [UN/LOCODE](https://www.unece.org/cefact/locode/service/location.html) of the Location. 

### address: string or list[string\]

The address, or the addresses, of the Node.

### lifetime_start: String

The time when the Node was put in service. See [Lifetime start](base.md#lifetime_start:_string)
for more information.

### lifetime_end: String

The time when the Node was discontinued or is set to be discontinued. 
See [Lifetime end](base.md#lifetime_end:_string) for more information.

### version: Datetime
The version of the Node. If added, it must be a datetime value of when
the Node was created or last edited in ISO format.

### additional_properties
Additional keyword arguments that are added to the Node as additional properties.

See [GRENMLObject additional_properties](base.md#additional_properties) for
more information and uses.

## Functions

### match
#### Arguments: (**kwargs)
#### Returns: True or False

Compares the [Attributes](#attributes) of the Node instance to all of the given 
arguments, and returning True if they match.

See the GRENMLObject [match](base.md#match) for options that can be used 
with the attributes.

### add_address
#### Arguments: (address)

Add an address to the Institution.

See [Location add_address](base.md#add_address) for more detail on usage

### remove_address
#### Arguments: (address)

Remove an address from the Institution.

See [Location remove_address](base.md#remove_address) for more detail on usage

### add_property
#### Arguments: (attr, value)

Get the [additional_properties](#additional_properties) from the current Institution, add the value to the property selected.

See [GRENMLObject add_property](base.md#add_property) for more information.

### del_property
#### Arguments: (attr, value=None)

Remove the value from the Institution's [additional_properties](#additional_properties), or delete that property if no value is given.

See [GRENMLObject del_property](base.md#del_property) for more information.
