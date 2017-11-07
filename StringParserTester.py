


from LogStringParser import LogStringReader

# ---------- needed input variables to run LogStringReader class -------------- #
# the one long string of the log
str_log = open('syslog.5', 'r').read()
# the error keys to look out for possible new errors
# having trouble filtering out errors of numbered values, so they're currently commented out
error_keys = 'exception', 'warn', 'error', 'fail', 'unauthorized', 'timeout', 'refused', 'NoSuchPageException' #, '404', '401', '500'
# the known words for confirmed errors.
# is having this and the keys redundant?
# I think i won't need the tuple values anymore since the server side will be holding the details of the errors themselves
known_errors = [
    ('HttpClientErrorException', 401, ''),
    ('AccessDeniedException', 403, 'AUTHORIZATION_FAILURE')
]
# is there some way we can write the code so that the keys that are triggered but have a '0' in front won't be counted as an error?
# something like 'from the discovered trigger, find the nearest ',' on either side and it theres a ' 0 ' (with spaces on both sides of the 0) then ignore this triggered error'
# when we ask user to tell us why a 'maybe' line is not an error, we should probably ask them to highlight the exact part of a phrase that makes it a non_error
known_non_errors = [
    '0 connect failure',
    '0 transport failure',
    '0 closed abnormally'
]

# ----------------------------------------------------------------------------- #

print ("Error log string received")
# lsp = LogStringReader(str_log, error_keys, known_errors, known_non_errors)

# testing maybe_errors
# maybes = lsp.maybe_new_errors()
# for key in maybes:
#     print (key)
#     print (maybes[key])

# testing add_errors --- won't be used
# print (lsp.errors)
# new_errors = ['timeout']
# lsp.add_new_error(new_errors)
# print (lsp.errors)

# testing find_errors
# log_errors = lsp.find_errors()
# for key in log_errors:
#     print (key)
#     for value in log_errors[key]:
#         print (value)
#         print ("im cheating for hacktober")

# testing finding ', 0 [problem]' regex
import re

lsp_regex = LogStringReader(str_log, error_keys, known_errors, ['ljkghfalwknsfhlawnsdflakwd'])
log_errors = lsp_regex.maybe_new_errors()
for key in log_errors:
    # print (key)
    this_means_theres_an_error = re.search(', [1-9],', key, re.M | re.I)
    if this_means_theres_an_error is None:
        print ("we didn't find an error with a number in it")
        print ("so no key for you")
    else:
        for value in log_errors[key]:
            print ("aw shit son, " + this_means_theres_an_error)
            print (value)



