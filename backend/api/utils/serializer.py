from itsdangerous import URLSafeTimedSerializer
from api.config import settings

serializer = URLSafeTimedSerializer(settings.cookie_secret_key) 