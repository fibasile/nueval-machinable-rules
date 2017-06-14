import yaml
import sys,traceback
import os
import json
from cStringIO import StringIO

SOURCE_FILES = [
    'computer-controlled_cutting'
]

def readYAML(source):
    print 'Reading %s' % source
    f = open(source, 'r')
    data = yaml.load(f.read())
    f.close()
    return data
    
    
def makeTask(task):
    taskMD = StringIO()
    print >>taskMD, '## %s\n' % task['name']
    print >>taskMD, task['description']
    print >>taskMD, '### Learning outcomes\n'
    for o in task['outcomes']:
        print >>taskMD, '* %s' % o
    print >>taskMD, '\n### Have you?\n'
    for c in task['checklist']:
        print >>taskMD, '* %s' % c
    return taskMD.getvalue()

def makeBookPage(data):
    md =  StringIO()
    print >>md, '# %s\n' % data['unit']
    for task in data['tasks']:
        print >>md, makeTask(task)
    print >>md, '## FAQ\n'
    print >>md, data['faq']
    return md.getvalue()
        



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: build.py [command]\n'
        print 'Available commands'
        print '   test: Check if file syntax is ok'
        print '   json: Export rules to nueval-app json'
        print '   gitbook: Build markdown pages from YAML source\n\n'
        sys.exit(-1)
    command = sys.argv[1]
    
    for source in SOURCE_FILES:
        if command == 'test':
            try:
                data = readYAML(os.path.join(os.getcwd(), '%s.yaml' % source))
                print 'Syntax OK'
            except Exception:
                print 'Syntax Error'
        elif command == 'json':
            try:
                data = readYAML(os.path.join(os.getcwd(), '%s.yaml' % source))
                
                print json.dumps(data, indent=4)
            except Exception:
                print 'Syntax Error'
        elif command == 'gitbook':
            try:
                data = readYAML(os.path.join(os.getcwd(), '%s.yaml' % source))
                print makeBookPage(data)
            except Exception,ex:
                 traceback.print_exc()
