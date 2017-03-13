#!/usr/bin/python

import part
from time import sleep
from arasClientUi import arasClientUi

#scan barcode and retrieve part
partItem = part.Part("111")
#assign builder name
partItem.Builder = "Admin"
partItem.StartBuild()
#show serial number
#show 1st instruction
#wait for buttons

ui = arasClientUi()

instructions = partItem.Instructions
for key, instruction in instructions.iteritems():
    #print key, instruction.instructionText, instruction.sequence, instruction.imageUrl
    ui.writeCompleteInstruction(instruction.instructionText, instruction.imageUrl)
    sleep(2)
    


#sleep(3)
partItem.CompleteBuild()
#press start (StartBuild)
#   start time (right button)
#   get new serial number
#   print serial number
#   show first instruction
#cycle through instrutions (right/left buttons)
#complete build (right button)
#   call CompleteSerialNumber
#update leader board

#instructions = partItem.Instructions
#for key, instruction in instructions.iteritems():
#    print key, instruction.instructionText, instruction.sequence, instruction.imageUrl



#print partItem.Builder
#partItem.NewSerialNumber()
#print partItem.SerialNumber
#print partItem.SerialGuid
#partItem.CompleteSerialNumber()
