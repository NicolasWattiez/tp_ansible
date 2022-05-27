def remote = [:] 
remote.name= 'jenkins'
remote.host='master'
remote.user='root'
remote.password='toor'
remote.allowAnyHosts=true
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
      stage('SSH into the serveur'){
        steps {
            sshCommand remote: remote, command: "ansible-playbook /etc/ansible/config-dbubuntu.yml"
            sshCommand remote: remote, command: "ansible-playbook /etc/ansible/config-dbcentos.yml"
            sshCommand remote: remote, command: "ansible-playbook /etc/ansible/config-appubuntu.yml"
            sshCommand remote: remote, command: "ansible-playbook /etc/ansible/config-appcentos.yml"

        }
      }
   }
}
