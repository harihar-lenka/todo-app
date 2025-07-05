<!-- Directory Layout -->

aws-FULLSTACK-TODO-APP/
├── backend/
│   ├── applambda_function.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── prometheus.yml
├── frontend/
│   ├── index.html
│   └── Dockerfile
├── docker-compose.yml
└── terraform/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── user_data.sh


Let’s create a simple web application on the AWS Free Tier, complete with a front-end, back-end, and database, using the tools

1. VS Code
2. Terraform,
3. AWS,
4. GitHub + GitHub Actions,
5. Prometheus,
6. Grafana,
7. Python + HTML,
8. Docker.

The app will be a basic to-do list, where users can add and view tasks, with the 
    **front-end hosted on Amazon S3, 
    the back-end on AWS Lambda via API Gateway, 
    and the database on DynamoDB, all within the AWS Free Tier.**
    set up monitoring with Prometheus and Grafana and automate deployment with GitHub Actions.

**Overview of the Web Application**
Front-End: A simple HTML page (with JavaScript for interactivity) hosted on Amazon S3, serving as a static website.
Back-End: A Python-based AWS Lambda function, exposed via API Gateway, to handle CRUD operations (create, read) for the to-do list.
Database: Amazon DynamoDB to store tasks.
Infrastructure: Provisioned using Terraform for reproducibility.
CI/CD: GitHub Actions to automate building, testing, and deploying the app.
Monitoring: Prometheus to collect metrics from the back-end, visualized in Grafana.
Development Environment: VS Code for coding, with Bash scripts for local setup and Docker for containerized testing.

**Prerequisites**
Before starting, ensure you have:

An AWS Free Tier account (sign up at aws.amazon.com; the Free Tier includes 750 hours of EC2 t2.micro, 5GB S3 storage, 1M Lambda requests, and 25GB DynamoDB storage monthly).
    VS Code installed (download from code.visualstudio.com).
    Git installed (git-scm.com) and a GitHub account (github.com).
    Docker Desktop installed (docker.com) for containerized testing.
    Terraform installed (hashicorp.com; follow their guide for your OS).
    AWS CLI installed (aws.amazon.com/cli) and configured with credentials (aws configure with your Access Key and Secret Key from AWS IAM).
A basic understanding of command-line usage

**Step-by-Step Guide**
    **Step 1**: Set Up Your Development Environment in VS Code
        Install VS Code Extensions:
        Open VS Code.
        Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X on Mac).
        Install:
            AWS Toolkit: For AWS integration.
            HashiCorp Terraform: For Terraform syntax highlighting and validation.
            Python: For Python development.
            Docker: For Docker file support.
            GitHub Pull Requests and Issues: For GitHub integration.

