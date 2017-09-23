'''
This is the file that is responsible for reading the incoming text file.
It is also responsible for analyzing the given text file and returning data on the errors within the given file. 

As of now, error finding is hard coded -- user must give the system the specific errors they want to find. 
    error = (exception name to print (string), exception number (int), phrase to search (string))

'''


'''
For now, read in a file and print out first line, just to figure out that the connection works ((due 9/25))
- hopefully set it to print out lines that have the keywords we're looking for
look up string searching algorithms to find something efficient
python's built in regex might already use it, look into it


date, machine type, (there's a common error format)
    - also look for 'principal=???' so that we can figure out who's doing what. only for authorization_failure

requestForAnalysis
    - a log file in a large string
    - list of confirmed errors
    - list of confirmed non-errors
    - (no need) start and end date/time to search

return:
    - potential new errors
        - must get a yes or no to determine if we need to run analysis for new error
        - maybe stop analysis mid-process so that we don't need to rerun whole thing
    - dictionary of errors
        analysis = {
                        (date, time, principal=null),
                        (date, time, principal=null),
                        (date, time, principal=null)
                    }


'

'''

import re

class FileReader:

    def __init__(self, files, errors):
        # self.files = []
        # for f in files:
            # if f is not .txt: print ("%s is not right file", %str(f))
            # else:
            # self.files.append((open(f, 'r')))

        self.file = open(files, 'r')

        # errors dictionary
        self.errors = {}
        for e in errors:
            self.errors[e[0]] = []

        # loop through self.file line by line and check for all known errors
        # if error found, append the line to that key's value
        self.__read_lines(self.file)

        # print total errors found for every known error results
        for key in self.errors:
            print ("Results for error " + key + "\n" +
                   "Total errors found: " + str(len(self.errors[key])) + "\n")

        self.new_error_added = False


    '''
    Reads through all the lines of the files.
    Once an error is found, append the string to the self.errors dictionary
    '''
    def __read_lines(self, open_file):
        file_lines = self.file.readlines()
        print("number of lines: " + str(len(file_lines)))
        for f in file_lines:
            for e in self.errors:
                error_found = re.search(str(e), f, re.M | re.I)
                if error_found:
                    date = f[:6]
                    time = f[7:15]
                    principal_index = f.find('AuditEvent')
                    principal_user = None
                    # if principal_index > 0:
                    #     principal_user = f[principal_index:].split()[6].split('=')[1].strip(',')
                    self.errors[e].append((date, time, f))
                    # print ("error found: " + e)
                    # print (f)




    # For when user wants to add a new error.
    # Flag is raised to remind user that a new error has been saved at end of session
    def __add_error(self, new_error):
        self.new_error_added = True
        self.errors.append(new_error)
        print("New error inputted")
        # possibly rerun analyzer for new errors?


    '''
    Used for when user wants to close the reader.
    Returns the dictionary of lists containing the original string from where the corresponding error was found
    '''
    def close(self):
        if self.new_error_added:
            print ("New error added during this session")
        self.file.close()
        return self.errors