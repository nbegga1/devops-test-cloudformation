pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        GCHAT_URL = credentials('credential_id_for_room1')
        AWS_REGION = 'us-east-1'
        STACK_NAME = 's3-test-3'
        TEMPLATE_NAME = 's3-test.yml'
        CHANGE_SET_NAME = 'change-set-test'
    }

    stages{
        
        stage("Start"){
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
                                aws cloudformation create-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --template-body file://$TEMPLATE_NAME --region $AWS_REGION --capabilities CAPABILITY_IAM --change-set-type CREATE
                                aws cloudformation wait change-set-create-complete --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --region $AWS_REGION
                            '''
                        }
                        stage("Describe changeset"){
                            sh '''
                                aws cloudformation describe-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --region $AWS_REGION
                            '''
                            def STACK_ID = sh(script: '''
                                    sudo yum install jq > /dev/null
                                    aws cloudformation describe-change-set --stack-name s3-test-3 --change-set-name change-set-test --region us-east-1 | jq -r '.StackId'
                                ''', returnStdout: true).trim()
                            def CHANGE_SET_ID = sh(script: '''
                                    sudo yum install jq > /dev/null
                                    aws cloudformation describe-change-set --stack-name s3-test-3 --change-set-name change-set-test --region us-east-1 | jq -r '.ChangeSetId'
                                ''', returnStdout: true).trim()
                            notifyChatChangesetURL(STACK_ID, CHANGE_SET_ID)
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
                                            aws cloudformation execute-change-set --change-set-name $CHANGE_SET_NAME --stack-name $STACK_NAME --region $AWS_REGION
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
                                aws cloudformation create-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --template-body file://$TEMPLATE_NAME --region $AWS_REGION --capabilities CAPABILITY_IAM --change-set-type UPDATE
                                aws cloudformation wait change-set-create-complete --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --region $AWS_REGION
                            '''
                        }
                        stage("Describe changeset"){
                            sh '''
                                aws cloudformation describe-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --region $AWS_REGION
                            '''
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
                                            aws cloudformation execute-change-set --change-set-name $CHANGE_SET_NAME --stack-name $STACK_NAME --region $AWS_REGION
                                            aws cloudformation wait stack-update-complete --stack-name $STACK_NAME --region $AWS_REGION
                                        '''
                                    }
                                }
                                else if(approveInput == 'no'){
                                    stage("Skip create/update"){
                                        sh '''
                                            aws cloudformation delete-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --region $AWS_REGION
                                        '''
                                        echo 'Updation of $STACK_NAME will not be executed'
                                    }
                                }
                            }
                        }
                    }
                }
                notifyChat()
            }
        }
    }
    // post {
    //     always  {
    //         googlechatnotification url: 'https://chat.googleapis.com/v1/spaces/AAAAP4bRfic/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Y0_Hc3eSM6h54s9E3MIHhT-J3CcOqMcNJ9wyFiHYAvk%3D', message: 'Build was succesfull.', notifySuccess: true
    //     }
    // }
}

def notifyChatChangesetURL(String STACK_ID, String CHANGE_SET_ID){
        String SI = URLEncoder.encode(STACK_ID, "UTF-8");
        String CSI = URLEncoder.encode(CHANGE_SET_ID, "UTF-8");
        String AWS_URL_BASE = "https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/changesets/changes?"

        String URL = AWS_URL_BASE+"stackId="+SI+"&changeSetId="+CSI

        googlechatnotification (
            url: "${GCHAT_URL}",
            message: "${URL}")
}


def notifyChat(){
        googlechatnotification (
            url: "${GCHAT_URL}",
            message: 'Build succesfull.')
}