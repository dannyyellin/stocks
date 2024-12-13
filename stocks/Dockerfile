FROM python:alpine3.17
# WORKDIR ./app
#RUN pip install Flask
#RUN pip install pymongo
#RUN pip install Flask-RESTful
#RUN pip install Flask-Pymongo
#RUN pip install requests
COPY requirements.txt .
RUN pip install -r requirements.txt --ignore-installed --no-cache-dir
#  RUN pip install bson   pymongo uses bson so need to import it.  doing so causes problems.
# so I removed "install bson from GT-requirements.txt".   works ok without this import.
ENV FLASK_APP=stocks.py
ENV FLASK_RUN_PORT=5001
ENV FLASK_DEBUG: "true"
ADD stocks.py .
ENV NINJA_API_KEY cMf1OoKKukDu21C4xel9L2i3EP9cYMbUesYfmFYg
EXPOSE 5001

# Set the directive to specify the executable that will run when the container is initiated
#ENTRYPOINT [ "python" ]

# Specify the command to run on container start
#CMD [ "cardholders-reference.py" ]
CMD ["flask", "run", "--host=0.0.0.0"]

