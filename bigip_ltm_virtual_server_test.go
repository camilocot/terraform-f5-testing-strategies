package main

import (
	"fmt"
	"net/http"
	"net/http/httptest"
	"regexp"
	"strings"
	"testing"

	bigip "github.com/f5devcentral/go-bigip"
	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestCreateLtmVirtualServer(t *testing.T) {

	vs := &bigip.VirtualServer{
		Destination: "/Common/100.1.1.102:80",
		Source:      "100.1.1.101/32",
		Pool:        "/Common/terraform-pool",
		Mask:        "255.255.255.255",
	}

	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Header().Set("Content-Type", "application/json")
		if r.Method == "GET" && r.URL.EscapedPath() == "/mgmt/tm/net/self" {
			fmt.Fprint(w, `{"msg": "dummy"}`)
		}
		if strings.HasPrefix(r.URL.EscapedPath(), "/mgmt/tm/ltm/virtual") {
			fmt.Fprintf(w, `{"destination": "%s", "source": "%s", "ipProtocol": "tcp","pool": "%s", "mask": "%s"}`, vs.Destination, vs.Source, vs.Pool, vs.Mask)
		}

	}))
	defer server.Close()

	terraformOptions := &terraform.Options{
		TerraformDir: "./",
		Vars: map[string]interface{}{
			"pool":        vs.Pool,
			"destination": vs.Destination,
		},
		EnvVars: map[string]string{
			"BIGIP_HOST":     server.URL,
			"BIGIP_USER":     "admin",
			"BIGIP_PASSWORD": "admin",
		},
		NoColor: true,
	}
	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	actualVsSource := terraform.Output(t, terraformOptions, "source")
	assert.Equal(t, vs.Source, actualVsSource)

	actualVsDestination := terraform.Output(t, terraformOptions, "destination")
	// Extract destination address from "/partition_name/(virtual_server_address)[%route_domain]:port"
	regex := regexp.MustCompile(`(\/.+\/)((?:[0-9]{1,3}\.){3}[0-9]{1,3})(?:\%\d+)?(\:\d+)`)
	expectedDestination := regex.FindStringSubmatch(vs.Destination)
	assert.Equal(t, expectedDestination[2], actualVsDestination)
}
