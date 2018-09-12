from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from Crawler.Serializers import UserSerializer
from Crawler.models import MyUser


class ErrorResponse:
    @staticmethod
    def error_response(error_code, message):
        data = {"message": message, "ErrorCode": error_code}
        return Response(data)

class SignUp(APIView):
    def post(self, request):
        data = request.data
        exist_id = MyUser.objects.filter(id=data['id'])
        if exist_id.count() != 0:
            return ErrorResponse.error_response(-200, 'same name exist')

        user = dict()
        user['push_token'] = data['push_token']
        user['id'] = data['id']
        user['pw'] = data['pw']
        user_serializer = UserSerializer(data=user)

        if user_serializer.is_valid():
            user_serializer.save()
            return_data = {'message': 'Success', 'ErrorCode': 0}
            return Response(return_data)
        return ErrorResponse().error_response(-1, 'Error at the end')

class SignIn(APIView):
    def post(self, request):
        data = request.data
