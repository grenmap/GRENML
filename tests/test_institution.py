import pytest
from grenml.models import Institution

TEST_INSTITUTION_ID = 'TEST_ID'
TEST_INSTITUTION_NAME = 'TEST_NAME'
TEST_SHORTNAME = 'TEST'
INSTITUTION_TYPE_DEFAULT = 'Test Inst'


@pytest.fixture
def institution():
    return Institution(TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT)


@pytest.fixture
def institution_all_details():
    return Institution(TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, 0, 0, 12, 'NY', '45')


@pytest.fixture
def institution_with_multiple_inst_type():
    return Institution(TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, ['pren', 'sren', 'nren'], 0, 0, 12, 'NY', '45')


@pytest.fixture
def institution_with_different_inst_type():
    return Institution(TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, 'pren', 0, 0, 12, 'NY', '45')


@pytest.mark.parametrize(
    'args, kwargs',
    (
        ([],
         {'id': TEST_INSTITUTION_ID, 'name': TEST_INSTITUTION_NAME, 'institution_type': INSTITUTION_TYPE_DEFAULT}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, INSTITUTION_TYPE_DEFAULT], {}),
        ([TEST_INSTITUTION_ID], {'name': TEST_INSTITUTION_NAME, 'institution_type': INSTITUTION_TYPE_DEFAULT}),
        ([], {'name': TEST_INSTITUTION_NAME, 'institution_type': INSTITUTION_TYPE_DEFAULT}),
        # If not provided an ID, the Institution creates one
        ([], {'id': '', 'name': TEST_INSTITUTION_NAME, 'institution_type': INSTITUTION_TYPE_DEFAULT}),
        ([], {'id': 123456, 'name': TEST_INSTITUTION_NAME, 'institution_type': INSTITUTION_TYPE_DEFAULT}),
        (
            [
                TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT,
                -89.999999, 89.99999999, '77', 'CA OTW', "45 O'Connor"
            ], {}
        ),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, 0, 0, 0, 0, 0], {}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, 'pRen', 0, 0, 0, 0, 0], {}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, 'pRen', 179.999, 89.99, 0, 0, 0], {}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, 'pRen', -179.999, -89.9999999], {}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, 'pRen', 0, 0, '', '', ''], {}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, 'pRen', 0, 0, '122+2332sds', '', ''], {}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, 'pRen', 0, 0, '', 'asdfa 12311', '12312'], {}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME], {}),
        ([TEST_INSTITUTION_NAME, TEST_INSTITUTION_NAME, TEST_SHORTNAME, 'pren', 0, 0,
          TEST_INSTITUTION_NAME, TEST_INSTITUTION_NAME, TEST_INSTITUTION_NAME], {}),
        (
            [],
            {
                'id': TEST_INSTITUTION_ID, 'name': TEST_INSTITUTION_NAME, 'short_name': TEST_SHORTNAME,
                'institution_type': INSTITUTION_TYPE_DEFAULT,
                'latitude': 22.893, 'longitude': 12 - 32.343, 'altitude': '123', 'unlocode': 'NY USA',
                'address': 'a'
            }
        ),
        ([], {'name': TEST_INSTITUTION_NAME, 'latitude': 22.893, 'longitude': 12 - 32.343}),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT],
         {'latitude': 22.893, 'longitude': 12 - 32.343, 'altitude': '123', 'unlocode': 'NY USA', 'address': 'a'}),
        ([TEST_INSTITUTION_NAME], {'name': TEST_INSTITUTION_NAME, 'longitude': .017e4}),
    ),
    ids=['kwargs with name, id and type', 'args with name, id and type', 'arg with id and kwargs with name and type',
         'kwargs with name and type', 'kwargs with name, type and empty id', 'kwargs with name, type and id as integer',
         'args with all details', 'args with lat, long, alt, unlocode, and address equal to 0',
         'checking lower and upper case in institution type in args', 'maximum value to lat. and long. in args',
         'minimum value to lat. and long. in args', 'passing alt, unlocode, and address empty in args',
         'passing alphabets in altitude in args', 'passing random value to unlocode in args', 'args with name and id',
         'passing institution name to all fields except type, long. and lat. in args', 'kwargs with all details',
         'passing name, lat. and long. only in kwargs', 'name and id in args and rest details in kwargs',
         'passing name in args and name and longitude in kwargs'
         ],
)
def test_institution_create_success(args, kwargs):
    """
    This test case checks the successful creation of institution. We use almost every possible combination which
    successfully creates the institution.
    The function also checks if the institution is created or not. If not raises an error
    This test case takes two parameters:
        (i) args: takes positional arguments using this parameter
        (ii) kwargs: takes keyword arguments using this parameter
    """
    # creating institution
    institution = Institution(*args, **kwargs)
    # checking that institution is created or not
    if institution.name is not TEST_INSTITUTION_NAME:
        pytest.raises('{0} not found exception'.format(TEST_INSTITUTION_NAME))


@pytest.mark.parametrize(
    'args, kwargs, exception',
    (
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, ],
         {'id': TEST_INSTITUTION_ID + '1', 'name': TEST_INSTITUTION_NAME,
          'institution_type': INSTITUTION_TYPE_DEFAULT},
         TypeError
         ),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, -180.1, -90.1, 0, 0, 0], {},
         AttributeError),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, 180.1, 90.1, 0, 0, 0], {},
         AttributeError),
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, 'Test', '90', 0, 0, 0], {},
         ValueError),
    ),
    ids=['kwargs and args with all details',
         'checking minimum value of long. and lat.', 'checking maximum value of long. and lat.',
         'passing string to lat and long',
         ],
)
def test_institution_create_failure(args, kwargs, exception):
    """
    This test case checks, when the creation of institution fails. We use almost every possible combination which
    fails the creation of the institution.
    The function raises an error when the institution successfully created
    This test case takes three parameters:
        (i) args: takes positional arguments using this parameter
        (ii) kwargs: takes keyword arguments using this parameter
        (iii) exception: exception which is generated during the creation of a institution
    """
    with pytest.raises(exception):
        Institution(*args, **kwargs)


@pytest.mark.parametrize(
    'kwargs',
    (
        {'id': TEST_INSTITUTION_ID, 'name': TEST_INSTITUTION_NAME, },
        {'id': TEST_INSTITUTION_ID, },
        {'name': TEST_INSTITUTION_NAME},
        {'id__contains': 'TEST'},
        {'id__contains': 'D'},
        {'id__contains': TEST_INSTITUTION_ID[3:5]},
        {'id__contains': ''},
        {'id__in': [TEST_INSTITUTION_ID, 'TEST ID 2']},
        {'id__in': 'TEST_ID_1231'},
        {'id__in': '123TEST_ID123'},
        {'id__in': '123' + TEST_INSTITUTION_ID + '123'},
        {'id__in': '3423 ' + TEST_INSTITUTION_ID},
        {'latitude__in': [None, 0]},
        {'longitude__in': [None, 0]},
        {'type': INSTITUTION_TYPE_DEFAULT},
        {'types__contains': INSTITUTION_TYPE_DEFAULT},
    ),
    ids=['id and name', 'id only', 'name only', 'id_contains subset',
         'id__contains alphabet', 'id__contains subset using slicing', 'id__contains empty',
         'id__in with list', 'id_in with req. string to left',
         'id__in with required string in between', 'id__in with required string in between using concat. operator',
         'id__in with required string to the right', 'correct latitude', 'correct longitude', 'default inst. type',
         'type__contains',
         ],
)
def test_institution_match_success(institution, institution_all_details, kwargs):
    """
    This test case checks the match function of the institution.
    This test case takes three parameters:
        (i) institution: calls the institution function which returns institution with name, id, and type
        (ii) institution_all_details: calls the institution_all_details function which returns
                                      institution with all details
        (iii) kwargs: takes keyword arguments using this parameter
    This test case passes when match function passes.
    """
    assert institution.match(**kwargs)
    assert institution_all_details.match(**kwargs)


@pytest.mark.parametrize(
    'kwargs',
    (
        {'address': '45'},
        {'unlocode': 'NY'},
        {'altitude': 12},
        {'name': TEST_INSTITUTION_NAME, 'longitude': 0.0, 'latitude': 0, 'unlocode': 'NY', 'address': '45',
         'id': TEST_INSTITUTION_ID},
    ),
    ids=['checking address', 'passing correct unlocode', 'correct altitude', 'all details', ],
)
def test_institution_all_details_match_success(institution_all_details, kwargs):
    """
    This test case checks the match function of the institution.
    This test case takes three parameters:
        (i) institution_all_details: calls the institution_all_details function which returns
                                          institution with all details
        (ii) kwargs: takes keyword arguments using this parameter
    This test case passes when match passes.
    """
    assert institution_all_details.match(**kwargs)


@pytest.mark.parametrize(
    'kwargs',
    (
        {'name': TEST_INSTITUTION_NAME},
        {'id__contains': '123456'},
        {'id__contains': '23'},
        {'id__contains': ''},
        {'id__in': ['123456', 'TEST ID 2']},
        {'id__in': 'TEST_ID_1234561'},
        {'id__in': '123456123'},
        {'id__in': str(12345667) + TEST_INSTITUTION_ID},
        {'latitude': 0},
        {'longitude': 0.0},
        {'type': INSTITUTION_TYPE_DEFAULT},
    ),
    ids=['name', 'id__contains string', 'id__contains with substring', 'id__contains empty', 'id__in with list',
         'id__in with required string in between', 'id__in with required string to the left',
         'id__in with concatenation operator', 'correct latitude', 'correct longitude', 'passing inst. type']
)
def test_institution_id_type_int_match_success(kwargs):
    """
    This test case checks the match function of the institution. This function takes keyword arguments as parameter by
    using kwargs.
    This test case is basically for institution which has id as a number. This test case passes when match passes.
    """

    new_institution = Institution(123456, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, 0, 0)
    assert new_institution.match(**kwargs)

    new_institution_all_details = Institution(123456, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, 0, 0, 0, '0', '0')
    assert new_institution_all_details.match(**kwargs)


@pytest.mark.parametrize(
    'kwargs',
    (
        {'address': '0'},
        {'unlocode': '0'},
        {'altitude': 0},
        {'id': str(123456), 'name': TEST_INSTITUTION_NAME, 'longitude': 0.0, 'latitude': 0, 'unlocode': '0',
         'address': '0', 'altitude': 0},
    ),
    ids=['checking address', 'passing correct unlocode', 'correct altitude', 'all details with string id', ]
)
def test_institution_all_details_id_type_int_match_success(kwargs):
    """
    This test case checks the match function of the institution. This function takes keyword arguments as parameter by
    using kwargs.
    This test case is basically for institution which has id as a number. This test case passes when match passes.
    These tests are only for the institution with details
    """
    new_institution_all_details = Institution(123456, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, 0, 0, 0, '0', '0')
    assert new_institution_all_details.match(**kwargs)


@pytest.mark.parametrize(
    'kwargs',
    (
        {'id': TEST_INSTITUTION_ID, 'name': 'Invalid'},
        {'id': 'invalid'},
        {'name': 'invalid'},
        {'id': TEST_INSTITUTION_ID, 'notname': TEST_INSTITUTION_NAME},
        {'id__in': '45612'},
        {'address': '5'},
        {'unlocode': 'Y'},
        {'latitude': 10},
        {'longitude': 10.0},
        {'altitude': 112},
        {'name': TEST_INSTITUTION_NAME + '2', 'longitude': 0.0, 'latitude': 0, 'unlocode': 'NaY', 'address': 'a45',
         'id': TEST_INSTITUTION_ID},
        {'address': 45},
        {'altitude': '12'},
        {'type': 'different'},
    ),
    ids=['id and name', 'id only', 'name only', 'invalid field', 'id__in with substring', 'invalid address',
         'invalid unlocode', 'invalid latitude', 'invalid longitude', 'invalid altitude', 'invalid all details',
         'passing valid string address as int', 'passing valid number altitude as string', 'different type'],
)
def test_institution_match_fail(institution, institution_all_details, kwargs):
    """
    This test case checks the match function of the institution.
    This test case takes three parameters:
        (i) institution: calls the institution function which returns institution with name, id, and type
        (ii) institution_all_details: calls the institution_all_details function which returns
                                      institution with all details
        (iii) kwargs: takes keyword arguments using this parameter
    This test case passes when match fails.
    """
    assert not institution.match(**kwargs)
    assert not institution_all_details.match(**kwargs)


@pytest.mark.parametrize(
    'kwargs',
    (
        {'id': 123456, 'name': TEST_INSTITUTION_NAME},
        {'id': 123456},
        {'id__in': [123456, 'TEST ID 2']},
        {'id__in': '45612'},
        {'id__in': ''},
        {'id': 123456, 'name': TEST_INSTITUTION_NAME, 'longitude': 0.0, 'latitude': 0, 'unlocode': '0',
         'address': '0', 'altitude': 12},
        {'address': '02'},
        {'unlocode': '02'},
        {'latitude': 10},
        {'longitude': 10.0},
        {'altitude': 10},
        {'address': 0},
        {'unlocode': 0},
        {'altitude': '0'},
        {'type': 'pren'}
    ),
    ids=['id and name', 'id', 'id__in with list', 'id__in with substring', 'id__in empty',
         'invalid id with all valid details', 'invalid address', 'invalid unlocode', 'invalid latitude',
         'invalid longitude', 'invalid altitude', 'passing valid string address as int',
         'passing valid string unlocode as int', 'passing valid int altitude as string', 'different inst. type']
)
def test_institution_id_type_int_match_fail(kwargs):
    """
    This test case checks the match function of the institution. This function takes keyword arguments as parameter by
    using kwargs.
    This test case is basically for institution which has id as a number. This test case passes when match fails.
    """
    # creating institution with id, name and type
    new_institution = Institution(123456, TEST_INSTITUTION_NAME, INSTITUTION_TYPE_DEFAULT)
    # checking match function
    assert not new_institution.match(**kwargs)

    # creating institution with all details
    new_institution_all_details = \
        Institution(123456, TEST_INSTITUTION_NAME, TEST_SHORTNAME, INSTITUTION_TYPE_DEFAULT, 0, 0, 0, '0', '0')
    # checking match function
    assert not new_institution_all_details.match(**kwargs)


def test_institution_eq_success(institution, institution_all_details, institution_with_different_inst_type):
    """
    This test case takes three parameters:
        (i)institution: calls the institution function which returns institution with name, id, and type
        (ii)institution_all_details: calls the institution_all_details function which returns
                                    institution with all details
        (iii)institution_with_different_inst_type: calls the institution_with_different_inst_type function which returns
                                    institution with all details but different institution type
    This test case passes when the two institutions are equal
    """
    new_inst = Institution(id=TEST_INSTITUTION_ID, short_name=TEST_SHORTNAME, name=TEST_INSTITUTION_NAME, institution_type=INSTITUTION_TYPE_DEFAULT)
    # Comparing institution with new_inst
    assert institution == new_inst

    inst_with_default_type = \
        Institution(id=TEST_INSTITUTION_ID, name=TEST_INSTITUTION_NAME, short_name=TEST_SHORTNAME, institution_type=INSTITUTION_TYPE_DEFAULT, longitude=0, latitude=0, altitude=12, unlocode='NY', address='45')
    # comparing inst_with_default_type with institution_all_details
    assert inst_with_default_type == institution_all_details

    inst_with_differ_inst_type = \
        Institution(id=TEST_INSTITUTION_ID, name=TEST_INSTITUTION_NAME, short_name=TEST_SHORTNAME, longitude=0, latitude=0, altitude=12, unlocode='NY', address='45',
                    institution_type='pren')
    # comparing inst_with_differ_inst_type with institution_with_different_inst_type
    assert inst_with_differ_inst_type == institution_with_different_inst_type


def test_institution_eq_fail(institution, institution_all_details, institution_with_different_inst_type):
    """
    This test case takes three parameters:
        (i)institution: calls the institution function which returns institution with name, id, and type
        (ii)institution_all_details: calls the institution_all_details function which returns
                                    institution with all details
        (iii)institution_with_different_inst_type: calls the institution_with_different_inst_type function which returns
                                    institution with all details but different institution type
    This test case passes when the two institutions are not equal
    """
    inst_with_diff_id = Institution(id="Test ID 2", name=TEST_INSTITUTION_NAME)
    inst_with_name_only = Institution(name=TEST_INSTITUTION_NAME, type=INSTITUTION_TYPE_DEFAULT)
    # comparing the above two created institutions with institution
    assert institution != inst_with_diff_id
    assert institution != inst_with_name_only

    # comparing the institutions passed as parameters with each other
    assert institution != institution_with_different_inst_type
    assert institution != institution_all_details
    assert institution_all_details != institution_with_different_inst_type


def test_refine_institution_add_address(institution):
    """
    This test case takes one parameter:
        (i)institution: calls the institution function which returns institution with name, id, and type
    This test case checks the functionality of add_address function of institution.
    """
    address = '110 Queens street'
    addresses = ['45 O\'Corner Street', '55 O\'Corner Street']

    # checking that institution has no address
    assert institution.address is None

    # passing string to the add_address function of institution
    institution.add_address(address)

    # checking passed address is added
    assert institution.address == address

    # passing list of strings to the add_address function of institution
    institution.add_address(addresses)

    # checking passed addresses are added
    assert address in institution.addresses
    assert addresses in institution.addresses


def test_refine_institution_remove_address(institution_all_details):
    """
    This test case takes one parameter:
        (i)institution_all_details: calls the institution_all_details function which returns
                                    institution with all details
    This test case checks the functionality of remove_address function of institution.
    """
    address = '110 Queens street'
    addresses = ['45 O\'Corner Street', '55 O\'Corner Street']

    default_address_of_institution = institution_all_details.address
    # checking that institution has by default address
    assert default_address_of_institution is not None

    # adding address to the institution
    institution_all_details.add_address(address)
    institution_all_details.add_address(addresses)

    # passing string to the remove_address function of institution
    institution_all_details.remove_address(address)

    # checking passed address is removed
    assert address not in institution_all_details.address

    # passing list of strings to the remove_address function of institution
    institution_all_details.remove_address(addresses)

    # checking passed addresses are removed
    assert addresses not in institution_all_details.addresses

    # removing default address of the institution
    institution_all_details.remove_address(address=default_address_of_institution)

    # checking all addresses are removed
    assert len(institution_all_details.addresses) == 0


def test_refine_institution_remove_address_fail(institution_all_details):
    """
    This test case takes one parameter:
        (i)institution_all_details: calls the institution_all_details function which returns
                                    institution with all details
    This test case checks the functionality of remove_address function of institution; when it can raise error
    """
    # checking that institution has address
    assert institution_all_details.address is not None

    # removing unknown address which raises error
    with pytest.raises(ValueError):
        institution_all_details.remove_address('unknown address')

    # passing id as a parameter to the remove address function
    with pytest.raises(TypeError):
        institution_all_details.remove_address(id=TEST_INSTITUTION_ID)

    # passing name as a parameter to the remove address function
    with pytest.raises(TypeError):
        institution_all_details.remove_address(name=TEST_INSTITUTION_NAME)


@pytest.mark.parametrize(
    'args, kwargs',
    (
        ([TEST_INSTITUTION_ID, TEST_INSTITUTION_NAME, TEST_SHORTNAME, ['pRen', 'sren'], 0, 0, 0, 0, 0], {}),
        ([TEST_INSTITUTION_ID], {'name': TEST_INSTITUTION_NAME, 'institution_type': [INSTITUTION_TYPE_DEFAULT, 'sren']}),
    ),
    ids=['args with multiple inst-types', 'kwargs with multi inst-types']
)
def test_inst_type_hold_multiple_values(args, kwargs):
    test_inst = Institution(*args, **kwargs)
    assert len(test_inst.types) > 1


@pytest.mark.parametrize(
    'kwargs',
    (
        {'name': TEST_INSTITUTION_NAME, 'longitude': 0.0, 'latitude': 0, 'unlocode': 'NY', 'address': '45',
         'id': TEST_INSTITUTION_ID, 'types': ['nren', 'sren', 'pren']},
        {'types__contains': 'nren'},
        {'types__contains': ['nren', 'sren']},
        {'types__in': ['nren', 'sren', 'pren', 'jj']},
        {'type__in': ['nren', 'sren', 'pren', 'jj']}
    ),
    ids=['all details', 'types__contains with single value', 'types__contains with types subset', 'types__in',
         'type__in'],
)
def test_institution_with_multiple_inst_type_match_success(institution_with_multiple_inst_type, kwargs):
    """
    This test case checks when the match function of the institution with multiple types passes.
    """
    assert institution_with_multiple_inst_type.match(**kwargs)


@pytest.mark.parametrize(
    'kwargs',
    (
        {'name': TEST_INSTITUTION_NAME, 'longitude': 0.0, 'latitude': 0, 'unlocode': 'NY', 'address': '45',
         'id': TEST_INSTITUTION_ID, 'type': ['nren', 'sren', 'pren']},
        {'type__contains': 'nren'},
        {'type__contains': ['nren', 'sren']},
    ),
    ids=['all details', 'type__contains with single value', 'type__contains with types subset', ],
)
def test_institution_with_multiple_inst_type_match_fail(institution_with_multiple_inst_type, kwargs):
    """
    This test case checks when the match function of the institution with multiple types fails.
    """
    assert not institution_with_multiple_inst_type.match(**kwargs)


def test_institution_with_multi_types_eq_success(institution_with_multiple_inst_type):
    """
    This test case passes when the two institutions are equal
    """
    new_inst = Institution(id=TEST_INSTITUTION_ID, short_name=TEST_SHORTNAME, name=TEST_INSTITUTION_NAME,
                           institution_type=['pren', 'sren', 'nren'], longitude=0, latitude=0, altitude=12,
                           unlocode='NY', address='45')
    # Comparing institution with new_inst
    assert new_inst == institution_with_multiple_inst_type
