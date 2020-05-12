# Vault

`export VAULT_ADDR='http://127.0.0.1:8200'`
`export VAULT_DEV_ROOT_TOKEN_ID=""`

Enable AWS

`vault secrets aws`

Setup Vault with the account Access Key and Secret Key

`[default]`
`aws_access_key_id=`
`aws_secret_access_key=`

```bash
vault write aws/config/root \
    access_key=<AWS_ACCESS_KEY_ID> \
    secret_key=<AWS_SECRET_ACCESS_KEY> \
    region=us-east-2
Sucess! Enabled the aws secrets engine at: aws/
```

Create EC2 role for user

```bash
vault write aws/roles/ec2_admin_role \
    credential_type=iam_user \
    policy_document=-<<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
        {
            "Effect": "Allow",
            "Action": "ec2:*",
            "Resource": "*"
        }
    ]
}
EOF
Success! Data written to: aws/roles/ec2_admin_role
```

You can also add by policy.json instead of inline bash code.

```bash
vault write aws/roles/ec2_admin_role \
    credential_type=iam_user \
    policy_document=@policy.json
Success! Data written to: aws/roles/ec2_admin_role
```

Save the credenttials
`vault read aws/roles/ec2_admin_role`
