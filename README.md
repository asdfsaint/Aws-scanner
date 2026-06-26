AWS Security Scanner

A Python tool that scans an AWS account for common S3 misconfigurations.
Built as a hands-on portfolio project to apply cloud security concepts in code.

What it checks right now:

S3 public access block settings (BlockPublicAcls, IgnorePublicAcls,
BlockPublicPolicy, RestrictPublicBuckets), S3 bucket encryption (flags
buckets with no server-side encryption configured), and more checks
coming as the project grows.

Requirements

Python 3, boto3, and an AWS IAM user with ReadOnly access configured
via aws configure.

Setup

Clone the repo, create a virtual environment with python -m venv venv,
activate it, and run pip install boto3. Make sure your AWS credentials
are configured before running. aws configure to configure your aws credentials

Usage

python3 AWScanner.py

Output shows PASS or FAIL for each check on each bucket. Designed to
be easy to read at a glance.

Note: Never commit AWS credentials. The .gitignore covers .env and
.aws but double check before pushing.
