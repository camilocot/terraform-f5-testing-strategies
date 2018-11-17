variable "pool" {
  default = "dummy-pool"
}
variable "destination" {
  default = "218.108.149.373"
}

resource "bigip_ltm_virtual_server" "http" {
  pool                       = "${var.pool}"
  name                       = "/Common/terraform_vs_http"
  destination                = "${var.destination}"
  port                       = 80
  source_address_translation = "automap"
}

output "source" {
  value = "${bigip_ltm_virtual_server.http.source}"
}
output "destination" {
  value = "${bigip_ltm_virtual_server.http.destination}"
}
