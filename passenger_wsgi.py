import sys, os
INTERP = "/home/jgwlibrary/schema.space/bin/python"
#INTERP is present twice so that the new python interpreter 
#knows the actual executable path 
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd + '/main')  #You must add your project here

sys.path.insert(0,cwd+'/schema.space/bin')
sys.path.insert(0,cwd+'/schema.space/lib/python3.8/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = "main.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()