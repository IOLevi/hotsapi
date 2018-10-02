from user import User
from dbs import storage

a = User()
storage.reload()
a.email = 'test@test.com'
a.set_password('test')
a.username = 'test'
a.save()