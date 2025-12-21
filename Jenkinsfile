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
ssh -o StrictHostKeyChecking=no ubuntu@13.60.24.69 << 'EOF'
set -e

echo "Pulling latest image..."
docker pull moiz314/hospital-management:latest

echo "Stopping existing container..."
docker stop hospital 2>/dev/null || true
docker rm hospital 2>/dev/null || true

echo "Ensuring port 8000 is free..."
sudo fuser -k 8000/tcp 2>/dev/null || true

echo "Waiting for port to be released..."
sleep 3

echo "Starting new container..."
docker run -d \
  --name hospital \
  --restart unless-stopped \
  -p 8000:8000 \
  moiz314/hospital-management:latest

echo "Deployment successful"
EOF
'''
                }
            }
        }
    }
}
