#!/bin/bash

curl -v -X POST \
	-d '{"to":["brian.refsdal@gmail.com"],"subject":"test mandrill","text":"This is a test for mandrill"}' \
	http://localhost:8000/send
