# Necessary imports
import requests
import json
import sys
from datetime import datetime, timezone
from prettyTime import prettyTime

query_template = """{{
  stopPlace(id: \"{}\") {{
      name
      estimatedCalls(timeRange: 72100, numberOfDepartures: {}) {{
        aimedArrivalTime
        expectedArrivalTime
        quay {{
          publicCode
        }}
        destinationDisplay {{
          frontText
        }}
        serviceJourney {{
          journeyPattern {{
            line {{
              publicCode
            }}
          }}
        }}
      }}
    }}
  }}"""

api_url = 'https://api.entur.io/journey-planner/v2/graphql'

iso_datestring = "%Y-%m-%dT%H:%M:%S%z"
now = datetime.now(timezone.utc)

class StopPlace:
  def __init__(self, nsr_id, noDepartures = 20):
    """Initializes object with the stop's NSR ID. May also take custom GraphQL query.
    
    noDepatures - Specifies entries to retrieve. Default is 20.
    """
    self.id = nsr_id
    self.query = query_template.format(self.id, noDepartures)
    r = requests.post(api_url, json={'query': self.query}, headers={'ET-Client-Name': 'kmaasrud - pythentur'}) # TODO: Not all requests should go through me. Require custom header.
    json_data = json.loads(r.text)['data']['stopPlace']
    self.name = json_data['name'] # TODO: Not always available. Constructor must handle this.

  def get(self):
    """Retrieves list of dictionaries, containing templated data."""
    r = requests.post(api_url, json={'query': self.query}, headers={'ET-Client-Name': 'kmaasrud - pythentur'})
    json_data = json.loads(r.text)['data']['stopPlace']

    data = []
    for call in json_data['estimatedCalls']:
      aimed = datetime.strptime(call['aimedArrivalTime'], iso_datestring)
      expected = datetime.strptime(call['expectedArrivalTime'], iso_datestring)
      delay = expected - aimed
      line = call['serviceJourney']['journeyPattern']['line']['publicCode']+" "+call['destinationDisplay']['frontText']
      platform = call['quay']['publicCode']
      readable = prettyTime((expected - now).seconds)

      dictio = {
          'platform': platform,
          'line': line,
          'aimedArrivalTime': aimed,
          'expectedArrivalTime': expected,
          'delay': delay,
          'readableTime': readable
      }

      data.append(dictio)

    return data

# TODO: Class handling custom route info.

if __name__ == "__main__":
  pass