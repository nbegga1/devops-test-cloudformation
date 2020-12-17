pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        GOOGLE_CHAT_URL = credentials('credential_id_for_room1')
        AWS_REGION = 'us-east-1'
        STACK_NAME = 's3-test-3'
        TEMPLATE_NAME = 's3-test.yml'
    }

    stages{
        
        // stage("Deploy and test python"){

        //     steps{
        //         sh '''
        //             python3 -m pytest test.py
        //             cd package
        //             zip -r lambda-deployment-package.zip ./*
        //             cd ..
        //             zip -g lambda-deployment-package.zip index.py
        //             aws s3 cp lambda-deployment-package.zip s3://lambda-package-bucket-test
        //         '''
        //     }
        // }
        stage("SonarQube Code Analysis"){
            withSonarQubeEnv('My SonarQube Server', envOnly: true) {
                // This expands the evironment variables SONAR_CONFIG_NAME, SONAR_HOST_URL, SONAR_AUTH_TOKEN that can be used by any script.
                println ${env.SONAR_HOST_URL} 
            }
        }
        stage("Check Update/Create"){
            steps{
                script{
                    def STACK_CREATE = sh(script: '''
                                     if aws cloudformation describe-stacks --region ${AWS_REGION} --stack-name ${STACK_NAME} > /dev/null; then
                                         echo "false"
                                     else
                                         echo "true"
                                     fi
                                     ''', returnStdout: true).trim()
                    if(STACK_CREATE == "true"){
                        stage("Create changeset"){
                            sh '''
                                aws cloudformation create-change-set --stack-name $STACK_NAME --change-set-name cg-${BUILD_NUMBER} --template-body file://$TEMPLATE_NAME --region $AWS_REGION --capabilities CAPABILITY_IAM --change-set-type CREATE
                                aws cloudformation wait change-set-create-complete --stack-name $STACK_NAME --change-set-name cg-${BUILD_NUMBER} --region $AWS_REGION
                            '''
                        }
                        stage("Describe changeset"){
                            sh '''
                                aws cloudformation describe-change-set --stack-name $STACK_NAME --change-set-name cg-${BUILD_NUMBER} --region $AWS_REGION
                            '''
                            def STACK_ID = sh(script: '''
                                    sudo yum install jq > /dev/null
                                    aws cloudformation describe-change-set --stack-name s3-test-3 --change-set-name cg-${BUILD_NUMBER} --region us-east-1 | jq -r '.StackId'
                                ''', returnStdout: true).trim()
                            def CHANGE_SET_ID = sh(script: '''
                                    sudo yum install jq > /dev/null
                                    aws cloudformation describe-change-set --stack-name s3-test-3 --change-set-name cg-${BUILD_NUMBER} --region us-east-1 | jq -r '.ChangeSetId'
                                ''', returnStdout: true).trim()
                            notifyApprove(STACK_ID, CHANGE_SET_ID)
                        }
                        stage("Approval"){
                            script{
                                
                                def approveInput = input(
                                    id: 'Approve',
                                    message: 'Do you approve of the changes?',
                                    parameters: [choice(name: 'Approvement', choices: "yes\nno", description: "Do you want to deploy these changes?")])

                                if(approveInput == 'yes'){
                                    stage("Execute changeset"){
                                        sh '''
                                            aws cloudformation execute-change-set --change-set-name cg-${BUILD_NUMBER} --stack-name $STACK_NAME --region $AWS_REGION
                                            aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --region $AWS_REGION
                                        '''
                                    }
                                }
                                else if(approveInput == 'no'){
                                    stage("Skip create/update"){
                                        sh '''
                                            aws cloudformation delete-stack --stack-name $STACK_NAME --region $AWS_REGION
                                        '''
                                        echo 'Creation/Updation of $STACK_NAME will not be executed'
                                    }
                                }
                            }                        
                        }
                    }

                    else if(STACK_CREATE == "false"){
                        stage("Create changeset"){
                            sh '''
                                aws cloudformation create-change-set --stack-name $STACK_NAME --change-set-name cg-${BUILD_NUMBER} --template-body file://$TEMPLATE_NAME --region $AWS_REGION --capabilities CAPABILITY_IAM --change-set-type UPDATE
                                aws cloudformation wait change-set-create-complete --stack-name $STACK_NAME --change-set-name cg-${BUILD_NUMBER} --region $AWS_REGION
                            '''
                        }
                        stage("Describe changeset"){
                            sh '''
                                aws cloudformation describe-change-set --stack-name $STACK_NAME --change-set-name cg-${BUILD_NUMBER} --region $AWS_REGION
                            '''
                            def STACK_ID = sh(script: '''
                                    sudo yum install jq > /dev/null
                                    aws cloudformation describe-change-set --stack-name s3-test-3 --change-set-name cg-${BUILD_NUMBER} --region us-east-1 | jq -r '.StackId'
                                ''', returnStdout: true).trim()
                            def CHANGE_SET_ID = sh(script: '''
                                    sudo yum install jq > /dev/null
                                    aws cloudformation describe-change-set --stack-name s3-test-3 --change-set-name cg-${BUILD_NUMBER} --region us-east-1 | jq -r '.ChangeSetId'
                                ''', returnStdout: true).trim()
                            notifyApprove(STACK_ID, CHANGE_SET_ID)
                        }
                        stage("Approval"){
                            script{
                                def approveInput = input(
                                    id: 'approve',
                                    message: 'Do you approve of the changes?',
                                    parameters: [choice(name: 'Approvement', choices: "yes\nno", description: "Do you want to deploy these changes?")])

                                if(approveInput == 'yes'){
                                    stage("Execute changeset"){
                                        sh '''
                                            aws cloudformation execute-change-set --change-set-name cg-${BUILD_NUMBER} --stack-name $STACK_NAME --region $AWS_REGION
                                            aws cloudformation wait stack-update-complete --stack-name $STACK_NAME --region $AWS_REGION
                                        '''
                                    }
                                }
                                else if(approveInput == 'no'){
                                    stage("Skip create/update"){
                                        sh '''
                                            aws cloudformation delete-change-set --stack-name $STACK_NAME --change-set-name cg-${BUILD_NUMBER} --region $AWS_REGION
                                        '''
                                        echo 'Updation of $STACK_NAME will not be executed'
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    post {
        success {
            notifyChat("success")
        }
        failure {
            notifyChat("failure")
        }
    }
}



//@Library('devops-test-cloudformation')
def notifyApprove(String STACK_ID, String CHANGE_SET_ID){
        String STACK_ID_ENC = URLEncoder.encode(STACK_ID, "UTF-8");
        String CHANGE_SET_ID_ENC = URLEncoder.encode(CHANGE_SET_ID, "UTF-8");
        String AWS_URL_BASE = "https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/changesets/changes?"

        String CHANGESET_URL = AWS_URL_BASE+"stackId="+STACK_ID_ENC+"&changeSetId="+CHANGE_SET_ID_ENC

        String gchatMessage = "`Notification from Jenkins:`\n"

        googlechatnotification (
            url: "${GOOGLE_CHAT_URL}",
            message: "${gchatMessage}" + "Review <${CHANGESET_URL}|*ChangeSet*>\n" +"Approve <${env.JENKINS_URL}/job/${env.JOB_NAME}/|*Build#${env.BUILD_NUMBER}>*")
}


def notifyChat(String result){
        // Not complete yet
        String gchatMessage = "`Notification from Jenkins:`\n" + "Pipeline name: *${env.JOB_BASE_NAME}*\n" + "Build number: *${env.BUILD_NUMBER}*\n" + "Branch: *main*\n"

        if(result == "success"){
            gchatMessage += "Result: *Success*\n"
        }
        else if(result == "failure"){
            gchatMessage += "Result: *Failure*\n"
        }

        googlechatnotification (
            url: "${GOOGLE_CHAT_URL}",
            message: "${gchatMessage}" +"View <${env.BUILD_URL}|*Build#${env.BUILD_NUMBER}*>")
}