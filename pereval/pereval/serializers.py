from rest_framework import serializers

from .models import Pereval, User, Coords, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'last_name', 'first_name', 'middle_name']

    def to_internal_value(self, data):
        data = data.copy()
        data['last_name'] = data.pop('fam', '')
        data['first_name'] = data.pop('name', '')
        data['middle_name'] = data.pop('otc', '')

        return super().to_internal_value(data)


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title',]


class PerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pereval
        fields = '__all__'

#Сериализатор для создания новой записи о перевале.
    
    #Обрабатывает вложенные данные для пользователя, координат и изображений.
    #При создании записи автоматически создаются связанные объекты.
    
class PerevalCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'images', 'level_spring',
                  'level_summer', 'level_autumn', 'level_winter']

    def create(self, validated_data):

        user_data = validated_data.pop('user', None)  # Added None as default
        coords_data = validated_data.pop('coords', None)  # Added None as default
        images_data = validated_data.pop('images')

        if user_data is None or coords_data is None:
            raise ValueError("User and Coords data must be provided.")

        user = User.objects.create(**user_data)
        coords = Coords.objects.create(**coords_data)
        pereval = Pereval.objects.create(user=user, coords=coords, **validated_data)

        for image in images_data:
            data = image.pop('data')
            title = image.pop('title')
            Image.objects.create(pereval=pereval, title=title, data=data)

        return pereval


class PerevalSubmitDataSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)
    
    class Meta:
        model = Pereval
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Обновление перевала с сохранением пользовательских данных
        """
        if instance.status != 'NE':
            raise serializers.ValidationError(
                {"message": "Редактирование запрещено - запись не в статусе 'new'"}
            )

        # Обновляем координаты
        coords_data = validated_data.pop('coords', None)
        if coords_data:
            coords_serializer = CoordsSerializer(instance.coords, data=coords_data)
            if coords_serializer.is_valid():
                coords_serializer.save()

        # Обновляем изображения
        images_data = validated_data.pop('images', None)
        if images_data:
            # Удаляем старые изображения
            instance.images.all().delete()
            # Создаем новые
            for image_data in images_data:
                Image.objects.create(pereval=instance, **image_data)

        # Обновляем основные поля перевала
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance




