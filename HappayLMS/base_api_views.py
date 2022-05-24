from rest_framework.views import APIView


class GlobalAPIView(APIView):
    authentication_classes = ()
    permission_classes = []
