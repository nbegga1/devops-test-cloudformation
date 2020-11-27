pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        AWS_REGION = 'us-east-1'
        STACK_NAME = 's3-test'
        TEMPLATE_NAME = 's3-test.yml'
    }

    stages{

        stage("Deploy lambda code"){

            steps{
                sh '''
                    cd package
                    zip -r lambda-deployment-package.zip ./*
                    mv lambda-deploymeny-package.zip ..
                    cd ..
                    zip -g lambda-deployment-package.zip index.py
                    aws s3 cp lambda-deployment-package.zip s3://lambda-package-bucket-test
                '''
            }
        }

        stage("Create/Update stack"){

            steps{

                sh '''
                    stack_create="False"
                    stack_update="False"
                    aws cloudformation describe-stacks --stack-name $STACK_NAME --region $AWS_REGION && stack_update="True" || stack_create="True"
                    
                    if [ $stack_create == "True" ]
                    then
                        aws cloudformation create-stack --stack-name $STACK_NAME --template-body file://$TEMPLATE_NAME --region $AWS_REGION
                    elif [ $stack_update == "True" ]
                    then
                        aws cloudformation update-stack --stack-name $STACK_NAME --template-body file://$TEMPLATE_NAME --region $AWS_REGION --capabilities CAPABILITY_IAM
                    else
                        echo "SOMETHING IS WRONG"
                    fi
                '''
            }
        }
    }
}