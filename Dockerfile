ARG IMAGE_ID=nginx:latest

FROM $IMAGE_ID

RUN rm /usr/share/nginx/html/index.html

COPY index.html /usr/nginx/html