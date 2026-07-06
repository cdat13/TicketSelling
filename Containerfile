FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN pip install .
RUN ticketselling create-db
RUN ticketselling populate-db
RUN ticketselling add-user -u admin -p admin
EXPOSE 5000
CMD ["ticketselling", "run"]
