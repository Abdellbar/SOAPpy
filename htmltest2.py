from HTMLParser import HTMLParser

pstring = source_code = """<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta http-equiv="Content-Style-Type" content="text/css" /><meta name="description" content="Proposal Title" /><meta name="keywords" content="Title and key words" /><meta name="generator" content="Aspose.Words for .NET 16.11.0.0" /><title>Proposal Title</title></head><body><div><p style="margin-top:10pt; margin-bottom:0pt; widows:0; orphans:0; font-size:10pt"><span style="font-family:Arial; color:#3e67a4">No</span><span style="font-family:Arial; color:#3e67a4">. Cisco Prime Infrastructure cannot </span><span style="font-family:Arial; color:#3e67a4">view the device health for virtual instances on a device (like on Nexus)</span><span style="font-family:Arial; color:#3e67a4">. </span><span style="font-family:Arial; color:#3e67a4">http://www.cisco.com/c/en/us/td/docs/net_mgmt/prime/infrastructure/</span><span style="font-family:Arial; color:#3e67a4">3-1</span><span style="font-family:Arial; color:#3e67a4">/user/guide/</span><span style="font-family:Arial; color:#3e67a4">pi_ug</span><span style="font-family:Arial; color:#3e67a4">/monitor_network.html</span></p></div><p>blabla</p></body></html>"""


class myhtmlparser(HTMLParser):
    def __init__(self):
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
    def handle_data(self, data):
        self.HTMLDATA.append(data)
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []

parser = myhtmlparser()
parser.feed(pstring)

# Extract data from parser
tags  = parser.NEWTAGS
attrs = parser.NEWATTRS
data  = parser.HTMLDATA

# Clean the parser
parser.clean()

# Print out our data
print tags
print attrs
print data
