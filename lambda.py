import boto3
import json
import urllib2

s3 = boto3.client('s3')
bucket = "epic-unicorns"
resp = []

def handle_msg(msg)
    msg_id = msg['Id']
    part_number = msg['PartNumber']
    total_parts = msg['TotalParts']
    data = msg['Data']
    try:
        obj = s3.get_object(Bucket=bucket, Key=msg_id)
        old_msg = json.loads(obj['Body'].read())
        old_msg['Data' + str(part_number)] = msg['Data']
        print("Found" + json.dumps(old_msg))
        combined=""
        for ind in range(0, total_parts):
            data_var = 'Data' + str(ind)
            if data_var not in old_msg:
                s3.put_object(Bucket='epic-unicorns', Key=msg_id, Body=json.dumps(msg))
                return
            combined = combined + old_msg[data_var]
        msg['Data'] = combined
        url = 'https://dashboard.cash4code.net/score/' + msg_id
        req = urllib2.Request(url, data=combined, headers={'x-gameday-token':'75114c5a0f'})
        resp = urllib2.urlopen(req)
        resp.close()
        print("Combined: " + json.dumps(msg))
        s3.delete_object(Bucket=bucket, Key=msg_id)
        return {
            "statusCode": 200,
            "headers": { },
            "body": combined
        }
    except Exception as e:
        print("Got exception " + str(e))
        msg['Data' + str(part_number)] = msg['Data']
        s3.put_object(Bucket='epic-unicorns', Key=msg_id, Body=json.dumps(msg))
        print("Stored " + json.dumps(msg))
        return {
            "statusCode": 200,
            "headers": { },
            "body": ""
        }

def lambda_handler(event, context):
    print("Got event: " + json.dumps(event))
    msg = json.loads(event['body'])
    return handle_msg(msg)
