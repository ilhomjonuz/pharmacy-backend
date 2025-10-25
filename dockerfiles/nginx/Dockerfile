FROM nginx:1.21-alpine

# Default nginx konfiguratsiyasini o'chirish
RUN rm /etc/nginx/conf.d/default.conf

# Maxsus nginx konfiguratsiya faylini qo'shish
COPY ./dockerfiles/nginx/nginx.conf /etc/nginx/conf.d/default.conf
