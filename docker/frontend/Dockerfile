FROM node:17-alpine3.15

# RUN addgroup app && adduser -S -G app app
# USER app

WORKDIR /app
COPY ./frontend/package.json ./
# for some reason npm install is not working if we don't install globaly
RUN npm install -g npm
RUN npm install
# RUN npm cache clean
#RUN npm rebuild node-sass --force
COPY ./frontend ./

EXPOSE 3000

CMD ["npm", "start"]