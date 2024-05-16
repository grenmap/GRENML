import pytest

import grenml.managers as managers
from grenml.parse import GRENMLParser

TOPOLOGY_MYISP = 'MyISP'
TOPOLOGY_ID = 'urn:ogf:network:global_MVP'
TOPOLOGY_INSTITUTION_1 = 'INST_1'
TOPOLOGY_INSTITUTION_2 = 'INST_2'
TOPOLOGY_INSTITUTION_3 = 'INST_3'
TOPOLOGY_NODE_1 = 'Node 1'
TOPOLOGY_NODE_2 = 'Node 2'
TOPOLOGY_NODE_3 = 'Node 3'
TOPOLOGY_LINK_1 = 'Link 1'
TOPOLOGY_LINK_2 = 'Link 2'
TOPOLOGY_LINK_3 = 'Link 3'
MAX_LONG = 180
MIN_LONG = -180
MAX_LAT = 90
MIN_LAT = -90
DEFAULT_FILE_PATH = './tests/test_parser_reader/'
MINIMAL_TOPOLOGY_FILE_LOCATION = DEFAULT_FILE_PATH + 'minimal_topology.xml'
MULTI_INST_FILE_LOCATION = DEFAULT_FILE_PATH + 'multiple_institutions.xml'
SINGLE_NODE_FILE_LOCATION = DEFAULT_FILE_PATH + 'topology_with_a_node.xml'
MUlTI_NODES_FILE_LOCATION = DEFAULT_FILE_PATH + 'topology_with_multiple_nodes.xml'
SINGLE_LINK_FILE_LOCATION = DEFAULT_FILE_PATH + 'topology_with_a_link.xml'
MULTI_LINKS_FILE_LOCATION = DEFAULT_FILE_PATH + 'topology_with_multiple_links.xml'


def check_location(grenml_object, latitude, longitude, altitude, unlocode, address):
    """
    This method checks the Location property of the object
    """
    assert grenml_object.latitude == latitude
    assert grenml_object.longitude == longitude
    assert grenml_object.altitude == altitude
    assert grenml_object.unlocode == unlocode
    assert grenml_object.address == address


def check_lifetime(grenml_object, lifetime_start, lifetime_end):
    """
    This method checks the lifetime property of the object
    """
    assert grenml_object.lifetime_start == lifetime_start
    assert grenml_object.lifetime_end == lifetime_end


def check_owners_or_nodes_or_links(owners_or_nodes_or_links, expected_names):
    """
    This method checks the owners or nodes or links
    param:
        owners_or_nodes_or_links: owners or nodes or links of the object
        expected_names: This is set of expected owners name or nodes name or links_name
    This method works only if owners, nodes, or links of the object are retrieved by function get_nodes(),
    get_institutions(), get_links() and not by the function get_institution(), get_node(), and get_link()
    """
    owners_or_nodes_or_links_name = []

    for owner_or_node_or_link in owners_or_nodes_or_links:
        owners_or_nodes_or_links_name.append(owner_or_node_or_link.name)

    assert set(owners_or_nodes_or_links_name) == expected_names


class TestReader:

    @pytest.fixture
    def manager(self):
        return managers.GRENMLManager('TEST_TOPOLOGY')

    @pytest.fixture
    def parser(self, manager):
        return GRENMLParser()

    def test_reader_minimal_topology(self, parser):
        """
        This test checks the parser's ability to read simple topology
        """
        manager = parser.parse_file(
            file_name=MINIMAL_TOPOLOGY_FILE_LOCATION
        )

        owner_id = manager.topology.primary_owner
        institution = manager.get_institution(id=owner_id)

        assert TOPOLOGY_MYISP == manager.topology.name
        assert TOPOLOGY_ID == manager.topology.id
        assert TOPOLOGY_INSTITUTION_1 == institution.name
        assert manager.get_nodes() is None
        assert manager.get_links() is None
        manager.validate()

    def test_reader_multiple_institutions(self, parser):
        """
        This test checks the ability of grenml library to read multiple institutions.
        """
        manager = parser.parse_file(MULTI_INST_FILE_LOCATION)

        owner_id = manager.topology.primary_owner
        detailed_institute = manager.get_institution(name=TOPOLOGY_INSTITUTION_1)

        assert TOPOLOGY_MYISP == manager.topology.name
        assert manager.topology.additional_properties.get('description') == ['This file contains multiple institutions']
        assert TOPOLOGY_INSTITUTION_1 == detailed_institute.name
        assert TOPOLOGY_INSTITUTION_2 == manager.get_institution(id=owner_id).name
        assert TOPOLOGY_INSTITUTION_3 == manager.get_institution(name=TOPOLOGY_INSTITUTION_3).name
        assert manager.get_nodes() is None
        assert manager.get_links() is None

        # checking institution with full details
        assert detailed_institute.version == '2020-04-08T08:20:15+00:00'
        assert detailed_institute.short_name == 'gren'
        assert detailed_institute.additional_properties.get(
            'description') == ['This is the description of institution gren']
        # checking location property of detailed_institute
        check_location(
            detailed_institute,
            latitude=MAX_LAT,
            longitude=MAX_LONG,
            altitude=5,
            unlocode='US NYC',
            address='45 NYC'
        )
        manager.validate()

    def test_reader_with_single_node(self, parser):
        """
        This test checks the parser's ability to read a node with full details
        """
        manager = parser.parse_file(
            file_name=SINGLE_NODE_FILE_LOCATION
        )
        node = manager.get_node()

        # Checking owners of the node
        check_owners_or_nodes_or_links(
            manager.get_institutions(id__in=node.owners),
            {TOPOLOGY_INSTITUTION_1, TOPOLOGY_INSTITUTION_2, TOPOLOGY_INSTITUTION_3}
        )

        assert node.name == TOPOLOGY_NODE_1
        assert node.id == 'urn:ogf:network:myisp.com:node1'
        assert node.short_name == 'node1'
        assert node.additional_properties.get('desc') == ['This is detailed node']

        # Checking location of the node
        check_location(
            node, MAX_LAT, MAX_LONG, 33, 'US NYC', '45 Rome'
        )
        # Checking lifetime of the node
        check_lifetime(
            node, lifetime_start='2020-04-08T08:20:15-04:00', lifetime_end='2020-01-30T02:10:23+00:00'
        )
        manager.validate()

    def test_reader_with_multiple_nodes(self, parser):
        """
        This test checks the parser's ability to read multiple nodes
        """
        manager = parser.parse_file(
            file_name=MUlTI_NODES_FILE_LOCATION
        )

        # checking that all node name's are present
        check_owners_or_nodes_or_links(
            manager.get_nodes(),
            set((TOPOLOGY_NODE_1, TOPOLOGY_NODE_2, TOPOLOGY_NODE_3))
        )

        # checking first node "TOPOLOGY_NODE_1"
        first_node = manager.get_node(name=TOPOLOGY_NODE_1)

        assert first_node.id == "urn:ogf:network:myisp.com:node1"
        assert first_node.version == "2020-04-14T08:20:15-05:00"
        check_location(first_node, MIN_LAT, MIN_LONG, None, None, None)
        check_lifetime(first_node, None, None)
        # checking owners of the first node
        check_owners_or_nodes_or_links(
            manager.get_institutions(id__in=first_node.owners),
            {TOPOLOGY_INSTITUTION_3, TOPOLOGY_INSTITUTION_2}
        )

        # checking second node "TOPOLOGY_NODE_2"
        second_node = manager.get_node(name=TOPOLOGY_NODE_2)

        # checking owners of the second node
        check_owners_or_nodes_or_links(
            manager.get_institutions(id__in=second_node.owners),
            set((TOPOLOGY_INSTITUTION_1, TOPOLOGY_INSTITUTION_2))
        )
        assert second_node.id == 'urn:ogf:network:myisp.com:node2'
        assert second_node.version == '2020-04-09T08:20:15-05:00'
        assert second_node.short_name == 'node2'
        assert second_node.additional_properties.get('desc') == ['This Node has multiple owners']
        check_location(second_node, MIN_LAT, MIN_LONG, 33, 'US NYC', '45 Rome')
        check_lifetime(second_node, '2020-04-08T08:20:15-04:00', '2020-01-30T02:10:23+00:00')

        # checking second node "TOPOLOGY_NODE_3"
        third_node = manager.get_node(name=TOPOLOGY_NODE_3)

        assert third_node.id == 'urn:ogf:network:myisp.com:node3'
        assert manager.get_institution(id__in=third_node.owners).name == TOPOLOGY_INSTITUTION_2
        check_location(third_node, 0, 0, None, None, None)
        check_lifetime(third_node, None, None)
        manager.validate()

    def test_reader_with_single_link(self, parser):
        """
            This test checks the parser's ability to read a link with full details
        """
        manager = parser.parse_file(
            file_name=SINGLE_LINK_FILE_LOCATION
        )

        link = manager.get_link()

        assert link.name == TOPOLOGY_LINK_1
        assert link.id == 'urn:ogf:network:myisp.com:link1'
        assert link.version == '2020-04-08T08:20:15-05:00'
        assert link.short_name == 'link1'
        assert link.additional_properties.get('desc') == ['Link with all details']
        assert link.additional_properties.get('desc2') == ['Link with multiple owners']
        check_lifetime(link, '2020-04-08T08:20:15-05:00', '2021-04-08T08:20:15+04:30')

        # checking link owners
        check_owners_or_nodes_or_links(
            manager.get_institutions(id__in=link.owners),
            {TOPOLOGY_INSTITUTION_1, TOPOLOGY_INSTITUTION_2}
        )

        # checking link nodes
        check_owners_or_nodes_or_links(
            manager.get_nodes(id__in=link.nodes),
            {TOPOLOGY_NODE_1, TOPOLOGY_NODE_2}
        )
        manager.validate()

    def test_reader_with_multiple_links(self, parser):
        """
            This test checks the parser's ability to read multiple links
        """
        manager = parser.parse_file(
            file_name=MULTI_LINKS_FILE_LOCATION
        )

        # checking that all link name's are present
        check_owners_or_nodes_or_links(
            manager.get_links(), set((TOPOLOGY_LINK_1, TOPOLOGY_LINK_2, TOPOLOGY_LINK_3))
        )

        # checking first link "TOPOLOGY_LINK_1"
        first_link = manager.get_link(name=TOPOLOGY_LINK_1)

        assert first_link.id == 'urn:ogf:network:myisp.com:link1'
        assert manager.get_institutions(id__in=first_link.owners)
        check_owners_or_nodes_or_links(
            manager.get_nodes(id__in=first_link.nodes),
            {TOPOLOGY_NODE_2, TOPOLOGY_NODE_3}
        )

        # checking second link "TOPOLOGY_LINK_2"
        second_link = manager.get_link(name=TOPOLOGY_LINK_2)

        assert second_link.id == 'urn:ogf:network:myisp.com:link2'
        assert second_link.version == '2020-03-15T08:20:15-05:00'
        assert second_link.short_name == 'link2'
        assert second_link.additional_properties.get('desc') == ['Link with all details']
        assert second_link.additional_properties.get('desc2') == ['Links']
        check_lifetime(second_link, '2020-04-08T08:20:15-05:00', '2021-04-08T08:20:15+04:30')
        # checking second_link owners
        assert manager.get_institutions(id__in=second_link.owners)
        # checking second_link nodes
        check_owners_or_nodes_or_links(manager.get_nodes(id__in=second_link.nodes), {TOPOLOGY_NODE_1, TOPOLOGY_NODE_3})

        # checking third_link "TOPOLOGY_LINK_3"
        third_link = manager.get_link(name=TOPOLOGY_LINK_3)

        assert third_link.id == 'urn:ogf:network:myisp.com:link3'
        assert manager.get_institutions(id__in=third_link.owners)
        check_owners_or_nodes_or_links(manager.get_nodes(id__in=third_link.nodes), {TOPOLOGY_NODE_2, TOPOLOGY_NODE_1})
        manager.validate()
