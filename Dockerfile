FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

COPY start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]
