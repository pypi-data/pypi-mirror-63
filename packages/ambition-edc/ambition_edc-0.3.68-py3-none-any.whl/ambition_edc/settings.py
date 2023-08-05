from datetime import datetime

import environ
import os
import sys

from ambition_sites import ambition_sites
from dateutil.tz import gettz
from django.core.exceptions import ImproperlyConfigured
from edc_sites import get_site_id
from pathlib import Path

# simple version check
try:
    assert (3, 6) <= (sys.version_info.major, sys.version_info.minor) <= (3, 7)
except AssertionError:
    raise ImproperlyConfigured(
        "Incorrect python version. Expected 3.6 or 3.7. Check your environment."
    )

BASE_DIR = str(Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

env = environ.Env(
    AWS_ENABLED=(bool, False),
    CDN_ENABLED=(bool, False),
    CELERY_ENABLED=(bool, False),
    DATA_MANAGER_ENABLED=(bool, True),
    DATA_MANAGER_SHOW_ON_DASHBOARD=(bool, True),
    DATABASE_SQLITE_ENABLED=(bool, False),
    DJANGO_AUTO_CREATE_KEYS=(bool, False),
    DJANGO_CSRF_COOKIE_SECURE=(bool, True),
    DJANGO_DEBUG=(bool, False),
    DJANGO_EDC_BOOTSTRAP=(int, 3),
    DJANGO_EMAIL_ENABLED=(bool, False),
    DJANGO_EMAIL_USE_TLS=(bool, True),
    DJANGO_LIVE_SYSTEM=(bool, False),
    DJANGO_LOGGING_ENABLED=(bool, True),
    DJANGO_SESSION_COOKIE_SECURE=(bool, True),
    DJANGO_USE_I18N=(bool, True),
    DJANGO_USE_L10N=(bool, False),
    DJANGO_USE_TZ=(bool, True),
    EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER=(bool, True),
    SAUCE_ENABLED=(bool, False),
    SENTRY_ENABLED=(bool, False),
    TWILIO_ENABLED=(bool, False),
    SIMPLE_HISTORY_PERMISSIONS_ENABLED=(bool, False),
    SIMPLE_HISTORY_REVERT_DISABLED=(bool, False),
    DJANGO_COLLECT_OFFLINE_ENABLED=(bool, False),
)

# copy your .env file from .envs/ to BASE_DIR
if "test" in sys.argv or "runtests.py" in sys.argv:
    env.read_env(os.path.join(BASE_DIR, ".env-tests"))
    print(f"Reading env from {os.path.join(BASE_DIR, '.env-tests')}")
else:
    env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env("DJANGO_DEBUG")

if DEBUG:
    INTERNAL_IPS = ["127.0.0.1"]

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

APP_NAME = env.str("DJANGO_APP_NAME")

LIVE_SYSTEM = env.str("DJANGO_LIVE_SYSTEM")

if env.str("DJANGO_ETC_FOLDER"):
    ETC_DIR = env.str("DJANGO_ETC_FOLDER")
else:
    ETC_DIR = BASE_DIR

TEST_DIR = os.path.join(BASE_DIR, APP_NAME, "tests")

ALLOWED_HOSTS = ["*"]  # env.list('DJANGO_ALLOWED_HOSTS')

ENFORCE_RELATED_ACTION_ITEM_EXISTS = False

# get site ID from more familiar town name
TOWN = env.str("DJANGO_TOWN")
if TOWN:
    SITE_ID = get_site_id(TOWN, sites=ambition_sites)
else:
    SITE_ID = env.int("DJANGO_SITE_ID")

DEFAULT_APPOINTMENT_TYPE = "hospital"

REVIEWER_SITE_ID = env.int("DJANGO_REVIEWER_SITE_ID")

LOGIN_REDIRECT_URL = env.str("DJANGO_LOGIN_REDIRECT_URL")

SENTRY_ENABLED = env("SENTRY_ENABLED")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_crypto_fields.apps.AppConfig",
    "django_revision.apps.AppConfig",
    # "debug_toolbar",
    "django_extensions",
    "django_celery_results",
    "django_celery_beat",
    "logentry_admin",
    "simple_history",
    "storages",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "django_collect_offline.apps.AppConfig",
    "django_collect_offline_files.apps.AppConfig",
    "edc_action_item.apps.AppConfig",
    "edc_adverse_event.apps.AppConfig",
    "edc_appointment.apps.AppConfig",
    "edc_auth.apps.AppConfig",
    "edc_data_manager.apps.AppConfig",
    "edc_consent.apps.AppConfig",
    "edc_dashboard.apps.AppConfig",
    "edc_export.apps.AppConfig",
    "edc_facility.apps.AppConfig",
    "edc_fieldsets.apps.AppConfig",
    "edc_form_validators.apps.AppConfig",
    "edc_lab_dashboard.apps.AppConfig",
    "edc_label.apps.AppConfig",
    "edc_locator.apps.AppConfig",
    "edc_reference.apps.AppConfig",
    "edc_reports.apps.AppConfig",
    "edc_metadata_rules.apps.AppConfig",
    "edc_model_admin.apps.AppConfig",
    "edc_navbar.apps.AppConfig",
    "edc_notification.apps.AppConfig",
    "edc_offstudy.apps.AppConfig",
    "edc_visit_schedule.apps.AppConfig",
    "edc_pdutils.apps.AppConfig",
    "edc_pharmacy.apps.AppConfig",
    # "edc_pharmacy_dashboard.apps.AppConfig",
    "edc_prn.apps.AppConfig",
    "edc_randomization.apps.AppConfig",
    "edc_registration.apps.AppConfig",
    "edc_subject_dashboard.apps.AppConfig",
    "edc_timepoint.apps.AppConfig",
    "edc_list_data.apps.AppConfig",
    "edc_review_dashboard.apps.AppConfig",
    "edc_sites.apps.AppConfig",
    "ambition_auth.apps.AppConfig",
    "ambition_lists.apps.AppConfig",
    "ambition_dashboard.apps.AppConfig",
    "ambition_labs.apps.AppConfig",
    "ambition_metadata_rules.apps.AppConfig",
    "ambition_rando.apps.AppConfig",
    "ambition_reference.apps.AppConfig",
    "ambition_subject.apps.AppConfig",
    "ambition_form_validators.apps.AppConfig",
    "ambition_visit_schedule.apps.AppConfig",
    "ambition_ae.apps.AppConfig",
    "ambition_prn.apps.AppConfig",
    "ambition_export.apps.AppConfig",
    "ambition_screening.apps.AppConfig",
    # "ambition_edc.apps.EdcAppointmentAppConfig",
    "ambition_edc.apps.EdcDeviceAppConfig",
    "ambition_edc.apps.EdcIdentifierAppConfig",
    "ambition_edc.apps.EdcLabAppConfig",
    "ambition_edc.apps.EdcMetadataAppConfig",
    "ambition_edc.apps.EdcProtocolAppConfig",
    "ambition_edc.apps.EdcVisitTrackingAppConfig",
    "ambition_edc.apps.AppConfig",
]

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MIDDLEWARE.extend(
    [
        "edc_dashboard.middleware.DashboardMiddleware",
        "edc_subject_dashboard.middleware.DashboardMiddleware",
        "edc_lab_dashboard.middleware.DashboardMiddleware",
        "edc_adverse_event.middleware.DashboardMiddleware",
        # 'simple_history.middleware.HistoryRequestMiddleware'
    ]
)

ROOT_URLCONF = f"{APP_NAME}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

if env("DATABASE_SQLITE_ENABLED"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

else:
    DATABASES = {"default": env.db()}
# be secure and clear DATABASE_URL since it is no longer needed.
DATABASE_URL = None

if env.str("DJANGO_CACHE") == "redis":
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"redis://127.0.0.1:6379/1",
            # "LOCATION": "unix://[:{DJANGO_REDIS_PASSWORD}]@/path/to/socket.sock?db=0",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PASSWORD": env.str("DJANGO_REDIS_PASSWORD"),
            },
            "KEY_PREFIX": f"{APP_NAME}",
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
    DJANGO_REDIS_IGNORE_EXCEPTIONS = True
    DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

elif env.str("DJANGO_CACHE") == "memcached":
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
            "LOCATION": "unix:/tmp/memcached.sock",
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

WSGI_APPLICATION = f"{APP_NAME}.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTHENTICATION_BACKENDS = ["edc_auth.backends.ModelBackendWithSite"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 20},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = env.str("DJANGO_LANGUAGE_CODE")

LANGUAGES = [x.split(":") for x in env.list("DJANGO_LANGUAGES")] or (("en", "English"),)

TIME_ZONE = env.str("DJANGO_TIME_ZONE")

USE_I18N = env("DJANGO_USE_I18N")

# set to False so DATE formats below are used
USE_L10N = env("DJANGO_USE_L10N")

USE_TZ = env("DJANGO_USE_TZ")

DATE_INPUT_FORMATS = ["%Y-%m-%d", "%d/%m/%Y"]
DATETIME_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%Y-%m-%d",  # '2006-10-25'
    "%d/%m/%Y %H:%M:%S",  # '25/10/2006 14:30:59'
    "%d/%m/%Y %H:%M:%S.%f",  # '25/10/2006 14:30:59.000200'
    "%d/%m/%Y %H:%M",  # '25/10/2006 14:30'
    "%d/%m/%Y",  # '25/10/2006'
]
DATE_FORMAT = "j N Y"
DATETIME_FORMAT = "j N Y H:i"
SHORT_DATE_FORMAT = "d/m/Y"
SHORT_DATETIME_FORMAT = "d/m/Y H:i"

# edc-pdutils
EXPORT_FILENAME_TIMESTAMP_FORMAT = "%Y%m%d"

# enforce https if DEBUG=False!
# Note: will cause "CSRF verification failed. Request aborted"
#       if DEBUG=False and https not configured.
if not DEBUG:
    # CSFR cookies
    CSRF_COOKIE_SECURE = env.str("DJANGO_CSRF_COOKIE_SECURE")
    SECURE_PROXY_SSL_HEADER = env.tuple("DJANGO_SECURE_PROXY_SSL_HEADER")
    SESSION_COOKIE_SECURE = env.str("DJANGO_SESSION_COOKIE_SECURE")

    # other security defaults
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31_536_000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True

# edc_lab and label
LABEL_TEMPLATE_FOLDER = env.str("DJANGO_LABEL_TEMPLATE_FOLDER") or os.path.join(
    BASE_DIR, "label_templates"
)
CUPS_SERVERS = env.dict("DJANGO_CUPS_SERVERS")

# django_collect_offline / django_collect_offline files
DJANGO_COLLECT_OFFLINE_ENABLED = env("DJANGO_COLLECT_OFFLINE_ENABLED")
DJANGO_COLLECT_OFFLINE_SERVER_IP = env.str("DJANGO_COLLECT_OFFLINE_SERVER_IP")
DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST = env.str(
    "DJANGO_COLLECT_OFFLINE_FILES_REMOTE_HOST"
)
DJANGO_COLLECT_OFFLINE_FILES_USER = env.str("DJANGO_COLLECT_OFFLINE_FILES_USER")
DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME = env.str(
    "DJANGO_COLLECT_OFFLINE_FILES_USB_VOLUME"
)

SUBJECT_CONSENT_MODEL = env.str("DJANGO_SUBJECT_CONSENT_MODEL")
SUBJECT_REQUISITION_MODEL = env.str("DJANGO_SUBJECT_REQUISITION_MODEL")
SUBJECT_VISIT_MODEL = env.str("DJANGO_SUBJECT_VISIT_MODEL")

EDC_NAVBAR_DEFAULT = env("EDC_NAVBAR_DEFAULT")

# dashboards
EDC_BOOTSTRAP = env("DJANGO_EDC_BOOTSTRAP")
DASHBOARD_URL_NAMES = env.dict("DJANGO_DASHBOARD_URL_NAMES")
DASHBOARD_BASE_TEMPLATES = env.dict("DJANGO_DASHBOARD_BASE_TEMPLATES")
LAB_DASHBOARD_BASE_TEMPLATES = env.dict("DJANGO_LAB_DASHBOARD_BASE_TEMPLATES")
LAB_DASHBOARD_URL_NAMES = env.dict("DJANGO_LAB_DASHBOARD_URL_NAMES")
# is this needed?
SUBJECT_REQUISITION_MODEL = env.str("DJANGO_SUBJECT_REQUISITION_MODEL")

# edc_facility
HOLIDAY_FILE = env.str("DJANGO_HOLIDAY_FILE")
COUNTRY = env.str("DJANGO_COUNTRY")

EMAIL_ENABLED = env("DJANGO_EMAIL_ENABLED")
EMAIL_CONTACTS = env.dict("DJANGO_EMAIL_CONTACTS")
if EMAIL_ENABLED:
    EMAIL_HOST = env.str("DJANGO_EMAIL_HOST")
    EMAIL_PORT = env.int("DJANGO_EMAIL_PORT")
    EMAIL_HOST_USER = env.str("DJANGO_EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = env.str("DJANGO_EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = env("DJANGO_EMAIL_USE_TLS")
    MAILGUN_API_KEY = env.str("MAILGUN_API_KEY")
    MAILGUN_API_URL = env.str("MAILGUN_API_URL")
TWILIO_ENABLED = env("TWILIO_ENABLED")
if TWILIO_ENABLED:
    TWILIO_ACCOUNT_SID = env.str("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = env.str("TWILIO_AUTH_TOKEN")
    TWILIO_SENDER = env.str("TWILIO_SENDER")

EDC_FACILITY_USE_DEFAULTS = True
EDC_RANDOMIZATION_BLINDED_TRIAL = env.str("EDC_RANDOMIZATION_BLINDED_TRIAL")
EDC_RANDOMIZATION_UNBLINDED_USERS = env.list("EDC_RANDOMIZATION_UNBLINDED_USERS")
EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER = env(
    "EDC_RANDOMIZATION_REGISTER_DEFAULT_RANDOMIZER"
)
EDC_RANDOMIZATION_LIST_PATH = env.str("EDC_RANDOMIZATION_LIST_PATH")

# edc-protocol
EDC_PROTOCOL = "BHP092"
EDC_PROTOCOL_INSTITUTION_NAME = "London School of Hygiene & Tropical Medicine"
EDC_PROTOCOL_NUMBER = "092"
EDC_PROTOCOL_PROJECT_NAME = "Ambition"
EDC_PROTOCOL_STUDY_OPEN_DATETIME = datetime(2016, 12, 31, 0, 0, 0, tzinfo=gettz("UTC"))
EDC_PROTOCOL_STUDY_CLOSE_DATETIME = datetime(
    2022, 12, 31, 23, 59, 59, tzinfo=gettz("UTC")
)
EDC_PROTOCOL_TITLE = (
    "BHP092"
    "High Dose AMBISOME on a Fluconazole Backbone for Cryptococcal Meningitis "
    "Induction Therapy in sub-Saharan Africa: A Phase 3 Randomised Controlled "
    "Non-Inferiority Trial (P.I. Joe Jarvis)."
)

# django_revision
GIT_DIR = BASE_DIR

# django_crypto_fields
KEY_PATH = env.str("DJANGO_KEY_FOLDER")
AUTO_CREATE_KEYS = env.str("DJANGO_AUTO_CREATE_KEYS")

EXPORT_FOLDER = env.str("DJANGO_EXPORT_FOLDER") or os.path.expanduser("~/")

# django_simple_history
SIMPLE_HISTORY_PERMISSIONS_ENABLED = env.str("SIMPLE_HISTORY_PERMISSIONS_ENABLED")
SIMPLE_HISTORY_REVERT_DISABLED = env.str("SIMPLE_HISTORY_REVERT_DISABLED")

FQDN = env.str("DJANGO_FQDN")
INDEX_PAGE = env.str("DJANGO_INDEX_PAGE")
INDEX_PAGE_LABEL = env.str("DJANGO_INDEX_PAGE_LABEL")
DJANGO_LOG_FOLDER = env.str("DJANGO_LOG_FOLDER")

# edc_adverse_event
ADVERSE_EVENT_ADMIN_SITE = env.str("EDC_ADVERSE_EVENT_ADMIN_SITE")
ADVERSE_EVENT_APP_LABEL = env.str("EDC_ADVERSE_EVENT_APP_LABEL")

# edc_data_manager
DATA_MANAGER_ENABLED = env("DATA_MANAGER_ENABLED")
DATA_DICTIONARY_APP_LABELS = [
    "ambition_subject",
    "ambition_prn",
    "ambition_screening",
    "ambition_ae",
    "edc_appointment",
]
DATA_MANAGER_SHOW_ON_DASHBOARD = env("DATA_MANAGER_SHOW_ON_DASHBOARD")

# static
if env("AWS_ENABLED"):
    # see
    # https://www.digitalocean.com/community/tutorials/
    # how-to-set-up-a-scalable-django-app-with-digitalocean-
    # managed-databases-and-spaces
    AWS_ACCESS_KEY_ID = env.str("AWS_ACCESS_KEY_ID")
    AWS_DEFAULT_ACL = "public-read"
    AWS_SECRET_ACCESS_KEY = env.str("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env.str("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = env.str("AWS_S3_CUSTOM_DOMAIN")
    AWS_S3_ENDPOINT_URL = env.str("AWS_S3_ENDPOINT_URL")
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_LOCATION = env.str("AWS_LOCATION")
    AWS_IS_GZIPPED = True
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATIC_URL = f"{os.path.join(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)}/"
    STATIC_ROOT = ""
else:
    # run collectstatic, check nginx LOCATION
    STATIC_URL = env.str("DJANGO_STATIC_URL")
    STATIC_ROOT = env.str("DJANGO_STATIC_ROOT")

SENTRY_DSN = None
if SENTRY_ENABLED:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        send_default_pii=True,
    )
else:
    if env("DJANGO_LOGGING_ENABLED"):
        from .logging.standard import LOGGING  # noqa

# CELERY
# see docs on setting up the broker
CELERY_ENABLED = env("CELERY_ENABLED")
if CELERY_ENABLED:
    CELERY_BROKER_USER = env.str("CELERY_BROKER_USER")
    CELERY_BROKER_PASSWORD = env.str("CELERY_BROKER_PASSWORD")
    CELERY_BROKER_HOST = env.str("CELERY_BROKER_HOST")
    CELERY_BROKER_PORT = env.str("CELERY_BROKER_PORT")
if DEBUG:
    CELERY_BROKER_VHOST = f"{APP_NAME}_debug"
elif LIVE_SYSTEM:
    CELERY_BROKER_VHOST = f"{APP_NAME}_production"
else:
    CELERY_BROKER_VHOST = f"{APP_NAME}_uat"
    CELERY_BROKER_URL = (
        f"amqp://{CELERY_BROKER_USER}:{CELERY_BROKER_PASSWORD}@"
        f"{CELERY_BROKER_HOST}:{CELERY_BROKER_PORT}/{CELERY_BROKER_VHOST}"
    )
    DJANGO_CELERY_RESULTS_TASK_ID_MAX_LENGTH = 191
    CELERY_RESULT_BACKEND = "django-db"
    #     CELERY_QUEUES = (
    #         Queue('high', Exchange('high'), routing_key='high'),
    #         Queue('normal', Exchange('normal'), routing_key='normal'),
    #         Queue('low', Exchange('low'), routing_key='low'),
    #     )
    #     CELERY_DEFAULT_QUEUE = 'normal'
    #     CELERY_DEFAULT_EXCHANGE = 'normal'
    #     CELERY_DEFAULT_ROUTING_KEY = 'normal'
    #     CELERY_ROUTES = {
    #         'edc_data_manager.tasks.*': {'queue': 'normal'},
    #     }

if "test" in sys.argv or "runtests.py" in sys.argv:

    class DisableMigrations:
        def __contains__(self, item):
            return True

        def __getitem__(self, item):
            return None

    MIGRATION_MODULES = DisableMigrations()
    PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)
    DEFAULT_FILE_STORAGE = "inmemorystorage.InMemoryStorage"

if env("SAUCE_ENABLED"):
    SAUCE_USERNAME = env.str("SAUCE_USERNAME")
    SAUCE_ACCESS_KEY = env.str("SAUCE_ACCESS_KEY")
