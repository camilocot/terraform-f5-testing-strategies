import unittest
import terraform_validate
import os

class TestLtmVirtualServer(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"./")
        self.v = terraform_validate.Validator(self.path)

    def test_create_no_interpolation_virtual_server(self):
        self.v.error_if_property_missing()
        self.v.resources('bigip_ltm_virtual_server').property('pool').should_equal('${var.pool}')
        self.v.resources('bigip_ltm_virtual_server').property('name').should_equal('/Common/terraform_vs_http')
        self.v.resources('bigip_ltm_virtual_server').property('destination').should_equal('${var.destination}')
        self.v.resources('bigip_ltm_virtual_server').property('port').should_equal('80')
        self.v.resources('bigip_ltm_virtual_server').property('source_address_translation').should_equal('automap')

    def test_create_default_interpolation_virtual_server(self):
        self.v.enable_variable_expansion()
        self.v.resources('bigip_ltm_virtual_server').property('pool').should_equal('dummy-pool')
        self.v.resources('bigip_ltm_virtual_server').property('destination').should_equal('218.108.149.373')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLtmVirtualServer)
    unittest.TextTestRunner(verbosity=2).run(suite)
