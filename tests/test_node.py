import pytest
from grenml.models import Institution, Node
from datetime import datetime
from dateutil.tz import tzlocal

TEST_NODE_ID = 'TEST_NODE_ID'
TEST_NODE_NAME = 'TEST_NODE_NAME'
TEST_INSTITUTION_ID1 = 'TEST_ID1'
TEST_INSTITUTION_NAME1 = 'TEST_NAME1'
TEST_INSTITUTION_ID2 = 'TEST_ID2'
TEST_INSTITUTION_NAME2 = 'TEST_NAME2'

INSTITUTION_TYPE_DEFAULT = 'other'

UTC_OFFSET = str(datetime.strftime(datetime.now().replace(tzinfo=tzlocal()), '%z'))
UTC_OFFSET = UTC_OFFSET[:3] + ':' + UTC_OFFSET[3:]


class TestNode:

    @pytest.fixture
    def institution(self):
        return [Institution(id=TEST_INSTITUTION_ID1, name=TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]

    @pytest.fixture
    def institutions(self, institution):
        return [
            institution[0],
            Institution(id=TEST_INSTITUTION_ID2, name=TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
            Institution(id='TEST_ID_3', name='TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT),
        ]

    @pytest.fixture
    def node(self):
        return Node(TEST_NODE_ID, TEST_NODE_NAME)

    @pytest.fixture
    def node_with_all_fields(self):
        return Node(
            id=TEST_NODE_ID,
            name=TEST_NODE_NAME,
            short_name='NODE_SHORT_NAME',
            version='2020-02-12T10:43:30+04:00',
            longitude=45,
            latitude=75,
            altitude=100,
            unlocode='CA OTT',
            address='TEST ADDRESS',
            lifetime_start='2020-03-20T14:30:43',
            lifetime_end='2020-03-29T14:30:43'
        )

    @pytest.mark.parametrize(
        'args, kwargs',
        (
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME,
                  'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME,
                  'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                             Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                             Institution('TEST_INSTITUTION_ID3', 'TEST_INSTITUTION_NAME3', INSTITUTION_TYPE_DEFAULT)]}),
            ([TEST_NODE_ID, TEST_NODE_NAME, [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]], {}),
            ([TEST_NODE_ID, TEST_NODE_NAME, [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                                             Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                                             Institution('TEST_INSTITUTION_ID3', 'TEST_INSTITUTION_NAME3', INSTITUTION_TYPE_DEFAULT)]], {}),
            ([TEST_NODE_ID], {'name': TEST_NODE_NAME, 'owners':
                              [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ([TEST_NODE_ID], {'name': TEST_NODE_NAME,
                              'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                                         Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                                         Institution('TEST_INSTITUTION_ID3', 'TEST_INSTITUTION_NAME3', INSTITUTION_TYPE_DEFAULT)]}),
            ([], {'name': TEST_NODE_NAME, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ([], {'name': TEST_NODE_NAME, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                                                     Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                                                     Institution('TEST_INSTITUTION_ID3', 'TEST_INSTITUTION_NAME3', INSTITUTION_TYPE_DEFAULT)]}),
            ([TEST_NODE_ID, TEST_NODE_NAME], {}),
            ([TEST_NODE_ID], {'name': TEST_NODE_NAME}),
            ([], {'name': TEST_NODE_NAME, 'id': TEST_NODE_ID}),
            ([], {'name': TEST_NODE_NAME}),
            ([], {'name': TEST_NODE_NAME, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ([], {'name': TEST_NODE_NAME, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                                                     Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                                                     Institution('TEST_INSTITUTION_ID3', 'TEST_INSTITUTION_NAME3', INSTITUTION_TYPE_DEFAULT)
                                                     ]}),
            ([''], {'name': TEST_NODE_NAME}),  # If not provided an ID, the Institution creates one
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'short name': 'Node Test Short Name'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'version': '2020-02-12T10:43:30+04:00'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'longitude': 45.5}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'latitude': 75.5}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'altitude': 100}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'unlocode': 'Node Test Unlocode'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'address': 'Node Test Address'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME,
                  'lifeime_start': '2020-03-20T14:30:43', 'lifetime_end': '2020-03-29T14:30:43'
                  }),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_end': '2020-03-20T14:30:43'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43-05:00'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43.999999'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43.999999+05:00'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20'}),
            ([], {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43Z'}),
        ),
        ids=['kwargs_with_a_institution', 'kwargs_with_institutions', 'args__with_a_institution',
             'args_with_institutions', 'args_with_node_id_and_kwargs_with_node_name_and_a_inst',
             'args_with_node_id_and_kwargs_with_node_name_and_inst_list', 'kwargs_with_name_and_a_institution',
             'kwargs_with_name_and_institution_list', 'args_with_Node_details',
             'args_with_node_id_and_kwargs_with_node_name', 'kwargs_with_node_details', 'kwargs_with_node_name',
             'kwargs_with_node_name_and_owner', 'kwargs_with_node_name_and_owners_list',
             'args_with_empty_string_and_kwargs_with_node_name', 'node with short name', 'node with version',
             'node with longitude', 'node with latitude', 'node with altitude', 'node with unlocode', 'node with address',
             'node with life time start and life time end', 'node with life time start', 'node with life time end',
             'node life time with ISO timezone', 'node life time with microsecond',
             'node life time ISO timezone and microsecond', 'node life time only date', 'node lifetime UTC']
    )
    def test_node_create_success(self, args, kwargs):
        node = Node(*args, **kwargs)
        if node.name is not TEST_NODE_NAME:
            pytest.raises('{} not found exception'.format(TEST_NODE_NAME))

    @pytest.mark.parametrize(
        'kwargs, expected',
        (
            (
                {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43Z'},
                '2020-03-20T14:30:43+00:00'
            ),
            (
                {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43-05:00'},
                '2020-03-20T14:30:43-05:00'
            ),
            (
                {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43.999999'},
                '2020-03-20T14:30:43' + UTC_OFFSET
            ),
            (
                {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43.999999Z'},
                '2020-03-20T14:30:43+00:00'
            ),
            (
                {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43.999999+05:00'},
                '2020-03-20T14:30:43+05:00'
            ),
            (
                {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20'},
                '2020-03-20T00:00:00' + UTC_OFFSET
            ),
            (
                {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T00:00:00'},
                '2020-03-20T00:00:00' + UTC_OFFSET
            ),
            (
                {'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T00:00:00Z'},
                '2020-03-20T00:00:00+00:00'
            ),
        ),
        ids=[
            'node life time with UTC timezone', 'node life time with ISO timezone', 'node life time with microsecond',
            'node life time UTC timezone and microsecond', 'node life time ISO timezone and microsecond',
            'node life time only date', 'node life time date with no time set', 'node life time with UTC label',
        ]
    )
    def test_node_lifetime_reformat(self, kwargs, expected):
        node = Node(**kwargs)
        assert node.lifetime_start == expected, 'Found life time: {}, expected life time is {}'.format(
            node.lifetime_start, expected
        )

    def test_node_lifetime_takes_iso_format(self):
        node = Node(lifetime_start=datetime(year=2020, month=2, day=13, hour=13, minute=30, second=40))
        node.lifetime_end = node.lifetime_start

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '14:30:43'}),
            ({'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '2020-03-20T14:30:43EST'}),
            ({'id': TEST_NODE_ID, 'name': TEST_NODE_NAME, 'lifetime_start': '03-20-2020T14:30:43'}),
        ),
        ids=['Life time only have time', 'Life time timezone using string', 'Life time with different format']
    )
    def test_node_create_lifetime_fail(self, kwargs):
        with pytest.raises(ValueError):
            Node(**kwargs)

    @pytest.mark.parametrize(
        'args, kwargs',
        (
            (
                [],
                {'name': TEST_NODE_NAME,
                 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                            Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                            Institution('TEST_INSTITUTION_ID1', 'TEST_INSTITUTION_NAME1', INSTITUTION_TYPE_DEFAULT)]
                 }
            ),
        ),
        ids=['kwargs_with_same_data'],
    )
    def test_node_create_success_same_data(self, args, kwargs):
        Node(*args, **kwargs)

    """
    id__in working:
       (i)when string matches fully matches with the other string
       (ii)when string matches with the string in the list of strings
            :only for list of strings: must be fully matched not be a substring
       (iii)when string matches with the substring of a string
           e.g : node with TEST_NODE_ID matches with TEST_NODE_ID123
    """
    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'id': TEST_NODE_ID, 'name': TEST_NODE_NAME}),
            ({'name': TEST_NODE_NAME}),
            ({'id': TEST_NODE_ID}),
            ({'id__in': TEST_NODE_ID}),
            ({'id__in': [TEST_NODE_ID, TEST_INSTITUTION_ID1, TEST_INSTITUTION_ID2]}),
            ({'id__in': 'TEST_NODE_ID123'}),
            ({'id__in': TEST_NODE_ID + '123'}),
            ({'id__in': '123_TEST_NODE_ID_123_TEST_NODE_ID_123_TEST_NODE_ID'}),
            ({'id__contains': TEST_NODE_ID}),
            ({'id__contains': 'TEST_NODE'}),
            ({'id__contains': 'TEST_NODE_I'}),
            ({'id__contains': ''})
        ),
        ids=['node_id_and_name', 'node_name', 'node_id', 'id__in_with_node_id', 'id__in_with_list_of_strings',
             'id__in_with_matching_string_pat1', 'id__in_with_matching_string_pat2', 'id__in_with_matching_string_pat3',
             'id__contains_with_node_id', 'id__contains_with_substring_of_string_pat_1',
             'id__contains_with_substring_of_string_pat_2', 'id__contains_empty'],
    )
    def test_node_match_success(self, node, kwargs):
        assert node.match(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'version': '2020-02-12T10:43:30+04:00'}),
            ({'longitude': 45}),
            ({'latitude': 75}),
            ({'altitude': 100}),
            ({'unlocode': 'CA OTT'}),
            ({'address': 'TEST ADDRESS'}),
            ({'lifetime_start__contains': '2020-03-20T14:30:43'}),
            ({'lifetime_end__contains': '2020-03-29T14:30:43'}),
        ),
        ids=['version', 'longitude', 'latitude', 'altitude', 'unlocode', 'address', 'life time start', 'life time end'],
    )
    def test_node_match_sucess_with_optional_fields(self, node_with_all_fields, kwargs):
        assert node_with_all_fields.match(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'id': TEST_NODE_ID, 'name': TEST_NODE_NAME}),
            ({'name': TEST_NODE_NAME}),
            ({'id': TEST_NODE_ID}),
            ({'id__in': TEST_NODE_ID}),
            ({'id__in': [TEST_NODE_ID, TEST_INSTITUTION_ID1, TEST_INSTITUTION_ID2]}),
            ({'id__in': 'TEST_NODE_ID123'}),
            ({'id__in': TEST_NODE_ID + '123'}),
            ({'id__in': '123_TEST_NODE_ID_123_TEST_NODE_ID_123_TEST_NODE_ID'}),
            ({'id__contains': TEST_NODE_ID}),
            ({'id__contains': 'TEST_NODE'}),
            ({'id__contains': 'TEST_NODE_I'}),
            ({'id__contains': ''}),
            ({'id__contains': TEST_NODE_ID[4:]}),
            ({'id': TEST_NODE_ID, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'name': TEST_NODE_NAME, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({
                'id': TEST_NODE_ID,
                'name': TEST_NODE_NAME,
                'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]
            }),
            ({
                'id': TEST_NODE_ID,
                'name': TEST_NODE_NAME,
                'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                           Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                           Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]
            }),
            ({'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                             Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                             Institution('TEST_INSTITUTION_ID1', 'TEST_INSTITUTION_NAME1', institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                             Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                             Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__in': [TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME2, TEST_INSTITUTION_ID2, INSTITUTION_TYPE_DEFAULT]}),
            ({'owners__in': [TEST_INSTITUTION_ID1]}),
            ({'owners__in': ['TEST_ID1']}),
            ({'id__in': TEST_NODE_ID, 'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                                     Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                                                     Institution('TEST_INSTITUTION_ID3', 'TEST_INSTITUTION_NAME3', institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                   Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                   Institution('TEST_ID1', 'TEST_NAME1', institution_type=INSTITUTION_TYPE_DEFAULT)],
              }),
            ({'owners__contains': TEST_INSTITUTION_ID1}),
        ),
        ids=['node_id_and_name', 'node_name', 'node_id', 'id__in_with_node_id', 'id__in_with_list_of_strings',
             'id__in_with_matching_string_pat1', 'id__in_with_matching_string_pat2', 'id__in_with_matching_string_pat3',
             'id__contains_with_node_id', 'id__contains_with_substring_of_string_pat_1',
             'id__contains_with_substring_of_string_pat_2', 'id__contains_empty', 'id__contains_node_id_pat',
             'node_id_and_owner', 'node_name_and_owner', 'node_details_with_owner', 'node_details_with_same_owners_list',
             'node_owner', 'owners__in_with_owner', 'owners__in_with_different_owner_list',
             'owners__in_with_same_owners_list', 'owners__in_list_of_strings', 'owners__in_institution_id',
             'owners__in_string', 'id__in_and_owners__in', 'owners__contains_with_owner',
             'owner__contains__same_owners_list', 'owners__contains_institution_id', ],
    )
    def test_node_with_a_owner_match_success(self, institution, kwargs):
        new_node_with_institution = Node(TEST_NODE_ID, TEST_NODE_NAME, 'NODE', institution)
        assert new_node_with_institution.match(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'id': TEST_NODE_ID, 'name': TEST_NODE_NAME}),
            ({'name': TEST_NODE_NAME}),
            ({'id': TEST_NODE_ID}),
            ({'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                         Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                         Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'id__in': TEST_NODE_ID}),
            ({'id__in': [TEST_NODE_ID, TEST_INSTITUTION_ID1, TEST_INSTITUTION_ID2]}),
            ({'id__in': 'TEST_NODE_ID123'}),
            ({'id__in': TEST_NODE_ID + '123'}),
            ({'id__in': '123_TEST_NODE_ID_123_TEST_NODE_ID_123_TEST_NODE_ID'}),
            ({'id__contains': TEST_NODE_ID}),
            ({'id__contains': 'TEST_NODE'}),
            ({'id__contains': 'TEST_NODE_I'}),
            ({'id__contains': ''}),
            ({'id__contains': TEST_NODE_ID[4:]}),
            ({'id': TEST_NODE_ID, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                             Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                                             Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'name': TEST_NODE_NAME, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                                 Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                                                 Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({
                'id': TEST_NODE_ID,
                'name': TEST_NODE_NAME,
                'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                           Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                           Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT)]
            }),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                             Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                             Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__in': [TEST_INSTITUTION_ID1, 'TEST_ID_3', TEST_INSTITUTION_ID2, 'TEST_INSTITUTION']}),
            ({'id__in': TEST_NODE_ID, 'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                                     Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                                                     Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                   Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                   Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT)],
              }),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, institution_type=INSTITUTION_TYPE_DEFAULT),
                                   Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, institution_type=INSTITUTION_TYPE_DEFAULT),
                                   Institution('TEST_ID_3', 'TEST_NAME_3', institution_type=INSTITUTION_TYPE_DEFAULT)],
              }),
            ({'owners__contains': TEST_INSTITUTION_ID1}),
        ),
        ids=['node_id_and_name', 'node_name', 'node_id', 'exact_institutions', 'id__in_with_node_id',
             'id__in_with_list_of_strings', 'id__in_with_matching_string_pat1', 'id__in_with_matching_string_pat2',
             'id__in_with_matching_string_pat3', 'id__contains_with_node_id',
             'id__contains_with_substring_of_string_pat_1', 'id__contains_with_substring_of_string_pat_2',
             'id__contains_empty', 'id__contains_node_id_pat', 'node_id_and_owner', 'node_name_and_owner',
             'node_details_with_owners', 'owners__in_with_different_owner_list', 'owners__in_list_of_strings',
             'id__in_and_owners__in', 'owners__contains_with_owner', 'owner__contains_same_owners_list',
             'owners__contains_different_owners_list', 'owners__contains_institution_id'],
    )
    def test_node_with_owners_match_success(self, institutions, kwargs):
        new_node_with_institutions = Node(TEST_NODE_ID, TEST_NODE_NAME, owners=institutions)
        assert new_node_with_institutions.match(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'id': TEST_NODE_ID, 'name': 'Invalid'}),
            ({'id': TEST_NODE_ID, 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ({'id': 'Invalid'}),
            ({'name': 'Invalid', 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ({'name': 'Invalid'}),
            ({'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ({
                'id': TEST_NODE_ID,
                'name': 'TEST_NAME',
                'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]
            }),
            ({
                'id': TEST_NODE_ID,
                'name': TEST_NODE_NAME,
                'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                           Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                           Institution('Test_ID_3', 'Test_NAME_3', INSTITUTION_TYPE_DEFAULT)]
            }),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                             Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                             Institution('Test_Institution_3', 'Test_Institution_name3', INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__in': [TEST_NODE_ID]}),
            ({'owners__in': [TEST_NODE_NAME]}),
            ({'owners__contains': TEST_NODE_NAME}),
            ({'owners__contains': TEST_NODE_ID}),
            ({'owners__contains': TEST_INSTITUTION_ID1}),
            ({'owners__contains': TEST_INSTITUTION_NAME1}),
            ({'owners__contains': Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)}),
            ({'owners__contains': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                                   Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                                   Institution('TEST_INSTITUTION_ID3', 'TEST_INSTITUTION_NAME3', INSTITUTION_TYPE_DEFAULT)]}),
            ({'id__in': TEST_NODE_NAME}),
            ({'id__in': ''}),
            ({'id__in': TEST_NODE_ID[4:0]}),
            ({'id__in': 'TEST_ID'}),
            ({'id__in': TEST_INSTITUTION_ID1}),
            ({'id__contains': [TEST_INSTITUTION_ID1, TEST_NODE_ID, TEST_INSTITUTION_ID2]}),
            ({'id__contains': TEST_NODE_ID + '123'}),
            ({'id__contains': 'TEST_NODE_ID_123'}),
        ),
        ids=['node_id_and_invalid_name', 'id_and_owner', 'invalid id only', 'name_and_owner', 'invalid_name_only',
             'owner_only', 'id_name_and_owner', 'id_name_and_owners', 'owner__in_without_list',
             'owners__in_with_ins_list', 'owners__in_node_id', 'owners__in_node_name', 'owners__contains_node_name',
             'owners__contains__node__name', 'owners_contains_inst_id', 'owners_contains_inst_name',
             'owners__contains_institution', 'owners_contains_institution_list', 'id__in_with_node_name',
             'id__in_empty', 'id__in_pattern', 'invalid_node_id', 'id__in_institution_id', 'id__contains_list_of_string',
             'id__contains_pat1', 'id__contains_pat2'],
    )
    def test_node_match_fail(self, node, kwargs):
        assert not node.match(**kwargs)

    @pytest.mark.parametrize(
        'kwargs',
        (
            ({'id': TEST_NODE_ID, 'name': 'Invalid'}),
            ({'id': 'Invalid'}),
            ({'name': 'Invalid', 'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ({
                'id': TEST_NODE_ID,
                'name': 'TEST_NAME',
                'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]
            }),
            ({
                'id': TEST_NODE_ID,
                'name': TEST_NODE_NAME,
                'owners': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT),
                           Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT),
                           Institution('Test_ID_3', 'Test_NAME_3', INSTITUTION_TYPE_DEFAULT)]
            }),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID2, TEST_INSTITUTION_NAME1, INSTITUTION_TYPE_DEFAULT)]}),
            ({'owners__in': [Institution(TEST_INSTITUTION_ID1, TEST_INSTITUTION_NAME2, INSTITUTION_TYPE_DEFAULT)]}),
            ({'id__in': TEST_NODE_NAME}),
            ({'id__in': ''}),
            ({'id__in': TEST_NODE_ID[4:0]}),
            ({'id__in': 'TEST_ID'}),
            ({'id__in': TEST_INSTITUTION_ID1}),
            ({'id__contains': [TEST_INSTITUTION_ID1, TEST_NODE_ID, TEST_INSTITUTION_ID2]}),
            ({'id__contains': TEST_NODE_ID + '123'}),
            ({'id__contains': 'TEST_NODE_ID_123'}),
        ),
        ids=['id and name', 'id only', 'name_and_owner', 'id_name_and_owner', 'id_name_and_owners',
             'owner__in_with_other_institution_id', 'owner__in_different_inst_name', 'id__in_with_node_name',
             'id__in_empty', 'id__in_pattern', 'invalid_node_id', 'id__in_institution_id', 'id__contains_list_of_string',
             'id__contains_pat1', 'id__contains_pat2'],
    )
    def test_node_with_owners_match_fail(self, institution, institutions, kwargs):
        new_node_with_institution = Node(TEST_NODE_ID, TEST_NODE_NAME, institution)
        assert not new_node_with_institution.match(**kwargs)
        new_node_with_institutions = Node(TEST_NODE_ID, TEST_NODE_NAME, institutions)
        assert not new_node_with_institutions.match(**kwargs)

    def test_institution_eq_success(self, node, institution, institutions):
        new_node = Node(id=TEST_NODE_ID, name=TEST_NODE_NAME)
        assert node == new_node
        new_node_with_institution = Node(
            id=TEST_NODE_ID,
            name=TEST_NODE_NAME,
            owners=institution
        )
        replica_new_node_with_institution = Node(
            id=TEST_NODE_ID,
            name=TEST_NODE_NAME,
            owners=institution
        )
        assert new_node_with_institution == replica_new_node_with_institution

    def test_institution_eq_fail(self, node, institution, institutions):
        new_node = Node(id="Test ID 2", name=TEST_NODE_NAME)
        new_node_with_institution = Node(
            id=TEST_NODE_ID,
            name=TEST_NODE_NAME,
            owners=institution
        )
        new_node_with_institutions = Node(
            id=TEST_NODE_ID,
            name=TEST_NODE_NAME,
            owners=institutions
        )
        assert node != new_node
        assert node != new_node_with_institution
        assert node != new_node_with_institutions
        assert new_node_with_institution != new_node_with_institutions
        assert new_node_with_institution != new_node
        assert new_node_with_institutions != new_node
