from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
import re
class UserResgistrationSeriallizer(serializers.ModelSerializer):
  password=serializers.CharField(write_only=True)

  class Meta:
    model=User
    fields=['user_id','full_name','email','contact_number','company_name','industry','username','password','address']
    read_only_fields=['user_id']

  def validate_password(self, password):
    try:
      validate_password(password)
    except serializers.ValidationError as e:
      raise serializers.ValidationError(e.messages)
    if not re.search(r'^(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])',password):
      raise serializers.ValidationError('Password must contain at least 1 number and a special character.')
    return password

  def create(self, validated_data):
    try:
      password=validated_data.pop('password')
      user=User(**validated_data)
      user.set_password(password)
      user.save()
      return user
    except Exception as e:
      raise serializers.ValidationError({'detail':f'User creation failed: {str(e)}'})


