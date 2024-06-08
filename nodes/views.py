from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Node, Sensor, Actuator, Data_Sensor, Data_Actuator
from gateway.settings import MQTT_NODE, NODE_AUTH

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def register(features):
    try:
        # Create a node object
        node_object = Node(
            feature=features,
        )
        # Save the node object
        node_object.save()
        if features == "sensor":
            sensor_object = Sensor(id=node_object)
            sensor_object.save()
        elif features == "actuator":
            actuator_object = Actuator(id=node_object)
            actuator_object.save()
        # Trả về ID của node sau khi nó được lưu
        return node_object.id
    except Exception as e:
        # Xử lý các trường hợp ngoại lệ nếu có
        print(f"Error registering node: {e}")
        return None

# Create a function to handle POST request /register_node for listening nodes registration
def register_node(request):
    if request.method == 'GET':
    # Check if the request has a variable named 'code' in body
        code = request.GET['code']
        if code is not None:
            # Get the code from the request body
            # Check if the code is correct
            if code == NODE_AUTH["SENSOR_KEY"] or code == NODE_AUTH["ACTUATOR_KEY"]:
                # Register the node
                if code == NODE_AUTH["SENSOR_KEY"]:
                    feature = 'sensor'
                else:
                    feature = 'actuator'

                node_id = register(feature)
                # Check if the node is registered
                if node_id is not None:
                    return JsonResponse({'status': 200, 'node_id': node_id, 'username': MQTT_NODE['username'], 'password': MQTT_NODE['password']})
                else:
                    # Return error
                    return JsonResponse({'status': 400, 'error': 'Error registering node'})
            else:
                # Return error
                return JsonResponse({'status': 400, 'error': 'Invalid code'})
        else:
            # Return error
            return JsonResponse({'status': 400, 'error': 'Invalid request'})
    else:
        return JsonResponse({'status': 400, 'error': 'Invalid request method'})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_data(request):
    nodes = Node.objects.all()
    list_data = []
    for node in nodes:
        status, data = node.get_data_latest()
        list_data.append({
            'id': node.id,
            'feature': node.feature,
            'status': status,
            'data': data
        })
    return Response(list_data)

@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
def auto_mode(request):
        from .mqtt import auto_flag
        return JsonResponse({'status': 200, 'auto_flag': auto_flag})
