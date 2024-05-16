# TopologyValidator

## Overview

The validation class designed to verify that all the objects in a topology 
have data in the format that is intended for converting the data to GRENML XML.

## Initialization

The TopologyValidator takes no arguments on initialization.

    from grenml.validation import TopologyValidator
    validator = TopologyValidator()

## Attributes

### topology: [Topology](topology.md)

A Topology object that can be attached to the class for validation 

### isvalid: boolean

This property validates the inset topology and gives a boolean.

Example use:

    >>> topology = Topology()
    >>> validator = TopologyValidator()
    >>> validator.topology = topology
    >>>
    >>> # Populate the Topology
    >>> 
    >>> if not validator.isvalid:
    >>>     # Do something because it's not valid

## Functions

### validate
#### Arguments (topology=None, raise_error=True)
#### Returns: List[String\]
#### Raises: ValueError

Execute the validation on the topology. This will go through every field of the topology
and every object in the topology. As it iterates through all the objects and fields, this function
creates a list of error messages to identify the points of invalid data.

If validation passes, the verified Topology is considered to meet or exceed the 
requirements outlined in the XSD.

#### topology
The Topology to validate. If it's None, the validate function will use the 
topology attached to the TopologyValidator by default. If both are None, then
a ValueError is raised

    >>> topology = Topology(name='Topology Name')
    >>> # fill the topology
    >>>
    >>> validator = TopologyValidator()
    >>> # You can to either of the following
    >>> validator.topology = topology
    >>> validator.validate()
    []
    >>> # or
    >>> validator.validate(topology=topology)
    []

#### raise_error
If raise_error is set to True, the validate function will raise an error if
there is any invalid data in the topology. If false, the validate function will
provide a list of points where the data is invalid.

    >>> topology = Topology(id='example')
    >>> 
    >>> validator = TopologyValidator()
    >>> validator.topology = topology
    >>> validator.validate(raise_error=False)
    ['Topology example must have a name', 'Topology example name must be a String']
    >>> validator.validate()
    ValueError: Topology example must have a name
    Topology example name must be a String
