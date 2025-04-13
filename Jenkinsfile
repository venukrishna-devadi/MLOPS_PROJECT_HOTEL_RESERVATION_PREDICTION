// 1. Cloning the code from github to jenkins

pipeline{
    agent any

    // here we will define all the stages
    stages{
        stage{'Cloning github repo to Jenkins'}{
            steps{
                script{
                    echp 'Cloning github repo to Jenkins........'
                    checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_token', url: 'https://github.com/venukrishna-devadi/MLOPS_PROJECT_HOTEL_RESERVATION_PREDICTION.git']])
                }
            }
        }

    }
}