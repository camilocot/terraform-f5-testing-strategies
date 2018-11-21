variable "pool" {
  default = "dummy-pool"
}

variable "destination" {
  default = "218.108.149.373"
}

variable "nodes" {
  type = "map"

  default = {
    # node0 = "10.10.10.10",
  }
}

variable port {
  default = "80"
}

resource "bigip_ltm_virtual_server" "http" {
  pool                       = "${var.pool}"
  name                       = "/Common/terraform_vs_http"
  destination                = "${var.destination}"
  port                       = "${var.port}"
  source_address_translation = "automap"
}

resource "bigip_ltm_pool" "pool" {
  name                = "${var.pool}"
  load_balancing_mode = "round-robin"
  monitors            = ["/Common/tcp"]
  allow_snat          = "yes"
  allow_nat           = "yes"
}

resource "bigip_ltm_pool_attachment" "attach_node" {
  count      = "${length(keys(var.nodes))}"
  pool       = "${var.pool}"
  node       = "/Common/${element(values(var.nodes), count.index)}:${var.port}"
  depends_on = ["bigip_ltm_pool.pool"]
}

output "pool_name" {
  value = "${bigip_ltm_pool.pool.name}"
}

output "vs_source" {
  value = "${bigip_ltm_virtual_server.http.source}"
}

output "vs_destination" {
  value = "${bigip_ltm_virtual_server.http.destination}"
}

output "pool_attachment_nodes" {
  value = ["${bigip_ltm_pool_attachment.attach_node.*.node}"]
}
