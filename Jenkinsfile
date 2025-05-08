pipeline{
    agent any 

    environment  {
        VENV_DIR = 'venv'
    }

    stages{
        stage('Cloning github repo to jenkins'){
            steps{
                script{
                    echo 'Cloning github repo to jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/yssh03/hotel-reservation-analysis.git']])

                }
            }
        }

        stage('Setting up virtual environment and install dependencies'){
            steps{
                script{
                    echo 'Setting up virtual environment and install dependencies'
                    sh  '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate

                    pip install --upgrade pip
                    pip install -e .

                    '''
                }
            }
        }
    }
}