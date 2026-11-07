# Fully Automated GitOps-driven Serverless Cloud Engineer Portfolio With Dynamic Visitor Counter

This project is a fully automated deployment pipeline that provisions a multi-environment serverless web application deployed on Amazon Web Services (AWS). This project demonstrates Infrastructure as Code (IaC), CI/CD automation, and serverless backend API integration.

## 🏗️ Architecture Overview

I built this project utilising a 100% serverless architecture, which ensures high availability, zero server maintenance, and seamless scalability.

Frontend - Hosted on Amazon S3 buckeet (Static Website Hosting).
Backend API - Made use of AWS Lambda via Function URLs (Python).
Database - Amazon DynamoDB (NoSQL).
Infrastructure as Code (IaC) - Terraform (with S3 Remote State).
CI/CD Pipeline - GitHub Actions.

## ✨ Key Features

Dynamic Visitor Counter - A full-stack feature where the frontend JavaScript fetches live data from an AWS Lambda Function URL. The Lambda function reads/updates a persistent visitor tally in DynamoDB and returns the value to the DOM.
Automated CI/CD (GitOps) - Every push to the repository triggers a GitHub Actions workflow that automatically provisions infrastructure changes via Terraform and syncs the latest frontend assets to the S3 bucket.
Infrastructure as Code (IaC) - Entire AWS environment (S3 buckets, DynamoDB tables, Lambda functions, IAM roles, and policies) is defined, deployed, and managed using Terraform.
Terraform Remote State: Utilizes a dedicated S3 bucket (`terraform.tfstate`) to maintain remote state, preventing concurrency issues and deployment amnesia.
Responsive UI with Theme Toggle: A professional, fully responsive frontend featuring a custom Dark/Light mode toggle built with vanilla HTML, CSS, and JavaScript.

## 🛠️ Tech Stack

Cloud Provider - Amazon Web Services (AWS - `us-east-1`)
Core Services - S3, Lambda, DynamoDB, IAM
Backend Language - Python 3.9 (Boto3)
Frontend Languages - HTML5, CSS3, JavaScript (Vanilla)
IaC Tool - HashiCorp Terraform
Version Control & CI/CD - Git, GitHub Actions

## 🚀 How It Works Under the Hood

1. The Knock (Frontend) - When a user visits the portfolio, the browser triggers `script.js`, which sends an asynchronous `fetch()` request to the Lambda Function URL.
2. The Bouncer (Lambda Logic) - The Python code first checks if the request is a ghost knock for a `/favicon.ico`. If it is, it ignores it to prevent double-counting. 
3. The Ledger (DynamoDB) - If valid, Lambda uses the `boto3` library to execute an atomic `UpdateItem` request, incrementing the `visit_count` attribute by 1. (Note: I avoided the reserved word `views` to prevent ValidationExceptions!)
4. The Delivery - The updated count is returned to the frontend via a JSON payload, utilizing Terraform-configured CORS headers to bypass browser security blocks safely.

## 🔐 Security & IAM

Security is handled following the Principle of Least Privilege:
- The Lambda function executes under a custom IAM role that only grants `AWSLambdaBasicExecutionRole` and strict `dynamodb:UpdateItem` / `dynamodb:GetItem` access to the specific DynamoDB table ARN.
- Public invocation of the Lambda function is controlled through an explicitly defined `aws_lambda_permission` resource.
- Cross-Origin Resource Sharing (CORS) is handled dynamically at the IaC level to prevent header duplication.

## 🧠 Key Learnings & Challenges Overcome

CORS Duplication - Resolved a `502 Bad Gateway` and `*, *` origin error by delegating CORS header management strictly to the Terraform Function URL resource rather than the Python payload.
DynamoDB Reserved Words - Debugged an `Internal Server Error` crash caused by attempting to use `views` as a database attribute (which is a reserved DynamoDB keyword) by migrating the schema to `visit_count`.
State Management - Implemented an S3 backend for Terraform to resolve `ResourceInUseException` and `BucketAlreadyExists` errors, ensuring the CI/CD pipeline correctly identifies existing infrastructure on subsequent runs.
Cache Busting - Implemented versioned query parameters (`?v=2`) to force browsers to pull the latest JavaScript logic during rapid deployment cycles.


Created by PAT Olusola