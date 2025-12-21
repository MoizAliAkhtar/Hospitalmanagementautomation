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
                ssh -o StrictHostKeyChecking=no ubuntu@13.60.24.69 bash -c "
                    echo 'Pulling latest image...'
                    docker pull moiz314/hospital-management:latest

                    echo 'Stopping old container if exists...'
                    if [ \$(docker ps -q --filter name=hospital) ]; then
                        docker stop hospital
                        docker rm hospital
                    fi

                    echo 'Killing any process using port 8000...'
                    sudo fuser -k 8000/tcp || true

                    echo 'Waiting for port 8000 to be free...'
                    while sudo lsof -i:8000 >/dev/null 2>&1; do
                        echo 'Port 8000 still in use. Waiting...'
                        sleep 2
                    done

                    echo 'Running new container...'
                    docker run -d --name hospital -p 8000:8000 moiz314/hospital-management:latest
                "
            '''
                }
            }
        }
    }
}
