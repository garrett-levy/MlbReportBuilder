pipeline {
    agent { docker { image 'python:3.7.3'} }
   
    parameters {
        string(name: 'Teams', defaultValue: ["New York Yankees"], description: 'description', trim: true)
    }
    stages {
        stage('Create Report') {
            steps {
                sh 'pip3 install -r requirements.txt'
                sh 'python mlb_report_builder.py'
            }
        }
    }
    post('Email Report') {
        success {
            archiveArtifacts artifacts: '**/*.xlsx', onlyIfSuccessful: true
            emailext attachLog: true, attachmentsPattern: "mlbreport.xlsx",
                to: "gjl8en@virginia.edu",
                body: "Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n More info at: ${env.BUILD_URL}",
                subject: "Report for ${Teams}"
         }  
         failure {  
             emailext attachLog: false,
                to: "gjl8en@virginia.edu",
                body: "Job ${env.JOB_NAME} build ${env.BUILD_NUMBER}\n More info at: ${env.BUILD_URL}",
                subject: "failed report"
         }  
     }  
}
