pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        AWS_REGION = 'us-east-1'
        STACK_NAME = 'test'
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
                        aws cloudformation create-stack --stack-name $STACK_NAME --template-body file://s3-test.yml --region $AWS_REGION
                    elif [ $stack_update == "True" ]
                    then
                        aws cloudformation update-stack --stack-name $STACK_NAME --template-body file://s3-lambda-db.yml --region $AWS_REGION
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


