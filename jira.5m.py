#!/opt/local/bin/python -W ignore

import sys
import os
from jira import JIRA
import datetime

# jira credentials
JIRA_HOSTNAME = ''
JIRA_USERNAME = ''
JIRA_APITOKEN = ''

# jira project prefixes to include
PROJECTS = ['TICKET']

# ticket statuses to include
STATUSES = [
  'In Progress',
  'QA',
  'Blocked',
  'Selected for Development',
  'More Info Requested',
  'Backlog'
]

if len(sys.argv) >1:
  if sys.argv[1] == 'openall':
    for ticket in sys.argv[2].split(','):
      os.system("/usr/bin/open 'https://%s/browse/%s'" % (JIRA_HOSTNAME, ticket))
  else:
    os.system("/usr/bin/open 'https://%s/browse/%s'" % (JIRA_HOSTNAME, sys.argv[1]))

  sys.exit(0)

options = {'server': 'https://%s' % (JIRA_HOSTNAME)}

SHOW_ALL_COUNT = 3

jira = JIRA(options, basic_auth=(JIRA_USERNAME, JIRA_APITOKEN))

tickets = {}

for project in PROJECTS:
  issues = jira.search_issues('project=%s and assignee = currentUser() and status in ("%s")' % (project, '","'.join(STATUSES)))

  for issue in issues:
    status = str(issue.fields.status)

    if status in STATUSES:
      if status not in tickets.keys():
        tickets[status] = []

      tickets[status].append(issue.key)


if STATUSES[0] in tickets.keys():
  line = ""
  for ticket in sorted(tickets[STATUSES[0]]):
    if len(line) >0:
      line += "  "
    line += ticket
else:
  line = ' | black'

print line

for status in STATUSES:
  if status in tickets.keys():
    print "---"

    for ticket in sorted(tickets[status]):
      print "%s (%s) | terminal=false bash='%s' param1=%s" % (ticket, status, sys.argv[0], ticket)

    if len(tickets[status]) >= SHOW_ALL_COUNT:
      print "Open all | terminal=false bash='%s' param1=openall param2=%s" % (sys.argv[0], ",".join(sorted(tickets[status])))
