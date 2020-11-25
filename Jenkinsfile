pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        AWS_REGION = 'us-east-1'
        STACK_NAME = 's-test'
    }

    stages{

        stage("list-stacks"){

            steps{

                sh '''
                    aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION && stack_exists = "True" || stack_exists="False"
                    echo $stack_exists
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


