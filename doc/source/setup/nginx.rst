################################
Setup behind Nginx reverse proxy
################################


********
Packages
********
Install Nginx and Let's Encrypt Certbot::

    apt install nginx certbot


*****
Nginx
*****
/etc/nginx/snippets/ssl/common.conf::

    # A universal location overlay for the Let's Encrypt ACME challenge protocol
    location /.well-known {
        alias /var/www/html/.well-known;
    }

    # Enable session resumption to improve https performance
    # http://vincent.bernat.im/en/blog/2011-ssl-session-reuse-rfc5077.html
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 5m;

    # Diffie-Hellman parameter for DHE ciphersuites, recommended 2048 bits
    # openssl dhparam -out /etc/nginx/dhparam.pem 2048
    ssl_dhparam /etc/nginx/dhparam.pem;

    # Enable server-side protection from BEAST attacks
    # http://blog.ivanristic.com/2013/09/is-beast-still-a-threat.html
    ssl_prefer_server_ciphers on;

    # Disable SSLv3 (enabled by default since nginx 0.8.19) since it's less secure than TLS
    # http://en.wikipedia.org/wiki/Secure_Sockets_Layer
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;

    # Chrome says "obsolete cipher suite" [system default]
    #ssl_ciphers AES:HIGH:!ADH:!MD5;

    # Chrome says "obsolete" to both cipher suites [janosch]
    #ssl_ciphers TLSv1.2+HIGH+AES256:TLSv1+HIGH+AES256:@STRENGTH:!kECDHe:!aECDSA:!aNULL:!eNULL:!PSK:!SRP:!DSS;
    #ssl_ciphers TLSv1.2+HIGH+AES256:TLSv1.2+HIGH+AES128:TLSv1+HIGH+AES256:TLSv1+HIGH+AES128:@STRENGTH:!kECDHe:!aECDSA:!aNULL:!eNULL:!PSK:!SRP:!DSS;

    # Ciphers chosen for forward secrecy and compatibility, Chrome says "modern cipher suite"
    # http://blog.ivanristic.com/2013/08/configuring-apache-nginx-and-openssl-for-forward-secrecy.html
    #ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:ECDHE-RSA-RC4-SHA:ECDHE-ECDSA-RC4-SHA:RC4-SHA:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!3DES:!MD5:!PSK';
    # Without RC4:
    ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:kEDH+AESGCM:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-DSS-AES256-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!3DES:!MD5:!PSK';

    # These are very agressive rules
    # https://www.scalescale.com/tips/nginx/hardening-nginx-ssl-tsl-configuration/
    #ssl_ciphers 'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES256-GCM-SHA384:AES128-GCM-SHA256:AES256-SHA256:AES128-SHA256:AES256-SHA:AES128-SHA:DES-CBC3-SHA:HIGH:!aNULL:!eNULL:!EXPORT:!CAMELLIA:!DES:!MD5:!PSK:!RC4';

    # Communicate with encryption only
    #add_header Strict-Transport-Security max-age=15768000;
    #add_header Strict-Transport-Security max-age=5;


/etc/nginx/snippets/ssl/kotori.example.org.conf::

    # SSL certificate and key file
    ssl_certificate     /etc/letsencrypt/live/kotori.example.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kotori.example.org/privkey.pem;

    # Redirect all requests to https
    if ($server_port = 80) {
        #rewrite ^ https://$host$request_uri;
        rewrite (.*) https://$http_host$1;
    }


/etc/nginx/sites-available/kotori.example.org.conf::

    server {

        # Your server name
        server_name kotori.example.org;

        # Listen on regular webserver port
        listen 80;

        # Enable SSL
        listen 443 ssl;
        # Best-practice SSL configuration
        include snippets/ssl/common.conf;
        #include snippets/ssl/kotori.example.org.conf;

        # Configure Kotori and friends
        include snippets/kotori-daq.conf;

        # Redirect "/" to Grafana
        location = / {
            rewrite ^ /grafana/ redirect;
        }

        # Log files
        access_log /var/log/nginx/kotori.example.org.access.log combined;
        error_log /var/log/nginx/kotori.example.org.error.log;

        # Performance parameters
        # Relax "414 Request-URI Too Large"
        large_client_header_buffers 6 16k;

    }


/etc/nginx/snippets/kotori-daq.conf::

    # Serve Grafana
    location /grafana/ {
        proxy_set_header   Host $host;

        rewrite  ^/grafana/(.*)  /$1 break;
        proxy_pass http://localhost:3000;


        # Performance parameters

        # Relax "413 Request Entity Too Large"
        client_max_body_size 20M;

        # If upstream is slow
        proxy_send_timeout          5m;
        proxy_read_timeout          5m;

        # If downstream is slow
        #client_header_timeout 3m;
        client_body_timeout 5m;
        send_timeout 5m;
    }

    # Serve Kotori HTTP API
    location /api {
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP          $remote_addr;
        proxy_set_header   X-Forwarded-For    $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto  $scheme;

        #rewrite  ^//(.*)  /$1 break;
        proxy_pass http://localhost:24642/api;


        # Performance parameters

        # Relax "413 Request Entity Too Large"
        client_max_body_size 20M;

        # Relax "414 Request-URI Too Large"
        large_client_header_buffers 6 16k;

        # If upstream is slow
        proxy_send_timeout          5m;
        proxy_read_timeout          5m;

        # If downstream is slow
        #client_header_timeout 3m;
        client_body_timeout 5m;
        send_timeout 5m;
    }


*******
Grafana
*******
/etc/grafana/grafana.ini::

    [server]

    # Protocol (http or https)
    protocol = http

    # The ip address to bind to, empty will bind to all interfaces
    http_addr = localhost

    # The public facing domain name used to access grafana from a browser
    domain = kotori.example.org

    # The full public facing url
    root_url = %(protocol)s://%(domain)s/grafana/

::

    systemctl restart grafana-server


*************
Let's Encrypt
*************
::

    ln -sr /etc/nginx/sites-available/weather.hiveeyes.org.conf /etc/nginx/sites-enabled/

    openssl dhparam -out /etc/nginx/dhparam.pem 2048

    nginx -t
    systemctl reload nginx

    certbot register --email 'operations@example.org'
    certbot certonly --webroot --domains weather.e-habit.at --webroot-path /var/www/html

