cpout:db.sqlite3
	cp -f db.sqlite3 /root/
	cp -r static/ /root/
	cp -f Makefile /root/
cpin:db.sqlite3
	cp -f /root/db.sqlite3 .
	cp -r /root/static/ .
	python manage.py migrate
run:manage.py
	python manage.py runserver 0.0.0.0:8080
init:
	rm -r miandui
	git clone /root/git/miandui.git
	lsof -i:8080