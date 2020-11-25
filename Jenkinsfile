pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
    }

    stages{

        stage("list-stacks"){

            steps{
                sh 'aws cloudformation describe-stacks --region us-east-1 --stack-name test'
            }
        }

        stage("deploy"){

            steps{
                echo 'deploy app...'
            }
        }
    }
}


