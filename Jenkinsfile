pipeline {
    agent any 

    environment  {
        VENV_DIR = 'venv'
        AWS_REGION = 'ca-central-1' 
        ECR_REPO_NAME = 'mlops-hotel-reservation'
        IMAGE_TAG = 'latest'
        AWS_ACCOUNT_ID = '522814733518' 
        ECR_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}"
    }

    stages {
        stage('Cloning GitHub Repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning GitHub repo to Jenkins'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token', 
                            url: 'https://github.com/yssh03/hotel-reservation-analysis.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting Up Virtual Environment and Install Dependencies') {
            steps {
                script {
                    echo 'Setting up virtual environment and installing dependencies'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        stage('Authenticate Docker with AWS ECR') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                        sh '''
                        aws ecr get-login-password --region ${AWS_REGION} | \
                        docker login --username AWS --password-stdin ${ECR_URI}
                        '''
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image'
                    sh '''
                    docker build -t ${ECR_REPO_NAME}:${IMAGE_TAG} .
                    '''
                }
            }
        }

        stage('Tag Docker Image') {
            steps {
                script {
                    echo 'Tagging Docker image for ECR'
                    sh '''
                    docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} ${ECR_URI}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Push Docker Image to AWS ECR') {
            steps {
                script {
                    echo 'Pushing Docker image to AWS ECR'
                    sh '''
                    docker push ${ECR_URI}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Run Docker Image from ECR') {
            steps {
                script {
                    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                        echo 'Pulling and running the image from ECR'
                        sh '''
                        docker pull ${ECR_URI}:${IMAGE_TAG}
                        docker run --rm \
                            -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
                            -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
                            -e AWS_DEFAULT_REGION=${AWS_REGION} \
                            ${ECR_URI}:${IMAGE_TAG}
                        '''
                    }
                }
            }
        }
    }
}
