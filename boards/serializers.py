from rest_framework import serializers, viewsets
from boards.models import Boards, Todos
from django.contrib.auth.models import User


class BoardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boards
        fields = ['id', 'name']


class TodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields = ['id', 'title', 'done', 'created', 'updated', 'board']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class BoardsViewSet(viewsets.ModelViewSet):
    queryset = Boards.objects.all()
    serializer_class = BoardsSerializer


class TodosViewSet(viewsets.ModelViewSet):
    queryset = Todos.objects.all()
    serializer_class = TodosSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
