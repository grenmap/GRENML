# GRENML Library

## Overview

The Global Research and Education Network (GREN) Mapping Initiative seeks to create a
standard data format & schema for sharing publicly-viewable data between Organizations, such as Research and Educational Networks (RENS).
To assist in solving this issue, the GRENML library has been developed.

The Global Research and Education Network Markup Language (GRENML) is an
XML format that extends [Network Markup Language (NML)](https://www.ogf.org/documents/GFD.206.pdf) with the purpose of 
sharing network topology data for mapping purposes.
 
## Development

Please review the following documents before working on the code:

- [Coding Conventions](development/coding_conventions.md)
- [GRENML Parsing](development/grenml-parser.md)
- [Release Procedure](development/release.md)
- [Changelog Update Procedure](development/changelog.md)

## Classes

### Base (grenml)

#### [GRENMLManager](classes/manager.md) 

The manager for the GRENML library. Allows for easy use of the Topology library
and a majority of use cases should be covered by the manager.

### Parser (grenml.parse)

#### [GRENMLParser](development/grenml-parser.md)

A reader for GRENML that loads a manager object with the data contained in a GRENML XML file

### Exceptions (grenml.exceptions)

#### [Exceptions](exception.md)

A list of custom exceptions that are used by GRENML.

### Validation (grenml.validation)

#### [TopologyValidator](classes/validation.md)

The validation class used to enforce the data structure for the GRENML output

### Models (grenml.models)

#### [Utility/Inherited Classes](classes/base.md) 

These classes are used by the other Model classes to allow for uniformity 
of functionality.

#### [Topology](classes/topology.md) 

The Topology class that contains all the elements to be represented in GRENML.

#### [Institutions](classes/institutions.md) 

A representation of an organization in the topology, used to determine ownership.

#### [Nodes](classes/nodes.md) 

A representation of a location of peering/connection point on a map.

#### [Links](classes/links.md)

A representation of a connection between two nodes.

## Required Attributes

Any Attribute labeled REQUIRED must have a non None value when it is processed 
by the validator.

## Excel Conversion Script

The Python program `excel_conversion.py` creates a GRENML file from an Excel workbook.

To get usage instructions:

```sh
python3 excel_conversion.py -h
```

The file `docs/Sample Conversion Spreadsheet/GREN_data.v1_0.xlsx` explains how to arrange the topology information in an Excel workbook.

The program attempts to continue reading the Excel file when it finds inconsistent or bad data. If this happens, it doesn't write the GRENML output, but prints a list of errors.

Possible data problems are: geographical location using an incorrect format, nodes referring to missing institutions, links referring to missing nodes or institutions, duplicate nodes, duplicate institutions.
