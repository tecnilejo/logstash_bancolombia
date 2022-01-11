FROM 289a76555877
WORKDIR /usr/share/logstash
COPY script/ .
COPY requeriments.txt .
COPY pipeline .
RUN pip install -r requirements.txt
RUN bin/logstash-plugin install logstash-output-exec

