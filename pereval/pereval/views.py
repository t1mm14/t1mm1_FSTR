from rest_framework import viewsets
from .models import User, Coords, Pereval, Image
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.db import DatabaseError
from .serializers import UserSerializer, CoordsSerializer, PerevalSerializer, ImageSerializer, PerevalCreateSerializer, PerevalSubmitDataSerializer
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


#API endpoint для создания новой записи о перевале.
    
    #Принимает POST запрос с данными о перевале, включая информацию о пользователе,
    #координатах и изображениях. При успешном создании возвращает ID созданной записи.
    
class PerevalCreateAPIView(CreateAPIView):
    serializer_class = PerevalCreateSerializer

    def post(self, request, *args, **kwargs):
        pereval_serializer = self.get_serializer(data=request.data)
        try:
            if pereval_serializer.is_valid(raise_exception=True):
                pereval = pereval_serializer.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    'message': 'Перевал успешно создан!',
                    "id": pereval.id
                }, status=status.HTTP_200_OK)

        except DatabaseError as db_err:
            # Обработка ошибок базы данных
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(db_err),
                "id": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Обработка других ошибок
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "id": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Если данные не валидны, вернуть ошибку валидации
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": pereval_serializer.errors,
            "id": None
        }, status=status.HTTP_400_BAD_REQUEST)

class SubmitDataViewSet(viewsets.ModelViewSet):
    serializer_class = PerevalSubmitDataSerializer
    
    def get_queryset(self):
        """
        Фильтрация перевалов по email пользователя
        """
        queryset = Pereval.objects.all()
        email = self.request.query_params.get('user__email', None)
        if email is not None:
            queryset = queryset.filter(user__email=email)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        GET /submitData/<id>
        Получение информации о перевале по id
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH /submitData/<id>
        Редактирование существующей записи
        """
        instance = self.get_object()
        
        # Удаляем поля пользователя из данных, если они присутствуют
        user_fields = ['user', 'email', 'fam', 'name', 'otc', 'phone']
        for field in user_fields:
            request.data.pop(field, None)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            return Response({
                'state': 1,
                'message': 'Запись успешно обновлена'
            })
        except serializers.ValidationError as e:
            return Response({
                'state': 0,
                'message': str(e.detail)
            }, status=status.HTTP_400_BAD_REQUEST)