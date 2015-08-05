* When upgrading to 4.2 from 4.1, if you deploy Seafile in a non-root domain, you need to add the following extra settings in seahub_settings.py:

    COMPRESS_URL = MEDIA_URL
    STATIC_URL = MEDIA_URL + '/assets/'
