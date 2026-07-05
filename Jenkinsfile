pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Basic Check') {
            steps {
                sh '''
                . venv/bin/activate
                python run.py &
                sleep 10
                pkill -f run.py
                '''
            }
        }
    }
}
