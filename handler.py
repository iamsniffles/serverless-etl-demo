import os
import json
import flatten_json
import dataset
import boto3
import s3fs

from copy import deepcopy

def executor(event, context):
    client = boto3.client('stepfunctions', region_name=os.environ['REG'])
    client.start_execution(stateMachineArn=os.environ['ARN'], input=json.dumps(event))

    return client.describe_execution(executionArn=os.environ['ARN'])

def extractRawEvent(event, context):
    return flatten_json.flatten(event, '_')

def extractEvent(event, context):
    result = deepcopy(event)
    result.pop('data', None)
    result['event_id'] = result.pop('id')

    return result

def extractCharge(event, context):
    result = deepcopy(event)
    result = result['data']['object']
    result.pop('source', None)
    result['charge_id'] = result.pop('id')
    result['refunds'] = None if not result['refunds'] else json.dumps(result['refunds'])
    result['metadata'] = None if not result['metadata'] else json.dumps(result['metadata'])

    return result

def extractCard(event, context):
    result = deepcopy(event)
    result = result['data']['object']['source']
    result['cc_id'] = result.pop('id')

    return result

def extractEventMap(event, context):
    result = {}
    result['event_id'] = event['id'] if 'id' in event else ''
    result['charge_id'] = event['data']['object']['id'] if 'id' in event else ''
    result['cc_id'] = event['data']['object']['source']['id'] if 'id' in event else ''

    return result

def upsertRawEvent(event, context):
    db = dataset.connect(os.environ['DB_URL'])
    tbl_event = db.get_table('event_raw', primary_id='id', primary_type='String')
    tbl_event.upsert(event, ['id'])

    return {
        'message': 'Upserted raw event to database!',
        'id': event['id']
    }

def upsertEvent(event, context):
    db = dataset.connect(os.environ['DB_URL'])
    tbl = db.get_table('event', primary_id='event_id', primary_type='String')
    tbl.upsert(event, ['event_id'])
    return {
        'message': 'Upserted event detail to database!',
        'event_id': event['event_id']
    }

def upsertCharge(event, context):
    db = dataset.connect(os.environ['DB_URL'])
    tbl = db.get_table('charge', primary_id='charge_id', primary_type='String')
    tbl.upsert(event, ['charge_id'])
    return {
        'message': 'Upserted charge detail to database!',
        'charge_id': event['charge_id']
    }

def upsertCard(event, context):
    db = dataset.connect(os.environ['DB_URL'])
    tbl = db.get_table('cc', primary_id='cc_id', primary_type='String')
    tbl.upsert(event, ['cc_id'])
    return {
        'message': 'Upserted credit card detail to database!',
        'cc_id': event['cc_id']
    }

def upsertEventMap(event, context):
    db = dataset.connect(os.environ['DB_URL'])
    tbl = db.get_table('event_map', primary_id='event_id', primary_type='String')
    tbl.upsert(event, ['event_id'])
    return {
        'message': 'Upserted event mapping to database!',
        'event_id': event['event_id']
    }

def writeCardCSVS3(event, context):
    s3 = s3fs.S3FileSystem()
    bucket = os.environ['BUCKET']
    fname = event['cc_id'] + '.csv'

    if s3.exists(bucket + '/' + fname):
        return {'message': event['cc_id'] + ' ' + 'exists!'}
    else:
        val = ['' if v is None else v for v in event.values()]
        val = [str(v) for v in val]
        content = ', '.join(event.keys()) + '\n' + ', '.join(val)

        with open('/tmp/' + fname, 'w') as f:
            f.write(content)

        s3.put('/tmp/' + fname, bucket + '/' + fname)

        os.remove('/tmp/' + fname)

        return {
            'message': 'Added credit card detail to S3!',
            'file': event['cc_id'] + '.csv'
        }
