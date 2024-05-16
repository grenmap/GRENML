import pytest
from grenml.models import Topology, Link, Institution, Node, INSTITUTIONS, NODES, LINKS
from grenml.exceptions import InstitutionNotFoundError, NodeNotFoundError, \
    LinkNotFoundError
from grenml.validation import TopologyValidator

TOPOLOGY_TEST_NAME = 'TEST_TOPOLOGY_NAME'
TOPOLOGY_TEST_ID = 'TEST_TOPOLOGY_ID'
INSTITUTION_TEST_ID = 'TEST_ID_1'
INSTITUTION_TEST_NAME = 'TEST_NAME_1'
INSTITUTION_TEST_ID_2 = 'TEST_ID_2'
INSTITUTION_TEST_NAME_2 = 'TEST_NAME_2'
INSTITUTION_TEST_ID_3 = 'TEST_ID_3'
INSTITUTION_TEST_NAME_3 = 'TEST_NAME_3'
INSTITUTION_TYPE_DEFAULT = 'Test Institution'
NODE_TEST_ID = 'TEST_NODE_ID'
NODE_TEST_NAME = 'TEST_NAME'
NODE_TEST_ID_2 = 'TEST_NODE_ID_2'
NODE_TEST_NAME_2 = 'TEST_NODE_NAME_2'
NODE_TEST_ID_3 = 'TEST_NODE_ID_3'
NODE_TEST_NAME_3 = 'TEST_NODE_NAME_3'
LINK_TEST_ID = 'TEST_LINK_ID'
LINK_TEST_NAME = 'TEST_LINK_NAME'
LINK_TEST_ID_2 = 'TEST_LINK_ID_2'
LINK_TEST_NAME_2 = 'TEST_LINK_NAME_2'


class TestTopology:

    @pytest.fixture
    def institution(self):
        return Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)

    @pytest.fixture
    def institutions(self, institution):
        return [
            institution,
            Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2, institution_type=INSTITUTION_TYPE_DEFAULT),
            Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3, institution_type=INSTITUTION_TYPE_DEFAULT),
        ]

    @pytest.fixture
    def node(self, institutions):
        return Node(
            id=NODE_TEST_ID,
            name=NODE_TEST_NAME,
            owners=[institutions[0].id, institutions[1].id, institutions[2].id],
            longitude=0,
            altitude=0,
            latitude=0
        )

    @pytest.fixture
    def nodes(self, institutions, node):
        return [
            node,
            Node(
                id=NODE_TEST_ID_2,
                name=NODE_TEST_NAME_2,
                owners=[institutions[0].id],
                custom='TEST_CUSTOM_ATTR',
                longitude=0,
                altitude=0,
                latitude=0
            ),
            Node(
                id=NODE_TEST_ID_3,
                name='TEST_NODE_NAME_3',
                owners=[institutions[0].id, institutions[1].id],
                custom_list=['TEST_CUSTOM_ATTR'],
                longitude=0,
                altitude=0,
                latitude=0
            ),
        ]

    @pytest.fixture
    def link(self, nodes, institutions):
        return Link(id=LINK_TEST_ID, name=LINK_TEST_NAME, owners=institutions, nodes=[nodes[0], nodes[1]])

    @pytest.fixture
    def links(self, nodes, institution, link):
        return [link,
                Link(id=LINK_TEST_ID_2, name=LINK_TEST_NAME_2, owners=[institution], nodes=[nodes[1], nodes[2]])]

    @pytest.fixture
    def topology(self, institutions, nodes, links):
        topology = Topology(
            id=TOPOLOGY_TEST_ID,
            name=TOPOLOGY_TEST_NAME,
        )
        for institution in institutions:
            topology.add_institution(institution)
        for node in nodes:
            topology.add_node(node)
        for link in links:
            topology.add_link(link)
        return topology

    @pytest.fixture
    def simple_topology(self):
        topology = Topology(
            id=TOPOLOGY_TEST_ID,
            name=TOPOLOGY_TEST_NAME,
        )
        return topology

    @pytest.mark.parametrize(
        'args, kwargs',
        (
            ([], {'id': TOPOLOGY_TEST_ID, 'name': TOPOLOGY_TEST_NAME}),
            ([], {'name': TOPOLOGY_TEST_NAME}),
            ([], {'id': '', 'name': TOPOLOGY_TEST_NAME}),
            ([], {'id': 12345, 'name': TOPOLOGY_TEST_NAME}),
            ([TOPOLOGY_TEST_NAME], {}),
            (
                [],
                {'id': TOPOLOGY_TEST_ID, 'name': TOPOLOGY_TEST_NAME, 'primary_owner': 'global', }
            ),
        ),
        ids=['kwargs with id name', 'kwargs with only name', 'kwargs name andempty id',
             'kwargs id as integer', 'args with name', 'kwargs with primary owner', ]
    )
    def test_topology_create_success(self, args, kwargs):
        """
        Check the topology creation pass cases
        """
        Topology(*args, **kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'id': TOPOLOGY_TEST_ID}),
            ({'name': TOPOLOGY_TEST_NAME}),
            ({'id': TOPOLOGY_TEST_ID, 'name': TOPOLOGY_TEST_NAME}),
            ({'id__in': TOPOLOGY_TEST_ID}),
            ({'id__in': [TOPOLOGY_TEST_ID, NODE_TEST_ID, NODE_TEST_ID_2]}),
            ({'id__in': 'TEST_TOPOLOGY_ID123'}),
            ({'id__in': TOPOLOGY_TEST_ID + '123'}),
            ({'id__in': '123_TEST_TOPOLOGY_ID1_123_TEST_NODE_ID_123_TEST_NODE_ID'}),
            ({'id__contains': TOPOLOGY_TEST_ID}),
            ({'id__contains': TOPOLOGY_TEST_ID[:8]}),
            ({'id__contains': ''}),
            ({'id__contains': '123_TEST_TOPOLOGY_ID1_123_TEST_NODE_ID_123_TEST_NODE_ID'[4:9]}),
        ),
        ids=['id only', 'name only', 'id name',
             'id institution', 'id nodes', 'id in list', 'id__in_with matching string',
             'id__in_with_matching string pat3', 'id__contains link id', 'id__contains substring',
             'id_ contains empty', 'id__contains slice func', ],
    )
    def test_topology_match_success(self, topology, nodes, institutions, kwargs):
        """
        Test link match function in topology, loop through possible combinations
        """
        assert topology.match(**kwargs)

    @pytest.mark.parametrize(
        'args, kwargs',
        [
            ([INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME], {}),
            ([], {'id': INSTITUTION_TEST_ID, 'name': INSTITUTION_TEST_NAME}),
            ([], {'name': INSTITUTION_TEST_NAME}),
        ],
        ids=['with args', 'with kwargs', 'without id'],
    )
    def test_adding_institution(self, args, kwargs):
        """
        Test topology add institution function, add institution with some basic
        options and check the institution could get the from the topology
        """
        topology = Topology()
        inst = Institution(*args, **kwargs)
        topology.add_institution(inst)
        assert topology.get_elements(INSTITUTIONS, **kwargs)

    def test_delete_institution(self, topology, institution):
        """
        Add and check the institution to the topology.
        Remove the institution from the topology.
        """
        inst = topology.get_element(INSTITUTIONS, id=INSTITUTION_TEST_ID)
        assert inst == institution
        topology.delete_elements(INSTITUTIONS, topology.get_elements(INSTITUTIONS, id=INSTITUTION_TEST_ID))
        with pytest.raises(InstitutionNotFoundError):
            topology.get_element(INSTITUTIONS, id=INSTITUTION_TEST_ID)

    @pytest.mark.parametrize(
        "args, kwargs",
        (
            ([NODE_TEST_ID, NODE_TEST_NAME], {}),
            ([], {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME}),
            ([NODE_TEST_ID, NODE_TEST_NAME, ], {'owners': [Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ([NODE_TEST_ID, NODE_TEST_NAME], {'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution(id='TEST_ID_2', name='TEST_NAME_2', institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution(id='TEST_ID_3', name='TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT),
            ]}),
            ([NODE_TEST_ID, NODE_TEST_NAME], {'owners': [INSTITUTION_TEST_ID]}),
            ([], {'name': NODE_TEST_NAME}),
        ),
        ids=[
            'values only', 'keywords only', 'with single owner',
            'with multiple owners', 'with owner id as string',
            'without id']
    )
    def test_topology_add_node(self, institutions, args, kwargs):
        """
        Test topology add node, add node with basic options and check the node
        could get from the topology.
        """
        topology = Topology()
        for institution in institutions:
            topology.add_institution(institution)
        node = Node(*args, **kwargs)
        topology.add_node(node)
        assert topology.get_element(NODES, **kwargs)

    def test_topology_delete_node(self, topology):
        topology.delete_elements(NODES, topology.get_elements(NODES, id=NODE_TEST_ID))
        with pytest.raises(NodeNotFoundError):
            topology.get_element(NODES, id=NODE_TEST_ID)

    def test_assigns_primary_owner_with_institution(self, topology, institution):
        topology.primary_owner = institution
        assert topology.primary_owner == institution

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'id': NODE_TEST_ID},
            {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME},
            {'owners': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3']},
            {'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT),
            ]},
            {'name': NODE_TEST_NAME},
            {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME, 'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT),
            ]},
        ),
        ids=[
            'id match', 'id and name match', 'owners match with strings',
            'owners match with objects', 'name match', 'all match'
        ]
    )
    def test_topology_get_node(self, topology, kwargs):
        topology.get_element(NODES, **kwargs)

    @pytest.mark.parametrize(
        "element, search, attribute, kwargs",
        [
            [
                INSTITUTIONS,
                {'id': INSTITUTION_TEST_ID},
                'name',
                {'value': 'TEST_REWRITE_NAME'}
            ],
            [
                INSTITUTIONS,
                {'id': INSTITUTION_TEST_ID},
                'new_attr',
                {'value': 'TEST_REWRITE_NAME'}
            ],
            [
                NODES,
                {'id': NODE_TEST_ID_2},
                'custom',
                {'value': 'TEST_REWRITE_NAME', 'append': True}
            ],
            [
                INSTITUTIONS,
                {'id__contains': 'TEST'},
                'name',
                {'value': 'TEST_REWRITE_NAME'}
            ],
            [
                NODES,
                {'id': NODE_TEST_ID_3},
                'custom_list',
                {'value': 'TEST_CUSTOM_ATTR', 'remove': True}
            ],
            [
                NODES,
                {'id': NODE_TEST_ID_2},
                'custom',
                {'remove': True}
            ],
        ],
        ids=[
            'add name property', 'add attribute', 'add to existing attribute', 'rewrite names of multiple elements',
            'remove only entry from list', 'can delete custom attribute'
        ]
    )
    def test_topology_update_elements(self, topology, element, search: dict, attribute: str, kwargs: dict):
        elements = topology.get_elements(element, **search)
        topology.update_elements_properties(element, search, attribute, **kwargs)
        for element in elements:
            attr = element.additional_properties.get(attribute, None)
            if 'append' in kwargs.keys():
                assert kwargs['value'] in attr
            elif 'remove' in kwargs.keys():
                if 'value' in kwargs.keys():
                    assert attr is None or not kwargs['value'] in attr
                else:
                    assert attr is None
            else:
                assert attr == kwargs['value']

    @pytest.mark.parametrize(
        "element, search, attribute, kwargs, exception",
        [
            [
                INSTITUTIONS,
                {'id': INSTITUTION_TEST_ID},
                'id',
                {'remove': True},
                KeyError
            ],
            [
                NODES,
                {'id': NODE_TEST_ID_2},
                'custom',
                {'value': "Entry that doesn't exist", 'remove': True},
                ValueError
            ],
            [
                NODES,
                {'id': NODE_TEST_ID_2},
                'custom',
                {'append': True, 'remove': True},
                ValueError
            ],
            [
                NODES,
                {'id': NODE_TEST_ID_3},
                'custom_list',
                {'value': "Entry that doesn't exist", 'remove': True},
                ValueError
            ],
        ],
        ids=[
            'user cannot delete non existent property', "Cannot remove value that doesn't exist",
            'cannot append and delete at the same time', "Cannot remove from list with value that doesn't exist"
        ]
    )
    def test_topology_update_elements_failure_cases(
            self, topology, element, search, attribute, kwargs, exception
    ):
        with pytest.raises(exception):
            topology.update_elements_properties(element, search, attribute, **kwargs)

    def test_topology_additional_properties(self, topology):
        assert not topology.additional_properties
        topology.add_property('custom', 'Test Value')
        assert topology.additional_properties == {'custom': ['Test Value']}

    def test_topology_additional_properties_case_sensitivity(self, topology):
        assert not topology.additional_properties
        topology.add_property('CUStom', 'Test Value')
        assert topology.additional_properties == {'custom': ['Test Value']}

    @pytest.mark.parametrize(
        "args, kwargs",
        (
            ([LINK_TEST_ID, LINK_TEST_NAME], {}),
            ([], {'name': LINK_TEST_NAME}),
            ([], {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME}),
            ([LINK_TEST_ID, LINK_TEST_NAME],
             {'nodes': [NODE_TEST_ID, NODE_TEST_ID_2]}),
            ([], {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME, 'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)
            ]}),
            ([], {
                'id': LINK_TEST_ID, 'name': LINK_TEST_NAME,
                'nodes': [
                    Node(
                        id=NODE_TEST_ID, name=NODE_TEST_NAME,
                        owners=[INSTITUTION_TEST_ID, INSTITUTION_TEST_ID_2, INSTITUTION_TEST_ID_3],
                        longitude=0, altitude=0, latitude=0,
                    )
                ]
            }),
            ([], {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME, 'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution(INSTITUTION_TEST_ID_2, INSTITUTION_TEST_NAME_2, institution_type=INSTITUTION_TYPE_DEFAULT)
            ]}),
        ),
        ids=['values only', 'name only', 'keywords only', 'link with nodes',
             'link has one owner', 'link with node has owner', 'link with multiple owners']
    )
    def test_topology_add_link(self, institutions, nodes, args, kwargs):
        """
        Test add link to topology with possible situtations.
        """
        topology = Topology()
        for institution in institutions:
            topology.add_institution(institution)
        for node in nodes:
            topology.add_node(node)
        link = Link(*args, **kwargs)
        topology.add_link(link)
        assert topology.get_element(LINKS, **kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'id': LINK_TEST_ID},
            {'name': LINK_TEST_NAME},
            {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME},
            {'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT),
            ]},
            {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME, 'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', institution_type=INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT),
            ]},
        ),
        ids=['id match', 'name match', 'id and name match', 'owners match with objects',
             'node name match']
    )
    def test_topology_get_link(self, topology, kwargs):
        topology.get_element(LINKS, **kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'id': ' '},
            {'id': 'garbage value'},
            {'id': NODE_TEST_ID},
            {'id': INSTITUTION_TEST_ID},
            {'name': ' '},
            {'name': NODE_TEST_NAME},
            {'name': INSTITUTION_TEST_NAME},
            {'name': 'garbage value'},
        ),
        ids=[
            'empty id', 'id: garbage_value', 'id: node_id', 'id: institution_id', 'name empty',
            'name: node_name', 'name: institution_name', 'name: garbage value']
    )
    def test_get_link_fail(self, topology, kwargs):
        with pytest.raises(LinkNotFoundError):
            topology.get_element(LINKS, **kwargs)

    def test_topology_delete_link(self, topology):
        """
        Test remove link using link id
        """
        topology.delete_elements(LINKS, topology.get_elements(LINKS, id=LINK_TEST_ID))
        with pytest.raises(LinkNotFoundError):
            topology.get_element(LINKS, id=LINK_TEST_ID)

    def test_pass_primary_owner_in_institution_list(self, simple_topology, institution):
        """
        Test topology validation owner in institution list
        """
        simple_topology.add_institution(institution)
        simple_topology.primary_owner = institution
        validator = TopologyValidator()
        validator.validate(topology=simple_topology)

    def test_fail_primary_owner_not_in_institution_list(self, simple_topology, institution):
        """
        Test topology validation owner not in institution list
        """
        simple_topology.primary_owner = institution
        validator = TopologyValidator()
        with pytest.raises(
            ValueError,
            match=r".* primary owner ID TEST_ID_1 must be in the Topologies Institutions"
        ):
            validator.validate(topology=simple_topology)

    def test_pass_add_institution_type_not_in_list(self, institution, simple_topology):
        """
        Test institution type not in the type list
        """
        simple_topology.add_institution(institution)
        simple_topology.primary_owner = institution
        validator = TopologyValidator()
        validator.validate(topology=simple_topology)
        test_institution = Institution(
            'New_INSTITUTION_ID',
            'New_INSTITUTION_NAME',
            'New_SHORTNAME',
            'connected institution'
        )
        test_institution._type = 'pren'
        simple_topology.add_institution(test_institution)
        validator.validate(topology=simple_topology)

    def test_fail_add_node_owner_not_in_list(self, institution, simple_topology):
        """
        Test node owner not in the institution list
        """
        simple_topology.add_institution(institution)
        simple_topology.primary_owner = institution
        validator = TopologyValidator()
        validator.validate(topology=simple_topology)
        test_institution = Institution(
            'New_INSTITUTION_ID',
            'New_INSTITUTION_NAME',
            'New_SHORTNAME',
            'connected institution'
        )
        test_node = Node(
            id='New Node ID',
            name='New Node Name',
            owners=[test_institution.id],
            longitude=0,
            latitude=0,
            altitude=0,
        )
        simple_topology.add_node(test_node)
        with pytest.raises(
            ValueError,
            match=r'.* owner id .* does not exist in parent Topology .*'
        ):
            validator.validate(topology=simple_topology)

    def test_fail_add_link_owner_not_in_list(self, institutions, nodes, simple_topology):
        """
        Test link owner not in the institution list
        """
        for institution in institutions:
            simple_topology.add_institution(institution)
        for node in nodes:
            node._short_name = 'Test Short Name'
            node.owners.add(institutions[0].id)
            simple_topology.add_node(node)
        simple_topology.primary_owner = institutions[0].id
        validator = TopologyValidator()
        validator.validate(topology=simple_topology)
        test_institution = Institution(
            'New_INSTITUTION_ID',
            'New_INSTITUTION_NAME',
            'New_SHORTNAME',
            'connected institution'
        )
        test_link = Link(
            id='New Link ID',
            name='New Link Name',
            owners=[test_institution.id],
            nodes=[nodes[0].id, nodes[1].id]
        )
        simple_topology.add_link(test_link)
        with pytest.raises(
            ValueError,
            match=r'Link New Link ID listed owner .* does not exist in parent Topology .*'
        ):
            validator.validate(topology=simple_topology)

    def test_fail_add_link_nodes_not_in_list(self, institutions, nodes, simple_topology):
        """
        Test link nodes not in the nodes list
        """
        for institution in institutions:
            simple_topology.add_institution(institution)
        for node in nodes:
            node._short_name = 'Test Short Name'
            node.owners.add(institutions[0].id)
        simple_topology.primary_owner = institutions[0].id
        validator = TopologyValidator()
        validator.validate(topology=simple_topology)
        test_link = Link(
            id='New Link ID',
            name='New Link Name',
            owners=[institutions[0].id],
            nodes=[nodes[0].id, nodes[1].id]
        )
        simple_topology.add_link(test_link)
        with pytest.raises(
            ValueError,
            match=r'Link New Link ID listed node .* does not exist in parent Topology .*'
        ):
            validator.validate(topology=simple_topology)

    def test_fail_add_link_with_one_node(self, institutions, nodes, simple_topology):
        """
        Test link that contains only one node
        """
        for institution in institutions:
            simple_topology.add_institution(institution)
        for node in nodes:
            node._short_name = 'Test Short Name'
            node.owners.add(institutions[0].id)
            simple_topology.add_node(node)
        simple_topology.primary_owner = institutions[0]
        validator = TopologyValidator()
        validator.validate(topology=simple_topology)
        test_link = Link(
            id='New Link ID',
            name='New Link Name',
            owners=[institutions[0].id],
            nodes=[nodes[0].id]
        )
        simple_topology.add_link(test_link)
        with pytest.raises(ValueError):
            validator.validate(topology=simple_topology)

    def test_fail_add_link_with_three_nodes(self, institutions, nodes, simple_topology):
        """
        Test link that contains more than two nodes
        """
        for institution in institutions:
            simple_topology.add_institution(institution)
        for node in nodes:
            node._short_name = 'Test Short Name'
            node.owners.add(institutions[0].id)
            simple_topology.add_node(node)
        simple_topology.primary_owner = institutions[0]
        validator = TopologyValidator()
        validator.validate(topology=simple_topology)
        test_link = Link(
            id='New Link ID',
            name='New Link Name',
            owners=[institutions[0].id],
            nodes=[nodes[0].id, nodes[1].id]
        )
        test_link.nodes.add(nodes[2].id)
        simple_topology.add_link(test_link)
        with pytest.raises(ValueError):
            validator.validate(topology=simple_topology)

    @pytest.mark.parametrize(
        'kwargs',
        [
            {
                'lifetime_start': '03-20T10:10:10',
                'lifetime_end': '03-20T10:10:10',
            },
            {
                'lifetime_start': '03-20-20',
                'lifetime_end': '03-20-22',
            },
            {
                'lifetime_start': '03-20-20T10:20',
                'lifetime_end': '03-20-22T10:20',
            },
            {
                'lifetime_start': '03-20-20T10:20AM',
                'lifetime_end': '03-20-22T10:20PM',
            },
            {
                'lifetime_start': '03-20-2020T10:20:10',
                'lifetime_end': '03-20-22T10:20PM',
            }
        ],
        ids=['no year', 'two digit year', 'no second', 'contains AM/PM', 'only end time error']
    )
    def test_fail_lifetime_with_incorrect_format(self, institutions, nodes, simple_topology, kwargs):
        """
        Test life time with incorrect format will fail
        """
        for institution in institutions:
            simple_topology.add_institution(institution)
        for node in nodes:
            node._short_name = 'Test Short Name'
            node.owners.add(institutions[0].id)
            simple_topology.add_node(node)
        simple_topology.primary_owner = institutions[0].id
        validator = TopologyValidator()
        validator.validate(topology=simple_topology)
        test_link = Link(
            name='New Link Name',
            owners=[institutions[0].id],
            nodes=[nodes[0].id, nodes[1].id],
        )
        for key, value in kwargs.items():
            if key == 'lifetime_start':
                test_link._lifetime_start = value
            if key == 'lifetime_end':
                test_link._lifetime_end = value
        simple_topology.add_link(test_link)
        validator = TopologyValidator()
        errors = validator.validate(topology=simple_topology, raise_error=False)
        for error in errors:
            if 'Lifetime Start' in error:
                assert 'Lifetime Start needs to be in full ISO format' in error
            else:
                assert 'Lifetime End needs to be in full ISO format' in error

    @pytest.mark.parametrize(
        'kwargs',
        [
            (
                {
                    'longitude': 300,
                    'latitude': -90
                }
            ),
            (
                {
                    'longitude': -180,
                    'latitude': 180
                }
            ),
            (
                {
                    'longitude': 180,
                    'latitude': 90,
                    'altitude': 'High'
                }
            ),
            (
                {
                    'longitude': 180,
                    'latitude': 90,
                    'unlocode': 10080
                }
            ),
            (
                {
                    'longitude': 180,
                    'latitude': 90,
                    'address': 45
                }
            ),
        ],
        ids=['longitiude over 180', 'latitude over 90', 'altitude is not float',
             'unlocode is not string', 'address is not string']
    )
    def test_fail_address_with_incorrect_format(self, institution, simple_topology, kwargs):
        """
        Test address with incorrect format will fail
        """
        simple_topology.add_institution(institution)
        simple_topology.primary_owner = institution.id
        test_institution = Institution(
            name='New Test Name',
        )
        for key, value in kwargs.items():
            if key == 'longitude':
                test_institution._longitude = value
            if key == 'latitude':
                test_institution._latitude = value
            if key == 'altitude':
                test_institution._altitude = value
            if key == 'unlocode':
                test_institution._unlocode = value
            if key == 'address':
                test_institution.address = value
        simple_topology.add_institution(test_institution)
        validator = TopologyValidator()
        with pytest.raises(ValueError):
            validator.validate(topology=simple_topology)
