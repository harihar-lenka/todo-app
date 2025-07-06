provider "aws" {
  region = "us-east-1"
}

# S3 Bucket for Frontend
resource "aws_s3_bucket" "frontend" {
  bucket = "todo-app-frontend"
  tags   = { Name = "todo-frontend" }
}

resource "aws_s3_bucket_ownership_controls" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket                  = aws_s3_bucket.frontend.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_acl" "frontend" {
  depends_on = [aws_s3_bucket_ownership_controls.frontend]
  bucket     = aws_s3_bucket.frontend.id
  acl        = "public-read"
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html"
  }
}

resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.frontend.arn}/*"
      }
    ]
  })
}

# DynamoDB Table
resource "aws_dynamodb_table" "todos" {
  name         = "todos"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name = "todo-table"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "todo_lambda_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "dynamodb_access" {
  name = "DynamoDBAccess"
  role = aws_iam_role.lambda_role.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:PutItem",
        "dynamodb:Scan",
        "dynamodb:GetItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem"
      ]
      Resource = aws_dynamodb_table.todos.arn
    }]
  })
}

# Lambda Function
resource "aws_lambda_function" "todo_lambda" {
  filename         = "../backend/lambda_package.zip"
  function_name    = "todo_lambda"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.9"
  source_code_hash = filebase64sha256("../backend/lambda_package.zip")
  environment {
    variables = {
      AWS_REGION = "us-east-1"
      TABLE_NAME = "todos"
    }
  }
}

# API Gateway
resource "aws_api_gateway_rest_api" "todo_api" {
  name = "todo-api"
}

resource "aws_api_gateway_resource" "todos" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  parent_id   = aws_api_gateway_rest_api.todo_api.root_resource_id
  path_part   = "todos"
}

resource "aws_api_gateway_method" "get_todos" {
  rest_api_id   = aws_api_gateway_rest_api.todo_api.id
  resource_id   = aws_api_gateway_resource.todos.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "post_todos" {
  rest_api_id   = aws_api_gateway_rest_api.todo_api.id
  resource_id   = aws_api_gateway_resource.todos.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_todos_integration" {
  rest_api_id             = aws_api_gateway_rest_api.todo_api.id
  resource_id             = aws_api_gateway_resource.todos.id
  http_method             = aws_api_gateway_method.get_todos.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.todo_lambda.invoke_arn
}

resource "aws_api_gateway_integration" "post_todos_integration" {
  rest_api_id             = aws_api_gateway_rest_api.todo_api.id
  resource_id             = aws_api_gateway_resource.todos.id
  http_method             = aws_api_gateway_method.post_todos.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.todo_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "todo_api_deployment" {
  rest_api_id = aws_api_gateway_rest_api.todo_api.id
  depends_on = [
    aws_api_gateway_integration.get_todos_integration,
    aws_api_gateway_integration.post_todos_integration
  ]
}

resource "aws_api_gateway_stage" "prod" {
  rest_api_id   = aws_api_gateway_rest_api.todo_api.id
  deployment_id = aws_api_gateway_deployment.todo_api_deployment.id
  stage_name    = "prod"
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.todo_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.todo_api.execution_arn}/*/*"
}

# Outputs
output "s3_website_url" {
  value = aws_s3_bucket_website_configuration.frontend.website_endpoint
}
output "api_gateway_url" {
  value = "${aws_api_gateway_deployment.todo_api_deployment.invoke_url}/${aws_api_gateway_stage.prod.stage_name}/todos"
}
output "dynamodb_table_name" {
  value = aws_dynamodb_table.todos.name
}
