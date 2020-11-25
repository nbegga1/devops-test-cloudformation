pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        AWS_REGION = 'us-east-1'
    }

    stages{

        stage("list-stacks"){

            steps{
                sh 'aws cloudformation describe-stacks --region $AWS_REGION --stack-name test'
            }
        }

        stage("deploy"){

            steps{
                echo 'deploy app...'
            }
        }
    }
}


