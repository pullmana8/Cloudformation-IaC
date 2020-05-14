# Udacity Cloud DevOps Capstone Project

> In this capstone project, I applied my skills and knowledge that I've gained throughout the Cloud DevOps Nanodegree program.

## Project Tasks

* AWS Environment / Console
* Utilize Jenkins to implement CI/CD
* Build Pipelines with Jenkins
* Utilizing CloudFormation to deploy clusters
* Build Kubernetes cluster
* Build Docker containers in pipelines

## About Project

This project is the capstone for Cloud DevOps Nanodegree program which comprise of all that I learned through the materials.

## Key Things to Look For

Plugins Needed:

* Blue Ocean
* CloudBees AWS Credentials
* AWS CodePipeline (optional)
* AWS Steps

### Project Requirements

* AWS CLI v2
* Docker
* Java 11
* Jenkins
* eksctl
* Kubectl
* tidy

## Deployment Strategy

This project shows blue/green deployment strategy for two different versions on nginx running. This Jenkinsfile will run after the initial cluster is created through one Jenkinsfile, and removed from the Jenkinsfile because the pipeline will attempt to build the cluster as if you don't have any. If you like to see screenshots, please see screenshots folder.