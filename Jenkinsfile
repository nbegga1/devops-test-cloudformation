pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
    }

    stages{

        stage("list-stacks"){

            steps{
                sh 'aws cloudformation list-stacks --region us-east-1'
            }
        }

        stage("deploy"){

            steps{
                echo 'deploy application...'
            }
        }
    }
}


