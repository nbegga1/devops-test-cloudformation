pipeline{
    agent any

    environment{
        AWS_ACCESS_KEY_ID     = credentials('aws-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret')
        AWS_REGION = 'us-east-1'
        STACK_NAME = 'test-1'
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
                        steps{
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
                            }
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
                    }
                }
            }
        }
        
        
        
        
        
        // stage("test"){
        //     environment{
        //         STACK_CREATE = sh(script: '''
        //                             if aws cloudformation describe-stacks --region ${AWS_REGION} --stack-name ${STACK_NAME} > /dev/null; then
        //                                 echo "false"
        //                             else
        //                                 echo "true"
        //                             fi
        //                             ''', returnStdout: true).trim()
        //         STACK_UPDATE = sh(script: '''
        //                             if aws cloudformation describe-stacks --region ${AWS_REGION} --stack-name ${STACK_NAME} > /dev/null; then
        //                                 echo "true"
        //                             else
        //                                 echo "false"
        //                             fi
        //                             ''', returnStdout: true).trim()
        //     }
        //     steps{
        //         sh '''
        //             echo $STACK_CREATE
        //             echo $STACK_UPDATE
        //         '''
        //     }
        // }

       
        // // stage("Deploy lambda code"){
            
        // //     steps{
                
        // //         sh '''
        // //         cd package
        // //         zip -r lambda-deployment-package.zip ./*
        // //         mv lambda-deployment-package.zip ..
        // //         cd ..
        // //         zip -g lambda-deployment-package.zip index.py
        // //         aws s3 cp lambda-deployment-package.zip s3://lambda-package-bucket-test
        // //         '''
                
        // //     }
        // // }

        // stage("Create changeset"){

        //     steps{

        //         sh '''
        //             echo $STACK_CREATE
        //             echo $STACK_UPDATE

        //             if [ $STACK_CREATE == true ]
        //             then
        //                 aws cloudformation create-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --template-body file://$TEMPLATE_NAME --region $AWS_REGION --capabilities CAPABILITY_IAM --change-set-type CREATE
        //                 aws cloudformation wait change-set-create-complete --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --region $AWS_REGION
        //             elif [ $STACK_UPDATE == true ]
        //             then
        //                 aws cloudformation create-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --template-body file://$TEMPLATE_NAME --region $AWS_REGION --capabilities CAPABILITY_IAM --change-set-type UPDATE
        //                 aws cloudformation wait change-set-create-complete --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --region $AWS_REGION
        //             else
        //                 echo "SOMETHING IS WRONG"
        //             fi
        //         '''
        //     }
        // }

        // stage("Describe changeset"){

        //     steps{

        //         sh '''
        //             aws cloudformation describe-change-set --stack-name $STACK_NAME --change-set-name $CHANGE_SET_NAME --region $AWS_REGION
        //         '''
        //     }
        // }


        // stage("Approval"){

        //     steps{
        //         script{
        //             def approveInput = input(
        //                 id: 'approve',
        //                 message: 'Do you approve of the changes?',
        //                 parameters: [choice(name: 'Approvement', choices: "yes\nno", description: "Do you want to deploy these changes?")])

        //             if(approveInput == 'yes'){
        //                 stage("Execute changeset"){
        //                     sh '''
                                
        //                         if [ $STACK_CREATE == true ]
        //                         then
        //                             aws cloudformation execute-change-set --change-set-name $CHANGE_SET_NAME --stack-name $STACK_NAME --region $AWS_REGION
        //                             aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --region $AWS_REGION
        //                     elif [ $STACK_UPDATE == true ]
        //                         then
        //                             aws cloudformation execute-change-set --change-set-name $CHANGE_SET_NAME --stack-name $STACK_NAME --region $AWS_REGION
        //                             aws cloudformation wait stack-update-complete --stack-name $STACK_NAME --region $AWS_REGION
        //                         else
        //                             echo "SOMETHING IS WRONG"
        //                         fi
        //                     '''
        //                 }
        //             }
        //             else if(approveInput == 'no'){
        //                 stage("Skip create/update"){
        //                     echo 'Creation/Updation of $STACK_NAME will not be executed'
        //                 }
        //             }





        //         }
                

        //     }
        // }
    }
}