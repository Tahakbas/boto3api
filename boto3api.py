import re
from flask import Flask, jsonify, request
from config import config
import boto3
import logging
from botocore.exceptions import ClientError

app = Flask(__name__)

#Session
session = boto3.Session(aws_access_key_id=config['AWS_ACCESS_KEY'],aws_secret_access_key=config['AWS_SECRET_KEY'],region_name=config['AWS_REGION'])

#Logs are written to file
#logging.basicConfig(
#cd    filename=config['LOG_FILE'], 
#   level=config['LOG_LEVEL']
#)
#Error status
@app.errorhandler(404)
def page_not_found(error):
    return "404! Page Not Found", 404

@app.errorhandler(400)
def bad_request(error):
    return "400! Bad Request", 400

@app.errorhandler(500)
def internal_server_error(error):
    return "500! Internal Server Error", 500


#Get instance id
def instanceId_factory():

    array = []
    ec2 = session.client('ec2')
    
    try:
        response = ec2.describe_instances()
        for id in range(len(response['Reservations'])):
            array.append(response['Reservations'][id]['Instances'][0]['InstanceId'])
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
                return "UnauthorizedOperation Error"
        else:
                return "Unexpected error"
    return array


#InstanceId list page
@app.route("/ec2/list",methods = ['GET'])
def instance_list():

    instance_array = instanceId_factory()
    return jsonify(instance_array)
    
    
#Instance detail page   
@app.route("/ec2/list/detail",methods = ['GET'])
def instance_detail_list():

    ec2 = session.client('ec2')

    try:
        response = ec2.describe_instances()
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
                return "UnauthorizedOperation Error"
        else:
                return "Unexpected error"
    return jsonify(response) 


#Instance start page
@app.route("/ec2/start",methods = ['GET','POST'] )
def start_instance():
    
    ec2 = session.client('ec2')
    response = []

    if request.method == 'POST':
        id =  request.args.get("id")
        if id != None:
            try:
                response.append(ec2.start_instances(
                    InstanceIds = [id]
                ))
            except ClientError as e:
                if e.response['Error']['Code'] == 'UnauthorizedOperation':
                    return "UnauthorizedOperation Error"
                else:
                    return "Unexpected error"
            return jsonify(response)
            
    elif request.method == 'GET':
        instance_array = instanceId_factory()
        for i in range(len(instance_array)):
            try:
                response.append(ec2.start_instances(
                    InstanceIds = [instance_array[i]]
                ))
            except ClientError as e:
                if e.response['Error']['Code'] == 'UnauthorizedOperation':
                    return "UnauthorizedOperation Error"
                else:
                    return "Unexpected error"
        return jsonify(response)


@app.route("/ec2/start/<id>",methods = ['POST'] )
def start_instance_url(id):

    response = []
    ec2 = session.client('ec2')
  
    try:
        response.append(ec2.start_instances(
            InstanceIds = [id]
        ))
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            return "UnauthorizedOperation Error"
        else:
            return "Unexpected error"

    return jsonify(response)   


#Instance stop page
@app.route("/ec2/stop",methods = ['GET','POST'] )
def stop_instance():

    response = []
    ec2 = session.client('ec2')

    if request.method == 'POST':
        id = request.args.get("id")
        if id != None:
            try:
                response.append(ec2.stop_instances(
                    InstanceIds = [id]
                ))
            except ClientError as e:
                if e.response['Error']['Code'] == 'UnauthorizedOperation':
                    return "UnauthorizedOperation Error"
                else:
                    return "Unexpected error"
            return jsonify(response)

    elif request.method == 'GET':
        instance_array = instanceId_factory()
        for i in range(len(instance_array)):
            try:
                response.append(ec2.stop_instances(
                    InstanceIds = [instance_array[i]]
                ))
            except ClientError as e:
                if e.response['Error']['Code'] == 'UnauthorizedOperation':
                    return "UnauthorizedOperation Error"
                else:
                    return "Unexpected error"

        return jsonify(response)   


@app.route("/ec2/stop/<id>",methods = ['POST'] )
def stop_instance_url(id):

    response = []
    ec2 = session.client('ec2')
  
    try:
        response.append(ec2.stop_instances(
            InstanceIds = [id]
        ))
    except ClientError as e:
        if e.response['Error']['Code'] == 'UnauthorizedOperation':
            return "UnauthorizedOperation Error"
        else:
            return "Unexpected error"

    return jsonify(response)   


if __name__ == "__main__":
    app.run(host=config["HOST"],debug=config["DEBUG"],port=config["PORT"])
