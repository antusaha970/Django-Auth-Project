from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ['id', 'email', 'profile_picture', 'bio',
                  'first_name', 'last_name', 'phone_number', 'password']
        extra_kwargs = {
            "email": {"required": True},
            "password": {"required": True},
            "phone_number": {"required": True},
            "bio": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if password is None:
            raise serializers.ValidationError("Password is required")
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        bio = validated_data.pop('bio', None)
        phone_number = validated_data.pop('phone_number', None)
        first_name = validated_data.pop('first_name', None)
        last_name = validated_data.pop('last_name', None)
        profile_picture = validated_data.pop('profile_picture', None)

        if bio is not None:
            instance.bio = bio
        if phone_number is not None:
            instance.phone_number = phone_number
        if first_name is not None:
            instance.first_name = first_name
        if last_name is not None:
            instance.last_name = last_name
        if profile_picture is not None:
            instance.profile_picture = profile_picture

        instance.save()

        return instance
