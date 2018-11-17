# terraform-f5-testing-strategies
Terraform testing strategies for F5 provider

## Policy enforcement for Terraform

Assert that all terraform resources in the configuration folder meet the user-defined standards. Mainly that default values are the right ones and the properties are defined.

```bash
mkvirtualenv terraform_validate
pip install -r requirements.txt
python bigip_ltm_virtual_server_test.py
```
## Automated deployment in a mock environment

Automated tests for f5 infrastructure using mocking the F5 iControl REST API.

```bash
go test ./...
```
## Testing libraries
- [terraform_validate](https://github.com/elmundio87/terraform_validate)
- [terratest](https://github.com/gruntwork-io/terratest)

## Reference
- [Go Client to interact with F5 BIG-IP systems using the REST API](https://github.com/scottdware/go-bigip)
- [Terraform F5 BigIP provider](https://github.com/terraform-providers/terraform-provider-bigip)
