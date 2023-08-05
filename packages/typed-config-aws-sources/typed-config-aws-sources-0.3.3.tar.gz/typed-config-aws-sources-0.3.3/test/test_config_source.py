from typedconfig_awssource import IniS3ConfigSource, DynamoDbConfigSource, SecretsManagerConfigSource, ParameterStoreConfigSource
import os
import boto3
import botocore.exceptions
from moto import mock_s3, mock_dynamodb2, mock_secretsmanager, mock_ssm
from unittest.mock import patch
import pytest
from typedconfig.source import ConfigSource
from typedconfig_awssource.__version__ import __version__


# Note - patching these credentials is a workaround until another release of moto is made
aws_cred_patch = patch.dict(os.environ, {
    "AWS_ACCESS_KEY_ID": "foobar_key",
    "AWS_SECRET_ACCESS_KEY": "foobar_secret",
    "AWS_DEFAULT_REGION": 'eu-west-1'
})


def do_assertions(source: ConfigSource, must_exist=False):
    assert source.get_config_value('S', 'A') == source.get_config_value('s', 'a')

    v = source.get_config_value('s', 'a')
    assert '1' == v

    if must_exist:
        with pytest.raises(Exception):
            source.get_config_value('t', 'a')
    else:
        v = source.get_config_value('t', 'a')
        assert v is None

    if must_exist:
        with pytest.raises(Exception):
            source.get_config_value('s', 'c')
    else:
        source.get_config_value('s', 'c')
        assert v is None


def do_assertions_with_limited_keys(source: ConfigSource, must_exist, only_these_keys):
    assert source.get_config_value('S', 'A') == source.get_config_value('s', 'a')

    if only_these_keys is not None:
        v = source.get_config_value('s', 'a')
        if ('s', 'a') in only_these_keys:
            assert v == '1'
        else:
            assert v is None
        if ('s', 'b') in only_these_keys:
            if must_exist:
                with pytest.raises(Exception):
                    source.get_config_value('s', 'b')
            else:
                v = source.get_config_value('s', 'b')
                assert v is None
        else:
            v = source.get_config_value('s', 'b')
            assert v is None
    else:
        do_assertions(source, must_exist)


@pytest.mark.parametrize("param_type", (
    "String",
    "SecureString"
))
@pytest.mark.parametrize("must_exist,only_these_keys", (
    (True, None),
    (False, None),
    (True, {('s', 'a')}),
    (True, {('s', 'b')}),
    (True, set()),
    (False, {('s', 'a')}),
    (False, {('s', 'b')}),
    (False, set()),
))
@mock_ssm
@aws_cred_patch
def test_parameter_store_config_source(param_type, must_exist, only_these_keys):
    client = boto3.client('ssm')
    client.put_parameter(
        Name='project/s/a',
        Value="1",
        Type=param_type
    )

    source = ParameterStoreConfigSource(parameter_name_prefix='project', must_exist=must_exist,
                                        only_these_keys=only_these_keys)

    do_assertions_with_limited_keys(source, must_exist, only_these_keys)


@pytest.mark.parametrize("must_exist,only_these_keys", (
    (True, None),
    (False, None),
    (True, {('s', 'a')}),
    (True, {('s', 'b')}),
    (True, set()),
    (False, {('s', 'a')}),
    (False, {('s', 'b')}),
    (False, set()),
))
@mock_secretsmanager
@aws_cred_patch
def test_secrets_manager_config_source(must_exist, only_these_keys):
    client = boto3.client('secretsmanager')
    client.create_secret(
        Name='project/s',
        SecretString='{"a": "1"}'
    )

    source = SecretsManagerConfigSource(secret_name_prefix='project', must_exist=must_exist, only_these_keys=only_these_keys)

    do_assertions_with_limited_keys(source, must_exist, only_these_keys)


@mock_s3
@aws_cred_patch
def test_ini_s3_config_source():
    client = boto3.client('s3')
    client.create_bucket(Bucket='test-bucket')
    client.put_object(Bucket='test-bucket', Key='test-key', Body="""
[s]
a = 1
""")
    source = IniS3ConfigSource('test-bucket', 'test-key')
    do_assertions(source)


@mock_s3
@aws_cred_patch
def test_ini_s3_config_source_no_bucket_must_exist_false():
    source = IniS3ConfigSource('test-bucket', 'test-key', must_exist=False)
    v = source.get_config_value('s', 'a')
    assert v is None


@mock_s3
@aws_cred_patch
def test_ini_s3_config_source_no_bucket_must_exist_true():
    with pytest.raises(botocore.exceptions.ClientError):
        source = IniS3ConfigSource('test-bucket', 'test-key', must_exist=True)


@mock_dynamodb2
@aws_cred_patch
def test_dynamodb_config_source():
    client = boto3.client('dynamodb')
    client.create_table(
        TableName='test-table',
        AttributeDefinitions=[
            {
                'AttributeName': 'section',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'key',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'value',
                'AttributeType': 'S'
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'section',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'key',
                'KeyType': 'RANGE'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    client.put_item(
        TableName='test-table',
        Item={
            'section': {
                'S': 's'
            },
            'key': {
                'S': 'a'
            },
            'value': {
                'S': '1'
            }
        }
    )

    source = DynamoDbConfigSource(
        table_name='test-table',
        section_attribute_name='section',
        key_attribute_name='key',
        value_attribute_name='value')

    do_assertions(source)


def test_version():
    assert type(__version__) is str
