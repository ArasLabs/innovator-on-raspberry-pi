#class that takes aml portion of soap call and returns result
# holds connection and user information

import httplib

innovatorServer = "169.254.64.111"
innovatorApp = "93sp6"
innovatorPage = "/" + innovatorApp + "/Server/InnovatorServer.aspx"
innovatorVault = "/" + innovatorApp + "/vault/vaultserver.aspx"
innovatorUser = "admin"
innovatorUserPassword =  "607920b64fe136f9ab2389e371852af2"
innovatorDatabase = "ACE_Pi_Prep"

SM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope 
SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"  
xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Body>
<ApplyItem xmlns:m="http://www.aras-corp.com">
%s
</ApplyItem>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

def callInnovator(item):
    soapMessage = SM_TEMPLATE%(item)

    webservice = httplib.HTTPConnection(innovatorServer)
    webservice.putrequest("POST", innovatorPage)
    webservice.putheader("AUTHUSER", innovatorUser)
    webservice.putheader("AUTHPASSWORD", innovatorUserPassword)
    webservice.putheader("DATABASE", innovatorDatabase)
    webservice.putheader("Content-length", "%d" % len(soapMessage))
    webservice.putheader("SOAPAction", "ApplyItem")
    webservice.endheaders()
    webservice.send(soapMessage)
    return webservice.getresponse()

#def GetPart():
#    def __init__(self):
        
def GetLogins():
    response = callInnovator('''<Item type="User" action="get" select="login_name"/>''')
    return response.read()
        
def ApplyItem(item):
    response = callInnovator(item)
    return response.read()
        
    
