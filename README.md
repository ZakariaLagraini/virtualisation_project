# Web Application Deployment

## Project Overview

This project consists of a web application hosted using Nginx, configured to serve over both HTTP and HTTPS. It is designed to be deployed within a Kubernetes cluster, leveraging services, deployments, and network policies for scalable and secure access.

## Project Components

### Nginx Configuration

Nginx is configured to handle HTTPS connections with TLS and serve static content such as HTML, CSS, JavaScript, and images. The configuration details are as follows:

- **SSL Configuration**: Ensures secure communication using TLS protocols.
- **Static Content Handling**: Serves HTML and assets, handling URL fallbacks for SPA (Single Page Application) behavior.
- **Error Handling**: Custom error responses for server errors.

```nginx
events {
    worker_connections 1024;
}

http {
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;

    server {
        listen 443 ssl;
        server_name localhost;
        ssl_certificate /etc/nginx/ssl/certificate.pem;
        ssl_certificate_key /etc/nginx/ssl/private_key.pem;

        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }

        location /assets {
            alias /usr/share/nginx/html/assets;
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
            root /usr/share/nginx/html;
        }
    }

    server {
        listen 80;
        server_name localhost;
        
        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
            try_files $uri $uri/ /index.html;
        }
    }
} 

```
## Kubernetes Deployment

### Deployment Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: front-end-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: front-end
  template:
    metadata:
      labels:
        app: front-end
    spec:
      containers:
      - name: front-end
        image: front-end:v1
        ports:
        - containerPort: 443
        volumeMounts:
        - name: tls-certs
          mountPath: /etc/tls
      volumes:
      - name: tls-certs
        secret:
          secretName: tls-certificate

```

### Deployment Configuration
```yaml
apiVersion: v1
kind: Service
metadata:
  name: front-end-service
spec:
  selector:
    app: front-end
  ports:
    - protocol: TCP
      port: 443
      targetPort: 443
  type: NodePort
```

# Usage Instructions



## Deployment

To deploy the Kubernetes manifests, use the following command for each YAML file:

```yaml
kubectl apply -f <filename>.yaml
```



## Access Application

After deployment, you can access the application locally using port forwarding:

```yaml 
kubectl port-forward svc/front-end-service 443:443
```



# Troubleshooting

SSL Certificates: Ensure that the SSL certificates are correctly mounted and accessible to the Nginx server.
Pod Logs: Check the logs of the pods for any runtime errors using:

```yaml
kubectl logs <pod-name>
```

# Contributing

Contributions to enhance the application or deployment configurations are welcome. Please fork the repository and submit a pull request.

