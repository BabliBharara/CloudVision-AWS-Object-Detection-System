import json
import boto3
import base64

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):

    body = json.loads(event['body'])

    # Get base64 image from website
    image_data = base64.b64decode(body['image'])

    # Detect labels directly from uploaded image
    response = rekognition.detect_labels(
        Image={
            'Bytes': image_data
        },
        MaxLabels=20,
        MinConfidence=70
    )

    labels = []

    for label in response['Labels']:

        if len(label['Instances']) == 0:
            continue

        if label['Name'] in ['Person', 'Adult', 'Female', 'Woman', 'Man']:
            continue

        for instance in label['Instances']:

            labels.append({
                "Name": label['Name'],
                "Confidence": round(label['Confidence'], 2),
                "BoundingBox": {
                    "Width": instance['BoundingBox']['Width'],
                    "Height": instance['BoundingBox']['Height'],
                    "Left": instance['BoundingBox']['Left'],
                    "Top": instance['BoundingBox']['Top']
                }
            })

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(labels)
    }
