pipeline {
   agent any

 
   stages {
      stage('Create Virtual Environment') {
         when {
            not { expression{ fileExists '/var/jenkins_home/workspace/venv/bin/activate' }}
         }
         steps {
            dir ('/var/jenkins_home/workspace') {
    	        sh 'python3 -m venv venv'
                sh 'echo "Environment Created"'
            }
         }
      }
      stage('Activate') {
         steps {
            dir ('/var/jenkins_home/workspace') {
                sh '''. venv/bin/activate
                    pip install -r jenkins-webhook_master/requirements.txt
                    '''
            }
         }
      }
      stage('cd Project directory and pull code') {
         steps {
            sh 'pwd'
            sh 'git pull origin master'
         }
      }
      stage('Run tests') {
         steps {
            dir ('/var/jenkins_home/workspace/jenkins-webhook_master') {
                sh '''. ../venv/bin/activate
                    python ./manage.py test
                    '''
            }
         }
      }
   }
}
