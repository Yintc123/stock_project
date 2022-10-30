# init a base image (Alpine is small Linux distro)
FROM python:3.9-slim
# define the present working directory
WORKDIR /stock_project
# copy the contents into the working dir
COPY . .
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container
# CMD ["python", "app.py"]
# 使用 WSGI Gunicorn
CMD ["gunicorn", "-c", "wsgi_config.py", "wsgi_config:app"]
