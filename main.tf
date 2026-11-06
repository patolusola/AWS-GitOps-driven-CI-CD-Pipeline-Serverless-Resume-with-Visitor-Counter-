# this is to signify that i am building in aws, us east to be precise.
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # here is my terraform memory bank
  backend "s3" {
    bucket = "pat-terraform-memory-bank" 
    key    = "state/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = "us-east-1" 
}

# my s3 bucket (it hosts my website's code and images)
resource "aws_s3_bucket" "frontend_bucket" {
  bucket = "pat-gitops-driven-project-bucket"
}

# my DynamoDB table (sort of a digital notebook where my app stores info)
resource "aws_dynamodb_table" "backend_database" {
  name           = "serverless-database"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S" # 'S' stands for String (text)
  }
}


# this sets up the iam permission so my app's brainbox can function
resource "aws_iam_role" "lambda_role" {
  name = "serverless_lambda_role"
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

# this gives the brainbox permission to record logs
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# this puts the brainbox in a zip file
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/backend"
  output_path = "${path.module}/backend.zip"
}

# here comes the main guy , my brainbox itself (aws lambda function)
resource "aws_lambda_function" "backend_brain" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "my_backend_brain"
  role             = aws_iam_role.lambda_role.arn
  handler          = "main.handler" # this directs it to main.py
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime          = "python3.9" # the language the brainbox speaks
}


# the lambda function url
resource "aws_lambda_function_url" "brain_door" {
  function_name      = aws_lambda_function.backend_brain.function_name
  authorization_type = "NONE" # this makes it accessible by anyone on the internet
}

# this is the access point of my function
output "brain_door_address" {
  value = aws_lambda_function_url.brain_door.function_url
}


# this is to inform aws the bucket would be hosting a website
resource "aws_s3_bucket_website_configuration" "frontend_website" {
  bucket = aws_s3_bucket.frontend_bucket.id
  index_document {
    suffix = "index.html"
  }
}

# this turns off security locks  
resource "aws_s3_bucket_public_access_block" "public_access" {
  bucket                  = aws_s3_bucket.frontend_bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# this allows public access and permission to read the files
resource "aws_s3_bucket_policy" "public_read" {
  bucket = aws_s3_bucket.frontend_bucket.id
  depends_on = [aws_s3_bucket_public_access_block.public_access]
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.frontend_bucket.arn}/*"
      }
    ]
  })
}


# this opens the brain's door for the public access
resource "aws_lambda_permission" "allow_public_brain_door" {
  statement_id           = "AllowPublicInvoke"
  action                 = "lambda:InvokeFunctionUrl"
  function_name          = aws_lambda_function.backend_brain.function_name
  principal              = "*"
  function_url_auth_type = "NONE"
}