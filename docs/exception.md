# AttributeNameError
## Inherits: AttributeError
Attribute 'name' must be a human readable string name and not None.

# AttributeIdError
## Inherits: AttributeError
Attribute 'identifier' must be a persistent globally unique string (URI, UUID, etc.) and not None

# AttributeOwnerError
## Inherits: AttributeError
Attribute 'owner' must be an Institution object.

# AttributeNodeError(AttributeError):
## Inherits: AttributeError
The attribute nodes must contain only Node objects and there can only be 2 Nodes on a Link.

# ObjectNotFoundError:
Unable to locate object in a single item search

# InstitutionNotFoundError
## Inherits: ObjectNotFoundError
Unable to find an institution when searching for a single institution

# NodeNotFoundError
## Inherits: ObjectNotFoundError
Unable to find a node that meets search parameters

# LinkNotFoundError
## Inherits: ObjectNotFoundError
Unable to find a link that meets search parameters

# TopologyNotFoundError
## Inherits: ObjectNotFoundError
Unable to find the selected sub-Topology that matches search parameters

# MultipleReturnedError:
A get single returned multiple values
