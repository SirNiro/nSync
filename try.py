import os

root, dirs, files = next(os.walk('.'))

print 'directories:', dirs
print 'files:', files
print root