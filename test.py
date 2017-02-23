import zeep
import logging.config
from lxml import etree
import sys
from HTMLParser import HTMLParser


logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

class MyHTMLParser(HTMLParser):
	def __init__(self):
		self.text = ''
		self.start = False
		self.end   = False
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		if ( not self.end):
			if  (tag == 'div') :
				self.start = True

	def handle_endtag(self, tag):
		if ( not self.end):
			if  (tag == 'div') :
				self.end = True

	def handle_data(self, data):
		if ( not self.end) and self.start :
			self.text += data

def update_endpoint(file,newurl):
	try :
		tree = etree.parse(file)
		namespaces = {'soap':'http://schemas.xmlsoap.org/wsdl/soap/'}
		tree.findall('.//soap:address',namespaces)[0].attrib['location']=newurl
		with open(file, 'w') as file_handle:
		    file_handle.write(etree.tostring(tree, pretty_print=True, encoding='utf8'))		
	except:
		e = sys.exc_info()[0]
		print e
		return False
	else:
		return True


class QvidianAuthentication:
	def __init__( self, wsdl_file, endpoint_url):
		update_endpoint(wsdl_file,endpoint_url)
		self.client = zeep.Client(wsdl=wsdl_file)
		self.ConnectResult = None
	def Connect(self, userName, password):
		self.ConnectResult = self.client.service.Connect(userName=userName, password=password)['body']['ConnectResult']

class Common:
	def __init__( self, wsdl_file, endpoint_url):
		update_endpoint(wsdl_file,endpoint_url)
		self.client = zeep.Client(wsdl=wsdl_file)
		self.HasPermissionsResponse = None
		self.HeaderType = self.client.get_element('ns0:QvidianCredentialHeader')
		
	def HasPermissions(self, AuthenticationToken , Permission):
		QvidianCredentialHeader = self.HeaderType(AuthenticationToken=AuthenticationToken)
		self.HasPermissionsResponse=self.client.service.HasPermissions(_soapheaders=[QvidianCredentialHeader],Permission=Permission)['body']

class ContentLibrary:
	def __init__( self, wsdl_file, endpoint_url):
		update_endpoint(wsdl_file,endpoint_url)
		self.client = zeep.Client(wsdl=wsdl_file)
		self.librarySearchRequestsInitResponse    = None
		self.librarySearchesAsListsResponse       = None
		self.libraryContentPreviewHTMLGetResponse = None
		self.HeaderType = self.client.get_element('ns0:QvidianCredentialHeader')

	def librarySearchRequestsInit(self, AuthenticationToken , requestCount):
		QvidianCredentialHeader = self.HeaderType(AuthenticationToken=AuthenticationToken)
		self.librarySearchRequestsInitResponse=self.client.service.librarySearchRequestsInit(_soapheaders=[QvidianCredentialHeader],requestCount=requestCount)['body']['librarySearchRequestsInitResult']		

	def librarySearchesAsLists(self, AuthenticationToken , searchRequestList):
		QvidianCredentialHeader = self.HeaderType(AuthenticationToken=AuthenticationToken)
		self.librarySearchesAsListsResponse=self.client.service.librarySearchesAsLists(_soapheaders=[QvidianCredentialHeader],searchRequestList=searchRequestList)['body']['librarySearchesAsListsResult']		

	def libraryContentPreviewHTMLGet(self, AuthenticationToken , ContentID):
		QvidianCredentialHeader = self.HeaderType(AuthenticationToken=AuthenticationToken)
		self.libraryContentPreviewHTMLGetResponse=self.client.service.libraryContentPreviewHTMLGet(_soapheaders=[QvidianCredentialHeader],contentID=ContentID,revision='-1')['body']['libraryContentPreviewHTMLGetResult']		



QvidianAuthenticationWSDL = './QvidianAuthentication.wsdl'
CommonWSDL ='./Common.wsdl'
ContentLibraryWSDL='./ContentLibrary.wsdl'
"""
update_endpoint(QvidianAuthenticationWSDL,'https://qpalogin.qvidian.com/QvidianAuthentication.asmx')
QvidianAuthentication_client = zeep.Client(wsdl=QvidianAuthenticationWSDL)
ConnectResult=QvidianAuthentication_client.service.Connect(userName='searchtermshelper@cisco.com', password='Chat4All')['body']['ConnectResult']
print ConnectResult['AuthToken']
print ConnectResult['CommonURL']

update_endpoint(CommonWSDL,ConnectResult['CommonURL'])
client2 = zeep.Client(wsdl=CommonWSDL)
HeaderType = client2.get_element('ns0:QvidianCredentialHeader')
QvidianCredentialHeader = HeaderType(AuthenticationToken=str(ConnectResult['AuthToken']))
HasPermissionsResponse=client2.service.HasPermissions(_soapheaders=[QvidianCredentialHeader],Permission='AllowPreviewHTML')['body']
print HasPermissionsResponse['HasPermissionsResult']"""


QvidianAuthentication_client = QvidianAuthentication(QvidianAuthenticationWSDL,'https://qpalogin.qvidian.com/QvidianAuthentication.asmx')
QvidianAuthentication_client.Connect('searchtermshelper@cisco.com','Chat4All')
print QvidianAuthentication_client.ConnectResult
print "==========="
Common_client = Common(CommonWSDL,QvidianAuthentication_client.ConnectResult['CommonURL'])
Common_client.HasPermissions(QvidianAuthentication_client.ConnectResult['AuthToken'],'AllowPreviewHTML')
print Common_client.HasPermissionsResponse
print "==========="
ContentLibrary_client = ContentLibrary(ContentLibraryWSDL,QvidianAuthentication_client.ConnectResult['ContentLibraryURL'])
ContentLibrary_client.librarySearchRequestsInit(QvidianAuthentication_client.ConnectResult['AuthToken'],1)
print ContentLibrary_client.librarySearchRequestsInitResponse
print "==========="
new_SearchRequest = ContentLibrary_client.librarySearchRequestsInitResponse
print "========"
new_SearchRequest['SearchRequest'][0]['SearchSettings']['SearchName'] = "abdel"
new_SearchRequest['SearchRequest'][0]['SearchSettings']['Title'] = "abdelsearch"
new_SearchRequest['SearchRequest'][0]['SearchSettings']['OneOrMoreOfTheseWords']=[{'string':"nexus" }]
new_SearchRequest['SearchRequest'][0]['SearchSettings']['Include'] = [{'eSearchIncludes' : "Content"},{'eSearchIncludes' : "Bundles"}]
new_SearchRequest['SearchRequest'][0]['SearchSettings']['FoundIn'] = [{'eSearchFoundIns' : "Title" },{'eSearchFoundIns' : "Content"},{'eSearchFoundIns' : "Keywords"}]
new_SearchRequest['SearchRequest'][0]['SearchSettings']['UseInflectional'] = "false"
new_SearchRequest['SearchRequest'][0]['SearchSettings']['resetSearchCache'] = "true"
new_SearchRequest['SearchRequest'][0]['getContentFileData'] = "false"
new_SearchRequest['SearchRequest'][0]['getTotalResultsCount'] = "true"
new_SearchRequest['SearchRequest'][0]['maxSearchResults'] = "10"
new_SearchRequest['SearchRequest'][0]['resultPageSize'] = "5"
new_SearchRequest['SearchRequest'][0]['resultPageIndex'] = "0"
new_SearchRequest['SearchRequest'][0]['saveAdvancedSearch'] = "false"
new_SearchRequest['SearchRequest'][0]['searchTabID'] = "00000000-0000-0000-0000-000000000000"
new_SearchRequest['SearchRequest'][0]['getSearchHistory'] = "false"
new_SearchRequest['SearchRequest'][0]['searchMode'] = "ClearSearch"
new_SearchRequest['SearchRequest'][0]['stdSearchID'] = "-1"
print new_SearchRequest
print "$$$$$$$$$$$$$$$"
ContentLibrary_client.librarySearchesAsLists(QvidianAuthentication_client.ConnectResult['AuthToken'],new_SearchRequest)
with open('output.json', 'w') as file_handle: 
	file_handle.write(str(ContentLibrary_client.librarySearchesAsListsResponse))	
print ContentLibrary_client.librarySearchesAsListsResponse['SearchResultsList'][0]['totalResultsCount']
print ContentLibrary_client.librarySearchesAsListsResponse['SearchResultsList'][0]['contentList']['Content'][0]['ContentID']

ContentLibrary_client.libraryContentPreviewHTMLGet(QvidianAuthentication_client.ConnectResult['AuthToken'],ContentLibrary_client.librarySearchesAsListsResponse['SearchResultsList'][0]['contentList']['Content'][1]['ContentID'])
print "*************************"
#print ContentLibrary_client.libraryContentPreviewHTMLGetResponse['htmlContent']
print ContentLibrary_client.librarySearchesAsListsResponse['SearchResultsList'][0]['contentList']['Content'][1]['LearnedTerms']
parser = MyHTMLParser()
parser.feed(ContentLibrary_client.libraryContentPreviewHTMLGetResponse['htmlContent'])
print parser.text
 













