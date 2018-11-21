import unittest
import terraform_validate
import os

class TestLtmVirtualServer(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"./")
        self.v = terraform_validate.Validator(self.path)

    def test_create_no_interpolation_virtual_server(self):
        self.v.error_if_property_missing()

        # Virtual Server
        self.v.resources('bigip_ltm_virtual_server').property('name').should_equal('/Common/terraform_vs_http')
        self.v.resources('bigip_ltm_virtual_server').property('source_address_translation').should_equal('automap')

        # Pool
        self.v.resources('bigip_ltm_pool').property('load_balancing_mode').should_equal('round-robin')
        self.v.resources('bigip_ltm_pool').property('allow_snat').should_equal('yes')
        self.v.resources('bigip_ltm_pool').property('allow_nat').should_equal('yes')
        self.v.resources('bigip_ltm_pool').property('monitors').should_equal(["/Common/tcp"])

    def test_create_default_interpolation_virtual_server(self):
        self.v.enable_variable_expansion()
        self.v.error_if_property_missing()

        # Virtual Server
        self.v.resources('bigip_ltm_virtual_server').property('pool').should_equal('dummy-pool')
        self.v.resources('bigip_ltm_virtual_server').property('destination').should_equal('218.108.149.373')
        self.v.resources('bigip_ltm_virtual_server').property('port').should_equal('80')

        # Pool
        self.v.resources('bigip_ltm_pool').property('name').should_equal('dummy-pool')

        # Attachment
        # has not been implemented in Terraform Validator
        # self.v.resources('bigip_ltm_pool_attachment').property('count').should_equal('1')
        self.v.resources('bigip_ltm_pool').property('name').should_equal('dummy-pool')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLtmVirtualServer)
    unittest.TextTestRunner(verbosity=2).run(suite)
