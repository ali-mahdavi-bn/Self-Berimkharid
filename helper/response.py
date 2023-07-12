from rest_framework.response import Response
from datetime import datetime
from rest_framework import status


def local_response(type, success, message, field, data):
    localStatus = status.HTTP_200_OK
    if type == 'ok': localStatus = status.HTTP_200_OK
    if type == 'create': localStatus = status.HTTP_201_CREATED
    if type == 'notFound': localStatus = status.HTTP_404_NOT_FOUND
    if type == 'found': localStatus = status.HTTP_200_OK
    if type == 'unAuthorized': localStatus = status.HTTP_401_UNAUTHORIZED
    if type == 'serverErr': localStatus = status.HTTP_500_INTERNAL_SERVER_ERROR
    if type == 'deleted': localStatus = status.HTTP_204_NO_CONTENT
    if type == 'badReq': localStatus = status.HTTP_400_BAD_REQUEST

    res = {
        'success': success,
        'message': {
            'field': field,
            'message': message,
            'logCode': '0'
        },
        'data': data,
        'time': datetime.now(),
        'v': '1'
    }
    return Response(res, status=localStatus)


def validation_response(messages):
    res = {
        'success': False,
        'messages': messages,
        'data': {},
        'time': datetime.now(),
        'v': '1'
    }
    return Response(res, status=status.HTTP_400_BAD_REQUEST)
