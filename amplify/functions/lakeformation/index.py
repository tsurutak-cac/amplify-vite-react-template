import boto3
import json
from aws_lambda_powertools import Logger

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    # TODO: フロントエンドアプリに依り認可の実装は変化するのでスキップ。event変数に含まれるトークン情報を利用
    sts_client = boto3.client('sts')

    # MEMO:  AssumeRoleの信頼ポリシーにアクセス元（Lambda）（arn:aws:sts::AWSアカウント:assumed-role/Lambda実行ロール/Lambda関数）への許可が必要
    # {
    #     "Effect": "Allow",
    #     "Principal": {
    #         "AWS": "arn:aws:sts::994763746457:assumed-role/amplify-amplifyvitereactt-lakeformationServiceRole0-9pWF8meZQDGP/amplify-amplifyvitereacttemp-lakeformation511FAEAF-oQWbwFEPYJf9"
    #     },
    #     "Action": "sts:AssumeRole"
    # }
    assumed_role_object = sts_client.assume_role(
        RoleArn="arn:aws:iam::994763746457:role/amplify-amplifyvitereactt-amplifyAuthtest1GroupRole-zNcgO3CzoluM",
        RoleSessionName="AssumedRoleSession"
    )

    athena_client = boto3.client(
        'athena',
        aws_access_key_id=assumed_role_object['Credentials']['AccessKeyId'],
        aws_secret_access_key=assumed_role_object['Credentials']['SecretAccessKey'],
        aws_session_token=assumed_role_object['Credentials']['SessionToken']
    )

    response = athena_client.start_query_execution(
        QueryString='SELECT * FROM sales_csv',
        QueryExecutionContext={
            'Database': 'kawarui_test6'
        },
        ResultConfiguration={
            'OutputLocation': 's3://dip2025/dbt/athena_query_result/'
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Query submitted successfully')
    }
