pipeline {
    agent any

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
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/MoizAliAkhtar/Hospitalmanagementautomation.git'
                    ]],
                    extensions: [
                        [$class: 'WipeWorkspace'],
                        [$class: 'CloneOption',
                         shallow: true,
                         depth: 1,
                         noTags: true,
                         timeout: 45]
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
