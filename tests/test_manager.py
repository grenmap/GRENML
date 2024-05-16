import pytest
from grenml import managers
from grenml.models import Institution, Node, Link, GLOBAL_INSTITUTION_ID
from grenml.exceptions import *

INSTITUTION_SHORT_NAME = 'TEST'
INSTITUTION_TEST_ID = 'TEST_ID'
INSTITUTION_TEST_NAME = 'TEST_NAME'
INSTITUTION_TEST_ID_2 = 'TEST_ID_2'
INSTITUTION_TEST_NAME_2 = 'TEST_NAME_2'
INSTITUTION_TEST_ID_3 = 'TEST_ID_3'
INSTITUTION_TEST_NAME_3 = 'TEST_NAME_3'
NODE_TEST_ID = 'TEST_NODE_ID'
NODE_TEST_NAME = 'TEST_NAME'
NODE_TEST_ID_2 = 'TEST_NODE_ID_2'
NODE_TEST_NAME_2 = 'TEST_NODE_NAME_2'
LINK_TEST_ID = 'TEST_LINK_ID'
LINK_TEST_NAME = 'TEST_LINK_NAME'
LINK_TEST_ID_2 = 'TEST_LINK_ID_2'
LINK_TEST_NAME_2 = 'TEST_LINK_NAME_2'

INSTITUTION_TYPE_DEFAULT = "Test Institution"


class TestManager:

    @pytest.fixture
    def manager(self):
        return managers.GRENMLManager('TEST_TOPOLOGY')

    @pytest.fixture
    def institution(self):
        return Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT)

    @pytest.fixture
    def institutions(self, institution):
        return [
            institution,
            Institution(INSTITUTION_TEST_ID_2, INSTITUTION_TEST_NAME_2, INSTITUTION_SHORT_NAME,
                        INSTITUTION_TYPE_DEFAULT),
            Institution(INSTITUTION_TEST_ID_3, INSTITUTION_TEST_NAME_3, INSTITUTION_SHORT_NAME,
                        INSTITUTION_TYPE_DEFAULT),
        ]

    @pytest.fixture
    def institution_with_details(self):
        return Institution(INSTITUTION_TEST_ID + '1', INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME,
                           INSTITUTION_TYPE_DEFAULT, 3.3, 3.5, '23',
                           'US', '45 street')

    @pytest.fixture
    def institutions_with_details(self, institution_with_details):
        return [
            institution_with_details,
            Institution(INSTITUTION_TEST_ID_2 + '1', INSTITUTION_TEST_NAME_2, INSTITUTION_SHORT_NAME,
                        INSTITUTION_TYPE_DEFAULT, 0, 0, 0, 'NYC',
                        '55'),
            Institution(INSTITUTION_TEST_ID_3 + '1', INSTITUTION_TEST_NAME_3, INSTITUTION_SHORT_NAME,
                        INSTITUTION_TYPE_DEFAULT),
        ]

    @pytest.fixture
    def node(self, institutions):
        return Node(id=NODE_TEST_ID, name=NODE_TEST_NAME, owners=institutions.copy(), longitude=0, latitude=0)

    @pytest.fixture
    def nodes(self, institutions, node):
        return [
            node,
            Node('TEST_NODE_2', 'TEST_NODE_NAME_2', 'NODE', [institutions[0]], longitude=180, latitude=90),
            Node('TEST_NODE_3', 'TEST_NODE_NAME_3', 'NODE', [institutions[0], institutions[1]], longitude=-180, latitude=-90),
        ]

    @pytest.fixture
    def node_with_details(self, institutions):
        return Node(id=NODE_TEST_ID, name=NODE_TEST_NAME, owners=institutions.copy(), short_name='N1', longitude=90,
                    latitude=-9, altitude=22, unlocode='NY', address='Bank Street', version='2020-02-12T10:43:30+04:00',
                    lifetime_start='2020-03-20T14:30:43', lifetime_end='2020-03-29T14:30:43')

    @pytest.fixture
    def nodes_with_details(self, institutions, node_with_details):
        return [
            node_with_details,
            Node('TEST_NODE_2', 'TEST_NAME', 'NODE2', [institutions[0]], 0, -0.33, 2222, 'CA', 'Queensway',
                 '2020-02-20T14:30:43', '2020-03-29T14:30:43', '2020-02-12T10:43:30+04:00'),
            Node('TEST_NODE_3', 'TEST_NAME', 'NODE3', [institutions[0], institutions[1]], -0.22, 44.33, 12222,
                 'IN', 'Carleton', '2020-02-20T14:30:43', '2020-03-29T14:30:43', '2020-02-12T10:43:30+04:00'),
        ]

    @pytest.fixture
    def link(self, nodes, institutions):
        return Link(id=LINK_TEST_ID, name=LINK_TEST_NAME, owners=institutions, nodes=[nodes[0], nodes[1]])

    @pytest.fixture
    def links(self, nodes, institution, link):
        return [link,
                Link(id=LINK_TEST_ID + '2', name=LINK_TEST_NAME, owners=[institution], nodes=[nodes[1], nodes[2]])]

    @pytest.fixture
    def link_with_all_fields(self):
        return Link(
            id=LINK_TEST_ID,
            name=LINK_TEST_NAME,
            short_name='TEST_LINK_SHORT_NAME',
            nodes=[Node(NODE_TEST_ID, NODE_TEST_NAME), Node(NODE_TEST_ID_2, NODE_TEST_NAME_2)],
            owners=[Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME)],
            lifetime_start='2020-03-20T14:30:43',
            lifetime_end='2020-03-29T14:30:43',
            version='2020-03-20',
        )

    @pytest.fixture
    def links_with_all_fields(self, nodes, institutions, link_with_all_fields):
        return [link_with_all_fields,
                Link(
                    id='LINK_TEST_ID_2',
                    name='LINK_TEST_NAME_2',
                    short_name='TEST_LINK_SHORT_NAME_2',
                    owners=[institutions[1]],
                    nodes=[nodes[1], nodes[2]],
                    lifetime_start='2020-03-21T14:30:43',
                    lifetime_end='2020-03-30T14:30:43',
                    version='2020-02-12T10:43:30+04:00',
                ),
                Link(
                    id='LINK_TEST_ID_3',
                    name='LINK_TEST_NAME_3',
                    short_name='TEST_LINK_SHORT_NAME_3',
                    owners=[institutions[1], institutions[2]],
                    nodes=[nodes[1], nodes[2]],
                    lifetime_start='2020-03-22T14:30:43',
                    lifetime_end='2020-03-31T14:30:43',
                    version='2020-02-24T10:43:30+04:00',
                ),
                ]

    @pytest.mark.parametrize(
        'args, kwargs',
        [
            ([INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME], {}),
            ([], {'id': INSTITUTION_TEST_ID, 'name': INSTITUTION_TEST_NAME}),
            ([], {'name': INSTITUTION_TEST_NAME}),
            ([Institution('ID', 'Name')], {}),
            ([], {}),
            ([INSTITUTION_TEST_ID], {'name': INSTITUTION_TEST_NAME}),
            ([INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, 'other'], {}),
            ([], {'id': INSTITUTION_TEST_ID, 'name': INSTITUTION_TEST_NAME, 'institution_type': 'other'}),
            ([], {'name': INSTITUTION_TEST_NAME, 'institution_type': ['other', 'nren']}),
            ([Institution('ID', 'Name', 'other', 0, 0)], {}),
            ([INSTITUTION_TEST_ID], {'name': INSTITUTION_TEST_NAME, 'longitude': .017e4}),
        ],
        ids=['name and id with args', 'id and name with kwargs', 'kwargs with name', 'args with pre-made institution',
             'empty args and kwargs',
             'args with id and kwargs with name', 'id, name and type with args', 'id, name, and type with kwargs',
             'kwargs with name and type', 'args with premade institution details', 'id, name and longitude',
             ],
    )
    def test_adding_institution(self, manager, args, kwargs):
        manager.add_institution(*args, **kwargs)

    def test_adding_institution_duplicate_id(self, manager):
        with pytest.raises(AttributeIdError):
            manager.add_institution(id=INSTITUTION_TEST_ID)
            manager.add_institution(id=INSTITUTION_TEST_ID, name='', latitude=23, longitude=4, type='ss')

    @pytest.mark.parametrize(
        'lists',
        (
            ([
                [INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT],
                [INSTITUTION_TEST_ID_2, INSTITUTION_TEST_NAME_2, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT],
                [INSTITUTION_TEST_ID_3, INSTITUTION_TEST_NAME_3, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT],
            ]),
            ([
                {'id': INSTITUTION_TEST_ID, 'name': INSTITUTION_TEST_NAME, 'short_name': INSTITUTION_SHORT_NAME,
                 'institution_type': INSTITUTION_TYPE_DEFAULT},
                {'id': INSTITUTION_TEST_ID_2, 'name': INSTITUTION_TEST_NAME_2, 'short_name': INSTITUTION_SHORT_NAME,
                 'institution_type': INSTITUTION_TYPE_DEFAULT},
                {'id': INSTITUTION_TEST_ID_3, 'name': INSTITUTION_TEST_NAME_3, 'short_name': INSTITUTION_SHORT_NAME,
                 'institution_type': INSTITUTION_TYPE_DEFAULT},
            ]),
            ([
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME,
                            INSTITUTION_TYPE_DEFAULT),
                Institution(INSTITUTION_TEST_ID_2, INSTITUTION_TEST_NAME_2, INSTITUTION_SHORT_NAME,
                            INSTITUTION_TYPE_DEFAULT),
                Institution(INSTITUTION_TEST_ID_3, INSTITUTION_TEST_NAME_3, INSTITUTION_SHORT_NAME,
                            INSTITUTION_TYPE_DEFAULT),
            ]),
            ([
                [INSTITUTION_TEST_ID + '1', INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT,
                 3.3, 3.5, '23', 'US',
                 '45 street'],
                {'id': INSTITUTION_TEST_ID_2, 'name': INSTITUTION_TEST_NAME_2, 'short_name': INSTITUTION_SHORT_NAME,
                 'institution_type': INSTITUTION_TYPE_DEFAULT},
                [Institution(INSTITUTION_TEST_ID_3, INSTITUTION_TEST_NAME_3, INSTITUTION_SHORT_NAME,
                             INSTITUTION_TYPE_DEFAULT)],
            ]),
        ),
        ids=['only args', 'only kwargs', 'only institutions', 'mixed args, kwargs, institutions']
    )
    def test_adding_multiple_institutions(self, manager, institutions, lists, institutions_with_details):
        institutions.append(Institution(GLOBAL_INSTITUTION_ID, 'GREN', institution_type='global'))
        institutions += institutions_with_details
        manager.add_institutions(lists)
        assert manager.topology.institutions.issubset(set(institutions))

    def test_manager_id_conflict(self, manager, institution, institution_with_details):
        """
        This test case verifies that manager raises the id conflict when same id is passed.
        This test case takes three parameters:
        (i) manager: calls the manager function which returns the manager object
        (ii) institution: calls the institution function which returns the institution object with name, id and type
        (iii) institution_with_details: calls the institution_with_details function which returns the institution object
                                        with all details
        """
        # Adding institution with add_institution function of manager
        manager.add_institution(institution)
        manager.add_institution(institution_with_details)
        # checking manager raises error, when same id is provided
        with pytest.raises(AttributeIdError):
            manager.add_institution(Institution(INSTITUTION_TEST_ID, 'OTHER NAME', INSTITUTION_TYPE_DEFAULT))
        # checking manager raises error, when same id is provided
        with pytest.raises(AttributeIdError):
            manager.add_institution(
                Institution(INSTITUTION_TEST_ID + '1', 'OTHER NAME', INSTITUTION_TYPE_DEFAULT, 0, 0))

    def test_getting_single_institution(self, manager, institution, institution_with_details):
        """
        This test case checks the functionality of get_institution function of manager.
        This test case takes three parameters:
            (i) manager: calls the manager function which returns the manager object
            (ii) institution: calls the institution function which returns the institution object with name, id and type
            (iii) institution_with_details: calls the institution_with_details function which returns the institution object
                            with all details
        """
        # Adding institution with add_institution function of manager
        manager.add_institution(institution)
        manager.add_institution(institution_with_details)
        # Passing id to get_institution function to get institution
        inst1 = manager.get_institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)
        inst2 = manager.get_institution(id=INSTITUTION_TEST_ID + '1')
        # Verifying institution got is correct
        assert inst1 == institution
        assert inst2 == institution_with_details

    def test_getting_multiple_institutions(self, manager, institution, institutions, institution_with_details,
                                           institutions_with_details):
        """
        This test case checks the functionality of get_institutions function of manager.
        This test case takes five parameters:
            (i) manager: calls the manager function which returns the manager object
            (ii) institution: calls the institution function which returns the institution object with name, id and type
            (iii) institutions: calls the institutions function which returns the list of institutions
            (iv) institution_with_details: calls the institution_with_details function which returns the institution object
                                           with all details
            (v) institutions_with_details: calls the institutions_with_details function which returns the list of
                                           institution with all details
        """
        # Adding all the institution in the institutions by add_institution function of manager
        for inst in institutions:
            manager.add_institution(inst)
        # Adding all the institution in the institutions_with_details by add_institution function of manager
        for inst in institutions_with_details:
            manager.add_institution(inst)
        # Passing id to get_institutions function to get institutions
        insts = manager.get_institutions(id=INSTITUTION_TEST_ID)
        insts1 = manager.get_institutions(id=INSTITUTION_TEST_ID + '1')
        # Verifying institution got is correct
        assert institution in insts
        assert institution_with_details in insts1

        # Passing name to get_institutions function to get institutions
        insts = manager.get_institutions(name=INSTITUTION_TEST_NAME)
        # verifying institutions got are correct
        assert insts in institutions or institutions_with_details

        # Passing type to get_institutions function to get institutions
        insts = manager.get_institutions(type=INSTITUTION_TYPE_DEFAULT)
        # verifying institutions got are correct
        assert insts in institutions or institutions_with_details

        # Passing id and name to get_institutions function to get institutions
        insts = manager.get_institutions(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)
        # verifying institutions got are correct
        assert insts in institutions or institutions_with_details

        # Passing address to get_institutions function to get institutions
        insts = manager.get_institutions(address='45 street')
        # verifying institutions got are correct
        assert insts.issubset(institutions_with_details)

    def test_empty_manager_get_institution(self, manager):
        """
        This test case checks the functionality of get_institution function of manager
        get_institution function raises error when institution not found
        """
        with pytest.raises(InstitutionNotFoundError):
            manager.get_institution(id=INSTITUTION_TEST_ID)

    def test_delete_institution(self, manager, institution, institution_with_details, institutions):
        """
        This test case checks the functionality of delete_institutions function of manager.
        This test case takes four parameters:
            (i) manager: calls the manager function which returns the manager object
            (ii) institution: calls the institution function which returns the institution object with name, id and type
            (iii) institution_with_details: calls the institution_with_details function which returns the institution
                                            with all details
            (iv) ii) institutions: calls the institutions function which returns the list of institution objects
        """
        # adding institution
        manager.add_institution(institution)
        # checking institution is added
        inst = manager.get_institution(id=INSTITUTION_TEST_ID)
        assert inst == institution
        # deleting institution by passing id
        manager.delete_institutions(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)
        # verifying institution is deleted
        with pytest.raises(InstitutionNotFoundError):
            manager.get_institution(id=INSTITUTION_TEST_ID)

        # adding institution
        manager.add_institution(institution_with_details)
        # checking institution is added
        inst = manager.get_institution(name=INSTITUTION_TEST_NAME)
        assert inst == institution_with_details
        # deleting institution by passing name
        manager.delete_institutions(name=INSTITUTION_TEST_NAME)
        # verifying institution is deleted
        with pytest.raises(InstitutionNotFoundError):
            manager.get_institution(name=INSTITUTION_TEST_NAME)

        # adding institution
        manager.add_institutions(institutions)
        # checking institution is added
        inst = manager.get_institutions(type__contains=INSTITUTION_TYPE_DEFAULT)
        assert inst.issuperset(institutions)
        # deleting institution by passing name
        manager.delete_institutions(type__contains=INSTITUTION_TYPE_DEFAULT)
        # verifying institution is deleted
        with pytest.raises(InstitutionNotFoundError):
            manager.get_institution(type__contains=INSTITUTION_TYPE_DEFAULT)

    def test_manager_assigns_primary_owner_with_institution(self, manager, institution, institution_with_details):
        manager.add_institution(institution, primary_owner=True)
        manager.add_institution(institution_with_details, primary_owner=True)
        assert manager.topology.primary_owner == institution_with_details

    def test_manager_assigns_primary_owner_with_values(self, manager):
        manager.add_institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME, type=INSTITUTION_TYPE_DEFAULT,
                                primary_owner=True)
        assert manager.topology.primary_owner == manager.get_institution(id=INSTITUTION_TEST_ID)

    def test_manager_assigns_primary_owner_with_no_value(self, manager, institution):
        manager.add_institution(institution)
        primary_owner_found = manager.topology.primary_owner
        assert primary_owner_found is None

    @pytest.mark.parametrize(
        'args, kwargs',
        (
            ([NODE_TEST_ID, NODE_TEST_NAME], {}),
            ([], {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME}),
            ([NODE_TEST_ID, NODE_TEST_NAME, ],
             {'owners': [INSTITUTION_TEST_ID]}),
            ([NODE_TEST_ID, NODE_TEST_NAME], {'owners': [
                INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3',
            ]}),
            ([NODE_TEST_ID, NODE_TEST_NAME], {'owners': [INSTITUTION_TEST_ID]}),
            ([Node('ID', 'Name')], {}),
            ([], {'name': NODE_TEST_NAME}),
            ([], {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME, 'short_name': 'N1', 'longitude': 90, 'latitude': -9,
                  'altitude': '22', 'unlocode': 'unlocode', 'address': 'address', 'version': '2020-02-24T10:00:00+04:00',
                  'lifetime_start': None, 'lifetime_end': None}),
            ([54, 34, 1212, [Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_TYPE_DEFAULT)],
              32, 43, 43, 44, 5, 33, 312, 33], {}),
            (['', '', '', [Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_TYPE_DEFAULT)],
              22, 43, 43, 44, 5, 33, 312, 33], {}),
        ),
        ids=[
            'values only', 'keywords only', 'with single owner',
            'with multiple owners', 'with owner id as string',
            'premade node', 'without id', 'kwargs with all details', 'args with all details as number',
            'passing empty node_name, node_id, and short_name'
        ]
    )
    def test_manager_add_node_without_primary_owner(self, manager, institutions, args, kwargs):
        manager.add_institutions(institutions)
        manager.add_node(*args, **kwargs)
        assert manager.get_node(**kwargs)

    @pytest.mark.parametrize(
        'args',
        (
            [NODE_TEST_ID, NODE_TEST_NAME, 'NODE', [], 32, -43, 77.78, 'NY', 'Merivale', '2020-03-20T14:30:43', '2020-03-29T14:30:43', '2020-03-20T14:30:43'],
            [NODE_TEST_ID, NODE_TEST_NAME, 'NODE', [
                'TEST_ID_2', 'TEST_ID_3',
            ]],
            [NODE_TEST_ID, NODE_TEST_NAME, 'NODE', [Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME,
                                                                INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT)]]
        ),
        ids=['no owners', 'multiple owners', 'set with primary owner']
    )
    def test_manager_add_node_with_primary_owner(self, manager, institution, institutions, args):
        expected = list(set(args[3] + [institution]))
        manager.add_institution(institution, primary_owner=True)
        manager.add_institutions(institutions[1:])
        manager.add_node(*args)
        node = manager.get_node(id=args[0])
        assert institution in node.owners
        for owner in expected:
            assert owner in node.owners

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'id': NODE_TEST_ID},
            {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME},
            {'owners': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3']},
            {'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
            ]},
            {'name': NODE_TEST_NAME},
            {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME, 'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
            ]},
            {'id__contains': NODE_TEST_ID[4:]},
            {'id__in': [NODE_TEST_ID, 'TEST ID']},
            {'id__in': 'TESTID1{}TESTID2'.format(NODE_TEST_ID)},
            {'owners__contains': INSTITUTION_TEST_ID},
            {'owners__contains': [INSTITUTION_TEST_ID]},
            {'owners__contains': [INSTITUTION_TEST_ID, 'TEST_ID_2']},
            {'owners__in': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3', 'TEST_ID_4']},
        ),
        ids=[
            'id match', 'id and name match', 'owners match with strings',
            'owners match with objects', 'name match', 'all match',
            'id contains', 'id in list', 'id in string', 'owners contains single owner as string',
            'owner contains single owner as list', 'owners contains multiple owner', 'owners in'
        ]
    )
    def test_manager_get_node(self, manager, institutions, node, kwargs):
        manager.add_institutions(institutions)
        manager.add_node(node)
        assert manager.get_node(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'id': NODE_TEST_ID},
            {'short_name': 'N1'},
            {'version': '2020-02-12T10:43:30+04:00'},
            {'longitude': 90},
            {'latitude': -9.0},
            {'altitude': 22.000},
            {'unlocode': 'NY'},
            {'address': 'Bank Street'},
            {'lifetime_start__contains': '2020-03-20T14:30:43'},
            {'lifetime_end__contains': '2020-03-29T14:30:43'},
            {'short_name__in': 'Name_N1'},
            {'short_name__contains': ''},
            {'version__in': ['2020-02-12T10:43:30+04:00', '2020-02-12T20:34:32+04:00']},
            {'version__contains': '2020-02-12'},
            {'unlocode__in': 'ny_NY'},
        ),
        ids=[
            'id match', 'short_name', 'version', 'longitude', 'latitude', 'altitude', 'unlocode', 'address',
            'lifetime start__contains', 'lifetime end__contains', 'short_name__in', 'short_name__contains', 'version__in',
            'version__contains', 'unlocode__in',
        ]
    )
    def test_manager_refine_get_node_optional_attributes(self, manager, institutions_with_details, node_with_details, kwargs):
        manager.add_institutions(institutions_with_details)
        manager.add_node(node_with_details)
        assert manager.get_node(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'owners__contains': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3', 'TEST_ID_4']},
            {'owners__in': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_4']},
            {'invalidname': NODE_TEST_NAME},
            {'owners__contains': []},
            {'owners__in': []},
            {'owners__contains': ['Hhioehise']},
            {'id': INSTITUTION_TEST_ID},
            {'id': NODE_TEST_ID.lower()},
            {'owners__contains': INSTITUTION_TEST_ID.lower()}
        ),
        ids=[
            'owners contains mismatch', 'owners in mismatch',
            'invalid field', 'empty contains', 'empty in', 'no matching owner',
            'id does not use owners id', 'id case sensitive', 'owner case sensitive'
        ]
    )
    def test_manager_get_node_fail(self, manager, institutions, node, kwargs):
        manager.add_institutions(institutions)
        manager.add_node(node)
        with pytest.raises(NodeNotFoundError):
            manager.get_node(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'short_name': 'N1N1'},
            {'version': '2.0'},
            {'longitude': 90.000000001},
            {'latitude': -9.000000000001},
            {'altitude': 22.000000000001},
            {'unlocode': 'ny'},
            {'address': 'BAnk Street'},
            {'lifetime_start': '2020-02-20t14:30:43'},
            {'lifetime_end': '2020-03-29t14:30:43'},
            {'latitude__in': 90}
        ),
        ids=[
            'invalid short_name', 'invalid version', 'invalid longitude', 'invalid latitude', 'invalid altitude',
            'valid unlocode in locode', 'valid address in upper and lower case', 'lifetime start in lowercase',
            'lifetime end in lower case', 'valid lat using latitude__in'
        ]
    )
    def test_manager_refine_get_node_fail_with_optional_attribute(
            self, manager, institutions_with_details, node_with_details, kwargs):
        """
        This test cases passes when node does not found.
        """
        manager.add_institutions(institutions_with_details)
        manager.add_node(node_with_details)
        with pytest.raises(NodeNotFoundError):
            manager.get_node(**kwargs)

    @pytest.mark.parametrize(
        'kwargs, expected_ids',
        (
            ({'id': NODE_TEST_ID}, [NODE_TEST_ID]),
            ({'owners__contains': INSTITUTION_TEST_ID}, [NODE_TEST_ID, 'TEST_NODE_2', 'TEST_NODE_3']),
            ({'owners__contains': [INSTITUTION_TEST_ID, 'TEST_ID_2']}, [NODE_TEST_ID, 'TEST_NODE_3'])
        ),
        ids=['by id return single', 'by owner return multiple', 'by multiple owner return multiple']
    )
    def test_manager_get_multiple_nodes(self, manager, institutions, nodes, kwargs, expected_ids):
        manager.add_institutions(institutions)
        manager.add_nodes(nodes)
        received_nodes = manager.get_nodes(**kwargs)
        for node in received_nodes:
            assert node.id in expected_ids

    @pytest.mark.parametrize(
        'kwargs, expected_ids',
        (
            ({'short_name': 'N1'}, [NODE_TEST_ID]),
            ({'address': 'Carleton'}, ['TEST_NODE_3']),
            ({'owners__contains': [INSTITUTION_TEST_ID, 'TEST_ID_2']}, [NODE_TEST_ID, 'TEST_NODE_3']),
            ({'short_name__contains': 'N'}, [NODE_TEST_ID, 'TEST_NODE_3', 'TEST_NODE_2']),
        ),
        ids=['by short_name', 'by address', 'by multiple owner return multiple', 'by short_name__contains', ]
    )
    def test_manager_refine_get_multiple_nodes(
            self, manager, institutions, nodes_with_details, kwargs, expected_ids):
        manager.add_institutions(institutions)
        manager.add_nodes(nodes_with_details)
        received_nodes = manager.get_nodes(**kwargs)
        for node in received_nodes:
            assert node.id in expected_ids

    def test_manager_add_owner_to_node(self, manager, institutions):
        manager.add_institutions(institutions)
        manager.add_node(NODE_TEST_ID, NODE_TEST_NAME)
        node = manager.get_node(id=NODE_TEST_ID)
        assert node.owners == set()
        manager.add_owner_to_node(INSTITUTION_TEST_ID, NODE_TEST_ID)
        assert node.owners != set()

    def test_manager_remove_owner_from_node(self, manager, institutions, node):
        manager.add_institutions(institutions)
        manager.add_node(node)
        assert node.owners == set(institutions)
        manager.remove_owner_from_node(institutions[0].id, node.id)
        assert node.owners != set(institutions)

    def test_manager_delete_node(self, manager, institutions, node):
        manager.add_institutions(institutions)
        manager.add_node(node)
        manager.delete_nodes(id=NODE_TEST_ID)
        with pytest.raises(NodeNotFoundError):
            manager.get_node(id=NODE_TEST_ID)

    def test_manager_refine_delete_nodes(self, manager, institutions, nodes_with_details):
        """
        This test delete multiple nodes at a time
        """
        manager.add_institutions(institutions)
        nodes_added = manager.add_nodes(nodes_with_details)
        assert nodes_added == nodes_with_details
        # deleting node with optional attribute
        manager.delete_nodes(short_name='N1')
        # checking node is deleted
        with pytest.raises(NodeNotFoundError):
            manager.get_node(id=NODE_TEST_ID)
        assert manager.get_nodes().issubset(nodes_with_details)
        # deleting multiple nodes
        manager.delete_nodes(name=NODE_TEST_NAME)
        with pytest.raises(NodeNotFoundError):
            manager.get_node(name=NODE_TEST_NAME)
        assert manager.get_nodes() is None

    @pytest.mark.parametrize(
        'args, kwargs',
        (
            ([LINK_TEST_ID, LINK_TEST_NAME, [INSTITUTION_TEST_ID], [NODE_TEST_ID, 'TEST_NODE_2']], {}),
            ([
                LINK_TEST_ID, LINK_TEST_NAME,
                [Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME)],
                [
                    Node(id=NODE_TEST_ID, name=NODE_TEST_NAME, owners=[
                        Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME),
                        Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2),
                        Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3),
                    ]),
                    Node('TEST_NODE_2', 'TEST_NODE_NAME_2',
                         [Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)])]
            ], {}),
            ([], {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME, 'owners': [INSTITUTION_TEST_ID],
                  'nodes': [NODE_TEST_ID, 'TEST_NODE_2']}),
            ([], {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME, 'nodes': [NODE_TEST_ID, 'TEST_NODE_2']}),
            ([], {'name': LINK_TEST_NAME, 'owners': [INSTITUTION_TEST_ID], 'nodes': [NODE_TEST_ID, 'TEST_NODE_2']}),
            ([Link(LINK_TEST_ID, LINK_TEST_NAME,
                   [Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)],
                   [
                       Node(id=NODE_TEST_ID, name=NODE_TEST_NAME, owners=[
                           Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME),
                           Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2),
                           Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3),
                       ]),
                       Node('TEST_NODE_2', 'TEST_NODE_NAME_2',
                            [Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)])
                   ]
                   ),
              ], {}),
            ([
                Link(name=LINK_TEST_NAME,
                     nodes=[Node(id='TEST_NODE_2', name='TEST_NODE_NAME_2',
                                 owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)]),
                            Node(id=NODE_TEST_ID, name=NODE_TEST_NAME,
                                 owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME),
                                         Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2),
                                         Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3)])]
                     ),
                Link(name=LINK_TEST_NAME,
                     nodes=[Node(id='TEST_NODE_3', name='TEST_NODE_NAME_3',
                                 owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME),
                                         Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2)]),
                            Node(id=NODE_TEST_ID, name=NODE_TEST_NAME,
                                 owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME),
                                         Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2),
                                         Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3), ])]
                     ),
                Link(name=LINK_TEST_NAME,
                     nodes=[Node(id='TEST_NODE_2', name='TEST_NODE_NAME_2',
                                 owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)]),
                            Node(id='TEST_NODE_2', name='TEST_NODE_NAME_2',
                                 owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)])]
                     ),
            ], {}),
        ),
        ids=[
            'args only with node and inst IDs', 'args only with node and inst objects', 'kwargs only',
            'no owners', 'no ID', 'premade link', 'args with list of links',
        ]
    )
    def test_manager_create_link_success(self, manager, institutions, nodes, args, kwargs):
        """
            This test checks the functionality of managers class. This test passes when managers class successfully
            adds the links. Here, we are passing Links to add_link managers function using args and kwargs.
            In args we are passing positional arguments and in kwargs we are passing keyword arguments
            We use almost every possible combination to create the link successfully.
        """
        manager.add_institutions(institutions)
        manager.add_nodes(nodes)
        manager.add_link(*args, **kwargs)
        link_found = manager.get_links(name=LINK_TEST_NAME)
        if link_found is None:
            pytest.fail('Link not found by using manager.get_links')

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'id': LINK_TEST_ID},
            {'name': LINK_TEST_NAME},
            {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME},
            {'owners': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3']},
            {'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
            ]},
            {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME, 'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
            ]},
            {'name': LINK_TEST_NAME[0:len(LINK_TEST_NAME)]},
            {'nodes': [NODE_TEST_ID, 'TEST_NODE_2']},
            {'id': LINK_TEST_ID, 'name': LINK_TEST_NAME, 'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_2', 'TEST_NAME_2', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT),
                Institution('TEST_ID_3', 'TEST_NAME_3', INSTITUTION_SHORT_NAME, INSTITUTION_TYPE_DEFAULT)],
             'nodes': [NODE_TEST_ID, 'TEST_NODE_2']
             },
            {'nodes': [Node(id=NODE_TEST_ID, name=NODE_TEST_NAME,
                            owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                                    Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                                    Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)],
                            latitude=0,
                            longitude=0,
                            ),
                       Node(id='TEST_NODE_2', name='TEST_NODE_NAME_2',
                            owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)],
                            longitude=180,
                            latitude=90
                            )]
             },
            {'id__contains': LINK_TEST_ID[4:]},
            {'id__contains': LINK_TEST_ID},
            {'id__contains': 'TEST'},
            {'id__in': LINK_TEST_ID},
            {'id__in': [LINK_TEST_ID, '1223', 'test']},
            {'id__in': '232' + LINK_TEST_ID + '123'},
            {'id__in': 'TESTID1{}TESTID2'.format(LINK_TEST_ID)},
            {'owners__contains': INSTITUTION_TEST_ID},
            {'owners__contains': [INSTITUTION_TEST_ID]},
            {'owners__contains': [INSTITUTION_TEST_ID, 'TEST_ID_2']},
            {'owners__contains': [INSTITUTION_TEST_ID, INSTITUTION_TEST_ID_3, INSTITUTION_TEST_ID_2]},
            {'owners__contains': [INSTITUTION_TEST_ID, INSTITUTION_TEST_ID, INSTITUTION_TEST_ID]},
            {'owners__in': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3', 'TEST_ID_4']},
            {'owners__in': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3']},
            {'nodes__in': [Node(id=NODE_TEST_ID, name=NODE_TEST_NAME,
                                owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                                        Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                                        Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)],
                                latitude=0,
                                longitude=0,
                                ),
                           Node(id='TEST_NODE_2', name='TEST_NODE_NAME_2',
                                owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)],
                                longitude=180,
                                latitude=90
                                )]
             },
            {'nodes__in': [NODE_TEST_ID, 'TEST_NODE_2']},
            {'nodes__in': [NODE_TEST_ID, 'TEST_NODE_2', 'TEST_NODE_3']},
            {'nodes__contains': [
                Node(
                    id=NODE_TEST_ID,
                    name=NODE_TEST_NAME,
                    owners=[Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                            Institution(id=INSTITUTION_TEST_ID_2, name=INSTITUTION_TEST_NAME_2, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT),
                            Institution(id=INSTITUTION_TEST_ID_3, name=INSTITUTION_TEST_NAME_3, short_name=INSTITUTION_SHORT_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)],
                    latitude=0,
                    longitude=0,
                ),
                Node(
                    id='TEST_NODE_2',
                    name='TEST_NODE_NAME_2',
                    owners=[Institution(
                        id=INSTITUTION_TEST_ID,
                        name=INSTITUTION_TEST_NAME,
                        short_name=INSTITUTION_SHORT_NAME,
                        institution_type=INSTITUTION_TYPE_DEFAULT
                    )],
                    longitude=180,
                    latitude=90
                )]
             },
            {'nodes__contains': [NODE_TEST_ID]},
            {'nodes__contains': [NODE_TEST_ID, 'TEST_NODE_2']},
        ),
        ids=[
            'id: link_id', 'id: link_name', 'link_id and link_name', 'owners as a list of strings',
            'owners as a list of objects', 'id name and owners', 'name slice function', 'two valid node_ids', 'all',
            'nodes as a list of objects', 'id__contains: slice_func', 'id__contains: link_id',
            'id__contains: substring',
            'id__in: link_id', 'id__in: list of strings', 'id__in: string_pattern', 'id__in: format function',
            'owners__contains: institution_id', 'owners__contains: list of a string',
            'owners_contains: list of strings',
            'owners__contains: all owners', 'owners__contains: list of same owners', 'owners__in: list of strings',
            'owners__in: all owners', 'nodes__in: list of node objects', 'nodes__in: list of 2 nodes',
            'nodes__in: list of 3 nodes', 'node__contains: list of node objects', 'node__contains: node_id',
            'nodes__contains: list of node strings'
        ]
    )
    def test_manager_get_link_and_links(self, manager, institutions, nodes, link, links, kwargs):
        """
            This test checks the functionality of managers class. This test passes when managers returns the link or
            links that we are looking for. Here, we are passing different values to get_link and get_links functions of
            managers class using kwargs.
            In kwargs we are passing keyword arguments.
            We use almost every possible combination to get link using managers class.
        """
        manager.add_institutions(institutions)
        manager.add_nodes(nodes)
        manager.add_link(link)
        link_found = manager.get_link(**kwargs)
        # checking link is in the topology
        if link_found is None:
            pytest.fail('Link not found by using manager.get_link')
        # Deleting the link
        manager.delete_links(id=link.id)
        # checking link are deleted
        with pytest.raises(LinkNotFoundError):
            manager.get_link(**kwargs)
        # adding links to the topology
        manager.add_links(links)
        # checking the links are in the topology
        link_found = manager.get_links(**kwargs)
        if link_found is None:
            pytest.fail('Link not found by using manager.get_links')

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
            {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME},
            {'id': INSTITUTION_TEST_ID, 'name': INSTITUTION_TEST_NAME_2},
            {'id': LINK_TEST_ID, 'name': NODE_TEST_NAME},
            {'owners': [' ']},
            {'owners': [1232, INSTITUTION_TEST_ID]},
            {'id': NODE_TEST_ID, 'name': NODE_TEST_NAME, 'owners': [
                Institution(INSTITUTION_TEST_ID, INSTITUTION_TEST_NAME),
                Institution('TEST_ID_2', 'TEST_NAME_2'),
                Institution('TEST_ID_3', 'TEST_NAME_3'),
            ]},
            {'id': LINK_TEST_ID[2:7]},
            {'name': LINK_TEST_NAME[0:len(LINK_TEST_NAME) - 3]},
            {'owners': [INSTITUTION_TEST_ID[0:6]]},
            {'owners': [INSTITUTION_TEST_ID]},
            {'owners': [INSTITUTION_TEST_ID, INSTITUTION_TEST_ID_2]},
            {'owners': [INSTITUTION_TEST_ID, INSTITUTION_TEST_ID_2, 'garbage_value']},
            {'nodes': [' ']},
            {'nodes': [NODE_TEST_ID]},
            {'nodes': ['TEST_NODE_2', 'TEST_NODE_3']},
            {'nodes': [NODE_TEST_ID, 'TEST_NODE_3', 'TEST_NODE_2']},
            {'nodes': [NODE_TEST_ID[0:4], 'TEST_NODE_2'[2:7]]},
            {'nodes': [Node('TEST_NODE_2', 'TEST_NODE_NAME_2',
                            [Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)]),
                       Node('TEST_NODE_2', 'TEST_NODE_NAME_2',
                            [Institution(id=INSTITUTION_TEST_ID, name=INSTITUTION_TEST_NAME)])]
             },
            {'id__contains': ' '},
            {'id__contains': INSTITUTION_TEST_ID},
            {'id__contains': NODE_TEST_ID},
            {'id__contains': [LINK_TEST_ID, '1223', 'test']},
            {'id__contains': LINK_TEST_NAME},
            {'id__in': LINK_TEST_ID[4:]},
            {'id__in': ' '},
            {'id__in': LINK_TEST_ID.lower()},
            {'id__in': INSTITUTION_TEST_ID},
            {'id__in': NODE_TEST_ID},
            {'id__in': LINK_TEST_NAME},
            {'id__in': 'TEST'},
            {'owners__contains': [INSTITUTION_TEST_ID[2:]]},
            {'owners__contains': ' '},
            {'owners__contains': LINK_TEST_ID},
            {'owners__contains': NODE_TEST_ID},
            {'owners__contains': [INSTITUTION_TEST_ID, 'TEST_ID_2', 'TEST_ID_3', 'TEST_ID_4']},
            {'owners__contains': INSTITUTION_TEST_NAME},
            {'owners__contains': '123' + INSTITUTION_TEST_ID + '233'},
            {'owners__contains': 'TEST'},
            {'owners': 'TEST'},
            {'owners__in': [INSTITUTION_TEST_ID[2:]]},
            {'owners__in': ' '},
            {'owners__in': LINK_TEST_ID},
            {'owners__in': NODE_TEST_ID},
            {'owners__in': INSTITUTION_TEST_NAME},
            {'owners__in': '123' + INSTITUTION_TEST_ID + '233'},
            {'owners__in': 'TEST'},
            {'owners__in': INSTITUTION_TEST_ID_2},
            {'owners__in': [INSTITUTION_TEST_ID_3]},
            {'nodes__contains': [' ']},
            {'nodes__contains': [LINK_TEST_ID]},
            {'nodes__contains': [NODE_TEST_ID, 'TEST_NODE_2', 'TEST_NODE_3']},
            {'nodes__contains': [NODE_TEST_ID[2:]]},
            {'nodes__contains': [NODE_TEST_NAME]},
            {'nodes__contains': 'TEST'},
            {'nodes__contains': '1234' + NODE_TEST_ID + '122' + 'TEST_NODE_2' + '12'},
            {'nodes__in': [' ']},
            {'nodes__in': [LINK_TEST_ID]},
            {'nodes__in': [NODE_TEST_ID]},
            {'nodes__in': [NODE_TEST_ID[2:]]},
            {'nodes__in': [NODE_TEST_NAME]},
            {'nodes__in': 'TEST'},
            {'nodes__in': '1234' + NODE_TEST_ID + '122' + 'TEST_NODE_2' + '12'},
            {'link__contains': LINK_TEST_ID},
            {'invalid_name': NODE_TEST_NAME},
        ),
        ids=[
            'empty id', 'id: garbage_value', 'id: node_id', 'id: institution_id', 'name empty', 'name: node_name',
            'name: institution_name', 'name: garbage value', 'node_id and node_name', 'id: owner_id, name: owner_name',
            'id: link_id and name: node_name', 'owners empty', 'owners: random value', 'node_id, name and valid owners',
            'id: slice_function', 'name: slice function', 'owners: slicing', 'one valid owner out of three owners',
            'two valid owners out of 3', 'one invalid and two valid owners', 'empty node', 'only one valid node_id',
            'one valid and one invalid node_id', 'Three nodes', 'nodes slicing', 'same nodes', 'id__contains: empty',
            'id__contains: institution_id', 'id_contains: node_id', 'id_contains: list of strings',
            'id_contains: link_name', 'id__in: slice_function', 'id__in: empty', 'id__in: link_id with lower function',
            'id__in: institution_id', 'id__in: node_id', 'id__in: link_name', 'id__in: substring',
            'owners__contains: slice_function', 'owners__contains: empty', 'owners__contains: link_id',
            'owners__contains: node_id', 'owners__contains: list of strings', 'owners__contains: institution_name',
            'owners__contains: string pattern', 'owners__contains: substring', 'owners with substring',
            'owners__in: slice function', 'owners__in: empty', 'owners__in: link_id', 'owners__in: node_id',
            'owners_in: institution_name', 'owners_in: with required string in between using concatenation operator',
            'owners__in: substring', 'owners__in: string', 'owners__in: list of a string', 'node__contains: empty',
            'node__contains: link_id', 'node__contains: list of 3 nodes', 'node__contains: slice_function',
            'node__contains: node_name', 'node__contains: substring', 'node__contains: string_pattern',
            'node_in: empty',
            'node__in: link_id', 'node__in: node_id', 'node__in: slice_function', 'node__in: node_name',
            'node__in: substring', 'node__in: string_pattern', 'link__contains: link_id', 'invalid_name'
        ]
    )
    def test_manager_get_link_fail(self, manager, institutions, nodes, link, kwargs):
        """
            This test checks the functionality of managers class. This test passes when managers raises error while
            returning the link that we are looking for. Here, we are passing different values to get_link functions of
            managers class using kwargs.
            In kwargs we are passing keyword arguments.
            We use almost every possible combination which raises error while getting link using managers class.
        """
        manager.add_institutions(institutions)
        manager.add_nodes(nodes)
        manager.add_links([link])
        with pytest.raises(LinkNotFoundError):
            manager.get_link(**kwargs)

    def test_manager_get_link_with_optional_fields(self, manager, links_with_all_fields):
        """
        Test getting link with optional fields
        """
        manager.add_links(links_with_all_fields)
        assert manager.get_link(id=LINK_TEST_ID) == manager.get_link(short_name='TEST_LINK_SHORT_NAME')
        assert manager.get_link(id='LINK_TEST_ID_2') == manager.get_link(version__contains='2020-02-12')

    @pytest.mark.parametrize(
        'kwargs',
        (
            {'nodes': ['TEST_NODE_2', 'TEST_NODE_3']},
        ),
        ids=[
            'nodes as list of strings',
        ]
    )
    def test_manager_get_links(self, manager, institutions, nodes, links, kwargs):
        manager.add_institutions(institutions)
        manager.add_nodes(nodes)
        manager.add_links(links)
        link_found = manager.get_links(**kwargs)
        if link_found is None:
            pytest.fail('Link not found by using manager.get_links')

    def test_manager_add_owner_to_link(self, manager, institutions, nodes):
        manager.add_institutions(institutions)
        manager.add_nodes(nodes)
        manager.add_link(id=LINK_TEST_ID, name=LINK_TEST_NAME, nodes=[nodes[0], nodes[1]])
        link_found = manager.get_link(id=LINK_TEST_ID)
        assert link_found.owners == set()
        manager.add_owner_to_link(INSTITUTION_TEST_ID, LINK_TEST_ID)
        assert link_found.owners != set()

    def test_manager_remove_owner_from_link(self, manager, institutions, nodes, link):
        manager.add_institutions(institutions)
        manager.add_nodes(nodes)
        manager.add_link(link)
        assert link.owners == set(institutions)
        manager.remove_owner_from_link(institutions[0].id, link.id)
        assert link.owners != set(institutions)

    def test_manager_delete_link(self, manager, institutions, nodes, link):
        manager.add_institutions(institutions)
        manager.add_nodes(nodes)
        manager.add_link(link)
        manager.delete_links(id=LINK_TEST_ID)
        with pytest.raises(NodeNotFoundError):
            manager.get_node(id=LINK_TEST_ID)

    def test_manager_delete_link_with_optional_fields(self, manager, links_with_all_fields):
        """
        Test deleting link with optional fields
        """
        links_added = manager.add_links(links_with_all_fields)
        assert links_added == links_with_all_fields
        # deleting link with optional attribute and check link deleted
        manager.delete_links(short_name='TEST_LINK_SHORT_NAME')
        with pytest.raises(LinkNotFoundError):
            manager.get_link(id=LINK_TEST_ID)
        manager.delete_links(version__contains='2020-02-24')
        with pytest.raises(LinkNotFoundError):
            manager.get_link(id='LINK_TEST_ID_3')

    def test_manager_successful_validation_with_default_objects(self, manager, institutions, nodes, links):
        manager.add_institutions(institutions)
        manager.set_primary_owner(INSTITUTION_TEST_ID)
        manager.add_nodes(nodes)
        manager.add_links(links)
        manager.validate()
