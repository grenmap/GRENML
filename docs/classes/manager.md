# GRENMLManager

## Overview

The GRENMLManager allows for streamlined use of the GRENML Library.

The GRENMLManager manages a [Topology](topology.md) and has many helper functions 
to allow for easy use.

If desired, one can use the Topology directly.

## Initialization

The GRENMLManager takes the following arguments arguments on initialization:

    from grenml import GRENMLManager
    manager = GRENMLManager(name=None, validator=TopologyValidator(), writer=GRENMLWriter, *args, **kwargs)

## Attributes

### topology: [Topology](topology.md)

The topology that is inside the GRENMLManager instance. 
Can be directly accessed for the scenario of if a helper function does not 
provide desired functionality. The name and any args/kwargs are passed to the topology

### validator: [TopologyValidation](validation.md)

The validation class used to verify that all the data in the Topology is in the format 
that's compatible with the GRENML XSD.

### writer: [GRENMLWriter](grenml-writer.md)

The writer class. 

## Functions

### set_primary_owner
#### Arguments: (institution_id)
#### Raises: InstitutionNotFoundError

Assigns the [primary owner](topology.md#primary_owner) of the Topology with
the institution that has the institution_id assigned.

If the institution_id does not correlate to an Institution in the Topology, 
this function will raise InstitutionNotFoundError

##### institution_id

The ID of the Institution being set at the primary owner. It must be already
an Institution that is in the Topology

### add_institution
#### Arguments: (id, name, short_name, institution_type, longitude, latitude, altitude, unlocode, address, version, primary_owner=False, **kwargs)
#### Raises: AttributeIdError
Add an [Institution](institutions.md) to the Topology. If the first argument is
an Institution instance, it is added directly to the Topology.

View the [Institution initialization](institutions.md##Initilization) for 
additional information on creating an Institution.

See [Topology add_institution](topology.md#add_institution) for 
any restrictions to an Institution to be added.

##### primary_owner
If `primary_owner` is True, then the Institution being added will be set as the Topologies owner.
Please see [Topology primary_owner](topology.md#primary_owner) for more information to how it's used.

### add_institutions
#### Arguments: (institutions)
#### Raises: AttributeIdError
As a shortcut to [add_institution](#add_institution), allow for the creation of multiple 
Institution objects and have all of them added to the Topology.

Note: This function adds Institutions one after the other. If there is an error part way through, it will not clean up 
any Institutions that were made before the error.

##### institutions
A list of either Institutions, argument lists, or key word argument dictionaries.
An example of its use:

    manager.add_institutions(
        [
            ['ID', 'NAME'],
            {'name': 'unique name', 'primary_owner': True},  # This institution would be set as the primary owner
            Institution('ID2', 'NAME'),
        ]
    )

### get_institution
#### Arguments: (**kwargs)
#### Returns: Institution
#### Raises: InstitutionNotFoundError, MultipleReturnedError

Collects a single institution that matched the given keyword arguments.
Reference [Institution match](institution.md#match) for fields and options for searching.

If multiple Institutions match, this function will raise MultipleReturnedError.

If no Institution matches the given criteria, this function will raise InstitutionNotFoundError

### get_institutions
#### Arguments: (**kwargs)
#### Returns: Set[[Institution]] or None

Collects any institutions that match the given keyword arguments.
Reference [Institution match](institution.md#match) for fields and options for searching.

If there are any Institutions that match the parameters, return a set containing all the Institutions 
that matched.

If no Institutions matched the parameters, the function will return None.

### delete_institutions
#### Arguments: (**kwargs)

Locate all Institutions that [match](institution.md#match) the given parameters
and goes through them one by one to delete them.

##### WARNING:
This performs a lazy lookup and will not evaluate if there are any dependencies attached to the 
Institution. Without care, this can easily invalidate your data. Use with caution.

### add_node
#### Arguments: (id, name, short_name, longitude, latitude, altitude, unlocode, address, lifetime_start, lifetime_end, version, **kwargs)
#### Raises: AttributeIdError

Add a [Node](nodes.md) to the [Topology](topology.md). If the first argument is
a Node instance, it is added directly to the Topology.

View the [Node initialization](nodes.md##Initilization) for 
additional information on creating a Node.

See [Topology add_node](topology.md#add_node) for 
any restrictions to a Node to be added.

When assigning `owners` to the node, this function will convert a list of strings 
into Institution objects, using the strings as IDs, or take Institution objects directly.


### add_nodes
#### Arguments: (nodes)
#### Raises: AttributeIdError
As a shortcut to [add_node](#add_node), allow for the creation of multiple 
Node objects and have all of them added to the Topology.

Note: This function adds Nodes one after the other. If there is an error part way through, it will not clean up 
any Nodes that were made before the error.

##### nodes
A list of either Nodes, argument lists, or key word argument dictionaries.
An example of its use:

    manager.add_nodes(
        [
            ['ID', 'NAME', ['INST_ID']],
            {'name': 'unique name', 'owners': ['INST_ID_1', 'INST_ID_2']},
            Node('ID2', 'NAME', ['INST_ID']),
        ]
    )

### get_node
#### Arguments: (**kwargs)
#### Returns: Node
#### Raises: NodeNotFoundError, MultipleReturnedError

Collects a single node that matched the given keyword arguments.
Reference [Node match](node.md#match) for fields and options for searching.

If multiple Nodes match, this function will raise MultipleReturnedError.

If no Node matches the given criteria, this function will raise NodeNotFoundError

### get_nodes
#### Arguments: (**kwargs)
#### Returns: Set[[Node]] or None

Collects any nodes that match the given keyword arguments.
Reference [Node match](node.md#match) for fields and options for searching.

If there are any Nodes that match the parameters, return a set containing all the Nodes 
that matched.

If no Nodes matched the parameters, the function will return None.

### delete_nodes
#### Arguments: (**kwargs)

Locate all Nodes that [match](node.md#match) the given parameters
and goes through them one by one to delete them.

##### WARNING:
This performs a lazy lookup and will not evaluate if there are any dependencies attached to the 
Node. Without care, this can easily invalidate your data. Use with caution.

### add_owner_to_node
#### Arguments: (owner_id, node_id)
#### Raises: InstitutionNotFoundError, NodeNotFoundError

Add an owner to an already existing node.

##### owner_id
The ID of the Institution to be added to the Node. If there is no Institution
with this ID, this function will raise InstitutionNotFoundError

##### node_id
The ID of the Node to add the Institution to. If there is no Node with this ID,
this function will raise NodeNotFoundError

### remove_owner_from_node
#### Arguments: (owner_id, node_id)
#### Raises: InstitutionNotFoundError, NodeNotFoundError, IndexError

Remove an Institution from a Node's owners list.

##### owner_id
The ID of the Institution to be added to the Node. If there is no Institution
with this ID, this function will raise InstitutionNotFoundError.

If the Node does not have this Institution in its owners list, an IndexError will be raised

##### node_id
The ID of the Node to add the Institution to. If there is no Node with this ID,
this function will raise NodeNotFoundError

### add_link
#### Arguments: (id, name, short_name, owners, nodes, lifetime_start, lifetime_end, version, **kwargs)
#### Raises: AttributeIdError

Add a [Link](links.md) to the [Topology](topology.md). If the first argument is
a Node instance, it is added directly to the Topology.

View the [Link initialization](links.md##Initilization) for 
additional information on creating a Node.

See [Topology add_link](topology.md#add_node) for 
any restrictions to a Link to be added.

### add_links
#### Arguments: (links)
#### Raises: AttributeIdError
As a shortcut to [add_link](#add_link), allow for the creation of multiple 
Link objects and have all of them added to the Topology.

Note: This function adds Links one after the other. If there is an error part way through, it will not clean up 
any Nodes that were made before the error.

##### links
A list of either Links, argument lists, or key word argument dictionaries.
An example of its use:

    manager.add_nodes(
        [
            ['ID', 'NAME', '', ['INST_ID'], ['Node 1', 'Node 2']],
            {'name': 'unique name', 'owners': ['INST_ID_1', 'INST_ID_2'], 'nodes': ['Node 3', 'Node 4']},
            Link('ID2', 'NAME', '', ['INST_ID'], ['Node 1', 'Node 3']),
        ]
    )

### get_link
#### Arguments: (**kwargs)
#### Returns: Link
#### Raises: LinkNotFoundError, MultipleReturnedError

Collects a single link that matched the given keyword arguments.
Reference [Link match](link.md#match) for fields and options for searching.

If multiple Nodes match, this function will raise MultipleReturnedError.

If no Link matches the given criteria, this function will raise LinkNotFoundError

### get_links
#### Arguments: (**kwargs)
#### Returns: Set[[Link]] or None

Collects any links that match the given keyword arguments.
Reference [Link match](link.md#match) for fields and options for searching.

If there are any Links that match the parameters, return a set containing all the Links 
that matched.

If no Links matched the parameters, the function will return None.

### delete_links
#### Arguments: (**kwargs)

Locate all Links that [match](link.md#match) the given parameters
and goes through them one by one to delete them.

##### WARNING:
This performs a lazy lookup and will not evaluate if there are any dependencies attached to the 
Link. Without care, this can easily invalidate your data. Use with caution.

### add_owner_to_link
#### Arguments: (owner_id, link_id)
#### Raises: InstitutionNotFoundError, LinkNotFoundError

Add an owner to an already existing link.

##### owner_id
The ID of the Institution to be added to the Link. If there is no Institution
with this ID, this function will raise InstitutionNotFoundError

##### link_id
The ID of the Node to add the Institution to. If there is no Link with this ID,
this function will raise LinkNotFoundError

### remove_owner_from_link
#### Arguments: (owner_id, link_id)
#### Raises: InstitutionNotFoundError, LinkNotFoundError, IndexError

Remove an Institution from a Link's owners list.

##### owner_id
The ID of the Institution to be added to the Link. If there is no Institution
with this ID, this function will raise InstitutionNotFoundError.

If the Link does not have this Institution in its owners list, an IndexError will be raised

##### link_id
The ID of the Node to add the Institution to. If there is no Link with this ID,
this function will raise LinkNotFoundError

### validate
#### Arguments: (raise_error=True)
#### Returns: List[[String]]
#### Raises: ValueError

Executes the validation classes validate function. See [TopologyValidator.validate](validation.md/#validate) for more details.

#### raise_error

Whether the validate function should raise an error if any errors are encountered or this function should raise an error.

### write_to_file
#### Arguments: (filename)

Executes the write_file function of the writer class, passing the provided file. See [GENMLWriter.write_file](grenml-writer.md#write_file) for more details.

### write_to_stream
#### Arguments: (stream)

Executes the write_stream function of the writer class, passing the provided output stream. See [GENMLWriter.write_stream](grenml-writer.md#write_stream) for more details.

### write_to_string

Executes the write_string function of the writer class. See [GENMLWriter.write_string](grenml-writer.md#write_string) for more details.
