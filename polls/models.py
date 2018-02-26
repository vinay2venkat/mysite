from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.sessions.models import Session



class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    def __unicode__(self):
        return u'ID: %s, question_text - %s, pub_date - %s' % (str(self.pk), self.question_text, self.pub_date)

    def __str__(self):
         return self.question_text


    def was_published_recently(self):
        #return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	    now = timezone.now()
	    return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


    def __str__(self):
        return self.choice_text


class VoteLog(models.Model):
    votelog_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    # def __unicode__(self):
    #     return u'ID: %s, votelog_id - %s, question - %s' % (str(self.pk), str(self.question.pk), self.votelog_id)

    def __int__(self):
        return self.question, self.choice

    # def __str__(self):
    #     votelog = VoteLog.objects.all()
    #     p = votelog.question.question_text
    #     return p





class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)



