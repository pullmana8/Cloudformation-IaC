# Cloudformation Project

---

## Setup infastructure

---

Change into the Infrastructure folder. Run the command below.

`aws cloudformation create-stack --stack-name network --template-body file://infrastructure.yml --parameters file://parameters/infrastructure-params.json --capabilities CAPABILITY_IAM`

## Setup bastion server

---

Chande into the Bastion directory. Create the key for EC2 and the S3 bucket before running this command.

`aws cloudformation create-stack --stack-name bastion-servers --template-body file://bastion.yml --parameters file://parameters/bastion-params.json --capabilities CAPABILITY_IAM`

## Setup the application

---

Change into the webapp folder. Create another bucket for the project itself.

`aws cloudformation create-stack --stack-name app-servers --template-body file://webapp.yml --parameters file://parameters/webapp-params.json --capabilities CAPABILITY_IAM`
