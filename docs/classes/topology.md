# Topology
## Inherits: [GRENMLObject](base.md#grenmlobject)

## Overview

An object that contains all of the elements of the network topology

## Initialization

The Topology takes no arguments on initialization.

    from grenml.models import Topology
    topology = Topology(name=None, **kwargs)

## Attributes

### id: string : REQUIRED
The unique identifier for the Topology.

#### Default: 
A UUID will automatically be generated for the ID.

### name: string : REQUIRED
The full name of the Topology.

#### Default:
Default is None

### primary_owner: Institution
The primary owner of the Topology. When setting this value, it must be an Institution
that is in the Topology. If a 'primary_owner' is set, every non-Institution object
added to the topology will have the `primary_owner` added to that object's `owners` list.

Attempting to set the `primary_owner` to an Institution that is not in the topology
will raise an InstitutionNotFoundError.

The GRENML library currently does not enforce a 'primary_owner' for a topology, this
is not inline with the XML Schema and will be addressed in conjunction with future
updates that address how information is stored in the GRENML DB Node.

#### Default: 
None

### institutions: Set[[Institution](institutions.md)]
The set of all the Institutions that are in the Topology.

#### Default: 
A set with 1 Institution inside it with ID 'global'

### nodes: Set[[Node](nodes.md)]
The set of all the Nodes that are in the Topology.

### links: Set[[Link](links.md)]
The set of all the Links in the Topology.

### topologies: Set[[Topologies](#topology)]
The set of all the sub-Topologies in this Topology.

## Constants

### INSTITUTIONS
The Institution Element Type. Used for access of the Institution list

### NODES
The Node Element Type. Used for access of the Nodes list

### LINKS
The Link Element Type. Used for access of the Links list.

### TOPOLOGIES
The Topology Element Type. Used to access the list of sub-Topologies

## Functions

### add_institution
#### Arguments: (inst)
#### Raises: AttributeIdError
Add the Institution to the Topology. 

The ID of the Institution must be unique, otherwise this function will raise
AttributeIdError.

##### inst
An Institution object to be added.

### add_node
#### Arguments: (node)
#### Raises: AttributeIdError
Add the Node to the Topology

The ID of the Node must be unique to other nodes, otherwise this function will
raise AttributeIdError.

The `primary_owner` of the Topology will automatically be added to a Node's owners list.

##### node
The Node object to be added

### add_link
#### Arguments: (link)
#### Raises: AttributeIdError
Add the Link to the Topology

The ID of the Link must be unique to the other links, otherwise this function will raise AttributeIdError.

The `primary_owner` of the Topology will automatically be added to a Link's owners list.

### get_element
#### Arguments: (search_type, **kwargs)
#### Returns: GRENMLObject
#### Raises: KeyError, ObjectNotFoundError, MultipleReturnedError
Search through the elements of this Topology and return the element that matches the 
key word arguments.

If there is no element that matches the arguments, this function will raise the
ObjectNotFoundError subclass relating to the element type.

If multiple elements match the parameters, then this function will raise 
MultipleReturnedError.

##### search_type
The type of element to search for. Uses the [constants](#CONSTANTS) to determine the
type.

If the search_type is an element that the Topology does not have, this function will
raise KeyError.

### get_elements
#### Arguments: (search_type, **kwargs)
#### Returns: Set(GRENMLObject) or None
#### Raises: KeyError
Search through all elements of the search_type in the Topology and return
all elements that match.

If no elements match, return None.

##### search_type
The type of element to search for. Uses the [constants](#CONSTANTS) to determine the
type.

If the search_type is an element that the Topology does not have, this function will
raise KeyError.

### delete_elements
#### Arguments: (ele_type, elements)
#### Raises: KeyError
Remove all the provided elements from the Topology

WARNING: This function performs lazy deletion. If an error rises in the middle
of execution, it will not restore any elements deleted before the error.

#### ele_type
The element type to remove from. Uses the [constants](#CONSTANTS) to determine the
type.

#### elements
A list of elements to be removed from the Topology of the element type.

If either the ele_type is a type that the Topology does not have, or
an element being removed does not exist in the Topology, this function will 
raise KeyError

### update_elements_properties
#### Arguments: (element_type, match_kwargs, attr, value=None, append=False, remove=False)
#### Raises: KeyError, ValueError, ObjectNotFoundError
Updates any element's additional properties that fit the matching 
arguments based on the options and values given.

Example uses:

    >>> # Add the attribute departments to the Institution with the name 'Harvard'
    >>> topology.update_elements(INSTITUTIONS, {'name': 'Harvard'}, 'departments')  
    >>> # Without a value, departments will be set to None
    >>> inst = topology.get_element(INSTITUTIONS, name='HARVARD')
    >>> inst.additional_properties['departments']
    None
    >>>
    >>> # Overwrite the value of an attribute
    >>> topology.update_element(INSTITUTIONS, {'name': 'Harvard'}, 'departments', 'accounting')
    >>> inst.additional_properties['departments']
    'accounting'
    >>>
    >>> # Adding an entry to a list, if the element is not a list, or None, it will be turned into a list.
    >>> topology.update_element(INSTITUTIONS, {'name': 'Harvard'}, 'departments', 'financial', append=True)
    >>> inst.additional_properties['departments']
    ['accounting', 'financial']
    >>> 
    >>> # Removing a value from a list
    >>> topology.update_element(INSTITUTIONS, {'name': 'Harvard'}, 'departments', 'accounting', remove=True)
    >>> inst.additional_properties['departments']
    ['financial'] 
    >>>
    >>> # Remove an attribute from an element
    >>> topology.update_element(INSTITUTIONS, {'name': 'Harvard'}, 'departments', remove=True)
    >>> inst.additional_properties['departments']
    KeyError 

#### element_type
The element type to update. Uses the [constants](#CONSTANTS) to determine the
type.

#### match_kwargs
A dictionary used to collect the elements to be updated. Functions the same as the
kwargs for get_elements.

#### attr
The attribute, as a string, to be added, removed, or modified. 

#### value
The value to be assigned, added, or removed from the property.

#### append
Determine if the value should be added to the property. If the value doesn't exist,
then add it as a list with one value. If the attribute exists, but is not a list,
the attribute will be converted to a list containing 2 items, the original value and the added value.

If append and remove are both set to True, this function will raise ValueError

#### remove
Determine if the value or attribute should be removed. If there is a value set, 
the value will be removed from the attribute list contents. If it's the last item in
the list, the attribute will be removed.

If append and remove are both set to True, this function will raise ValueError
