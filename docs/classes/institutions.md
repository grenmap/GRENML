# Institution
## Inherits: [GRENMLObject](base.md#grenmlobject), [Location](base.md#Location)
## Overview

A representation of an organization in the network.

The purpose of an Institution is to represent ownership and peering to Nodes
and Links, to be able to show the topology of a network based on what 
institution owns the network, and show where different Institutions peer and
connect to each other.

## Initialization

An Institution can be initialized with the following fields.

    Institution(id=None, name=None, short_name=None, institution_type=None, longitude=0, latitude=0, altitude=None, unlocode=None, address=None, version=None, **kwargs)

And can be implemented in the following forms:

    from grenml.models import Institution
    inst = Institution('ID', 'NAME')
    inst = Institution(name='NAME')
    
    from grenml import GRENMLManager
    manager = GRENMLManager()
    manager.add_institution()  # This will automatically create an Institution object and provide the ID

## Attributes

### id: String : REQUIRED
The unique identifier for the Institution. Cannot be the same value as another 
Institution in the topology.

#### Default: 
If no ID is provided, a UUID will automatically be generated for the ID.

### name: String : REQUIRED
The full name of the Institution.

### short_name: String
The short name of the Institution.

### type: List[String\] : REQUIRED : DEPRECATED
The types of the institution. 

The first type assigned can be accessed using the `institution.type` property.

All types can be accessed using the `institution.types` property

#### DEPRECATED:
The type fields are to be removed and replaced with using the additional_properties entry 'tag'

### longitude: float : REQUIRED

The longitude co-ordinate of the Institution. The value must be between 180 and -180.

### latitude: float : REQUIRED

The latitude co-ordinate of the Institution. The value must be between 90 and -90.

### altitude: float

The altitude of the Institution.

### unlocode: string

The [UN/LOCODE](https://www.unece.org/cefact/locode/service/location.html) of the Location. 

### address: string or list[string\]

The address, or the addresses, of the Institution.

### version: Datetime
The version of the Institution. If added, it must be a datetime value of when
the Institution was created or last edited in ISO format.

### additional_properties
Additional keyword arguments that are added to the Institution as additional properties.

See [GRENMLObject additional_properties](base.md#additional_properties) for
more information and uses.

## Constants

### INSTITUTION_TYPES: List[string\] : DEPRECATED
The allowed types for institutions. All values will be converted to lowercase.

The Types allowed are:

    rren
    nren
    ran
    global
    connected institution
    other
    
WARNING: This is kept as a list of recommended types, but will be removed in future versions

## Functions

### match
#### Arguments: (**kwargs)
#### Returns: True or False

Compares the [Attributes](#attributes) of the Institution instance to all of the given 
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
