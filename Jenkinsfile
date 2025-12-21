pipeline {
    agent { label 'ec2-agent' }

    environment {
        DOCKER_IMAGE = 'moiz314/hospital-management'
        DOCKER_TAG   = 'latest'
    }

    options {
        timeout(time: 45, unit: 'MINUTES')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/MoizAliAkhtar/Hospitalmanagementautomation.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                sh 'docker push $DOCKER_IMAGE:$DOCKER_TAG'
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
            ssh -o StrictHostKeyChecking=no ubuntu@13.60.24.69 "
                docker pull $DOCKER_IMAGE:$DOCKER_TAG

                # Stop old container
                docker ps -q --filter name=hospital | grep -q . && docker stop hospital || true
                docker ps -a -q --filter name=hospital | grep -q . && docker rm hospital || true

                # Kill any process using port 8000 (with sudo, no password)
                sudo lsof -t -i:8000 | xargs -r sudo kill -9

                # Run the new container
                docker run -d --name hospital -p 8000:8000 $DOCKER_IMAGE:$DOCKER_TAG
            "
            '''
                }
            }
        }
    }
}
