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
                    stack_create="False"
                    stack_update="False"
                    aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION && stack_update="True" || stack_create="True"
                    
                    if [ $stack_create == "True" ]
                    then
                        echo "CREATE A NEW STACK"
                    elif [ $stack_update == "True" ]
                    then
                        echo "UPDATE EXISTING STACK"
                    else
                        echo "SOMETHING IS WRONG"
                    fi
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


