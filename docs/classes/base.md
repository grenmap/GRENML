# General Classes

## Overview

A number of classes need to have shared functionality and attribute.
All classes in this document are intended to be inherited and not used directly.

This document is intended to cover the shared functionality from the inherited classes.

# GRENMLObject
## Overview

The default class that is inherited by all model classes. 
Contains all the default variables and functions that all model classes 
should have.

## Initialization

The GRENMLObject can take multiple values upon initialization:

    from grenml.models.meta import GRENMLObject
    GRENMLObject(id=None, name=None, short_name=None, version=None, id_format: IDGeneration = None, **kwargs)

## Object IDs
Every GRENMLObject needs to have a unique ID. If an ID is not supplied, the library will generate an ID based on the manager or library default format.

The library can generate an ID in one of two ways, either a random UUID string or deterministically from the object properties (the default setting).

A deterministically generated ID is a SHA256 hash of the following object properties:
 - Object type
 - Name
 - Short name 

NOTE: A deterministic ID will only be generated on object creation. Updating properties used to generate the ID will not update the ID.


## Attributes:

### id: String : REQUIRED
The unique identifier for the Institution. Cannot be the same value as another 
Institution in the topology.

#### Default: 
If no ID is provided, an ID will be generated.

### name: String : REQUIRED
The full name of the Object.

### short_name: String
The short name of the Object

### version: Datetime
The version of the Object. If added, it must be a datetime value of when
the object was created or edited in ISO format.

### id_format: meta.IDGeneration
The format used to generate an ID, if an ID is not supplied. See [Object IDs](#Object IDs) for more information.

#### Default:
If no ID format is provided, and no ID is supplied, the ID will be deterministically generated.

### additional_properties

Additional keyword arguments that are added to the object as additional properties.
These attributes can be lists, sets, tuples, numbers, or strings but cannot be dictionaries.

Any key word arguments passed into the kwargs will be converted to lowercase and be accessible through the additional_properties getter. However, the related values will not have their case changed.

    >>> gremnl_obj = GRENMLObject(name='test', Quality='high', coordinates=[0.3, 43.2, 12.3])
    >>> grenml_obj.additional_properties['quality']
    'high'
    >>> grenml_obj.additional_properties['coordinates'][2]
    12.3
    >>> grenml_obj.additional_properties['name'] = 'Example additional name'
    >>> grenml.additional_properties['name']
    'Example additional name'


## Functions

### match
#### Arguments: (**kwargs)
#### Returns: True or False

Dynamically evaluate the attributes of the class/subclass and return 
the evaluation that the key word arguments given match the attributes of the class.

The match also provides a few options for matching.

##### __contains

Contains will evaluate that the field has the given parameter as a substring 
or is an element in its list, or is a sub section of it.

Example use: 
    
    >>> # This is to demonstrate multiple types of fields. Not exact to use.
    >>> grenml_object = GRENMLObject(id='some_text', name='name', others=['id1', 'id2', 'id3'])
    >>> grenml_object.match(id__contains='some')
    True
    >>> grenml_object.match(others__contains=['id1', 'id3']
    True
    >>> grenml_object.match(others__contains='id2')
    True

##### __in

In will check if the field is a substring or is in the list of the given 
parameter.

Example uses: 
    
    >>> # This is to demonstrate multiple types of fields. Not exact to use.
    >>> grenml_object = GRENMLObject(id='some_text', name='name', others=['id1', 'id2', 'id3'])
    >>> grenml_object.match(id__in='some_text_or_other_text')
    True
    >>> grenml_object.match(others__in=['id1', 'id2', 'id3', 'id4']
    True
    >>> grenml_object.match(id_in=['some_text', 'other_text'])
    True
    
### __eq\_\_
#### Arguments: (other)
#### Returns: True or False

Override of the __eq\_\_ function to dynamically evaluate all fields of the 
subclass and return True only if all fields match rather than a pointer comparison.

If the GRENMLObject is being compared to a string, it will evaluate True if
the ID of the GRENMLObject is the same.

Example uses:
    
    >>> grenml_object = GRENMLObject('ID', 'NAME')
    >>> other_object = GRENMLObject('ID', 'NAME')
    >>> grenml_object == other_object
    True
    >>> grenml_object == 'ID'
    True
    >>> third_object = GRENMLObject('ID', 'OTHER_NAME')
    >>> grenml_object == third_object
    False

##### other
The object being compared to.

### add_property
#### Arguments: (attr, value)

Get the [additional_properties](#additional_properties) from the current object and either creates and assigns the
property on the object's additional_properties or converts the property to a list and adds the value to 
the list.

#### attr
The attribute, as a string, to add, or to add to.

#### value
The value to assign to the attribute, or to add to the attribute

### del_property
#### Arguments: (attr, value=None)

Remove the value from the [additional_properties](#additional_properties), or delete that property if no value is given.

#### attr
The attribute, as as string, to remove from or to delete.

#### value
The value to remove from the attribute or, if it's None, remove the attribute from the object.

# Location

## Overview

An representation of the fields needed to identify a location for the purposes of being represented on a map.

Any object that needs to be represented as a point on a map should inherit this class.

## Initialization

A Location can be initialized with the following values:

    from grenml.models.meta import Location
    Location(longitude, latitude, altitude, unlocode, address, **kwargs)

## Attributes

### longitude: Float : REQUIRED

The longitude co-ordinate of the Location. The value must be between 180 and -180.

### latitude: Float : REQUIRED

The latitude co-ordinate of the Location. The value must be between 90 and -90.

### altitude: Float

The altitude of the Location.

### unlocode: String

The [UN/LOCODE](https://www.unece.org/cefact/locode/service/location.html) of the Location. 

### address: List[String\]

The address, or the addresses, of the Location.

## Functions:

### add_address 
#### Arguments: (address)

Take an address and assigns it to the address field. If the address field is
None, it will assign the address to the address field. Otherwise convert the address field into a 
list, and add the given address to that list. 

Example use:

    >>> location = Location(0, 0, 0, None, None)
    >>> location.address
    None
    >>> location.add_address('example address')
    >>> location.address
    'example address'
    >>> location.add_address('example address 2')
    >>> location.address
    ['example addresss', 'example address 2']
    

### remove_address
#### Arguments: (address)
#### Raises: ValueError, AttributeError

Take an address, and remove that from the addresses list. If the address either
doesn't match the current address or is not in the address list, it will raise a ValueError.

Example use:

    >>> location = Location(0, 0, 0, None, ['example addresss', 'example address 2'])
    >>> location.remove_address('example address')
    >>> location.address
    ['example address 2']
    >>> location.remove_address('example address 2')
    >>> location.address
    []

# Lifetime

## Overview
A representation of the lifetime of an Object. 

A lifetime is used to indicate when the Object was added to the Topology and 
when, if it has an expiry time, it would/was removed from the Topology. 

Some examples of the use of this lifetime can be:

* To outline the start and end of a contract
* To show the changing topology over time
* To represent when a contract needs to be renewed

## Initialization

A Lifetime can be initialized with the following values:

    from grenml.models.meta import Lifetime
    Lifetime(lifetime_start=None, lifetime_end=None, **kwargs)

## Attributes

### lifetime_start: String
The start time of the lifetime of the object as a string. This must be assigned an ISO format 
compatible string, integer timestamp, or a Datetime value. 

This attribute performs some amount of modification on a given value when assigned.
The lifetime_start will always have the following format:

    <Year>-<Month>-<Day>T<Hour>:<Minute>:<Second><Time zone difference from UTC>

An example is:

    2020-04-02T09:34:23-04:00

A few examples of this in use:

    >>> lifetime = Lifetime()
    >>> lifetime.lifetime_start
    None
    >>> lifetime.lifetime_start = '2020-04-02T15:00:00'
    >>> lifetime.lifetime_start
    '2020-04-02T15:00:00-04:00'
    >>> lifetime.lifetime_start = datetime(2020, 4, 2)
    >>> lifetime.lifetime_start
    '2020-04-02T00:00:00-04:00'
    >>> lifetime.lifetime_start = '2020-04-07T00:00:00-08:00'
    >>> lifetime.lifetime_start
    '2020-04-07T00:00:00-08:00'
    
### lifetime_end: String
The end time of the lifetime of the object as a string. This must be assigned 
an ISO format compatible string, integer timestamp, or a Datetime value.

See [lifetime_start](#lifetime_start) for the requirements for assigning 
a value to lifetime_end.

NOTE: If supplied a lifetime end, a lifetime start must also be supplied.

