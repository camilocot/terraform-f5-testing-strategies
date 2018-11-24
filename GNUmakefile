.PHONY: test dep

test:
	go test -v -timeout 30m
deps:
	go get -u github.com/golang/dep/cmd/dep
	dep ensure -v
