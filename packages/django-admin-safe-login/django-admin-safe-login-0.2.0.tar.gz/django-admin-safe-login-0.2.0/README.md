# django-admin-safe-login

Add captcha field for django admin's login page.

## Install

```shell
pip install django-admin-safe-login
```

## Usage

**pro/settings.py**

```python
INSTALLED_APPS = [
    ...
    'django_static_jquery3',
    'django_secure_password_input',
    'django_admin_safe_login',
    'captcha',
    ...
]

CAPTCHA_IMAGE_SIZE = (100, 30)
ENABLE_LOGIN_CAPTCHA = True
```

**Note:**

1. Insert django_static_jquery3, django_secure_password_input, django_admin_safe_login and captcha into INSTALLED_APPS.
1. Application django_static_jquery3 provides static jquery.js.
1. Application django_secure_password_input provides rsa encryption and decryption function for password field.
1. Application django_admin_safe_login provides all functions about safe login.
1. Application captcha provides image captcha functions.
1. Configuration item CAPTCHA_IMAGE_SIZE is required, and must set to (100, 30) so that it will not break the display style. If you want other size image, you have to rewrite some css code.
1. Configuration item ENABLE_LOGIN_CAPTCHA is optional, it's default to True value. You can use it for disable captcha for a short time. If you want remove the captcha functional, just remove the app django_admin_safe_login.

**pro/urls.py**

```python
from django.urls import path
from django.urls import include

urlpatterns = [
    ...
    path('captcha/', include("captcha.urls")),
    ...
]
```

**Note:**

1. Include captcha.urls is required so that the captcha image can be displayed.

## When things go down!

We have override some part of admin/login.html. But the admin/login.html content may change in future releases. So you should known what part is overrided.

```html
{% extends "admin/login.html" %}
{% load i18n static %}

{% block extrastyle %}
    {{ block.super }}
    <!-- resource files included below is ours -->
    <link rel="stylesheet" type="text/css" href="{% static "django-admin-safe-login/css/django-admin-safe-login.css" %}" />
    <script src="{% static "jquery3/jquery.js" %}"></script>
    <script src="{% static "django-admin-safe-login/js/django-admin-safe-login.js" %}"></script>
    <!-- resource files included above is ours -->
{% endblock %}

{% block content %}
.....
<form action="{{ app_path }}" method="post" id="login-form">{% csrf_token %}
  ......
  <div class="form-row">
    {{ form.password.errors }}
    {{ form.password.label_tag }} {{ form.password }}
    ....
  </div>
  <!-- form-row below is ours -->
  <div class="form-row">
    <label for="id_captcha" class="required">{% trans "Captcha" %}</label>
    <div class="captcha-input">
        {{ form.captcha }}
    </div>
    {% if not form.this_is_the_login_form.errors %}{{ form.captcha.errors }}{% endif %}
  </div>
  <!-- form-row above is ours -->
......
</form>
......
{% endblock %}
```

**Steps:**

1. Our login.html is extends from "admin/login.html"
2. Override block extrastyle, append our css and js.
3. Override block content, all content of this block must copy from "admin/login.html", and add our form-row after form-row of password.


## Releases

### v0.2.0 2020/03/07

- Add rsa encryption and decrption functions for password field.
- Fix requirements.txt missing django-static-jquery3 problem.

### v0.1.0 2020/03/06

- First release.