# Project Overview
- `lambda_function.py` holds the Python code where the handler of the Lambda function is defined.
- `deploy.yml` holds the GitHub workflow that automates the deployment.
- `deploy_hello_world.yml` holds the CloudFormation template that specifies the infrastructure.

GitHub Actions are used to trigger a workflow on every commit to the main branch.
The workflow zips the Python code used for the handler of the Lambda function and then uses an AWS CloudFormation script to deploy it. 
AWS S3 is used to store versions of the zipped Python file that contains the handler for the Lambda function.
AWS CloudFormation is used to provide Infrastructure as Code and to make the setup reproducible and maintainable.
AWS Lambda and API Gateway are used to create the serverless solution, as both services are inherently scalable and highly available.
AWS CloudWatch is used for monitoring - it allows for an easy way to view the logs, as well as for setting up automatic alarms in case of errors.

# Testing the Ready Solution
The Lambda function is deployed to this URL: https://ryq6wwm4gj.execute-api.eu-west-2.amazonaws.com/prod/hello
If you would like to have access to the repository in which I have set up the pipeline, I would be more than happy to grant you access. Just give me your email :) 

# Note on Security and Best Practices
The process outlined below does not conform to AWS security best practices. It creates an AWS IAM User with permanent access keys, which are then used to give programmatic AWS access to GitHub. This is not recommended, as the permanent keys are a security risk. A better approach would be to use IAM roles and set up an OIDC provider that can generate temporary credentials for the GitHub actions. Furthermore, the permissions granted to the IAM User are broader than strictly needed. In a production environment, I would ensure that the role created has only the permissions it needs. AWS provides a lot more granular control over permissions; however, I am using their presets for simplicity, even though they are too broad. 
All of the above is due to time constraints.

# Pre-requisites for Replicating the Solution

- An AWS account
- A GitHub account 
- The `deploy_hello_world.yml` file saved on your local machine
- The `lambda_function.py` saved on your local machine
- The `deploy.yml` file saved on your local machine

# Steps for Replicating the Solution
Creating the S3 Bucket
- Navigate to AWS -> Amazon S3 -> Buckets.
- Press on "Create Bucket."
- Enter a Name for the bucket, enable Bucket Versioning, scroll down, and press "Create bucket."
  
Creating the AWS IAM User That Will Be Used by the GitHub Actions
- Navigate to AWS -> IAM -> Users.
- Press on "Create User."
- Add a Name for the new User and press Next.
- In the Permissions Options, select "Attach policies directly." Note that this is done here for simplicity. In a real production environment, it is generally better to manage permissions using groups, as it provides a reproducible, clearer, centralized way to manage permissions.
- Add the following permissions to the user:
    - AWSCodePipeline_FullAccess
    - AWSCodeCommitFullAccess
    - AWSCodeBuildAdminAccess
    - AWSCloudFormationFullAccess
    - AmazonAPIGatewayAdministrator
    - IAMFullAccess
    - AmazonSNSFullAccess
    - CloudWatchFullAccess
    - AWSLambda_FullAccess
    - AmazonS3FullAccess
- Press Next and "Create User."
- Select the new user, navigate to "Security Credentials," and press "Create Access Keys."
- Select "Other" and press "Next."
- Save the Access Key ID and the Secret Access Key in a secure location on your machine. Note that you will not be able to view the secret access key at a later point.

Creating the GitHub Repository
- Navigate to GitHub and create a new private repository.
- Navigate to your GitHub repository -> Settings -> Secrets and Variables.
- Create new secrets `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` and provide the values you got from AWS.
- Create a new variable `S3_BUCKET_NAME` and provide the name of the S3 bucket you created earlier.
- Create a new variable `S3_KEY` and enter `lambda_function.zip`.
- Create a new variable `ALERT_EMAIL` and provide the email address that you wish to be subscribed to the automated CloudWatch Alarms.

Adding the Necessary Files to the Repository (Instructions for creating an SSH key are for MacOS)
- Open a terminal.
- Create a new SSH key by running ```ssh-keygen -t ed25519 -C "your_email@example.com"```.
- Start the SSH agent by running ```eval "$(ssh-agent -s)"```.
- Add your private key to the agent by running ```ssh-add ~/.ssh/id_ed25519```.
- Navigate to GitHub -> Settings -> SSH and GPG Keys.
- Press on "New SSH Key," add the contents of `id_ed25519.pub`, and press "Add SSH Key."
- Copy the SSH URL of the repository and clone it locally by running ```git clone “git@github.com:YourName/YourRepository.git”```.
- Inside the repository, create a `.github/workflows` directory and copy the `deploy.yml` file into it.
- Copy the `lambda_function.py` and the `deploy_hello_world.yml` files into the repository.
- Commit and push.

Testing the New Endpoint
- Navigate to AWS -> CloudFormation -> Stacks.
- Press on "HelloWorldStack" -> Outputs.
- You should be able to see the URL on which the endpoint is deployed.

Monitoring
- Besides the configured Alarms, you can view the logs of the Lambda function.
- Navigate to AWS -> CloudWatch -> Log Groups.
- Select the group that was created for the new stack (its name will start with "/aws/lambda/HelloWorldStack").
- Press on the Log Stream.

# Room for Improvements (Including, but Not Limited To)
- Proper setup for granting AWS access to the GitHub actions, as explained above.
- Registering the function to a more user-friendly URL using AWS Route 53 to configure the DNS.
- Implementing HTTPS by setting up SSL/TLS certificates using AWS Certificate Manager.
- Making the function available in other regions besides by deploying the Stack in them as well.
