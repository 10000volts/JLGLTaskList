kill -9 $(ps aux | grep JLGLTaskList.ini | awk '{print $2}')
