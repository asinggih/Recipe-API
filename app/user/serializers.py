from django.contrib.auth import get_user_model, \
    authenticate

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = (
            'email',
            'password',
            'name'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    # overriding create function inside
    # the serializer class. This is according to their docs
    def create(self, validated_data):
        """Create a new user with encrypted pass and return it"""

        return get_user_model().objects.create_user(**validated_data)

    # overriding the update function of ModelSerializer
    # instance is the user object that is linked to the serializer
    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""

        # if the key of password does not exist within our validated data,
        # we provide a default value of None
        password = validated_data.pop('password', None)
        # calling the default update function from the
        # ModelSerializer superclass, and update that particular object
        user = super().update(instance, validated_data)

        # if the user provided a password, we update it with
        # that pssword
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    # attrs is all the vars that we pass above
    def validate(self, attrs):
        """validate and authenticate the user"""

        email = attrs.get('email')
        password = attrs.get('password')

        # authenticate our request
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            message = _('Unable to authenticate with provided creds')
            # code='authentication' lets django know how to handle this error,
            # and handle the error by sending 400 response
            raise serializers.ValidationError(message, code='authentication')

        # add 'user' into the attributes
        attrs['user'] = user
        # return attributes since we ovverride the validate function
        return attrs
