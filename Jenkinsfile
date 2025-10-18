pipeline {
    agent any

    environment {
        JIRA_URL = "https://neverabdicate.atlassian.net"
        JIRA_ISSUE = "PSP-36"
        JIRA_CRED = credentials('Jira_API_Key')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/jas09/Python_Selenium_SwagLabs.git'
            }
        }

        stage('Setup Python Environment') {
            steps {
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Pytest Suite') {
            steps {
                bat '''
                pytest -n 2 -m smoke ^
                --browser_name=Edge ^
                --url_key=SwagLabs ^
                --headless ^
                --html=reports/report.html ^
                --json-report ^
                --json-report --json-report-file=reports/report.json
                '''
            }
        }
        stage('Extract Test Summary') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                python extract_summary.py
                '''
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'reports',
                    reportFiles: 'report.html',
                    reportName: 'Pytest Smoke Report'
                ])
            }
        }
        stage('Update Jira') {
            when {
                expression { fileExists('reports/summary.txt') }
            }
            steps {
                script {
                    def summary = readFile('reports/summary.txt').trim()
                    def buildStatus = currentBuild.currentResult ?: 'UNKNOWN'
                    def jiraCommentFile = 'reports/jira_comment.json'

                    def jiraComment = """{
                        "body": {
                            "type": "doc",
                            "version": 1,
                            "content": [{
                                "type": "paragraph",
                                "content": [{
                                    "type": "text",
                                    "text": "Automation run completed.\\nStatus: ${buildStatus}.\\n${summary}\\nBuild URL: ${env.BUILD_URL}"
                                }]
                            }]
                        }
                    }"""
                // Use withCredentials for secure access
                withCredentials([usernamePassword(credentialsId: 'Jira_API_Key', usernameVariable: 'JIRA_USER', passwordVariable: 'JIRA_TOKEN')]) {
                    bat """
                        curl -X POST ^
                        --ssl-no-revoke ^
                        -u ${JIRA_CRED_USR}:${JIRA_CRED_PSW} ^
                        -H "Content-Type: application/json" ^
                        --data "${jiraComment}" ^
                        ${JIRA_URL}/rest/api/3/issue/${JIRA_ISSUE}/comment
                    """
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/*.*', allowEmptyArchive: true
        }
        failure {
            echo 'Build failed. Check the HTML report for details.'
        }
    }
}
