#!/bin/sh
set -eu

ENDPOINT="http://localhost:4566"
FUNCTION_NAME="process-business-case-response"
SOURCE_DIR="/lambdas/process_business_case_response"
PROJECT_SOURCE_DIR="/lambda_project_src"
BUILD_DIR="/tmp/${FUNCTION_NAME}-build"
ZIP_PATH="/tmp/${FUNCTION_NAME}.zip"

python3 -m pip --version >/dev/null 2>&1 || python3 -m ensurepip --default-pip >/dev/null 2>&1

rm -rf "$BUILD_DIR" "$ZIP_PATH"
mkdir -p "$BUILD_DIR"
cp -r "$SOURCE_DIR"/* "$BUILD_DIR"/
cp -r "$PROJECT_SOURCE_DIR"/apps "$BUILD_DIR"/
cp -r "$PROJECT_SOURCE_DIR"/config "$BUILD_DIR"/

if [ -f "$BUILD_DIR/requirements.txt" ]; then
    python3 -m pip install --no-cache-dir --target "$BUILD_DIR" -r "$BUILD_DIR/requirements.txt"
fi

python3 - "$BUILD_DIR" "$ZIP_PATH" <<'PY'
import sys
import zipfile
from pathlib import Path

build_dir, zip_path = Path(sys.argv[1]), sys.argv[2]

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
    for path in build_dir.rglob("*"):
        if path.is_file():
            zip_file.write(path, path.relative_to(build_dir))
PY

if aws --endpoint-url="$ENDPOINT" lambda get-function --function-name "$FUNCTION_NAME" >/dev/null 2>&1; then
    aws --endpoint-url="$ENDPOINT" lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --zip-file "fileb://${ZIP_PATH}" \
        >/dev/null
else
    aws --endpoint-url="$ENDPOINT" lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime python3.13 \
        --role arn:aws:iam::000000000000:role/lambda-local-role \
        --handler lambda_function.lambda_handler \
        --environment "Variables={DB_HOST=${DB_HOST},DB_PORT=${DB_PORT},DB_NAME=${DB_NAME},DB_USER=${DB_USER},DB_PASSWORD=${DB_PASSWORD},DJANGO_SETTINGS_MODULE=config.settings,SECRET_KEY=${SECRET_KEY},AWS_S3_ENDPOINT_URL=${ENDPOINT},AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID},AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY},AWS_S3_REGION_NAME=${MINISTACK_REGION},AWS_STORAGE_BUCKET_NAME=${AWS_STORAGE_BUCKET_NAME}}" \
        --zip-file "fileb://${ZIP_PATH}" \
        >/dev/null
fi

aws --endpoint-url="$ENDPOINT" lambda wait function-updated --function-name "$FUNCTION_NAME"

LAMBDA_ARN=$(aws --endpoint-url="$ENDPOINT" lambda get-function \
    --function-name "$FUNCTION_NAME" \
    --query 'Configuration.FunctionArn' \
    --output text)

aws --endpoint-url="$ENDPOINT" lambda add-permission \
    --function-name "$FUNCTION_NAME" \
    --statement-id s3-invoke-business-case-uploads \
    --action lambda:InvokeFunction \
    --principal s3.amazonaws.com \
    --source-arn "arn:aws:s3:::${AWS_STORAGE_BUCKET_NAME}" \
    >/dev/null 2>&1 || true

aws --endpoint-url="$ENDPOINT" s3api put-bucket-notification-configuration \
    --bucket "$AWS_STORAGE_BUCKET_NAME" \
    --notification-configuration '{
        "LambdaFunctionConfigurations": [
            {
                "LambdaFunctionArn": "'"${LAMBDA_ARN}"'",
                "Events": ["s3:ObjectCreated:*"]
            }
        ]
    }'
