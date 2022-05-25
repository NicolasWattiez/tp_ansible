pipeline {
 agent any
   stages {
    stage('clone'){
      steps {
        git branch: 'main',
        url: 'https://github.com/NicolasWattiez/tp_ansible.git'
        
      }
    }
	  stage ('Build') {
      tools {
        gradle 'gradle'
      }
      steps {
        sh 'gradle purge'
        sh 'gradle dependencies'
        sh 'gradle packageDistribution'
      }
	   }

	  stage ('Lancement playbook') {

      steps {
        sh 'ssh root@master'
        sh 'cd etc'
        sh 'cd ansible'
        sh 'ansible-playbook config-dbserver.yml'
        sh 'ansible-playbook config-appserver.yml'
        sh 'ansible-playbook config-dbcentos.yml'
        sh 'ansible-playbook config-appcentos.yml'
      }
	    
   }
}
)