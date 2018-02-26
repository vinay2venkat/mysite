from rest_framework import serializers
from .models import Question, Choice


class QuestionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Question
        fields = ['pk','question_text', 'pub_date']
        #read_only_fields = ['question_text']


class ChoiceSerializer(serializers.ModelSerializer):


    class Meta:
        model = Choice
        fields = ['pk', 'question', 'choice_text', 'votes']
