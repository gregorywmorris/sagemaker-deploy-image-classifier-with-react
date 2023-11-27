import json
import boto3
import base64


endpoint_name='demo-pneumonia-classifier-gm'

sagemaker_runtime_cient=boto3.client('runtime.sagemaker')

# event comes from API
# A context object is passed to your function by Lambda at runtime. This object provides methods and properties that provide information about the invocation, function, and runtime environment.
def lambda_handler(event, context):
    print(event)
    image=base64.b64decode(event['image'])
    print(image)
    return _predictPneumonia(image)
    
def _predictPneumonia(image):
    response=sagemaker_runtime_cient.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/x-image",
        Body=image)
        
    result=response['Body'].read()
    # json to covnert from byte array
    result=json.loads(result)
    print('results',result)
    predicted_class=0 if result[0]>result[1] else 1
    toSend=result[0] if result[0]>result[1] else result[1]
    
    if predicted_class==0:
        return f'Negative for pnemonia with a probability of : {toSend}'
    else:
            return f'Positive for pneumonia with a probability of : {toSend}'