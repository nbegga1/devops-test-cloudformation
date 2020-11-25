pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        AWS_REGION = 'us-east-1'
        STACK_NAME = 's3-test'
    }

    stages{

        stage("list-stacks"){

            steps{
                sh 'aws cloudformation describe-stacks --region $AWS_REGION --stack-name $STACK_NAME'
            }
        }

        stage("deploy"){

            steps{
                echo 'deploy app...'
            }
        }
    }
}


