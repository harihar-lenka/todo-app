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

Overview of the Web Application

Frontend: React app hosted on an S3 bucket with static website hosting.
Backend: Flask API on ECS Fargate, interacting with DynamoDB.
Database: DynamoDB table for to-do items.
Infrastructure: AWS S3 for frontend, ECS Fargate for backend, DynamoDB, managed by Terraform.
CI/CD: GitHub Actions to build and deploy frontend to S3 and backend to ECS.
Monitoring: Prometheus and Grafana (unchanged, monitoring backend only).
Tools: VS Code, Terraform, AWS, GitHub, Python, Bash, HTML, Docker (unchanged).

Step-by-Step Guide
Step 1: Set Up Your Development Environment on Windows

Install VS Code:
    Download and install Visual Studio Code from code.visualstudio.com.
    Open VS Code and install extensions:
    Python (by Microsoft) for Python development.
    Docker (by Microsoft) for Docker support.
    Terraform (by HashiCorp) for syntax highlighting.
    React Snippets for frontend development.
    Install Python:
    Download Python 3.9+ from python.org and install it. Check "Add Python to PATH" during installation.
    Verify installation by opening Command Prompt (cmd) and running:
        python --version


Install pip (Python package manager) if not included:
Verify installation:
        python -m ensurepip --upgrade
        python -m pip install --upgrade pip


Install Node.js (for React):
Download and install Node.js (LTS version) from nodejs.org.
Verify installation:
        node --version
        npm --version


Install Docker Desktop:
Download Docker Desktop for Windows from docker.com/products/docker-desktop.
Install and enable WSL 2 (Windows Subsystem for Linux) as prompted.
Verify installation:

        docker --version


Install Terraform:
Download the Terraform binary for Windows from terraform.io/downloads.html.
Extract the terraform.exe to C:\Terraform.
Add C:\Terraform to your system PATH:
Search for "Environment Variables" in Windows, select "Edit the system environment variables."
In "System Properties," click "Environment Variables," edit "Path," and add C:\Terraform.
Verify:

        terraform -version



Install Git (for GitHub):
Download and install Git for Windows from git-scm.com/download/win.
Verify:

        git --version


Install AWS CLI:
Download and install AWS CLI for Windows from aws.amazon.com/cli.
Verify:

        aws --version

Set Up Bash:
Use Git Bash (installed with Git) for Bash scripting.
Verify:

    bash --version


Configure AWS CLI:
Create an AWS IAM user with programmatic access (in AWS Console, go to IAM > Users > Add User, enable "Programmatic access").
Save the Access Key ID and Secret Access Key.
Configure AWS CLI:

        aws configure
    Enter your Access Key, Secret Key, region (e.g., us-east-1), and output format (json).


Set Up GitHub:
Create a GitHub account at github.com.
