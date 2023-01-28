# Devops-cloudformation

End-to-end AWS DevOps project for automatically storing Excel document data uploaded to S3 in a DynamoDB database.

Project consists of the following components:
- Lambda Function written in Python
- Cloudformation template, which triggers the creation of the necessary resources (S3 bucket, Lambda Function, DynamoDB database) including all the appropriate roles, policies and permissions compliant to AWS best practices.
- Jenkins Pipeline for CI/CD. This triggers the creation (or updation) of the Cloudformation Template on source changes. Includes testing (Pytest), a quality gate (SonarQube) and  integration with Google Chat for job approval and notifications.
