import io
import os
import xml.etree.ElementTree as ET  # noqa: N817
import pytest
from grenml import managers
from grenml.models import *

INSTITUTION_SHORT_NAME = 'TEST'
INSTITUTION_TEST_ID = 'TEST_ID'
INSTITUTION_TEST_NAME = 'TEST_NAME'
INSTITUTION_TEST_ID_2 = 'TEST_ID_2'
INSTITUTION_TEST_NAME_2 = 'TEST_NAME_2'
INSTITUTION_TEST_ID_3 = 'TEST_ID_3'
INSTITUTION_TEST_NAME_3 = 'TEST_NAME_3'
DEFAULT_INSTITUTION_ID = 'urn:ogf:networking:global'
NODE_TEST_ID = 'TEST_NODE_ID'
NODE_TEST_NAME = 'TEST_NODE_NAME'
LINK_TEST_ID = 'TEST_LINK_ID'
LINK_TEST_NAME = 'TEST_LINK_NAME'
TOPOLOGY_NAME = 'MyISP'
DEFAULT_TOPOLOGY_NAME = 'TEST_TOPOLOGY'
TOPOLOGY_ID = 'urn:ogf:network:myisp.com:Topology_ID'

INSTITUTION_TYPE_DEFAULT = 'other'
INSTITUTION_TYPE_GLOBAL = 'global'
INSTITUTION_TYPE_NREN = 'nren'

namespaces = {'grenml': 'http://schemas.ogf.org/nml/2020/01/grenml',
              'nml': 'http://schemas.ogf.org/nml/2013/05/base#'}
FILE_PATH = './tests/test_writer/{}'


def check_location_tag(location_element, longitude, latitude, altitude, unlocode, address):
    """
    This method verifies that location element is correct or not
    """
    if longitude is not None:
        assert location_element.find('grenml:long', namespaces).text == str(longitude)
    if latitude is not None:
        assert location_element.find('grenml:lat', namespaces).text == str(latitude)
    if altitude is not None:
        assert location_element.find('grenml:alt', namespaces).text == str(altitude)
    if unlocode is not None:
        assert location_element.find('grenml:unlocode', namespaces).text == unlocode
    if address is not None:
        if not isinstance(address, (list, set, tuple)):
            address = [address]
        list_of_address = []
        for addr in location_element.findall('grenml:address', namespaces):
            list_of_address.append(addr.text)
        assert list_of_address == address


def check_lifetime_tag(lifetime_element, lifetime_start, lifetime_end):
    """
    This method verifies that lifetime element is correct or not
    """
    assert lifetime_element.find('nml:start', namespaces).text == lifetime_start
    assert lifetime_element.find('nml:end', namespaces).text == lifetime_end


def check_owners_tag(owners_tag, set_of_owners):
    """
    This method verifies the owners are correct or not
    """
    for owner in owners_tag:
        assert owner.text in set_of_owners


def check_additional_property_tag(properties, **kwargs):
    """
    This method verifies the additional properties are correct or not
    """
    property_dictionary = {}
    for property_element in properties:
        try:
            property_dictionary[property_element.get('name')].append(property_element.text)
        except KeyError:
            property_dictionary[property_element.get('name')] = [property_element.text]

    assert property_dictionary == kwargs


class TestWriterShortCut:

    @pytest.fixture
    def manager(self):
        return managers.GRENMLManager('TEST_TOPOLOGY')

    @pytest.fixture
    def simple_institution(self):
        return Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)

    @pytest.fixture
    def detailed_institution(self):
        return Institution(INSTITUTION_TEST_ID_2, INSTITUTION_TEST_NAME_2, INSTITUTION_SHORT_NAME + '2',
                           INSTITUTION_TYPE_GLOBAL, -180, -89.9, -44, 'TOR CA', ['55 TOR', '45 TOR'],
                           '2020-01-30T02:10:23+00:00', desc='detailed_institute',
                           desc1='added additional properties using Institute Constructor')

    @pytest.fixture
    def simple_node(self, simple_institution):
        return Node(id=NODE_TEST_ID, name=NODE_TEST_NAME, longitude=180, latitude=90, owners=[simple_institution],
                    lifetime_start='2020-01-30T02:10:23+00:00', lifetime_end='2019-01-30T02:10:23+00:00',
                    desc='simple_node')

    def test_checking_write_to_string_shortcut(self, manager, detailed_institution):
        """
        This test checks the write_to_string() function
        """
        manager.topology.name = TOPOLOGY_NAME
        manager.topology.id = TOPOLOGY_ID
        manager.add_institution(detailed_institution, primary_owner=True)
        xml_data = manager.write_to_string()

        # checking data
        root = ET.fromstring(xml_data)

        # checking Topology's id
        assert root.attrib.get('id') == TOPOLOGY_ID

        # checking topology's name
        assert root.find('grenml:name', namespaces=namespaces).text == TOPOLOGY_NAME

        # checking topology's owner
        assert root[1].text == INSTITUTION_TEST_ID_2

        # checking topology's institutes
        institutes = root.findall('grenml:Institution', namespaces)
        for institute in institutes:
            # checking both institutes are present
            assert institute.get('id') in [DEFAULT_INSTITUTION_ID, INSTITUTION_TEST_ID_2]
            # checking topology's institution
            if institute.get('id') == INSTITUTION_TEST_ID_2:
                assert institute.get('version') == '2020-01-30T02:10:23+00:00'
                assert institute.find('grenml:name', namespaces).text == INSTITUTION_TEST_NAME_2
                assert institute.find('grenml:short-name', namespaces).text == INSTITUTION_SHORT_NAME + '2'
                check_location_tag(
                    institute.find('grenml:Location', namespaces),
                    -180.0, -89.9, -44, 'TOR CA', ['55 TOR', '45 TOR']
                )
                check_additional_property_tag(
                    institute.findall('grenml:Property', namespaces),
                    desc=['detailed_institute'],
                    desc1=['added additional properties using Institute Constructor'],
                    tag=[INSTITUTION_TYPE_GLOBAL]
                )

    def test_checking_write_to_output_stream_shortcut(self, manager, detailed_institution):
        """
        This test checks the write_to_output_stream() function
        """
        manager.topology.name = TOPOLOGY_NAME
        manager.topology.id = TOPOLOGY_ID
        manager.add_institution(detailed_institution, primary_owner=True)
        xml_data = io.StringIO()
        manager.write_to_output_stream(stream=xml_data)

        # checking data
        root = ET.fromstring(xml_data.getvalue())

        # checking Topology's id
        assert root.attrib.get('id') == TOPOLOGY_ID

        # checking topology's name
        assert root.find('grenml:name', namespaces=namespaces).text == TOPOLOGY_NAME

        # checking topology's owner
        assert root[1].text == INSTITUTION_TEST_ID_2

        # checking topology's institutes
        institutes = root.findall('grenml:Institution', namespaces)
        for institute in institutes:
            # checking both institutes are present
            assert institute.get('id') in [DEFAULT_INSTITUTION_ID, INSTITUTION_TEST_ID_2]

    def test_checking_write_to_file_shortcut(self, manager, simple_institution, simple_node):
        """
        This test checks the write_to_file() function
        """
        file_name = 'topology_with_single_node.xml'
        manager.add_institution(simple_institution, primary_owner=True)
        manager.add_node(simple_node)
        manager.write_to_file(FILE_PATH.format(file_name))

        # checking the xml file created by write_to_file() function
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's owner
        assert topology.find('grenml:owner', namespaces).text == INSTITUTION_TEST_ID

        # checking topology's node
        node = topology.find('grenml:Node', namespaces)
        # checking node's id
        assert node.attrib.get('id') == NODE_TEST_ID
        # checking node's name
        assert node.find('grenml:name', namespaces).text == NODE_TEST_NAME
        # checking node's owner
        assert node.find('grenml:owner', namespaces).text == INSTITUTION_TEST_ID

        # checking node's location
        check_location_tag(
            node.find('grenml:Location', namespaces),
            longitude=180.0,
            latitude=90.0,
            altitude=None,
            unlocode=None,
            address=None
        )

        # checking node's lifetime
        check_lifetime_tag(
            node.find('grenml:Lifetime', namespaces),
            lifetime_start='2020-01-30T02:10:23+00:00',
            lifetime_end='2019-01-30T02:10:23+00:00'
        )

        # checking node's additional properties
        check_additional_property_tag(
            node.findall('grenml:Property', namespaces),
            desc=['simple_node'],
        )
        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))
