// 1. Cloning the code from github to jenkins

pipeline {
    agent any
    // Create virtual environment in Jenkins
    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "sincere-octane-455720-d4"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
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
        } 

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
        }
        
        stage('Building and Pushing image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'Google_Application_Credentials')]){
                    script{
                        echo 'Building and Pushing image to GCR................'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${Google_Application_Credentials}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml_ops_project-1:latest .
                         
                        docker push gcr.io/${GCP_PROJECT}/ml_ops_project-1:latest 
                        '''
                    }
                }
            }
        } // Added closing bracket for the stage

        stage('Deploy to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'Google_Application_Credentials')]){
                    script{
                        echo 'Deploy to GCR................'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${Google_Application_Credentials}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml_ops_project-1\
                            --image=gcr.io/${GCP_PROJECT}/ml_ops_project-1:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                        '''
                    }
                }
            }    
        }
    }
}
