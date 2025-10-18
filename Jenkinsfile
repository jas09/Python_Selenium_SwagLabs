pipeline {
    agent any

    environment {
        JIRA_URL = "https://neverabdicate.atlassian.net"
        JIRA_ISSUE = "RPS-6"
        JIRA_CRED = credentials('Jira_API_Key')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/jas09/RobotFramework_Python_Swaglabs.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {	
                bat 'pabot --processes 2 --outputdir results tests/'
            }
        }

        stage('Publish Robot Results') {
            steps {
                robot(
                    outputPath: 'results',
                    outputFileName: 'output.xml',
                    logFileName: 'log.html',
                    reportFileName: 'report.html',
                    passThreshold: 80,
                    unstableThreshold: 70,
                    otherFiles: 'screenshot-*.png'
                )
            }
        }
		stage('Convert to JUnit (Optional)') {
            steps {
                bat 'rebot --xunit results/xunit.xml results/output.xml'
            }
        }
		stage('Publish JUnit Results') {
            steps {
                junit 'results/xunit.xml'
            }
        }
        stage('Update Jira') {
            steps {
                script {
                    def status = currentBuild.currentResult == 'SUCCESS' ? "PASS" : "FAIL"
                    def message = "Automation run completed. Status: ${status}. Build: ${env.BUILD_URL}"
                    bat """
                        curl -X POST ^
						--ssl-no-revoke ^
                        -u ${JIRA_CRED_USR}:${JIRA_CRED_PSW} ^
                        -H "Content-Type: application/json" ^
                        --data "{\\"body\\":{\\"type\\":\\"doc\\",\\"version\\":1,\\"content\\":[{\\"type\\":\\"paragraph\\",\\"content\\":[{\\"type\\":\\"text\\",\\"text\\":\\"Automation run completed successfully. Status: PASS. Build URL: ${BUILD_URL}\\"}]}]}}" ^
                        ${JIRA_URL}/rest/api/3/issue/${JIRA_ISSUE}/comment
                    """
                }
            }
        }
    }

    post {
        always {
            junit 'results/xunit.xml'
            archiveArtifacts artifacts: 'results/*.xml', allowEmptyArchive: true
        }
    }
}
