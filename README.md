zapret2acl
==========

Программа для конвертации access-list и загрузки на cisco xml-файла полученного от zapret-info.gov.ru 

Есть консольный режим и возможность загрузки через web-интерфейс

Консольный режим
================

пример:
`zapret2acl -f ~/Загрузки/dump.xml -c 192.168.1.1 -a 150 -u admin -p 123`

Обязательные опции:
```
  -f FILE, --file=FILE  read data from FILE
  -a ACL, --acl=ACL     acl number
  -c CISCO, --cisco=CISCO IP
```

Не обязательные опции:
```
  -u USER, --user=USER  Username
  -p PASSWORD, --password=PASSWORD
```

Веб-интерфейс:
=============
Чтобы не заполнять форму каждый раз можно прописать параметы в development.ini

Программа для автоматической загрузки дампов с zapret-info.gov.ru 
================
https://github.com/aleksandr-rakov/zapret2acl/tree/master/service
