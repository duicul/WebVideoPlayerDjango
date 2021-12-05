FROM nginx

WORKDIR /home

RUN apt-get update && \
    rm -rf /var/lib/apt/lists/*

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf .

COPY ../WebVideoPlayer/static /home/staticinit
COPY ./entrypoint_nginx.sh /docker-entrypoint.d
# Replace with our own nginx.conf
COPY nginx.conf /etc/nginx/conf.d/
#CMD ["./entrypoint_nginx.sh"]