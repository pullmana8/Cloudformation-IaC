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
        stage('Build Docker image') {
            steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]){
                    sh '''
                        docker build -t pyrrhus/udacity-capstone .
                        '''
            }
        }
    }
    stage('Push image to DockerHub') {
        steps {
                withCredentials([[$class: 'UsernamePasswordMultiBinding', credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD']]){
                    sh '''
                        docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
                        docker push pyrrhus/udacity-capstone
                    '''
                }
            }
        }
    stage('Set current kubectl context') {
            steps {
                withAWS(region:'us-east-1', credentials:'jenkins_creds') {
                    sh '''
                        kubectl config use-context arn:aws:eks:us-east-2:663355930064:cluster/finalCluster
                    '''
                }
            }
        }
    }
}
