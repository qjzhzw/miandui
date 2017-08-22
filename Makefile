cpout:db.sqlite3
	cp -f db.sqlite3 /root/www/
	cp -r static/ /root/www/
	cp -f Makefile /root/www/
cpin:db.sqlite3
	cp -f /root/www/db.sqlite3 .
	cp -r /root/www/static/ .
	python manage.py migrate
run:manage.py
	nohup python manage.py runserver 0.0.0.0:8080
init:
	rm -r miandui
	git clone /root/git/miandui.git
	lsof -i:8080