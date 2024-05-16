import pytest
from grenml.models import Institution, Node, Link, meta

TEST_LINK_ID = 'TEST_LINK_ID1'
TEST_LINK_NAME = 'TEST_LINK_NAME1'
TEST_NODE_ID1 = 'TEST_NODE_ID1'
TEST_NODE_NAME1 = 'TEST_NODE_NAME1'
TEST_NODE_ID2 = 'TEST_NODE_ID2'
TEST_NODE_NAME2 = 'TEST_NODE_NAME2'
TEST_INSTITUTION_ID1 = 'TEST_ID1'
TEST_INSTITUTION_NAME1 = 'TEST_NAME1'
TEST_INSTITUTION_ID2 = 'TEST_ID2'
TEST_INSTITUTION_NAME2 = 'TEST_NAME2'


class TestLinks:

    @pytest.fixture
    def institution(self):
        return [Institution(id=TEST_INSTITUTION_ID1, name=TEST_INSTITUTION_NAME1)]

    @pytest.fixture
    def institutions(self, institution):
        return [
            institution[0],
            Institution(id=TEST_INSTITUTION_ID2, name=TEST_INSTITUTION_NAME2),
        ]

    @pytest.fixture
    def node1(self):
        return Node(TEST_NODE_ID1, TEST_NODE_NAME1)

    @pytest.fixture
    def node2(self):
        return Node(TEST_NODE_ID2, TEST_NODE_NAME2)

    @pytest.fixture
    def link(self):
        return Link(
            id=TEST_LINK_ID,
            name=TEST_LINK_NAME,
            nodes=[Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
            owners=[Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]
        )

    @pytest.fixture
    def link_many_owners(self):
        return Link(
            id=TEST_LINK_ID,
            name=TEST_LINK_NAME,
            nodes=[Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
            owners=[Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                    Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2)]
        )

    @pytest.fixture
    def link_with_all_fields(self):
        return Link(
            id=TEST_LINK_ID,
            name=TEST_LINK_NAME,
            short_name='TEST_LINK_SHORT_NAME',
            nodes=[Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
            owners=[Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                    Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2)],
            lifetime_start='2020-03-20T14:30:43',
            lifetime_end='2020-03-29T14:30:43',
            version='2020-03-20',
        )

    @pytest.mark.parametrize(
        'args, kwargs',
        (
            (
                [],
                {
                    'name': TEST_LINK_NAME,
                    'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)]
                }
            ),
            (
                [],
                {
                    'name': TEST_LINK_NAME,
                    'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
                    'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]
                }
            ),
            (
                [],
                {
                    'name': TEST_LINK_NAME,
                    'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
                    'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                               Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2)]
                }
            ),
            (
                [],
                {
                    'id': TEST_LINK_ID,
                    'name': TEST_LINK_NAME,
                    'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
                    'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                               Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2)]
                }
            ),
            (
                [],
                {
                    'id': '',
                    'name': TEST_LINK_NAME,
                    'owners': '',
                    'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)]
                }
            ),
            (
                [
                    TEST_LINK_ID,
                    TEST_LINK_NAME,
                    [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)],
                    [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID1, TEST_NODE_NAME1)]
                ],
                {}
            ),
            (
                [
                    TEST_NODE_NAME1,
                    TEST_NODE_NAME1,
                    None,
                    [Institution(TEST_NODE_NAME1, TEST_NODE_NAME1)],
                    [Node(TEST_NODE_NAME1, TEST_NODE_NAME1), Node(TEST_NODE_NAME1, TEST_NODE_NAME1)]
                ],
                {}
            ),
            (
                [
                    TEST_LINK_ID,
                    TEST_LINK_NAME,
                    'short_name',
                    [Institution(TEST_NODE_NAME1, TEST_NODE_NAME1),
                     Institution(TEST_NODE_NAME1, TEST_NODE_NAME1)]
                ],
                {'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)]}
            ),
            (
                [
                    TEST_LINK_ID,
                    TEST_LINK_NAME,
                ],
                {
                    'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
                    'owners': [Institution(TEST_NODE_NAME1, TEST_NODE_NAME1),
                               Institution(TEST_NODE_NAME1, TEST_NODE_NAME1)]
                }
            ),
            (
                [
                    TEST_LINK_ID,
                ],
                {
                    'name': TEST_LINK_NAME,
                    'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
                    'owners': [Institution(TEST_NODE_NAME1, TEST_NODE_NAME1),
                               Institution(TEST_NODE_NAME1, TEST_NODE_NAME1)]
                }
            ),
            (
                [
                    TEST_LINK_ID,
                ],
                {
                    'name': ' TestLink',
                    'nodes': [Node('N1', 'NN', [Institution('I1', 'IN1')]),
                              Node('N1', 'NN', [Institution('I1', 'IN1')])],
                    'owners': [Institution(TEST_NODE_NAME1, TEST_NODE_NAME1),
                               Institution(TEST_NODE_NAME1, TEST_NODE_NAME1)]
                }
            ),
            (
                ['', ],
                {
                    'name': ' TestLink',
                    'nodes': [Node('N1', 'NN', [Institution('I1', 'IN1')]),
                              Node('N1', 'NN', [Institution('I1', 'IN1')])],
                    'owners': [Institution('I1', 'IN1'), Institution('I1', 'IN1')]
                }
            ),
            (
                [123, 'name', 'name', [Institution('I1', 'IN1'), Institution('I1', 'IN1')],
                 [Node('N1', 'NN', [Institution('I1', 'IN1')]), Node('N1', 'NN', [Institution('I1', 'IN1')])]],
                {},
            ),
            (
                [123, 12345, 'name', [Institution('I1', 'IN1'), Institution('I1', 'IN1')],
                 [Node('N1', 'NN', [Institution('I1', 'IN1')]), Node('N1', 'NN', [Institution('I1', 'IN1')])]],
                {},
            ),
            (
                [],
                {'id': 12345, 'name': 1222, 'nodes': [Node('N1', 'NN'), Node('N1', 'NN')], 'owners': ''},
            ),
            (
                ['', TEST_LINK_NAME, '', [Node('', 'N1'), Node('', 'N1')]],
                {},
            ),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'short_name': 'TEST_LINK_SHORT_NAME'}),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'version': '2020-03-20'}),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME,
                  'lifeime_start': '2020-03-20T14:30:43', 'lifetime_end': '2020-03-29T14:30:43'
                  }),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'lifetime_start': '2020-03-20T14:30:43'}),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'lifetime_end': '2020-03-20T14:30:43'}),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'lifetime_start': '2020-03-20T14:30:43-05:00'}),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'lifetime_start': '2020-03-20T14:30:43.999999'}),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'lifetime_start': '2020-03-20T14:30:43.999999+05:00'}),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'lifetime_start': '2020-03-20'}),
            ([], {'id': TEST_LINK_ID, 'name': TEST_LINK_NAME, 'lifetime_start': '2020-03-20T14:30:43Z'}),
        ),
        ids=['kwargs: name and nodes', 'kwargs: name, nodes and a owner', 'kwargs: name, nodes and owners',
             'kwargs: all details', 'kwargs: name, node and rest empty', 'args: all details',
             'args: same details', 'kwargs: nodes and rest in args', 'args: name, id and kwargs: rest',
             'args: id and kwargs: rest', 'args: id and kwargs: links and nodes has different owners',
             'args: empty and kwargs: links and nodes has same owners', 'args: all details but id as int',
             'args: all details but id and name as number', 'kwargs: nodes, owners empty, and name and id as number',
             'args: nodes, name but without id and owners', 'link with short name', 'link with version',
             'link with life time start and end', 'link with only life time start', 'link with life time end',
             'link life time with IOS time zone', 'link life time with microsecond',
             'link life time ISO timezone and microsecond', 'link life time only date', 'link lifetime UTC']
    )
    def test_creating_links(self, args, kwargs):
        """
            This test checks the successful creation of links by passing different values to args and kwargs
            In args we are passing positional arguments and in kwargs we are passing keyword arguments
            Each test case has unique id.
            for example: 'kwargs: name and nodes'
            This id represents that we are passing name and nodes only using kwargs and link creation is successful
            We use almost every possible combination to create the link successfully.
        """
        link = Link(*args, **kwargs)
        assert link.name

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'id': TEST_LINK_ID}),
            ({'name': TEST_LINK_NAME}),
            ({'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)]}),
            ({'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2),
                        Node(TEST_NODE_ID2, TEST_NODE_NAME2)]}),
            ({'id': TEST_LINK_ID,
              'name': TEST_LINK_NAME,
              'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
              'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({'id': TEST_LINK_ID, 'name': TEST_LINK_NAME}),
            ({'id': TEST_LINK_ID, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({
                'id': TEST_LINK_ID,
                'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)]
            }),
            ({'id__in': TEST_LINK_ID}),
            ({'id__in': [TEST_LINK_ID, TEST_NODE_ID1, TEST_NODE_ID2]}),
            ({'id__in': 'TEST_LINK_ID123'}),
            ({'id__in': TEST_LINK_ID + '123'}),
            ({'id__in': '123_TEST_LINK_ID1_123_TEST_NODE_ID_123_TEST_NODE_ID'}),
            ({'id__contains': TEST_LINK_ID}),
            ({'id__contains': 'TEST_LINK'}),
            ({'id__contains': 'TEST_LINK_I'}),
            ({'id__contains': ''}),
            ({'id__contains': '123_TEST_LINK_ID1_123_TEST_NODE_ID_123_TEST_NODE_ID'[4:9]}),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                             Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2),
                             Institution('TEST_INSTITUTION_ID1', 'TEST_INSTITUTION_NAME1')]}),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                             Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                             Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({'owners__in': [TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME2, TEST_INSTITUTION_ID2]}),
            ({'owners__in': [TEST_INSTITUTION_ID1]}),
            ({'owners__in': ['TEST_ID1']}),
            ({
                'id__in': TEST_LINK_ID,
                'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                               Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2),
                               Institution('TEST_INSTITUTION_ID3', 'TEST_INSTITUTION_NAME3')]
            }),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                                   Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                                   Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)],
              }),

            ({'owners__contains': TEST_INSTITUTION_ID1}),
            ({'nodes__in': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)]}),
            ({'nodes__in': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2),
                            Node('TEST_NODE', 'TESTNODENAME')]}),
            ({'nodes__contains': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)]}),
            ({'nodes__contains': [Node(TEST_NODE_ID1, TEST_NODE_NAME1)]}),
            ({'nodes__contains': TEST_NODE_ID1}),
        ),
        ids=['id only', 'link name only', 'owners only', 'nodes only', 'one node repeating', 'all details',
             'id and name', 'id and owners', 'id and nodes', 'id__in with link_id', 'id__in with list of strings',
             'id__in with required string to the left', 'id__in with required string to the left using concat. operator',
             'id__in with required string in between', 'id__contains with link_id', 'id__contains with substring',
             'id__contains with small substring', 'id__contains with empty', 'id__contains with slice function',
             'owners__in with a owner', 'owners__in with owners one repeating', 'owners__in with same owners',
             'owners__in with a list of strings', 'owners__in with list of a string variable',
             'owners__in with list of a string literal', 'owners__in and id__in',
             'owners__contains a owner', 'owners__contains same owners', 'owners__contains institution_id',
             'nodes__in list of nodes', 'nodes__in with list of different nodes', 'nodes_contains list of nodes',
             'nodes__contains list of a node', 'nodes__contains node_id', ],
    )
    def test_link_match_success(self, link, kwargs):
        """
            This test checks the functionality of match function of the link. In this test, we have passed different
            values to the attributes of the link which makes the match pass. We are passing values using kwargs.
            In kwargs, we are passing keyword arguments
            Each test case has unique id.
            for example: 'id only'
            This id represents that we have passed only id to the match function.
            # We are not using args and kwargs. Because this function use kwargs only
            We use almost every possible combination which pass the match function of the link.
        """
        assert link.match(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1)]}),
            ({'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2),
                        Node('TEST_NODE_ID4', 'TEST_NODE_NAME4')]}),
            ({'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID1, TEST_NODE_NAME1)]}),
            ({'id': '  '}),
            ({'name': ' '}),
            ({'owners': ' '}),
            ({'nodes': ' '}),
            ({'id': TEST_LINK_ID,
              'name': TEST_LINK_NAME,
              'nodes': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2)],
              'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                         Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2)]}),
            ({'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                         Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2)]}),
            ({'name': 'TEST_LINK_NAmE1'}),
            ({'id__in': [Node(TEST_NODE_ID1, TEST_NODE_NAME1)]}),
            ({'id__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({'id__in': TEST_LINK_NAME}),
            ({'id__in': ''}),
            ({'id__in': TEST_LINK_ID[4:0]}),
            ({'id__in': 'TEST_ID'}),
            ({'id__in': TEST_INSTITUTION_ID1}),
            ({'id__contains': [TEST_INSTITUTION_ID1, TEST_LINK_ID, TEST_INSTITUTION_ID2]}),
            ({'id__contains': TEST_LINK_ID + '123'}),
            ({'id__contains': 'TEST_LINK_ID_123'}),
            ({'id__contains': TEST_NODE_ID1}),
            ({'id__contains': [Node(TEST_NODE_ID1, TEST_NODE_NAME1)]}),
            ({'id__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({'id__contains': ' '}),
            ({'owners__in': ['']}),
            ({'owners__in': ' '}),
            ({'owners__in': [Institution('', TEST_NODE_NAME1)]}),
            ({'owners__in': TEST_NODE_ID1}),
            ({'owners__in': [Node(TEST_NODE_ID1, TEST_NODE_NAME1)]}),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1),
                                   Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2),
                                   Institution('TEST_ID_3', 'TEST_NAME_3')],
              }),
            ({'owners__contains': TEST_INSTITUTION_NAME1}),
            ({'owners__contains': ''}),
            ({'owners__contains': Node(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)}),
            ({'owners__contains': TEST_NODE_NAME1}),
            ({'nodes__in': [Node(TEST_NODE_ID1, TEST_NODE_NAME1)]}),
            ({'nodes__in': [' ']}),
            ({'nodes__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1)]}),
            ({'nodes__in': TEST_NODE_ID1}),
            ({'nodes__in': TEST_NODE_NAME1}),
            ({'nodes__contains': [Node(TEST_NODE_ID1, TEST_NODE_NAME1), Node(TEST_NODE_ID2, TEST_NODE_NAME2),
                                  Node('TEST_NODE', 'TESTNODENAME')]}),
            ({'nodes__contains': ' '}),
            ({'nodes__contains': TEST_NODE_NAME1}),
            ({'nodes__contains': TEST_NODE_ID1[3:7]}),
            ({'nodes__contains': 'TEST_NODE_ID1_213'}),
            ({'nodes__contains': 'TEST_NODE'}),
        ),
        ids=['nodes only', 'two same nodes', 'three different nodes', 'empty id only', 'empty link and name only',
             'empty owners only', 'nodes only', 'all details with 2 owners', '2 owners', 'checking caps',
             'id__in with node object', 'id__in with owner object', 'id__in link_name', 'id__in empty',
             'id__in slice func', 'id__in invalid_id', 'id__in institution_id', 'id__contains list of strings',
             'id_contains string with required string to the left using concat. operator',
             'id__contains string with required string to the left', 'id__contains node_id',
             'id__contains node object', 'id__contains owner object', 'id__contains empty', 'owners__in empty list',
             'owners__in empty list', 'owners_in institution with no id', 'owners__in node_id',
             'owners__in with node object', 'owners__contains list of different owners',
             'owners__contains institution_name', 'owners__contains empty', 'owners__contains node object',
             'owners__contains node_name', 'nodes__in with a node', 'nodes__in empty', 'nodes__in institution object',
             'nodes__in with node_id', 'nodes__in with node_name', 'nodes__contains different_nodes',
             'nodes__contains empty', 'nodes__contains node_name', 'node__contains slice_function',
             'nodes__contains with required string to the left', 'nodes_contains with substring of required string'],
    )
    def test_link_match_fail(self, link, kwargs):
        """
            This test checks the functionality of match function of the link. In this test, we have passed different
            values to the attributes of the link which makes the match fail. We are passing values using kwargs.
            In kwargs, we are passing keyword arguments
            Each test case has unique id.
            for example: 'nodes only'
            This id represents that we have passed only nodes to the match function.
            # We are not using args and kwargs. Because this function use kwargs only
            We use almost every possible combination which fail the match function of the link.
        """
        assert not link.match(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'version__contains': '2020-03-20'}),
            ({'short_name': 'TEST_LINK_SHORT_NAME'}),
            ({'lifetime_start__contains': '2020-03-20T14:30:43'}),
            ({'lifetime_end__contains': '2020-03-29T14:30:43'}),
        ),
        ids=['version', 'short name', 'life time start', 'life time end'],
    )
    def test_link_match_sucess_with_optional_fields(self, link_with_all_fields, kwargs):
        assert link_with_all_fields.match(**kwargs)

    def test_link_eq_success(self, link, link_many_owners, node1, node2, institution, institutions):
        """
            This test checks the equality of links. The test passes when the links are equal
        """
        replica_of_link_with_owner = Link(TEST_LINK_ID, TEST_LINK_NAME, None, institution, [node1, node2])
        assert link == replica_of_link_with_owner

        replica_of_link_with_owners = Link(TEST_LINK_ID, TEST_LINK_NAME, None, institutions, [node1, node2])
        assert link_many_owners == replica_of_link_with_owners

        link_with_id_name_nodes = Link(id=TEST_LINK_ID, name=TEST_LINK_NAME, nodes=[node1, node2])
        replica_of_link_with_id_name_nodes = \
            Link(
                id='TEST_LINK_ID1',
                name='TEST_LINK_NAME1',
                nodes=[Node('TEST_NODE_ID1', 'TEST_NODE_NAME1'), Node('TEST_NODE_ID2', 'TEST_NODE_NAME2')]
            )
        assert link_with_id_name_nodes == replica_of_link_with_id_name_nodes

    def test_link_not_eq(self, link, link_many_owners, node1, node2, institution, institutions):
        """
            This test checks the equality of links. The test passes when the links are not equal
        """
        link_with_name_and_nodes = Link(name=TEST_LINK_NAME, nodes=[node1, node2])
        simple_link = Link(name='TEST_LINK_NAME1',
                           nodes=[Node('TEST_NODE_ID1', 'TEST_NODE_NAME1'), Node('TEST_NODE_ID2', 'TEST_NODE_NAME2')])
        """
            Only check if the nodes are not using determinate id scheme, as different nodes with
            the same data will have the same id
        """
        if simple_link._id_format != meta.IDGeneration.DETERMINATE \
                and link_with_name_and_nodes._id_format != meta.IDGeneration.DETERMINATE:
            assert simple_link != link_with_name_and_nodes

        link_with_name_owners_nodes = Link(name=TEST_LINK_NAME, owners=institution, nodes=[node1, node2])
        replica_of_link_with_name_owners_nodes = \
            Link(
                name='TEST_LINK_NAME1',
                owners=[Institution('TEST_ID1', 'TEST_NAME1')],
                nodes=[Node('TEST_NODE_ID1', 'TEST_NODE_NAME1'), Node('TEST_NODE_ID2', 'TEST_NODE_NAME2')]
            )
        """
            Only check if the nodes are not using determinate id scheme, as different nodes with
            the same data will have the same id
        """
        if replica_of_link_with_name_owners_nodes._id_format != meta.IDGeneration.DETERMINATE \
                and link_with_name_owners_nodes._id_format != meta.IDGeneration.DETERMINATE:
            assert link_with_name_owners_nodes != replica_of_link_with_name_owners_nodes

        assert link != link_many_owners
        assert link != link_with_name_owners_nodes
        assert link != link_with_name_and_nodes
        assert link_many_owners != link_with_name_and_nodes
        assert link_many_owners != link_with_name_owners_nodes
        assert link_with_name_and_nodes != link_with_name_owners_nodes
