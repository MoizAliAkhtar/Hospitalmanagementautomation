pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/MoizAliAkhtar/Hospitalmanagementautomation.git'
                    ]],
                    extensions: [
                        [$class: 'CloneOption',
                         shallow: true,
                         depth: 1,
                         timeout: 30]
                    ]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t hospital-management:latest .'
            }
        }
    }
}
