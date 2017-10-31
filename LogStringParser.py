'''
this version takes in a big long string of the log file rather than a file object thing


'''

import re


class LogStringReader:

    def __init__(self, log, error_keys, known_errors, known_non_errors):
        self.log_lines = log.split("\n")
        self.non_errors = known_non_errors
        self.error_keys = error_keys

        # errors dictionary
        self.errors = {}
        for e in known_errors:
            self.errors[e[0]] = []

    '''
    Search for potential new errors.
    Skips the known_errors since we're only looking for potential new ones
    :returns: maybe_new_error -- dictionary of the lines that contained the error_key(s), value is list of the triggered keys
        ex: "this is the string containing 'fail' and 'error'" : ['fail', 'error']
    '''
    def maybe_new_errors(self):
        maybe_new_error = {}
        for line in self.log_lines:
            # check if line contains any of the error keywords
            if any (key in line for key in self.error_keys):
                # don't bother if the line contains something from the known non_errors
                if not any (non_error in line for non_error in self.non_errors):
                    maybe_new_error[line] = []
                    for k in self.error_keys:
                        if str(k.upper()) in line.upper():
                            maybe_new_error[line].append(k)

        return maybe_new_error

    '''
    Appends a new error to the self.errors list
    :parameter: new_errors -- a list of new errors given by the user 
    '''
    def add_new_error(self, new_errors):
        for new in new_errors:
            self.errors[new] = []

    '''
    Searches for the known errors, that is, the errors recorded in self.errors
    :returns: self.error -- dictionary of Name of Error (key) and the lines that were caught on it (values)
            the values themselves have a tuple of date, time, and original line
    '''
    def find_errors(self):
        print("number of lines: " + str(len(self.log_lines)))
        for f in self.log_lines:
            for e in self.errors:
                error_found = re.search(str(e), f, re.M | re.I)
                # figure out regex expressions for finding varied length characters, ignoring spaces, etc
                # re.search(‘principal=([^ ]*)‘, principal_line)[1]
                # 'within string we're matching=(this is the capture we want[here are rules for one character ('^' means not the things after it)]* repeat as many times as it can)
                if error_found:
                    date = f[:6]
                    time = f[7:15]
                    principal_index = f.find('AuditEvent')
                    principal_user = None
                    # if principal_index > 0:
                    #     principal_user = f[principal_index:].split()[6].split('=')[1].strip(',')
                    self.errors[e].append((date, time, f))
        return self.errors