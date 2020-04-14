sudo /etc/init.d/nginx restart
source venv/bin/activate
nohup uwsgi --ini script/JLGLTaskList.ini
