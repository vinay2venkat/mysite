from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.index, name='index'),
	#path('<int:question_id>/', views.detail, name='detail'),
    #path('<int:question_id>/results/', views.results, name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
	#GenericViews
	#path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('question/<int:pk>/', views.QuestionRudView.as_view(), name='quesapibyid'),
    path('question/', views.QuestionList.as_view(), name='quesapi'),
    path('createquestion/', views.QuestionCreateView.as_view(), name='creaques'),
    path('createchoice/', views.ChoiceCreateView.as_view(), name='creachoice'),
    path('createchoice/', views.ChoiceCreateView.as_view(), name='creachoice'),
    path('useractivity/', views.UserActivity, name='user_activity'),

]

urlpatterns = format_suffix_patterns(urlpatterns)