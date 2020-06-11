from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .serializers import BoardsSerializer, TodosSerializer
from rest_framework.generics import GenericAPIView
from .models import Boards, Todos
from django.db import transaction
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.utils import timezone


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    csrf_exempt analogue
    """
    def enforce_csrf(self, request):
        return


class BoardApiView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BoardsSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)

    def _get_elements(self):
        """
        Get all board's elements
        :return: dict with boards elements
        """
        boards_queryset = Boards.objects.all()
        todo_count = Todos.objects.filter(board__in=boards_queryset).count()
        return {"todo_count": todo_count,
                "boards": self.serializer_class(boards_queryset, many=True).data}

    def _get_todos(self, board_id, type):
        """
        :param board_id: board pk
        :param type: 1 - returns todos objects, 2- return todos objects with done=False
        :param request: request obj
        :return: type: 1 - returns todos objects, 2- return todos objects with done=False, else returns all boards
        """
        if int(type) == 1:
            return {"todos": TodosSerializer(Todos.objects.filter(board=int(board_id)), many=True).data}
        elif int(type) == 2:
            return {"todos": TodosSerializer(Todos.objects.filter(board=int(board_id), done=False), many=True).data}
        else:
            return self._get_elements()

    def get(self, request, **kwargs):
        """
        board : pk of board
        type : 1 - returns todos objects,
        type : 2- return todos objects with done=False,
        all else returns all boards
        :param request:
        :param kwargs:
        :return: JsonResponse with todos or boards elements, based on request
        """
        if request.query_params.get('type') is not None:
            todos = self._get_todos(request.query_params.get('board'), request.query_params.get('type'))
            return JsonResponse(todos)
        response = self._get_elements()
        return JsonResponse(response)

    def post(self, request, **kwargs):
        """
        creates a board
        names : list of boards names
        :param request:
        :param kwargs:
        :return: all boards
        """
        Boards.objects.bulk_create([Boards(name=x) for x in request.data["names"]])
        response = self._get_elements()
        return JsonResponse(response)

    def put(self, request):
        """
        updates board name by id
        id : board pk
        title : new name of board
        :param request:
        :return: all boards
        """
        with transaction.atomic():
            for i in request.data['boards']:
                frame = Boards.objects.get(id=i['id'])
                frame.name = str(i.get('title')) if i.get('title', None) is not None else frame.name
                frame.updated = timezone.now()
                frame.save()
        response = self._get_elements()
        return JsonResponse(response)

    def delete(self, request):
        """
        id_s : list of boards pk which should be deleted
        deletes boards by ids
        :param request:
        :return:
        """
        Boards.objects.filter(id__in=request.data['id_s']).delete()
        response = self._get_elements()
        return JsonResponse(response)


class ToDoApiView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodosSerializer
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)

    def _get_elements(self):
        """
        return all todos elements
        :param request:
        :return:
        """
        return {"todos": self.serializer_class(Todos.objects.all(), many=True).data}

    def _get_todos(self, type, ):
        """
        :param type 1- return todos objects with done=False
        :param request: request obj
        :return: 1 - return todos objects with done=False, else returns all boards
        """
        if int(type) == 1:
            return {"todos": TodosSerializer(Todos.objects.filter(done=False), many=True).data}
        else:
            return self._get_elements()

    def get(self, request, **kwargs):
        """
        board : pk of board
        type : 1 - returns todos objects,
        type : 2- return todos objects with done=False,
        all else returns all boards
        :param request:
        :param kwargs:
        :return: JsonResponse with todos or boards elements, based on request
        """
        if request.query_params.get('type') is not None:
            todos = self._get_todos(request.query_params.get('type'))
            return JsonResponse(todos)
        response = self._get_elements()
        return JsonResponse(response)

    def post(self, request, **kwargs):
        """
        creates a board
        names : list of boards names
        :param request:
        :param kwargs:
        :return: all boards
        """
        Todos.objects.bulk_create(
            [Todos(title=x['title'], author=request.user, board_id=int(x['board'])) for x in request.data['todos']])
        response = self._get_elements()
        return JsonResponse(response)

    def put(self, request):
        """
        updates board name by id
        id : board pk
        title : new name of board
        :param request:
        :return: all boards
        """
        with transaction.atomic():
            for i in request.data['todos']:
                frame = Todos.objects.get(id=i['id'])
                frame.title = str(i.get('title')) if i.get('title', None) is not None else frame.title
                frame.done = i.get('done') if i.get('done', None) is not None else frame.done
                frame.board_id = i.get('board') if i.get('board', '') != '' else frame.board_id
                frame.updated = timezone.now()
                frame.save()
        response = self._get_elements()
        return JsonResponse(response)

    def delete(self, request):
        """
        id_s : list of todos pk which should be deleted
        deletes boards by ids
        :param request:
        :return:
        """
        Todos.objects.filter(id__in=request.data['id_s']).delete()
        response = self._get_elements()
        return JsonResponse(response)
