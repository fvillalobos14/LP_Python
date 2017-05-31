FROM python:2.7.10

RUN git clone https://github.com/fvillalobos14/Python.git
RUN pip install googlemaps
RUN pip install Pillow
RUN pip install Flask

EXPOSE 8080

CMD cd Python && python tarea.py