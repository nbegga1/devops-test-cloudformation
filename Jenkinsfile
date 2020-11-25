pipeline{
    agent any

    stages{

        stage("Set credentials"){

            steps{
                sh 'aws configure'
                sh '$AWS_ACCESS_KEY_ID'
                sh '$AWS_SECRET_ACCESS_KEY'
                sh '$AWS_DEFAULT_REGION'
                sh 'json'
            }
        }

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


