#!/bin/bash

curl -d "{\"Id\": \"$1\", \"TotalParts\": 2,\"PartNumber\": $2, \"Data\": \"$3\" }" -XPOST https://mmm1sky3wf.execute-api.eu-central-1.amazonaws.com/prod/-
