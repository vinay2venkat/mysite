from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F, Count, Value
from .models import Choice, Question, VoteLog, UserSession
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sessions.models import Session
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer, ChoiceSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler, jwt_encode_handler
from rest_framework import generics, mixins
from django.db.models import Q
from django.db.models import Count
from django.db import IntegrityError
from django.shortcuts import render_to_response
import requests
from django.views.generic import View






def UserActivity(request):
    session_id = request.session.session_key
    session = Session.objects.get(session_key=session_id)
    user_id = session.get_decoded().get('_auth_user_id')
    #votelog = VoteLog.objects.all()
    votelog = VoteLog.objects.filter(user_id=user_id)
    totalvotes = VoteLog.objects.filter(user=user_id).count()

    print(votelog)
    # for r in votelog:
    #     # print(r)
    #     # print(r.user.username)
    #     print(r.question.question_text)
    #     print(r.choice.choice_text)
        #print(r.user.username.count())

    context = {
        'votelog' : votelog,
        'totalvotes' : totalvotes


    }

    return render(request, 'polls/user_activity.html', context)




def stats(request):
    question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    saved_reports = VoteLog.objects.all()
    context = {
           'question_list': question_list,
           'tweets': getTweets(),
           'weather': getWeather(request),
           'dc':getiMMi(request),

       }

    print(context['weather'])
    return render(request, 'home.html', context)


def getWeather(request):
    weather = []
    zip = request.POST.get('zip')
    # tempt = {'tempt': 0.0}
    if zip is not None:
       z=requests.get('http://api.openweathermap.org/data/2.5/weather?zip='+zip+',in&appid=c90036e4396e0b0f12c2dbfa04cb00a3')
       # c=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+zip+',in&appid=c90036e4396e0b0f12c2dbfa04cb00a3')
       json_object = z.json()
       print(json_object)
       tempt = float(json_object['main']['temp'])
       place = json_object['name']
       tempa = (tempt - 273.15)
       tempi = str(tempa)
       print(tempi)
       weather.append({'place': place, 'content': 'temperature is', 'tempi': tempi, 'cont':'Degree Celsius'})
       return {'weather':weather}

def getiMMi(request):
    immi = []
    patid = request.POST.get('patid')
    if patid is not None:
       z = requests.get('https://immi.imminentlife.com/Prod/patient/routineFinalInference?immiPatId=000-000-'+patid+'')
       json_object = z.json()
       dc = json_object['routineResults']
       return dc

    # eg = Question.objects.get(pk=1).votelog_set.all()
    # print(eg)
    # print(saved_reports)
    # for r in saved_reports:
    #     print(r)
    #     print(r.user.username)
    #     print(r.question.question_text)
    #     print(r.choice.choice_text)
        #print(r.user.username.count())

def getTweets():
    tweets = []
    try:
        import twitter
        api = twitter.Api(consumer_key='8b78Yp3VEpc6uNxgx3Pg4j2Ai',
                          consumer_secret='ddOQDloDrQOTImurCbmYVdZtM8oBF3H4JBykAdWUoLDGFLcqkB',
                          access_token_key='511582481-j0RKp48WyaNE6oghpcL3fvnyJKnS0iSWaBRHgVnY',
                          access_token_secret='eC4eupA3GrdMarH9rz4trx1QqcN6qanuTZCXbCjIx2yB9')
        latest = api.GetUserTimeline(screen_name='@GalGadot', count=5)
        for tweet in latest:
            status = tweet.text
            tweets.append({'status': status})
    except:
        tweets.append({'status': 'follow us at vinay venkat edits'})
    return {'tweets':tweets}



@login_required()
def index(request):
    session_id = request.session.session_key
    session = Session.objects.get(session_key=session_id)
    user_id = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=user_id)


    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    context = {
        'latest_question_list': latest_question_list,
        'user' : user
    }

    return render(request, 'polls/index.html', context)


class DetailView(LoginRequiredMixin, generic.DetailView):
    #login_url = '/login/'
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(LoginRequiredMixin, generic.DetailView):
    #login_url = '/login/'
    model = Question
    template_name = 'polls/results.html'


@login_required()
def vote(request, question_id):
    login_url = '/register/login/'
    session_id = request.session.session_key
    session = Session.objects.get(session_key=session_id)
    user_id = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=user_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if VoteLog.objects.filter(user_id=user_id, question=question_id).exists():
                #raise forms.ValidationError("You already gave your vote")
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "You already gave your vote.",
                })

        selected_choice.votes = F('votes') + 1
        print(user_id)
        selected_choice.save()
        selected_choice.votelog_set.create(question_id=question_id, user_id=user_id)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#User SESSION Views
def user_logged_in_handler(sender, request, user, **kwargs):
    try:
        UserSession.objects.get_or_create(
              user = user,
              session_id = request.session.session_key
        )
    except IntegrityError:
        message = 'IntegrityError accoured'
        return render_to_response("login/login.html", {"message": message})
user_logged_in.connect(user_logged_in_handler)


def delete_user_sessions(user):
    user_sessions = UserSession.objects.filter(user = user)
    for user_session in user_sessions:
        user_session.session.delete()

#API Views
class QuestionCreateView(mixins.CreateModelMixin, generics.ListAPIView):
    serializer_class = QuestionSerializer


    def get_queryset(self):
        qs=Question.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs=qs.filter(Q(pk__icontains=query)|Q(question_text__icontains=query)).distinct()
        return qs

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



class QuestionRudView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    serializer_class = QuestionSerializer


    def get_queryset(self):
        # content = {
        #     'user': unicode(request.user),  # `django.contrib.auth.User` instance.
        #     'auth': unicode(request.auth),  # None
        # }

        return Question.objects.all()

class QuestionList(APIView):

    def get(self, request):

        question =Question.objects.all()
        serializer = QuestionSerializer(question, many=True)
        return Response(serializer.data)

class ChoiceCreateView(generics.CreateAPIView):
    serializer_class = ChoiceSerializer


    def get_queryset(self):
        return Choice.objects.all()

