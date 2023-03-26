from django.conf import settings
from django_redis import get_redis_connection
from rest_framework.response import Response
from rest_framework.views import APIView

from URLShortener.mongo import MongoDB


class Healthcheck(APIView):
    throttle_scope = "healthcheck"

    def get(self, request, format=None):
        """
        Return a response, containing flags to indicate service healthcheck.
        """

        logs = []
        status_code = 200
        is_database_working = True
        is_redis_working = True

        try:
            MongoDB._get_db(db_name=settings.MONGODB_DB_NAME)
        except Exception as e:
            logs.append(str(e))
            is_database_working = False
            status_code = 400

        try:
            redis_conn = get_redis_connection()
            redis_conn.ping()
        except Exception as e:
            logs.append(str(e))
            is_redis_working = False
            status_code = 400

        return Response(
            data={
                "healthcheck": "Running" if status_code == 200 else "Failed",
                "is_database_working": is_database_working,
                "is_redis_working": is_redis_working,
            },
            status=status_code,
        )
