FROM node:16
WORKDIR /app
COPY package*.json ./
# Install project dependenices (from package*.json)
RUN npm install
# Don't forget to update .dockerignore before executing COPY
COPY . .
EXPOSE 3000
# Commant to start your Nest.js app in debug mode
CMD ["npm", "run", "start:debug"]