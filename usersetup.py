from user import User
from dbs import storage

a = User()
storage.reload()
a.email = 'tet@test.com'
a.set_password('tst')
a.username = 'tst'
a.save()