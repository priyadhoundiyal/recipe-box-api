from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the users object """
    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5}}

    def create(self, validated_data):
        """Create a user with an encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """ serializer for user auth object """
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """ validate and authentiacte the user """
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with the provided credentials')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
