FROM python:3.8

RUN useradd whereph
WORKDIR ~/prog/where-ph



RUN apt-get update

#install geopandas
RUN echo Y |  apt-get install libgdal-dev
RUN echo Y | apt install libspatialindex-dev
RUN pip install --upgrade pip
RUN pip install pandas fiona shapely pyproj rtree
RUN pip install geopandas 
RUN pip install flask
RUN pip install gunicorn

#unimportant additions
RUN pip install numpy python-dotenv
RUN pip install Flask-WTF


#App related
COPY app app
COPY whereph.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP whereph.py

RUN chown -R whereph:whereph ./
USER whereph

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
