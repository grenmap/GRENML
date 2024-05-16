import pytest
import grenml.managers as managers
from grenml.models import *
from grenml.exceptions import *
import xml.etree.ElementTree as ET  # noqa: N817
import grenml.write as write
import os

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


class TestManager:

    @pytest.fixture
    def manager(self):
        return managers.GRENMLManager('TEST_TOPOLOGY')

    @pytest.fixture
    def simple_institution(self):
        return Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME)

    @pytest.fixture
    def detailed_institution(self):
        return Institution(INSTITUTION_TEST_ID_2, INSTITUTION_TEST_NAME_2, INSTITUTION_SHORT_NAME + '2',
                           INSTITUTION_TYPE_GLOBAL, -180, -89.9, -44, 'TOR CA', ['55 TOR', '44 TOR'], '2020-01-30T02:10:23Z',
                           desc='detailed_institute', desc1='added additional properties using Institute Constructor')

    @pytest.fixture
    def multiple_institutions(self, simple_institution, detailed_institution):
        return [
            simple_institution,
            detailed_institution,
            Institution(id=INSTITUTION_TEST_ID + '_4', name=INSTITUTION_TEST_NAME + '_4', latitude=40, longitude=45,
                        institution_type=INSTITUTION_TYPE_GLOBAL),
            Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3, short_name=INSTITUTION_SHORT_NAME + '3',
                        institution_type=INSTITUTION_TYPE_NREN, longitude=180, latitude=89.9, altitude=25,
                        unlocode='US NYC', address='45 NYC', version='2020-01-30T02:10:23.Z',
                        property=['desc', 'Institution with all details'], desc='description of multiple institutes'),
        ]

    @pytest.fixture
    def simple_node(self, multiple_institutions):
        return Node(id=NODE_TEST_ID, name=NODE_TEST_NAME)

    @pytest.fixture
    def detailed_node(self, multiple_institutions):
        return Node(id=NODE_TEST_ID + '_4', name=NODE_TEST_NAME, owners=multiple_institutions.copy(), short_name='N4',
                    longitude=90, latitude=-9, altitude=22, unlocode='NY', address='Bank Street', version='2020-03-24T14:30:43-05:00',
                    lifetime_start='2020-03-20T14:30:43+05:00', lifetime_end='2020-03-29T14:30:43Z', desc='description')

    @pytest.fixture
    def multiple_nodes(self, multiple_institutions, simple_node, detailed_node):
        return [
            simple_node,
            detailed_node,
            Node(NODE_TEST_ID + '_2', 'TEST_NODE_NAME_2', 'NODE2', [multiple_institutions[0]], 0, 0, 2222, 'CA',
                 'Queensway', '2020-02-20T14:30:43+05:00', '2020-03-29T14:30:43-05:00', '2020-03-24T14:30:43-05:00',
                 desc='Node with details', desc1='This node has one owner'),
            Node(NODE_TEST_ID + '_3', 'TEST_NODE_NAME_3', 'NODE3', [multiple_institutions[2], multiple_institutions[3]],
                 -0.22, 44.33, 12222, 'IN', 'Carleton', '2020-02-20T14:30:43+07:00', '2020-03-29T14:30:43-07:00',
                 '2020-03-24T14:30:43-05:00')
        ]

    @pytest.fixture
    def simple_link(self, multiple_nodes):
        return Link(id=LINK_TEST_ID, name=LINK_TEST_NAME, nodes=[multiple_nodes[0], multiple_nodes[3]])

    @pytest.fixture
    def detailed_link(self):
        return Link(
            id=LINK_TEST_ID + '_2',
            name=LINK_TEST_NAME + '_2',
            short_name='TEST_LINK_SHORT_NAME',
            nodes=[Node(NODE_TEST_ID, NODE_TEST_NAME), Node(NODE_TEST_ID + '_2', NODE_TEST_NAME + '_2')],
            owners=[Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME)],
            lifetime_start='2020-03-20T14:30:43+05:00',
            lifetime_end='2020-03-29T14:30:43Z',
            version='2020-03-24T14:30:43-05:00',
            desc='Description of detailed link'
        )

    @pytest.fixture
    def multiple_links(self, multiple_nodes, multiple_institutions, simple_link, detailed_link):
        return [simple_link,
                detailed_link,
                Link(
                    id=LINK_TEST_ID + '_3',
                    name=LINK_TEST_NAME + '_3',
                    short_name='TEST_LINK_SHORT_NAME_3',
                    owners=[multiple_institutions[1]],
                    nodes=[multiple_nodes[1], multiple_nodes[2]],
                    lifetime_start='2020-03-21T14:30:43',
                    lifetime_end='2020-03-30T14:30:43',
                    version='2020-03-24T14:30:43-05:00',
                ),
                Link(
                    id=LINK_TEST_ID + '_4',
                    name=LINK_TEST_NAME + '_4',
                    short_name='TEST_LINK_SHORT_NAME_4',
                    owners=[multiple_institutions[1], multiple_institutions[2]],
                    nodes=[multiple_nodes[1], multiple_nodes[2]],
                    lifetime_start='2020-03-22T14:30:43',
                    lifetime_end='2020-03-31T14:30:43',
                    version='2020-03-24T14:30:43-05:00',
                ),
                ]

    def test_writer_create_default_topology(self, manager):
        """
        This test checks the writer's ability to write default xml when pass only instance of manager
        """
        file_name = 'default_topology.xml'
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        default_topology = dom.getroot()

        # checking default_topology has random id and is not None
        assert default_topology.attrib.get('id') is not None

        # checking default_topology's name
        assert default_topology.find('grenml:name', namespaces).text == DEFAULT_TOPOLOGY_NAME

        # checking default_topology's default institution
        inst = default_topology.find('grenml:Institution', namespaces)
        # checking default institute's id
        assert inst.attrib.get('id') == 'urn:ogf:networking:global'
        # checking default institute's name
        assert inst.find('grenml:name', namespaces).text == 'GREN'
        # checking default institute's type
        check_additional_property_tag(
            inst.findall('grenml:Property', namespaces),
            tag=[INSTITUTION_TYPE_GLOBAL]
        )
        assert inst.find('grenml:type', namespaces) is None

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_simple_topology_with_no_institution(self, manager):
        """
        This test checks the writer's ability to write xml when no institution is added to the manager
        """
        file_name = 'simple_topology_with_no_institution.xml'
        manager.topology.id = TOPOLOGY_ID
        manager.topology.name = TOPOLOGY_NAME
        manager.topology.add_property('description', 'The topology has default institution')
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's id
        assert topology.attrib.get('id') == TOPOLOGY_ID

        # checking topology's name
        assert topology.find('grenml:name', namespaces).text == TOPOLOGY_NAME

        # checking topology's additional properties
        check_additional_property_tag(
            topology.findall('grenml:Property', namespaces),
            description=['The topology has default institution']
        )

        # checking topology's default institution is present. We have checked the properties of the default institution
        # in the test def test_writer_create_default_topology(self, manager):
        assert topology.find('grenml:Institution', namespaces) is not None

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_topology_with_single_institution(self, manager, detailed_institution):
        """
        This test checks the writer's ability to write xml when detailed institution is added to the manager.
        This test also tests that we can pass additional properties using constructor of the object
        """
        file_name = 'simple_topology_with_institution.xml'
        manager.topology.name = TOPOLOGY_NAME
        manager.topology.id = TOPOLOGY_ID
        manager.topology.add_property('description', 'The topology has one institution')
        manager.topology.add_property('description2', 'The topology has two additional properties')
        manager.add_institution(detailed_institution)
        institute = manager.get_institution(id=INSTITUTION_TEST_ID_2)
        institute.add_property('desc', 'that is the description')
        institute.add_property('desc1', 'added additional property using add_property() method')
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's additional properties
        check_additional_property_tag(
            topology.findall('grenml:Property', namespaces),
            description=['The topology has one institution'],
            description2=['The topology has two additional properties'],

        )

        # checking topology's institution and default institution
        institutes = topology.findall('grenml:Institution', namespaces)
        for institute in institutes:
            # checking both institutes are present
            assert institute.get('id') in [DEFAULT_INSTITUTION_ID, INSTITUTION_TEST_ID_2]

            # checking topology's institution
            if institute.get('id') == INSTITUTION_TEST_ID_2:
                assert institute.get('version') == '2020-01-30T02:10:23+00:00'
                assert institute.find('grenml:name', namespaces).text == INSTITUTION_TEST_NAME_2
                assert institute.find('grenml:short-name', namespaces).text == INSTITUTION_SHORT_NAME + '2'
                check_location_tag(institute.find('grenml:Location', namespaces), -180.0, -89.9, -44, 'TOR CA',
                                   ['55 TOR', '44 TOR'])
                # checking institute's additional properties
                check_additional_property_tag(
                    institute.findall('grenml:Property', namespaces),
                    desc=['detailed_institute', 'that is the description'],
                    desc1=['added additional properties using Institute Constructor',
                           'added additional property using add_property() method'],
                    tag=[INSTITUTION_TYPE_GLOBAL]
                )

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_topology_with_institution_as_primary_owner(self, manager, simple_institution):
        """
        This test checks the writer's ability to write xml when simple institution that has only id and name; is
        set as primary owner
        """
        file_name = 'topology_with_institution_as_primary_owner.xml'
        manager.topology.name = TOPOLOGY_NAME
        manager.topology.id = TOPOLOGY_ID
        manager.add_institution(simple_institution)
        manager.set_primary_owner(INSTITUTION_TEST_ID)
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's id
        assert topology.attrib.get('id') == TOPOLOGY_ID

        # checking topology's name
        assert topology.find('grenml:name', namespaces).text == TOPOLOGY_NAME

        # checking topology's owner
        assert topology.find('grenml:owner', namespaces).text == INSTITUTION_TEST_ID

        # checking topology's institution and default institution are present
        institutes = topology.findall('grenml:Institution', namespaces)
        for institute in institutes:
            assert institute.get('id') in [DEFAULT_INSTITUTION_ID, INSTITUTION_TEST_ID]

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_topology_with_multiple_institutions(self, manager, multiple_institutions):
        """
        This test checks the writer's ability to write xml when multiple institutions are added to the manager
        """
        file_name = 'topology_with_multiple_institutions.xml'
        manager.topology.name = TOPOLOGY_NAME
        manager.topology.id = TOPOLOGY_ID
        manager.add_institutions(multiple_institutions)
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's institutions
        institutes = topology.findall('grenml:Institution', namespaces)
        for institute in institutes:
            # checking all institutes are present
            assert institute.get('id') in \
                   [DEFAULT_INSTITUTION_ID, INSTITUTION_TEST_ID, INSTITUTION_TEST_ID_2, INSTITUTION_TEST_ID_3,
                    INSTITUTION_TEST_ID + '_4']

            # checking topology's institution
            if institute.get('id') == INSTITUTION_TEST_ID + '_4':
                assert institute.find('grenml:name', namespaces).text == INSTITUTION_TEST_NAME + '_4'
                check_location_tag(institute.find('grenml:Location', namespaces), 45.0, 40.0, None, None, None)

            if institute.get('id') == INSTITUTION_TEST_ID_3:
                assert institute.find('grenml:name', namespaces).text == INSTITUTION_TEST_NAME_3
                check_additional_property_tag(
                    institute.findall('grenml:Property', namespaces),
                    property=['desc', 'Institution with all details'],
                    desc=['description of multiple institutes'],
                    tag=[INSTITUTION_TYPE_NREN],
                )

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_topology_with_single_node(self, manager, simple_institution, simple_node):
        """
        This test checks the writer's ability to write xml when a node is added to the manager.
        The node has no owner. But the topology primary owner becomes its owners
        """
        file_name = 'topology_with_single_node.xml'
        manager.add_institution(simple_institution, primary_owner=True)
        manager.add_node(simple_node)
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
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

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_topology_with_detailed_node(
            self, manager, multiple_institutions, detailed_node
    ):
        """
        This test checks the writer's ability to write default xml when a detailed node is added to the manager.
        """
        file_name = 'topology_with_detailed_node.xml'
        manager.add_institutions(multiple_institutions)
        manager.topology.primary_owner = INSTITUTION_TEST_ID
        manager.topology.add_property('description', 'Topology with multiple Institutes and a detailed node')
        manager.add_node(detailed_node)
        manager.get_node(id=NODE_TEST_ID + '_4').add_property('description', 'Node with all properties')
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's owner
        assert topology.find('grenml:owner', namespaces).text == INSTITUTION_TEST_ID

        # checking topology's detailed node
        node = topology.find('grenml:Node', namespaces)
        # checking node's id
        assert node.attrib.get('id') == NODE_TEST_ID + '_4'
        # checking node's version
        assert node.attrib.get('version') == '2020-03-24T14:30:43-05:00'
        # checking node's name
        assert node.find('grenml:name', namespaces).text == NODE_TEST_NAME
        # checking node's short-name
        assert node.find('grenml:short-name', namespaces).text == 'N4'
        # checking node's location
        check_location_tag(node.find('grenml:Location', namespaces), 90.0, -9.0, 22, 'NY', 'Bank Street')
        # checking node's lifetime
        check_lifetime_tag(
            node.find('grenml:Lifetime', namespaces=namespaces),
            lifetime_start='2020-03-20T14:30:43+05:00',
            lifetime_end='2020-03-29T14:30:43+00:00')
        # checking node's owner
        check_owners_tag(
            node.findall('grenml:owner', namespaces),
            {INSTITUTION_TEST_ID, INSTITUTION_TEST_ID_2, INSTITUTION_TEST_ID_3, INSTITUTION_TEST_ID + '_4'}
        )
        # checking node's additional property
        check_additional_property_tag(
            node.findall('grenml:Property', namespaces),
            desc=['description'],
            description=['Node with all properties']
        )

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_topology_with_multiple_nodes(self, manager, multiple_institutions, multiple_nodes):
        """
        This test checks the writer's ability to write xml when multiple nodes are added to the manager.
        """
        file_name = 'topology_with_multiple_nodes.xml'
        manager.topology.name = TOPOLOGY_NAME
        manager.topology.id = TOPOLOGY_ID
        manager.add_institutions(multiple_institutions)
        manager.add_nodes(multiple_nodes)
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's node
        nodes = topology.findall('grenml:Node', namespaces)
        for node in nodes:
            # checking all nodes are present
            assert node.get('id') in [NODE_TEST_ID, NODE_TEST_ID + '_2', NODE_TEST_ID + '_3', NODE_TEST_ID + '_4']

            # checking topology's node
            if node.get('id') == NODE_TEST_ID + '_2':
                assert node.find('grenml:name', namespaces).text == NODE_TEST_NAME + '_2'
                assert node.find('grenml:short-name', namespaces).text == 'NODE2'
                check_location_tag(node.find('grenml:Location', namespaces), 0.0, 0.0, 2222, 'CA', 'Queensway')
                check_owners_tag(node.findall('grenml:owner', namespaces), {INSTITUTION_TEST_ID})
                check_lifetime_tag(
                    node.find('grenml:Lifetime', namespaces),
                    lifetime_start='2020-02-20T14:30:43+05:00',
                    lifetime_end='2020-03-29T14:30:43-05:00'
                )
                check_additional_property_tag(
                    node.findall('grenml:Property', namespaces),
                    desc=['Node with details'],
                    desc1=['This node has one owner']
                )

            if node.get('id') == NODE_TEST_ID + '_3':
                assert node.find('grenml:name', namespaces).text == NODE_TEST_NAME + '_3'
                check_owners_tag(
                    node.findall('grenml:owner', namespaces),
                    {INSTITUTION_TEST_ID_3, INSTITUTION_TEST_ID + '_4'}
                )

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_topology_with_single_link(self, manager, multiple_institutions, multiple_nodes, simple_link):
        """
        This test checks the writer's ability to write xml when a link is added to the manager.
        """
        file_name = 'topology_with_single_link.xml'
        manager.add_institution(multiple_institutions[0], primary_owner=True)
        manager.add_institutions([multiple_institutions[2], multiple_institutions[3]])
        manager.add_node(multiple_nodes[0])
        manager.add_node(multiple_nodes[3])
        manager.add_link(simple_link)
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's link
        link = topology.find('grenml:Link', namespaces)

        # checking link's id
        assert link.get('id') == LINK_TEST_ID
        # checking link' name
        assert link.find('grenml:name', namespaces).text == LINK_TEST_NAME
        # checking link's owner
        check_owners_tag(
            link.findall('grenml:owner', namespaces),
            {INSTITUTION_TEST_ID}
        )
        # checking link's node
        check_owners_tag(
            link.findall('grenml:Node', namespaces),
            {NODE_TEST_ID, NODE_TEST_ID + '_3'}
        )

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))

    def test_writer_create_topology_with_multiple_links(
            self, manager, multiple_institutions, multiple_nodes, multiple_links):
        """
        This test checks the writer's ability to write xml when multiple links are added to the manager.
        """
        file_name = 'topology_with_multiple_links.xml'
        manager.topology.name = TOPOLOGY_NAME
        manager.topology.id = TOPOLOGY_ID
        manager.add_institutions(multiple_institutions)
        manager.add_nodes(multiple_nodes)
        manager.add_links(multiple_links)
        manager.get_link(id=LINK_TEST_ID).add_property('desc', 'Description')
        writer = write.GRENMLWriter(manager)
        writer.write_file(FILE_PATH.format(file_name))

        # checking the xml file created by writer
        dom = ET.parse(FILE_PATH.format(file_name))
        topology = dom.getroot()

        # checking topology's links
        links = topology.findall('grenml:Link', namespaces)

        for link in links:
            # checking all links are present
            assert link.get('id') in [LINK_TEST_ID, LINK_TEST_ID + '_2', LINK_TEST_ID + '_3', LINK_TEST_ID + '_4']

            # checking topology's link
            if link.get('id') == LINK_TEST_ID:
                assert link.find('grenml:name', namespaces).text == LINK_TEST_NAME
                check_additional_property_tag(
                    link.findall('grenml:Property', namespaces),
                    desc=['Description'],
                )
            elif link.get('id') == LINK_TEST_ID + '_2':
                assert link.find('grenml:name', namespaces).text == LINK_TEST_NAME + '_2'
                assert link.find('grenml:short-name', namespaces).text == 'TEST_LINK_SHORT_NAME'
                assert link.get('version') == '2020-03-24T14:30:43-05:00'
                # checking link's owners
                check_owners_tag(link.findall('grenml:owner', namespaces), {INSTITUTION_TEST_ID})
                # checking link's lifetime
                check_lifetime_tag(
                    link.find('grenml:Lifetime', namespaces),
                    lifetime_start='2020-03-20T14:30:43+05:00',
                    lifetime_end='2020-03-29T14:30:43+00:00'
                )
                # checking link's additional property
                check_additional_property_tag(
                    link.findall('grenml:Property', namespaces),
                    desc=['Description of detailed link']
                )
                # checking link's nodes
                check_owners_tag(link.findall('grenml:Node', namespaces), {NODE_TEST_ID, NODE_TEST_ID + '_2'})
            elif link.get('id') == LINK_TEST_ID + '_3':
                assert link.find('grenml:name', namespaces).text == LINK_TEST_NAME + '_3'
                check_owners_tag(
                    link.findall('grenml:owner', namespaces),
                    {INSTITUTION_TEST_ID_2}
                )
                # checking link's nodes
                check_owners_tag(
                    link.findall('grenml:Node', namespaces),
                    {NODE_TEST_ID + '_4', NODE_TEST_ID + '_2'}
                )
            else:
                assert link.find('grenml:name', namespaces).text == LINK_TEST_NAME + '_4'

        # Removing file after all asserts are true
        os.remove(FILE_PATH.format(file_name))
