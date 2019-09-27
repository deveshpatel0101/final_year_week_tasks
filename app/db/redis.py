import redis
import os

host1 = os.getenv('RDB_HOSTNAME_FIRST') or 'localhost'
port1 = (os.getenv('RDB_PORT_FIRST') and int(
    os.getenv('RDB_PORT_FIRST'))) or 6379
db1 = os.getenv('RDB_NAME_FIRST')
password1 = os.getenv('RDB_PASSWORD_FIRST')

host2 = os.getenv('RDB_HOSTNAME_SECOND') or 'localhost'
port2 = (os.getenv('RDB_PORT_SECOND') and int(
    os.getenv('RDB_PORT_SECOND'))) or 6379
db2 = os.getenv('RDB_NAME_SECOND')
password2 = os.getenv('RDB_PASSWORD_SECOND')

print('HOST1', host1)
print('PORT1', port1)
print('NAME1', db1)
print('PASSWORD1', password1)
print('HOST2', host2)
print('PORT2', port2)
print('NAME2', db2)
print('PASSWORD2', password2)

rds = redis.Redis(host=host1, port=port1, db=0, password=password1)

rds_for_db = redis.Redis(host=host2, port=port2, db=0, password=password2)
