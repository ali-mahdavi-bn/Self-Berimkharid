# dataBase
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'trob',
        'USER': 'trob',
        'PASSWORD': 'trob',
        'HOST': '195.28.11.20',
        'PORT': '5432',
    }
}

# minio
minioAddress = "127.0.0.1:9000"
minioAccessKey = "minioadmin"
minioSecretKey = "minioadmin"
minioBucketNames = {
    'brand': "berimkharid-brand",
    'product': "berimkharid-product",
    'category': "berimkharid-category",
    'userImage': "berimkharid-user-image",
    'vendor': "berimkharid-vendor",
    'eNamad': "berimkharid-enamad",
}

# kavenegar
kavenegarApiKey = 'xxxxxxxxxxxxxxxx'
kavenegarUrl = 'xxxxxxxxxxxxxxxx'
kavenegarTemplates = {
    'customerRegister': 'xxxxxxxxxxxxxxxx',
    'storeActivation': 'xxxxxxxxxxxxxxxx',
    'sendUserNamePassSeller': 'xxxxxxxxxxxxxxxx',
    'planActivation': 'xxxxxxxxxxxxxxxx',
    'customerForgotPassword': 'xxxxxxxxxxxxxxxx'
}

# captcha
RE_CAPTCHA_SECRET_KEY = "YOUR_RE_CAPTCHA_SECRET_KEY"

# fixed token
fixedTokenAddNewAdmin = 'xxxxxxxxxxxxxxxx'
fixedTokenAddProductItem = 'xxxxxxxxxxxxxxxx'
