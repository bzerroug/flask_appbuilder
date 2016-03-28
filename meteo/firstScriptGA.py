import argparse
from datetime import datetime

from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools


def get_service(api_name, api_version, scope, client_secrets_path):
  """Get a service that communicates to a Google API.

  Args:
    api_name: string The name of the api to connect to.
    api_version: string The api version to connect to.
    scope: A list of strings representing the auth scopes to authorize for the
      connection.
    client_secrets_path: string A path to a valid client secrets file.

  Returns:
    A service that is connected to the specified API.
  """
  # Parse command-line arguments.
  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
  flags = parser.parse_args([])

  # Set up a Flow object to be used if we need to authenticate.
  flow = client.flow_from_clientsecrets(
      client_secrets_path, scope=scope,
      message=tools.message_if_missing(client_secrets_path))

  # Prepare credentials, and authorize HTTP object with them.
  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to a file.
  storage = file.Storage(api_name + '.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)
  http = credentials.authorize(http=httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service


#def get_first_profile_id(service):
#  # Use the Analytics service object to get the first profile id.
#
#  # Get a list of all Google Analytics accounts for the authorized user.
#  accounts = service.management().accounts().list().execute()
#
#  if accounts.get('items'):
#    # Get the first Google Analytics account.
#    account = accounts.get('items')[0].get('id')
#
#    # Get a list of all the properties for the first account.
#    properties = service.management().webproperties().list(
#        accountId=account).execute()
#
#    if properties.get('items'):
#      # Get the first property id.
#      property = properties.get('items')[0].get('id')
#
#      # Get a list of all views (profiles) for the first property.
#      profiles = service.management().profiles().list(
#          accountId=account,
#          webPropertyId=property).execute()
#
#      if profiles.get('items'):
#        # return the first view (profile) id.
#        return profiles.get('items')[0].get('id')

  return None


def get_results(service, profile_id, datedeb, datefin):
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions in the past seven days.
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=datedeb,
      end_date=datefin,
      metrics='ga:sessions').execute()


def print_results(results):
  # Print data nicely for the user.
  if results:
    print 'View (Profile): %s' % results.get('profileInfo').get('profileName')
    print 'Total Sessions: %s' % results.get('rows')[0][0]

  else:
    print 'No results found'


def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, '/Users/bzerroug/projects/googleAnalyticsAPI/client_secrets.json')
  profile = '97199161'#get_first_profile_id(service) 
  print_results(get_results(service, profile, '2016-03-01', '2016-03-13'))

#site : ga:97200935
#appli : ga:97198927

def getSessions(profile, datedeb, datefin):
  scope = ['https://www.googleapis.com/auth/analytics.readonly']
  service = get_service('analytics', 'v3', scope, '/Users/bzerroug/projects/googleAnalyticsAPI/client_secrets.json')
  profile = profile#get_first_profile_id(service) 
  results=get_results(service, profile, datedeb, datefin)
  return results.get('rows')[0][0]
  

def get_TTR_site(profile_id, datedeb, datefin):
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions in the past seven days.
  scope = ['https://www.googleapis.com/auth/analytics.readonly']
  service = get_service('analytics', 'v3', scope, '/Users/bzerroug/projects/googleAnalyticsAPI/client_secrets.json')
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=datedeb,
      end_date=datefin,
      metrics='ga:transactionsPerSession').execute()

if __name__ == '__main__':
  main()
  
#  scope = ['https://www.googleapis.com/auth/analytics.readonly']
#  service = get_service('analytics', 'v3', scope, 'client_secrets.json') 
#  api_query = service.data().ga().get(
#    ids='ga:97200935',
#    start_date='2016-01-01',
#    end_date='2016-01-15',
#    metrics='ga:sessions',
#    #dimensions='ga:source,ga:keyword',
#    #sort='-ga:sessions,ga:source',
#    #filters='ga:medium==organic',
#   max_results='25')
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  