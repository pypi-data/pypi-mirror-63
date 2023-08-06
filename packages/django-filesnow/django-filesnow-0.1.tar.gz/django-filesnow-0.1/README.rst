=========
FilesNow
=========

FilesNow is a Django app to download documnets, images 
from AWS S3 and serve is a temporary static content to customers.

FilesNow is a way to serve AWS S3 documents/media files
without giving access to your s3 buckets.

FilesNow itself cleans it's downloaded presentable
files, as such maintainig a healthy file system

Dependecies
-----------
AWS Boto3 Framework : pip install boto3
Configure AWS Credentilas using command : aws configure

Quick start
-----------

1. Add "filesnow" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'filesnow',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('filesnow/', include('filesnow.urls'))
	
	Your URL Pattern must end with concinated string of "+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"
	
	It should look something like
	
	urlpatterns = [
    path('admin/', admin.site.urls),
	path('filesnow/', include('filesnow.urls')) ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

3. Add the environment variables for media files within filesnow/settings.py::
	
	DOWNLOAD_LOC = < Describe Media Directory of your django Project or App >
	APP_MEDIA_URL = < Describe Media URL in case of App >
	
	Example : 
	I have a django project with below descriptions
	django Project name => "docdocgo"
	django App name => "filesnow"
	django App Media directory => C:\\Users\\Jackuna\\PycharmProjects\\docdocgo\\media\\filesnow\\
	
	Incase we don't have a media directory, create a media directory under django parent project folder
	and then add a folder named by app name.
	docdocgo --> media --> filesnow
	
	Considering above below is the way we define it.
	
	DOWNLOAD_LOC = 'C:\\Users\\Jackuna\\PycharmProjects\\docdocgo\\media\\filesnow\\'
    APP_MEDIA_URL = MEDIA_URL+'filesnow/'

4. Start the development server ``python manage.py runserver 0.0.0.0:9090``

5. Visit http://127.0.0.1:9090/filesnow and explore it.