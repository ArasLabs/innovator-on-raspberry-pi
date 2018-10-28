import pygame
from pygame.locals import *
import time
import part
import urllib2
import StringIO
import string
from time import sleep
import RPi.GPIO as GPIO



#def __del__(self):
#    "Destructor to make sure pygame shuts down, etc."
	
def newPart():
    global building
    global currentInstruction
    #print "ci=" + str(currentInstruction)
    clearScreen()
    global partItem
    partNo = ask(screen, "Part Number")
    while (partNo != "xxx" and partNo != ""):
    	partItem = part.part(partNo)
        partItem.Builder = "Admin"
        partItem.StartBuild()
        print "pn: " + partItem.PartNumber
        print "instruction 1: " + partItem.Instructions[1].instructionText
        building = True
    	buildPart()
    	clearScreen()
    	partNo = ask(screen, "Part Number")
        partItem = None
        currentInstruction = 0
    
def nextButton():
    global currentInstruction
    global building
    #print "nextButton: currentInstruction - " + str(currentInstruction)
    if (currentInstruction == len(partItem.Instructions)):
        #print "current instruction number matches total instrutions"
        building = False
        return
    else:
        currentInstruction += 1
    
    #print "currentInstruction: " + str(currentInstruction)
    
    itext = partItem.Instructions[currentInstruction].instructionText
    iurl = partItem.Instructions[currentInstruction].imageUrl
    writeCompleteInstruction(itext, iurl)

def previousButton():
    global currentInstruction
    if (currentInstruction != 1):
        currentInstruction -= 1
    #itext = partItem.Instructions[currentInstruction].instructionText
    itext = partItem.Instructions[currentInstruction].instructionText
    iurl = partItem.Instructions[currentInstruction].imageUrl
    writeCompleteInstruction(itext, iurl)

def buildPart():
	#instructions = partItem.Instructions
	#setup gpio
    global partItem
    global building
    #print "BP pn: " + partItem.PartNumber
    #print "buildPart ci=" + str(currentInstruction)
    #print "BP instruction 1: " + partItem.Instructions[1].instructionText

    GPIO.setmode(GPIO.BCM)
	# GPIO 23 set up as input. It is pulled up to stop false signals
    GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(23, GPIO.FALLING) #, callback=nextButton, bouncetime=200)  # add rising edge detection on a channel
    GPIO.add_event_detect(24, GPIO.FALLING) #, callback=button24, bouncetime=200)  # add rising edge detection on a channel
    GPIO.add_event_detect(25, GPIO.FALLING) #, callback=button24, bouncetime=200)  # add rising edge detection on a channel
    time_stamp = time.time()    
    #header

    #global time_stamp       # put in to debounce  
    #time_now = time.time()  
    #if (time_now - time_stamp) >= 0.3:  
    #    print "Rising edge detected on port 24 - even though, in the main thread,"  
    #    print "we are still waiting for a falling edge - how cool?\n"  
    #time_stamp = time_now  


    #first instruction
    nextButton()
    #event loop
    #building = True
    print "building: " + str(building)

    while building:
    	try:
            time_now = time.time()
            if (GPIO.event_detected(23) and ((time_now - time_stamp) > 0.3)):
                print "channel 23"
                print "time now: " + str(time_now)
                print "time stamp: " + str(time_stamp)
                print "time diff: " + str(time_now - time_stamp)
                time_stamp = time_now
                sleep(0.02)
                nextButton()
                
            if (GPIO.event_detected(24) and ((time_now - time_stamp) > 0.3)):
                print "channel 24"
                time_stamp = time_now
                sleep(0.02)
                previousButton()

            #wait for button events
    		sleep(0.1)
    	except KeyboardInterrupt:
            GPIO.cleanup()
            pygame.quit()
            
    waitForComplete = True
    while waitForComplete:
        try:
            if GPIO.event_detected(25):
                partItem.CompleteBuild()
                waitForComplete = False
        except KeyboardInterrupt:
            GPIO.cleanup()
            pygame.quit()
    
    GPIO.cleanup()               

    
    #        for key, instruction in instructions.iteritems():
    #            #print key, instruction.instructionText, instruction.sequence, instruction.imageUrl
    #            self.writeCompleteInstruction(instruction.instructionText, instruction.imageUrl)
    #            sleep(0.5)

    
def display_box(screen, message):
	"Print a message in a box in the middle of the screen"
	fontobject = pygame.font.Font(None,30)
#        pygame.draw.rect(screen, (0,0,0),
#                                  ((screen.get_width() / 2) - 100,
#                                    (screen.get_height() / 2) - 10,
#                                    200,20), 0)
#        pygame.draw.rect(screen, (255,255,255),
#                                  ((screen.get_width() / 2) - 102,
#                                    (screen.get_height() / 2) - 12,
#                                    204,24), 1)
	pygame.draw.rect(screen, (0,0,0),
							  ((screen.get_width() / 2) - 200,
								10,
								400,30), 0)
	pygame.draw.rect(screen, (255,255,255),
							  ((screen.get_width() / 2) - 202,
								8,
								404,34), 1)
	#screen, color, ((start x, start y), x, y), thickness
	if len(message) != 0:
#            screen.blit(fontobject.render(message, 1, (255,255,255)),
#                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
		screen.blit(fontobject.render(message, 1, (255,255,255)),
			((screen.get_width() / 2) - 200, 14))
		pygame.display.flip()
        
def ask(screen, question):
    "ask(screen, question) -> answer"
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + string.join(current_string,""))
    try:
        while 1:
        	inkey = get_key()
        	if inkey == K_BACKSPACE:
        		current_string = current_string[0:-1]
        	elif inkey == K_RETURN:
        		break
        	elif inkey == K_MINUS:
        		current_string.append("_")
        	elif inkey <= 127:
        		current_string.append(chr(inkey))
        	display_box(screen, question + ": " + string.join(current_string,""))
        return string.join(current_string,"")
    except KeyboardInterrupt:
        GPIO.cleanup()
        pygame.quit()
    
def get_key():
	while 1:
		event = pygame.event.poll()
		if event.type == KEYDOWN:
			return event.key
		else:
			pass

    
def clearScreen():
	screen.fill((211, 211, 211))

def writeInstruction(instruction):
	instructionSurface = instructionFont.render(instruction, True, instructionFontColor) 
	screen.blit(instructionSurface, instructionPosition)

def writeInstructionImage(instructionUrl):
	#stream = urllib2.urlopen('http://' + arasServer + '/93sp6/vault/vaultserver.aspx?dbName=ACE_Pi_Prep&fileID=2269BC0B454B4106AEBBD52A7F1F395E&fileName=Jeep%20Page%2003.png')
	stream = urllib2.urlopen(instructionUrl)
	buffer = StringIO.StringIO(stream.read())        
	#instructionImage = pygame.image.load(instructionImageName).convert()
	instructionImage = pygame.image.load(buffer)
	screen.blit(instructionImage, (390, 100))
	
def writeCompleteInstruction(instruction, instructionUrl):
	clearScreen()
	writeInstruction(instruction)
	if instructionUrl != '':
		writeInstructionImage(instructionUrl)
	pygame.display.update()



screen = None
partNo = None
partItem = None
building = True
currentInstruction = 0
#print "currentInstruction=" + str(currentInstruction)

size = (1500,900)
print "Framebuffer size: %d x %d" % (size[0], size[1])
#self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Assembly Instructions')
# Clear the screen to start
#self.screen.fill((211, 211, 211))        
clearScreen()
# Initialise font support
pygame.font.init()
instructionFont = pygame.font.Font(None, 30)
instructionFontColor = (0, 0, 0)
instructionPosition = (50, 800)

newPart()


# Render the screen
pygame.display.update()


# Create an instance of the PyScope class
#client = arasClientUi()
#client.writeInstruction("Testing")
#pygame.display.update()
#time.sleep(3)
#client.clearScreen()
#client.writeInstruction("BlahBlahBlah")
#pygame.display.update()
#time.sleep(3)
