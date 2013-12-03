# import the standard JSON parser
import json
# import the REST library
from restful_lib import Connection
import urllib
import time
import datetime
import json
import logging
from optparse import OptionParser

# CONSTANT parameters
PAGER_DUTY = "https://webdemo.pagerduty.com"
AUTHORIZATION_CODE = "VxuRAAxQoTgTjbo7wmmG"


# Write a script that lists the created date, assigned user, and status 
# for each of the 10 most recently created incidents, in descending date order.
# Return the last 24 hours datetime, now - datetime
def getLast24Hours():

	todayDateTime = datetime.datetime.now();
	yesterdayDateTime = datetime.datetime.now() - datetime.timedelta(hours = 24)
	return (yesterdayDateTime.isoformat(), todayDateTime.isoformat())
 
# Return the incidents 
def getIncidents(numberOfIncidents, sortedby):
	base_url = PAGER_DUTY
	conn = Connection(base_url)

	yesterdayDateTime, todayDateTime = getLast24Hours()
	fields = 'status,created_on,assigned_to_user'

	# Specify authorization token
	# Specify content type - json
	resp = conn.request_get("/api/v1/incidents", args={'limit': numberOfIncidents, 'since': yesterdayDateTime, 'until': todayDateTime, 'sort_by' : sortedby, 'fields' : fields}, headers={'Authorization': 'Token token=' + AUTHORIZATION_CODE, 'content-type':'application/json', 'accept':'application/json'})
	status = resp[u'headers']['status']
	body = json.loads(resp[u'body'])

	# check that we got a successful response (200) 
	if status == '200':
		print json.dumps(body, sort_keys=False, indent=4, separators=(',', ': '))
	   
	else:
	    print 'Error status code: ', status
	    print "Response", json.dumps(body, sort_keys=False, indent=4, separators=(',', ': '))

# Define command line parameters 
def main():
	usage = "usage: %prog [options] arg"
	parser = OptionParser(usage)
	parser.add_option("-v", "--verbose",
                      help="output to stdout")
    
	parser.add_option("-i", "--numberOfIncidents",
                      action="store", default=10, dest="numberOfIncidents")

	parser.add_option("-s", "--sortby",
                      action="store", default="desc", dest="sortby")
 
    
	(options, args) = parser.parse_args()
	if len(args) != 0:
		parser.error("Incorrect number of arguments")
	if options.verbose:
		print "Running %prog..."
	if options.sortby == "desc":
		sortedby = 'created_on:desc'
	else:
		sortedby = 'created_on:asc'

	logging.info('Running ...')
	getIncidents(options.numberOfIncidents, sortedby)


#######################################################################################################################
	
if __name__ == "__main__":
    main()
