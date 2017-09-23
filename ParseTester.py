'''

testing for LogParser.py

'''

from LogParser import FileReader



errors = [
    ('HttpClientErrorException', 401, ''),
    ('AccessDeniedException', 403, 'AUTHORIZATION_FAILURE')
]

def __init__():
    file = "syslogClassShare.5"
    fr = FileReader(file, errors)
    error_log = fr.close()

    print("Error log received")
    for e in error_log:
        print ("Error: " + e)
        print ("Total errors: " + str(len(error_log[e])))
        # for line in error_log[e]:
        #     print (line)


__init__()