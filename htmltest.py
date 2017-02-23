from HTMLParser import HTMLParser


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



parser = MyHTMLParser()
parser.feed('<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta http-equiv="Content-Style-Type" content="text/css" /><meta name="description" content="Proposal Title" /><meta name="keywords" content="Title and key words" /><meta name="generator" content="Aspose.Words for .NET 16.11.0.0" /><title>Proposal Title</title></head><body><div><p style="margin-top:10pt; margin-bottom:0pt; widows:0; orphans:0; font-size:10pt"><span style="font-family:Arial; color:#3e67a4">No</span><span style="font-family:Arial; color:#3e67a4">. Cisco Prime Infrastructure cannot </span><span style="font-family:Arial; color:#3e67a4">view the device health for virtual instances on a device (like on Nexus)</span><span style="font-family:Arial; color:#3e67a4">. </span><span style="font-family:Arial; color:#3e67a4">http://www.cisco.com/c/en/us/td/docs/net_mgmt/prime/infrastructure/</span><span style="font-family:Arial; color:#3e67a4">3-1</span><span style="font-family:Arial; color:#3e67a4">/user/guide/</span><span style="font-family:Arial; color:#3e67a4">pi_ug</span><span style="font-family:Arial; color:#3e67a4">/monitor_network.html</span></p></div><p>blabla</p></body></html>')
print parser.text