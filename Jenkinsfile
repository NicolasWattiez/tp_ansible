pipeline {
 agent any
   stages {
    stage('clone'){
      steps {
        git branch: 'main',
        url: 'https://github.com/NicolasWattiez/tp_ci_cd'
        
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
   }
}
