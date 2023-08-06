import requests
class SharedCount:
    def __init__(self, apiToken):
        self.apiToken = apiToken

    def getApiToken(self):
        return self._apiToken

    def setApiToken(self, value):
        if not isinstance(value, str):
            raise ValueError('Api token must be a string')
        self._apiToken = value
        
    def getQuota(self, urlToCheck):
        if not isinstance(urlToCheck, str):
            raise ValueError('Url must be a string')
        response = requests.get('https://api.sharedcount.com/v1.0/?apikey=' + self._apiToken + '&url=' + urlToCheck)
        json = response.json()
        return json
    
    def getBulkId(self, urlsToCheck):
        if not isinstance(urlsToCheck, list):
            raise ValueError('Array must be provided')
        urlsToCheck = '\n'.join([str(elem) for elem in urlsToCheck]) 
        response = requests.post('https://api.sharedcount.com/v1.0/bulk?apikey=' + self._apiToken, data = urlsToCheck)
        json = response.json()
        return json
    
    def getBulkQuota(self, bulkId):
        if not isinstance(bulkId, str):
            raise ValueError('Bulk id must be a string')
        response = requests.get('https://api.sharedcount.com/v1.0/bulk?apikey=' + self._apiToken + '&bulk_id=' + bulkId)
        json = response.json()
        return json

    apiToken = property(getApiToken, setApiToken)
    