FROM eclipse-temurin:21-jre-alpine

LABEL org.opencontainers.image.source="https://github.com/morta5/graphhopper-docker"
LABEL org.opencontainers.image.description="Lightweight GraphHopper Docker Image based on Alpine and Temurin Java 21"

WORKDIR /graphhopper

RUN apk add --no-cache curl wget bash \
    && wget -q -O graphhopper-web.jar https://github.com/graphhopper/graphhopper/releases/download/11.0/graphhopper-web-11.0.jar \
    && mkdir -p /graphhopper/cache /data

COPY config.yml /graphhopper/config.yml

EXPOSE 8989

ENV JAVA_OPTS="-Xms1500m -Xmx2800m -XX:+UseG1GC -XX:+UseStringDeduplication"

ENTRYPOINT ["sh", "-c", "exec java $JAVA_OPTS -jar graphhopper-web.jar server /graphhopper/config.yml"]
