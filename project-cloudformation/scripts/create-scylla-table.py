import boto3
dynamodb = boto3.resource('dynamodb',endpoint_url='http://54.157.164.63:8000',
                  region_name='None', aws_access_key_id='AKIAZU4YYGXIHX6BOT7U', aws_secret_access_key='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')

dynamodb.create_table(
    AttributeDefinitions=[
    {
        'AttributeName': 'todoId',
        'AttributeType': 'S',
        'AttributeName': 'userId',
        'AttributeType': 'S'
    },
    ],
    BillingMode='PAY_PER_REQUEST',
    TableName='todostable',
    KeySchema=[
    {
        'AttributeName': 'todoId',
        'KeyType': 'HASH',
        'AttributeName': 'userId',
        'KeyType': 'RANGE'
    },
])

