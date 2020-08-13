from .base_zappa import *

STATIC_S3_NAME_BUCKET = os.getenv('S3_BUCKET_NAME')
STATICFILES_STORAGE = "django_s3_storage.storage.StaticS3Storage"
AWS_S3_BUCKET_NAME_STATIC = STATIC_S3_NAME_BUCKET
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % STATIC_S3_NAME_BUCKET
STATIC_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
AWS_REGION = "us-west-2"
AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365
AWS_S3_GZIP = True
AWS_S3_BUCKET_AUTH_STATIC = False

DEFAULT_FILE_STORAGE = "django_s3_storage.storage.StaticS3Storage"
# zappa invoke --raw dev "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'noreply@gmail.com', '123456789')"
