pipeline {
    agent any
    stages {
        stage('Create conf file cluster') {
            steps {
                withAWS(region:'us-east-2', credentials:'jenkins_creds') {
                    sh '''
                        aws eks --region us-east-2 update-kubeconfig --name finalCluster
                        '''
                }
            }
        }
        stage('Lint HTML') {
            steps {
                sh 'tidy -q -e *.html'
            }
        }
        stage('Build Docker image Blue') {
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]){
                    sh '''
                        docker build -t pyrrhus/udacity-capstone:blue --build-arg IMAGE_ID="nginx:1.16.1" .
                        '''
            }
        }
    }
        stage('Build Docker image Green') {
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]){
                    sh '''
                        docker build -t pyrrhus/udacity-capstone:green --build-arg IMAGE_ID="nginx:1.17.8" .
                        '''
            }
        }
    }
    stage('Push image to DockerHub') {
        steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]){
                    sh '''
                        docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                        docker push pyrrhus/udacity-capstone:blue
                        docker push pyrrhus/udacity-capstone:green
                    '''
                }
            }
        }

    stage('Set current kubectl context') {
            steps {
                withAWS(region:'us-east-2', credentials:'jenkins_creds') {
                    sh '''
                        kubectl config use-context arn:aws:eks:us-east-2:663355930064:cluster/finalCluster
                    '''
                }
            }
        }
        stage('Deploy blue containers for blue environment') {
            steps {
                withAWS(region:'us-east-2', credentials:'jenkins_creds') {
        					sh '''
        						sed -e 's/{{TARGET_ROLE}}/blue/g' -e 's/{{IMAGE_VERSION}}/blue/' deployment.yaml | kubectl apply -f -
        					'''
        				}
        			}
        		}
                stage('Deploy blue containers for green environment') {
                    steps {
                        withAWS(region:'us-east-2', credentials:'jenkins_creds') {
                					sh '''
                						sed -e 's/{{TARGET_ROLE}}/green/g' -e 's/{{IMAGE_VERSION}}/blue/' deployment.yaml | kubectl apply -f -
                					'''
                				}
                			}
                		}

         stage('Create service for cluster and redirect to blue') {
         			steps {
         				withAWS(region:'us-east-2', credentials:'jenkins_creds') {
         					sh '''
         						sed  's/{{TARGET_ROLE}}/blue/g' service.yaml | kubectl apply -f -
         					'''
         				}
         			}
         		}

         stage('Deploy green containers for green environment') {
                         			steps {
                         				withAWS(region:'us-east-2', credentials:'jenkins_creds') {
                         					sh '''
                         						sed -e 's/{{TARGET_ROLE}}/green/g' -e 's/{{IMAGE_VERSION}}/green/' deployment.yaml | kubectl apply -f -
                         					'''
                         				}
                         			}
                         		}

        stage('Create service to test green') {
                 			steps {
                 				withAWS(region:'us-east-2', credentials:'jenkins_creds') {
                 					sh '''
                 						sed  's/{{TARGET_ROLE}}/green/g' service-test.yaml | kubectl apply -f -
                 					'''
                 				}
                 			}
                 		}



        stage('Wait for user approval') {
             steps {
                      input "Are you ready to redirect traffic to green environment?"
              }
         }

        stage('Update service for cluster and redirect to green') {
                 			steps {
                 				withAWS(region:'us-east-2', credentials:'jenkins_creds') {
                 					sh '''
                 						sed  's/{{TARGET_ROLE}}/green/g' service.yaml | kubectl apply -f -
                 					'''
                 				}
                 			}
                 		}
    }
 }