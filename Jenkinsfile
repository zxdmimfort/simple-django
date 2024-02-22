#!groovy
properties([disableConcurrentBuilds()])
pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
        timestamps()
    }
    stages {
        stage("docker login") {
            steps {
                echo "=========== docker login ==========="
                withCredentials([usernamePassword(credentialsId: 'dockerhub_zxdmimfort', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'docker login -u $USERNAME -p $PASSWORD'
                }
            }
        }
        stage("create docker image") {
            steps {
                echo "=========== start building image ==========="
                dir ('backend') {
                    sh 'docker build -t zxdmimfort/simple_django:latest .'
                }
            }
        }
        stage("docker push") {
            steps {
                echo "=========== docker push ==========="
                sh 'docker push zxdmimfort/simple_django:latest'
            }
        }
        stage("deploy to srv") {
            steps {
                echo "=========== trigger watchtower on srv ==========="
                withCredentials([string(credentialsId: 'watchtower_token', variable: 'TOKEN')]) {
                    sh 'curl -H "Authorization: Bearer $TOKEN" localhost:54321/v1/update'
                }
            }
        }
    }
}