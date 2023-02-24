pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/i190534']], extensions: [], userRemoteConfigs: [[credentialsId: '3e4562c3-4044-4567-7422-53543567435e', url: 'https://github.com/NUCES-ISB/i190555_i190534_assignment1']])
            }
        }
        stage('Install python dependencies') {
            steps {
                bat '''pip install --upgrade setuptools
                       pip install pylint black setuptools
                       pip install -r requirements.txt'''
            }
        }

        stage('Run black') {
            steps {
                bat '''python -m black ../Assignment1-Test'''
            }
        }

        stage('Run pylint') {
            steps {
                bat '''pylint ../Assignment1-Test --exit-zero '''
            }
        }
    }
}
