pipeline{
    agent any

    stages{

        stage("list-stacks"){

            steps{
                sh 'aws cloudformation list-stack-instances --region us-east-1'
            }
        }

        stage("deploy"){

            steps{
                echo 'deploy application...'
            }
        }
    }
}


