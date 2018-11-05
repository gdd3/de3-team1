FROM java:8

WORKDIR /usr/local/

RUN wget http://divolte-releases.s3-website-eu-west-1.amazonaws.com/divolte-collector/0.9.0/distributions/divolte-collector-0.9.0.tar.gz && \
    tar -xvf divolte-collector-0.9.0.tar.gz --strip-components=1 && \
    rm divolte-collector-0.9.0.tar.gz

ADD divolte-collector.conf /usr/local/conf/
ADD mapping.groovy /usr/local/conf
ADD event.avsc /usr/local/conf

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

EXPOSE 8290

ENTRYPOINT ["divolte-collector"]  
