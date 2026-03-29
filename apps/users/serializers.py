from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

# ============================================================
# REGISTER SERIALIZER
# ============================================================
# Why: Validates and creates a new user account
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name',
            'phone', 'password', 'password2', 'role'
        ]

    # Why: Check both passwords match
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Passwords do not match'}
            )
        return attrs

    # Why: Create user with hashed password
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


# ============================================================
# USER PROFILE SERIALIZER
# ============================================================
# Why: Returns user profile data — used in profile API
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'phone', 'address', 'role',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'role', 'created_at', 'updated_at']


# ============================================================
# CHANGE PASSWORD SERIALIZER
# ============================================================
# Why: Validates old password and sets new password securely
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {'new_password': 'Passwords do not match'}
            )
        return attrs