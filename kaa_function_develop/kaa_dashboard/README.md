# Hướng dẫn cài đặt với Nginx
Bước 1. Cài nginx

	apt install nginx-full

Bước 2. Cấu hình web server trong file /etc/nginx/sites-available/iot.admin:


	server {
		listen 80;
		listen [::]:80;
		# server_name iot.admin;
		root /var/www/iot.admin;

		location / {
		        index  index.html index.htm index.nginx-debian.html;
		        try_files $uri $uri/ /index.html;
		}
	}

Bước 3. copy source code vào thư mục /var/www:
	
	mkdir /var/www/iot.admin
	cp -r * iotadmin/* /var/www/iot.admin

Bước 4. Kiểm tra cấu hình Nginx OK và reload:
	ln -s /etc/nginx/sites-available/iot.admin /etc/nginx/sites-enabled
	nginx -t
	service nginx reload

Bước 5. Nhớ mở cổng 80.

