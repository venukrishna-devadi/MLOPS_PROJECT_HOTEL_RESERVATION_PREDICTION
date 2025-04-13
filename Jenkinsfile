// 1. Cloning the code from github to jenkins

pipeline {
    agent any
    // Create virtual environment in Jenkins
    environment {
        VENV_DIR = 'venv'
    }

    stages {
        stage('Cloning github repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning github repo to Jenkins........'
                    checkout scmGit(
                        branches: [[name: '*/master']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github_token',
                            url: 'https://github.com/venukrishna-devadi/MLOPS_PROJECT_HOTEL_RESERVATION_PREDICTION.git'
                        ]]
                    )
                }
            }
        } // Added closing bracket for the stage

        stage('Setting up our Virtual Environment and Installing dependencies') {
            steps {
                script {
                    echo 'Setting up our Virtual Environment and Installing dependencies........'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        } // Added closing bracket for the stage
    } // Added closing bracket for the stages
} // Added closing bracket for the pipeline

