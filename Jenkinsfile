pipeline {
    agent {
        docker {
            image 'python:3.8.7'
            args '-u root'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install radon'
            }
        }
        stage('Run tests') {
            steps {
                sh 'python -m unittest discover -s tests'
            }
        }
        stage('Metrics - Coverage') {
            steps {
                sh 'coverage run -m unittest discover -s tests'
                sh 'coverage report'
            }
        }
        stage('Metrics - Radon') {
            steps {
                sh 'radon cc --show-complexity --total-average tests'
            }
        }
        stage('Metrics - Bandit') {
            steps {
                sh 'bandit -r tests'
            }
        }
        stage('Post Actions') {
            steps {
                script {
                    try {
                        // Perform post-action steps
                    } catch (Exception e) {
                        // Handle the exception or send notifications
                        echo "Post-action failed: ${e.getMessage()}"
                        // Send email notification, Slack message, etc.
                        // You can use the Jenkins email or Slack plugins for this purpose
                    }
                }
            }
        }
    }
}
