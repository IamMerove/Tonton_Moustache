# Étape 1 : build avec Node
FROM node:20-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build   # ← crée le dossier /app/dist avec tout le site statique

# Étape 2 : servir avec Nginx (léger et parfait pour production)
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]