from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS =[
    'core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'social_django',
    "allauth.socialaccount.providers.facebook",
]
INSTALLED_APPS.extend(EXTERNAL_APPS)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'restaurant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.current.current_date'
            ],
        },
    },
]
SOCIAL_AUTH_PIPELINE = ( 
    'social_core.pipeline.social_auth.social_details', 
    'social_core.pipeline.social_auth.social_uid', 
    # 🔥 Custom step 
    'core.pipeline.associate_by_email', 
    'social_core.pipeline.social_auth.auth_allowed', 
    'social_core.pipeline.social_auth.social_user', 
    'social_core.pipeline.user.get_username', 
    'social_core.pipeline.user.create_user', 
    'social_core.pipeline.social_auth.associate_user', 
    'social_core.pipeline.social_auth.load_extra_data', 
    'social_core.pipeline.user.user_details', 
)

LOGIN_URL="log_in"
LOGIN_REDIRECT_URL ="index"
LOGOUT_URL="log_out"
LOGOUT_REDIRECT_URL ="log_in"

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# google oauth
SOCIAL_AUTH_URL_NAMESPACE = config('SOCIAL_AUTH_URL_NAMESPACE')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

# github 
SOCIAL_AUTH_GITHUB_KEY = config('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = config('SOCIAL_AUTH_GITHUB_SECRET')

# facebook
SOCIAL_AUTH_FACEBOOK_KEY=config('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET=config('SOCIAL_AUTH_FACEBOOK_SECRET')

# Force HTTP for local testing redirect URIs
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

# Required if running behind a local reverse proxy or tunnel
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

WSGI_APPLICATION = 'restaurant.wsgi.application'

# Database
# https://docs.djangoproject.com/en/6.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

PASSWORD_RESET_TIMEOUT = 3000


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = BASE_DIR/'media'
MEDIA_URL = '/media/'


# Email
# https://docs.djangoproject.com/en/6.1/topics/email/#topic-email-configuration

# Email
#email setup in django (smtp,outlook, yahoo)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")