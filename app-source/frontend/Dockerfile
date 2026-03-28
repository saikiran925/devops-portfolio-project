# ---------- Stage 1 : Asset Preparation (Builder) ----------
# For a pure HTML file, this stage simply gathers the assets.
# If you upgrade to React/Node.js later, you would run 'npm install' and 'npm run build' here.
FROM alpine AS builder

WORKDIR /app

# Copy the source code into the builder
COPY index.html .


# ---------- Stage 2 : Production Server (Runtime) ----------
FROM nginx:alpine

# Remove the default Nginx index page (best practice)
RUN rm -rf /usr/share/nginx/html/*

# Copy ONLY the finalized assets from the builder stage
COPY --from=builder /app/index.html /usr/share/nginx/html/index.html

# Expose port 80 (the default HTTP port)
EXPOSE 80

# Nginx starts automatically, so no CMD is needed