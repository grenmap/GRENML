import pytest
from grenml import managers
from grenml.models import Institution, Node, meta

TEST_NODE_ID_CUSTOM = 'TEST_NODE_ID'
TEST_NODE_ID_DET = '77ec8a45e8dd685d7a85a8f41c6598a95a895ef1991927a663b09276f5ea3231'
TEST_NODE_NAME = 'TEST_NODE_NAME'
TEST_INSTITUTION_ID_CUST = 'TEST_ID1'
TEST_INSTITUTION_ID_DET = '17f5f49420c8d9d329d100af7588b2bcc3da5e15fbb38be34832fd684affd2ad'
TEST_INSTITUTION_NAME = 'TEST_NAME1'


class TestIDGeneration:
    @pytest.fixture
    def manager(self):
        return managers.GRENMLManager('TEST_TOPOLOGY')

    def test_node_id_default_eq(self):
        """
        Test that two nodes with the same details generate the same id and are equal, using
        default id generation scheme
        """
        node_1 = Node(id=None, name='TEST_NODE_NAME')
        assert node_1.id == TEST_NODE_ID_DET

        node_1_replica = Node(id=None, name=TEST_NODE_NAME)
        assert node_1_replica.id == TEST_NODE_ID_DET

        assert node_1 == node_1_replica

    def test_node_id_default_custom_eq(self):
        """
        Test that two nodes with the same details and with a custom id are equal, using
        default id generation scheme
        """
        node_1 = Node(id=TEST_NODE_ID_CUSTOM, name='TEST_NODE_NAME')
        assert node_1.id == TEST_NODE_ID_CUSTOM

        node_1_replica = Node(id='TEST_NODE_ID', name=TEST_NODE_NAME)
        assert node_1_replica.id == TEST_NODE_ID_CUSTOM

        assert node_1 == node_1_replica

    def test_node_id_det_eq(self):
        """
        Test that two nodes with the same details generate the same id and are equal
        """
        node_1 = Node(id=None, name='TEST_NODE_NAME', id_format=meta.IDGeneration.DETERMINATE)
        assert node_1.id == TEST_NODE_ID_DET

        node_1_replica = Node(id=None, name=TEST_NODE_NAME,
                              id_format=meta.IDGeneration.DETERMINATE)
        assert node_1_replica.id == TEST_NODE_ID_DET

        assert node_1 == node_1_replica

    def test_node_id_rnd_eq_fail(self):
        """
        Test that two nodes with the same details, but with random id generation,
         generates different ids and are equal
        """
        node_1 = Node(id=None, name='TEST_NODE_NAME', id_format=meta.IDGeneration.RANDOM)
        node_1_replica = Node(id=None, name=TEST_NODE_NAME, id_format=meta.IDGeneration.RANDOM)

        assert node_1 != node_1_replica

    def test_node_inst_id_det_eq_fail(self):
        """
        Test that a node and an institution with the same details generate different ids and
        are not equal
        """
        node_1 = Node(id=None, name='TEST_NODE_NAME', id_format=meta.IDGeneration.DETERMINATE)
        assert node_1.id == TEST_NODE_ID_DET

        inst_1 = Institution(id=None, name=TEST_INSTITUTION_NAME,
                             id_format=meta.IDGeneration.DETERMINATE)
        assert inst_1.id == TEST_INSTITUTION_ID_DET

        assert node_1 != inst_1

    def test_node_id_extra_details_diff_id_eq_fail(self):
        """
        Test that nodes with extra details, that affect the det. id, generate different ids
        and are not equal
        """

        node_1 = Node(id=None, name='TEST_NODE_NAME')
        assert node_1.id == TEST_NODE_ID_DET

        node_1_short_name = Node(id=None, name='TEST_NODE_NAME', short_name='NODE_NAME')
        assert node_1_short_name.id == '7cbdb669c41644ca5547f4565fa27c3433dcefdfd0c721384ab52831603c2b4d'
        assert node_1 != node_1_short_name

    def test_node_id_extra_details_same_id_eq_fail(self):
        """
        Test that nodes with extra details, that don't affect the det. id, generate different
        ids and are not equal
        """

        node_1 = Node(id=None, name=TEST_NODE_NAME)
        assert node_1.id == TEST_NODE_ID_DET

        node_1_address = Node(id=None, name=TEST_NODE_NAME, address='NODE_ADDRESS')
        assert node_1_address.id == TEST_NODE_ID_DET

        assert node_1 != node_1_address

    def test_manager_node_id(self, manager):
        """
        Test that a GRENMLManager will create a new node with the correct id
        """
        node_id = manager.add_node(id=None, name=TEST_NODE_NAME)
        assert node_id == TEST_NODE_ID_DET
