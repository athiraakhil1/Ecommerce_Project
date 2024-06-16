from django.db.models.base import Model
from django.db.models.fields import Field
from rest_framework import serializers
from website.models import User
from rest_framework import serializers


class userserializer(serializers.ModelSerializer):
     class Meta:
          model=User
          fields=['username','email','phone']