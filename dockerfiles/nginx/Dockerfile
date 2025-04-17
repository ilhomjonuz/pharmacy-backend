FROM nginx:1.21-alpine

# Remove the default NGINX configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy your custom NGINX configuration file
COPY ./dockerfiles/nginx/nginx.conf /etc/dockerfiles/conf.d/default.conf