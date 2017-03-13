#part.py
import instruction as INSTR
import araslib
import xml.etree.cElementTree as ET
from datetime import datetime
from time import sleep

ITEM_TEMPLATE = """
<AML>
    <Item action='get' type='Part'>
        <item_number>%s</item_number>
        <Relationships>
                        <Item type="Part Assembly Instructions" action="get" orderBy="sort_order">
                                <related_id>
                                <Item type="Assembly Instruction" action="get"></Item>
                                </related_id>
                        </Item>
                </Relationships>
        </Item>
</AML>
"""

NEW_SERIAL_TEMPLATE = """
<AML>
    <Item action='add' type="Part Serial Numbers">
    <source_id>%s</source_id>
    <related_id>
                <Item action="add" type="Serial Number" select="serial_number">
                    <rl_build_date>__now()</rl_build_date>
            <rl_builder><Item action="get" type="user"><login_name>%s</login_name></Item></rl_builder>
                </Item>
        </related_id>
        </Item>
</AML>
"""
GET_SERIAL_NUMBER_ITEM = """
<AML>
    <Item type="Serial Number" action="get" id="%s"/>
</AML>
"""

PROMOTE_SERIAL_NUMBER = """
<AML>
    <Item type="Serial Number" action="PromoteItem" id="%s">
                <state>Assembled</state>
        </Item>
</AML>
"""
COMPLETE_SERIAL_NUMBER = """
<AML>
    <Item type="Serial Number" action="edit" id="%s">
        <rl_time_to_build>%s</rl_time_to_build>
        </Item>
</AML>
"""

server = araslib.innovatorServer
vault = araslib.innovatorVault
database = araslib.innovatorDatabase

class part:
    def __init__(self,partNumber):
        #Initialize properties
        self.PartNumber = partNumber
        self.Instructions = {}
        self.Builder = None
        self.RawResponse = None
        self.PartGuid = None
        self.SerialGuid = None
        self.SerialNumber = None
        self.StartBuildTime = None
        self.StopBuildTime = None
        #self.BuildTime = None
        
        item = ITEM_TEMPLATE%(partNumber)
        self.RawResponse = araslib.ApplyItem(item)
        i = 0
        root = ET.fromstring(self.RawResponse)
        self.PartGuid = root.find(".//Item[@type='Part']").get("id")
        for instructionItem in root.findall(".//Item[@type='Part Assembly Instructions']"):
            i += 1
            sort_order = instructionItem.find('sort_order').text
            t1 = instructionItem.findall(".//Item[@type='Assembly Instruction']")
            t2 = t1[0]
            instructionText =  t2.find('rl_instruction').text
            imageEl = t2.find('rl_image')
            if not imageEl is None:
                instructionImageGuid = t2.find('rl_image').text
                instructionImageName = t2.find('rl_image').get('keyed_name')
                instructionUrl = 'http://' + server + '/' + vault + '?dbName=' + database + '&fileID=' + instructionImageGuid + '&fileName=' + instructionImageName
            else:
                instructionImageGuid = ""
                instructionImageName = ""
                instructionUrl = ""
            #print sort_order, instructionText, instructionImageGuid, instructionImageName, instructionUrl
            instructionInstance = INSTR.Instruction(sort_order, instructionText, instructionImageName, instructionImageGuid, instructionUrl)
            self.Instructions[i] = instructionInstance
        
    def StartBuild(self):
        self.StartBuildTime = datetime.now()
        self.NewSerialNumber()
        print self.SerialNumber
        print self.Instructions[1].instructionText
        
    def CompleteBuild(self):
        self.StopBuildTime = datetime.now()
        self.CompleteSerialNumber()
    
    def BuildTime(self):
        return "{0:.2f}".format((self.StopBuildTime - self.StartBuildTime).seconds / 60.0)
    
    def NewSerialNumber(self):
        if self.Builder is None:
            raise NameError('Builder not set')
        if self.PartGuid is None:
            raise NameError('PartGuid not set')

        serialAML = NEW_SERIAL_TEMPLATE%(self.PartGuid,self.Builder)
        serialResponse = araslib.ApplyItem(serialAML)
        root = ET.fromstring(serialResponse)
        self.SerialGuid = root.find(".//Item[@type='Serial Number']").get("id")
        getSerialNumberAML = GET_SERIAL_NUMBER_ITEM%(self.SerialGuid)
        result = araslib.ApplyItem(getSerialNumberAML)
        root = ET.fromstring(result)
        self.SerialNumber = root.find(".//Item[@type='Serial Number']/serial_number").text

    def CompleteSerialNumber(self):
        #update with time
        serialAML = COMPLETE_SERIAL_NUMBER%(self.SerialGuid,self.BuildTime())
        #print serialAML
        result = araslib.ApplyItem(serialAML)
        #print "complete ", result
        serialAML = PROMOTE_SERIAL_NUMBER%(self.SerialGuid)
        result = araslib.ApplyItem(serialAML)
        #promote
    
#p1 = part("111")
#p1.Builder = "Admin"
#p1.NewSerialNumber()
#print p1.SerialNumber
#p1.CompleteSerialNumber()
#print p1.PartNumber
#print p1.PartGuid
#print p1.Builder
#print p1.RawResponse
#print p1.Instructions[1].instructionText

#Get part 123, get new serial number, build (sleep), complete
#p1 = Part("123")
#p1.Builder = "Admin"
#p1.StartBuild()
#print p1.SerialNumber
#sleep(5)
#p1.CompleteBuild()
#print "Build Time: ", "{0:.2f}".format(p1.BuildTime())

#print "done"