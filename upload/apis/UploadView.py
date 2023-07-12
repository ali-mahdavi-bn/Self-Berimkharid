from rest_framework.views import APIView

from upload.serializers.UploadSerializer import UploadCreateSerializer, UploadShowSerializer

from helper.response import local_response, validation_response

from rest_framework.permissions import IsAuthenticated


class UploadCreateView(APIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = UploadCreateSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = UploadShowSerializer(serializer.save())
            return local_response('create', True, "ok", '', {'id': result.data['id']})
        else:
            return validation_response(serializer.errors)
