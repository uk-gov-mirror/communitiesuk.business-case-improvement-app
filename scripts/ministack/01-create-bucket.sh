#!/bin/sh
set -eu

aws --endpoint-url=http://localhost:4566 s3 mb "s3://${AWS_STORAGE_BUCKET_NAME}"
