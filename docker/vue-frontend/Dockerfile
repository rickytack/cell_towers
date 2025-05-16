# Build
FROM node:lts as builder

WORKDIR /app

# Copy package files from the vue-frontend directory
COPY vue-frontend/package*.json ./
RUN npm install

# Copy the rest of the vue-frontend files
COPY vue-frontend/ .
RUN npm run build

# Serve with NGINX
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY docker/vue-frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]