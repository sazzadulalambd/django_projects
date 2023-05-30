from django.views import View
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter  # search and ordering
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import Task, Team
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.core.paginator import Paginator
from rest_framework.pagination import LimitOffsetPagination
# for mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
# for pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import os


# Create your views here.


class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 6
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 10


class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({'status': False, 'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({'status': False, 'message': 'Invalid User'}, status.HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)
        print(token)
        return Response({'status': True, 'message': 'User login successful', 'token': str(token)}, status.HTTP_201_CREATED)


class RegisterAPI(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({'status': False, 'message': serializer.errors}, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'status': True, 'message': 'User created successful'}, status.HTTP_201_CREATED)

# for team


class TeamView(viewsets.ModelViewSet):

    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    [TokenAuthentication]
    [IsAuthenticated]

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    pagination_class = MyLimitOffsetPagination

    # for search
    filter_backends = [SearchFilter]
    search_fields = ['^name', 'name', 'position']

    # for ordering
    # filter_backends=[OrderingFilter]


# for task
@api_view(['GET'])
def index(request):
    all_urls = {
        'login  urls': 'http://127.0.0.1:8000/login/',
        'signup urls': 'http://127.0.0.1:8000/register/',
        'task   urls': 'http://127.0.0.1:8000/tasks/',
        'teams  urls': 'http://127.0.0.1:8000/api/teams/',

    }
    return Response(all_urls)

#    return render(request, "Home/index.html")


@api_view(['GET', 'POST'])
def task_list(request):

    [TokenAuthentication]
    [IsAuthenticated]

    if request.method == 'GET':

        tasks = Task.objects.all()
        # tasks = Task.objects.all().filter(pending = True, completed = False).values()

        serializer = TaskSerializer(
            tasks, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):

    [TokenAuthentication]
    [IsAuthenticated]

    try:
        task = Task.objects.get(id=pk)   # task
    except task.DoesNotExist:            # task
        return Response({'message': 'This task is unable'}, status=status.HTTP_404_NOT_FOUND)

    # make pdf

    template = get_template('Task/task_pdf.html')
    data = {
        'title':  task.title,
        'description':  task.description,
        'assign':  task.assign,
        'position':  task.assign.position,
        'completed': task.completed,
        'pending':  task.pending,
        'created_at':  task.created_at,
        'updated_at':  str(task.updated_at),
    }
    html = template.render(data)
    result = BytesIO()
    # , link_callback=fetch_resources)
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    pdf = result.getvalue()
    filename = 'Task_' + data['title'] + '.pdf'

    # Send mail
    subject = 'This Task', pk
    from_email = "noreply.ygbl@gmail.com"
    to = "shawon.ygbl@gmail.com"
    text_content = "This is an important message."
    html_content = "<p>This is an <strong>important task Primary key: {pk} </strong> message.</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.attach(filename, pdf, 'application/pdf')
    msg.attach_file("F:/Tools/task/Task Manager/AIUB.jpg")
    msg.send()

    if request.method == 'GET':

        serializer = TaskSerializer(
            task, many=False, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(instance=task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_426_UPGRADE_REQUIRED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task.delete()
        return Response({'message': 'Task is deleted'}, status=status.HTTP_204_NO_CONTENT)


# make pdf

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # , link_callback=fetch_resources)
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePdf(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            task_db = Task.objects.get(id=pk)
        except:
            return HttpResponse("505 Not Found")
        data = {
            'title':  task_db.title,
            'description':  task_db.description,
            'assign':  task_db.assign,
            'position':  task_db.assign.position,
            'completed': task_db.completed,
            'pending':  task_db.pending,
            'created_at':  task_db.created_at,
            'updated_at':  str(task_db.updated_at),
        }
        pdf = render_to_pdf('Task/task_pdf.html', data)
        # return HttpResponse(pdf, content_type='application/pdf')

        # force download
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "task_%s.pdf" % (data['title'])
            content = "inline; filename='%s'" % (filename)
            # download = request.GET.get("download")
            # if download:
            content = "attachment; filename=%s" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


# old apis

# @api_view(['GET'])
# def index(request):
#     all_urls = {
#         'Task list  ': 'http://127.0.0.1:8000/tasks/',
#         'Single task': 'http://127.0.0.1:8000/task/0/',
#         'Create task': 'http://127.0.0.1:8000/task/',
#         'Update task': 'http://127.0.0.1:8000/task-update/0/',
#         'Delete task': 'http://127.0.0.1:8000/task-delete/0/',
#     }
#     return Response(all_urls)


# @api_view(['GET'])
# def alltasks(request):
#         # tasks = Task.objects.all()
#         tasks = Task.objects.all().filter(pending = True, completed = False).values()
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)


# @api_view(['GET'])
# def task(request, pk):
#     task = Task.objects.get(id=pk)
#     serializer = TaskSerializer(task, many=False)
#     return Response(serializer.data)


# @api_view(['POST'])
# def create(request):
#     serializer = TaskSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['PUT'])
# def update(request, pk):
#     task = Task.objects.get(id=pk)
#     serializer = TaskSerializer(instance=task, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_426_UPGRADE_REQUIRED)


# @api_view(['DELETE'])
# def delete(request, pk):
#     task = Task.objects.get(id=pk)
#     task.delete()
#     return Response('Task Deleted!!!', status=status.HTTP_508_LOOP_DETECTED)
