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

                sh '''
                    stack_create="False"
                    stack_update="False"
                    aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION && stack_update="True" || stack_create="True"
                    echo $stack_create
                    echo $stack_update
                '''
            }
        }

        stage("deploy"){

            steps{
                echo 'deploy app...'
            }
        }
    }
}


