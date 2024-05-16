from grenml.excel_converter import XLSParser, ExcelParseError


def convert_xls_to_grenml(topology_name, read_file_location, write_file_location, owner):
    parser = XLSParser(topology_name, owner)
    manager, errors = parser.parse_file(read_file_location)

    manager.write_to_file(write_file_location)
    print('File {} has been written'.format(write_file_location))


def main():
    import argparse
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=""
                    "Takes in a copy of the initial version of the standard"
                    " issue NREN GREN XLSX form and converts it into GRENML"
                    " XML format."
                    "\nAll arguments need to be passed for a successful run."
                    "\nExample use: python3 ./excel_conversion.py"
                    " -o MyISP\ Inc."  # noqa: W605
                    " -t MyISP\ GRENML\ Topology"  # noqa: W605
                    " -r ./MyISP\ GREN\ Map\ Data\ Form.xlsx"  # noqa: W605 W505
                    " -w ./output/MyISP_GRENML.xml"
    )
    parser.add_argument(
        '-topology', '-t', type=str,
        help='The name of the Topology for the generated XML file',
        required=True,
    )
    parser.add_argument(
        '-read_file', '-r', type=str,
        help='The XLSX file to be read in.'
             ' It must have the same formatting as the official data spreadsheet',
        required=True,
    )
    parser.add_argument(
        '-write_file', '-w', type=str,
        help='The XML file destination to export the GRENML XML to',
        required=True,
    )
    parser.add_argument(
        '-organization', '-o', type=str,
        help='The organization name that is generating this XML file',
        required=True,
    )
    args = parser.parse_args()

    try:
        convert_xls_to_grenml(
            args.topology, args.read_file, args.write_file, args.organization,
        )
    except ExcelParseError as error:
        print('Errors found in the spreadsheet:\n{}'.format(
            '\n'.join(error.error_list)
        ))


if __name__ == '__main__':
    main()
