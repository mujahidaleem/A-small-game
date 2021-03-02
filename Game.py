'''Final Summative Game

The following game is a dungeon based wave game!

Enjoy!

'''

from pygame import *
import pygame #Since I defined time twice in my classes, there was an error that occured if I didnt use this... its not a mistake!
import random
import sys
import os
import time
init()

#Setting the screensize and defining various variables that will be used throughout the game
size = width, height = 1024, 576
screen = display.set_mode(size)
button = 0
state = 'Main Menu' #Initial State
wave = 1 #Initial Wave

#Text
EightBitText = font.SysFont('8 Bit Wonder', 50)
font = font.SysFont('Times New Roman', 20)
introText = EightBitText.render('Mj\'s Games',1,(0,0,255)) # Intro

waveText1 = EightBitText.render('Wave 1',1,(0,0,0)) #Wave text that tells what wave it is
waveText2 = EightBitText.render('Wave 2',1,(0,0,0))
waveText3 = EightBitText.render('Wave 3',1,(0,0,0))
waveText4 = EightBitText.render('Wave 4',1,(0,0,0))
waveText5 = EightBitText.render('Wave 5',1,(0,0,0))
startText = EightBitText.render('Start Game',1,(255,255,255))

instructionsText = EightBitText.render('Instructions',1,(255,255,255)) #All menu and instrunctions text
previousInstructionsText = EightBitText.render('Previous Page',1,(255,255,255))
nextInstructionsText = EightBitText.render('Next Page',1,(255,255,255))
QuitGameText = EightBitText.render('Quit',1,(255,255,255))
backText = EightBitText.render('Back to Menu',1,(255,255,255))

#Colours used in the game (I dont think I used any...)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE =(0,0,255)

#Music and sounds that will be used in the game
mainMusic = 'menuMusic.mp3'
gameMusic = 'gameMusic.mp3'
deadMusic ='deadmusic.mp3'
winMusic = 'winMusic.mp3'

#Misc
logo = image.load('logo.png')
logo = transform.scale(logo, (200,200))

instructions1 = image.load('1.png') #The instruction pages with the actual instructions on them
instructions2 = image.load('2.png')
instructions3 = image.load('3.png')

#Backgrounds
titleBackground = image.load('titleBackground.png') #title background
titleBackground = transform.scale(titleBackground,(1024,576))
gameBackground = image.load('gameBackground.jpg') #Game background
gamebackground = transform.scale(gameBackground,(1024,576))
diedBackground = image.load('dead.jpg') #Death background
diedBackground = transform.scale(diedBackground,(1024,576))
winBackground = image.load('win.jpg') #Win background
winBackground = transform.scale(winBackground,(1024,576))

#Characters
'''----------Regarding the classes, for the main character I had to create an animation class that consists of the Pyganimator, the Conductor that updates the animation on screen, and the actual main character itself.
AAll classes include: the class for the character, the animation as well as the main character's actions regarding what it can do, and the mob class too.----------'''

''' All constants below are for the pyganimator class'''
#Defines the constants of which define how the character should be animated (used in the animation class)
PLAYING = 'playing'
PAUSED = 'paused'
STOPPED = 'stopped'

#Defines the constants that define how the character should be animated based on direction, also defines where the character should shoot
NORTHWEST = 'northwest'
NORTH = 'north'
NORTHEAST = 'northeast'
WEST = 'west'
CENTER = 'center'
EAST = 'east'
SOUTHWEST = 'southwest'
SOUTH = 'south'
SOUTHEAST = 'southeast'

'''The animator class, lets me animate the character on screen.'''
class PygAnimation(object):
    def __init__(self, frames, loop=True):
        ''' Defines the inital lists, and contansts that will be used to define when the animation of the character should initiate.
        The character will be labeled as self, and tbe frames will be defined as frames. The whole thing must loop continuingly until all the frames are accounted for, therefore loop = true. '''

        #Creates a list for the individual images that will be used as frames
        self._images = []

        #Defines a list to how long each frame should last. For example image 2 should have a duration of 100 milliseconds before changing
        self._durations = []

        #Defines start times for each frame (in seconds), start times indicate when each frame should begin based on the time variable that is later defined
        #The end of the list of self._starttimes will be the cumulative time for all the frames to take place, while each other element will the elapsed time after each frame
        #For example if _durations is [1.5, 1.5, 2.5], then _startTimes will be [0, 1.5, 2.5, 5]
        self._startTimes = None

        # Defines the list for the transformed sprites (change in size etc)
        self._transformedImages = []

        '''Defines the state of the character. I previously defined these constants above, however now I assigned each to a variable here so that they can be manipulated in the context of the character (self).'''
        #Defines if an animation should occur, the animation is either PLAYING, PAUSED, or STOPPED. IF stopped, there is no animation, if paused the animation is paused etc.
        self._state = STOPPED

        #Defines if the animation should be looping given a condition. For eg if running, then keep looping the running animation
        self._loop = loop

        #Defines the rate of which the animation should be played, at 1.0 its normal speed
        self._rate = 1.0

        #Defines if the character is visible on screen. If its false, then the blit methods later do nothing!
        self._visibility = True

        # the time that the play() function was last called. Helps us determine what frame to blit when the character is in a playing state (moving in this case)
        self._playingStartTime = 0

        #The time that the pause() function was last called. Helps us determine what frame to blit when the character is in a paused state (standing in this case)
        self._pausedStartTime = 0

        #Loop for loading each frame into the 'frame' list that I previously defined above
        if frames != '_copy': # Checks if the given frame is a copy of the original image, the reason for why this was done can be found in the getCopies() definition below
            self.numFrames = len(frames)
            for i in range(self.numFrames):
                # load each frame of animation into _images
                frame = frames[i]
                if type(frame[0]) == str: #Checks if the frame is a string - very useful!
                    frame = (image.load(frame[0]), frame[1])
                self._images.append(frame[0])
                self._durations.append(frame[1])
            self._startTimes = self._getStartTimes()


    def _getStartTimes(self):
        '''This method is for getting the start times based off of the _durations list. As mentioned previously, it gets the start times by looking at the time elapsed per duration...'''
        startTimes = [0]
        for i in range(self.numFrames):
            startTimes.append(startTimes[-1] + self._durations[i])
        return startTimes


    def reverse(self):
        ''' This method reverses the order for the animations, allows me to blit a theoretical right running image for a left one and so on.'''
        self.elapsed = self._startTimes[-1] - self.elapsed
        self._images.reverse()
        self._transformedImages.reverse()
        self._durations.reverse()


    def getCopy(self):
        '''Allows me to get a copy of the pygameAnimation object. But instead, it only refers to the surface blits, this saves memory as a result.'''
        return self.getCopies(1)[0]


    def getCopies(self, numCopies=1):
        '''Same idea with the method above, it allows me to get a copies of the pygameAnimation object. But instead, it only refers to the surface blits, this saves memory as a result.'''
        retval = []
        for i in range(numCopies):
            newAnim = PygAnimation('_copy', loop=self.loop)
            newAnim._images = self._images[:]
            newAnim._transformedImages = self._transformedImages[:]
            newAnim._durations = self._durations[:]
            newAnim._startTimes = self._startTimes[:]
            newAnim.numFrames = self.numFrames
            retval.append(newAnim)
        return retval


    def blit(self, destSurface, dest):
        '''This method is perhaps the most important, as it draws the correct frame at the given position on screen.'''
        #As mentioned previously, if the visibility is set to false then it wont be drawn
        if self.isFinished():
            self.state = STOPPED
        if not self.visibility or self.state == STOPPED:
            return
        frameNum = findStartTime(self._startTimes, self.elapsed)
        destSurface.blit(self.getFrame(frameNum), dest)

    def getFrame(self, frameNum):
        '''This method returns which frame the object should be drawn in...'''
        if self._transformedImages == []:
            return self._images[frameNum]
        else:
            return self._transformedImages[frameNum]


    def getCurrentFrame(self):
        '''This method returns the current frame being displayed. '''
        return self.getFrame(self.currentFrameNum)


    def clearTransforms(self):
        '''Deletes all the transformed frames, so that when the animated object is blited, it displays as the original as it was before'''
        self._transformedImages = []

    def makeTransformsPermanent(self):
        '''Makes the animations/images that I feed into the class as the permanent for a given scenario, see the anchor function to see what the purpose of this is...'''
        self._images = [Surface(surfObj.get_size(), 0, surfObj) for surfObj in self._transformedImages]
        for i in range(len(self._transformedImages)):
            self._images[i].blit(self._transformedImages[i], (0,0))

    def blitFrameNum(self, frameNum, destSurface, dest):
        '''Draws the specified frame of the animated object (state does not matter). '''
        if self.isFinished():
            self.state = STOPPED
        if not self.visibility or self.state == STOPPED:
            return
        destSurface.blit(self.getFrame(frameNum), dest)


    def blitFrameAtTime(self, elapsed, destSurface, dest):
        '''Draws a frame after the frame duration or 'elapsed' number of seconds into the animation'''
        if self.isFinished():
            self.state = STOPPED
        if not self.visibility or self.state == STOPPED:
            return
        frameNum = findStartTime(self._startTimes, elapsed)
        destSurface.blit(self.getFrame(frameNum), dest)


    def isFinished(self):
        '''Returns True if this animation doesn't loop and has finished playing'''
        return not self.loop and self.elapsed >= self._startTimes[-1]


    def play(self, startTime=None):
        '''Starts playing the animation from a given point that is taken from other functions'''
        if startTime is None:
            startTime = time.time()

        if self._state == PLAYING:
            if self.isFinished():
                # if the animation doesn't loop and has already finished, then calling the play function causes it to replay from the beginning
                self._playingStartTime = startTime
        elif self._state == STOPPED:
            # if animation was stopped, start playing from the beginning
            self._playingStartTime = startTime
        elif self._state == PAUSED:
            # if animation was paused, start playing from where it was paused
            self._playingStartTime = startTime - (self._pausedStartTime - self._playingStartTime)
        self._state = PLAYING


    def pause(self, startTime=None):
        '''Stop having the animation progress, and keep it at the current frame.'''
        if startTime is None:
            startTime = time.time()
        if self._state == PAUSED:
            return # do nothing
        elif self._state == PLAYING:
            self._pausedStartTime = startTime
        elif self._state == STOPPED:
            rightNow = time.time()
            self._playingStartTime = rightNow
            self._pausedStartTime = rightNow
        self._state = PAUSED


    def stop(self):
        '''Stops the animation in progress, it allows me to set a different image in place to indicate the character is standing for example.'''
        if self._state == STOPPED:
            return # do nothing
        self._state = STOPPED

    def togglePause(self):
        '''If the animation is in a paused state, it starts playing again'''
        if self._state == PLAYING:
            if self.isFinished():
                '''If the animation has finished playing however, then this will just restart the animation over again'''
                self.play()
            else:
                self.pause()
        elif self._state in (PAUSED, STOPPED):
            self.play()


    def areFramesSameSize(self):
        '''Returns if all frames are the same size or not.'''
        width, height = self.getFrame(0).get_size()
        for i in range(len(self._images)):
            if self.getFrame(i).get_size() != (width, height):
                return False
        return True


    def getMaxSize(self):
        '''Gets the dimentions of the character by looking at the max possible width and height of the images/frames'''
        frameWidths = []
        frameHeights = []
        for i in range(len(self._images)):
            frameWidth, frameHeight = self._images[i].get_size()
            frameWidths.append(frameWidth)
            frameHeights.append(frameHeight)
        maxWidth = max(frameWidths)
        maxHeight = max(frameHeights)

        return (maxWidth, maxHeight)


    def getRect(self):
        '''Returns a rect that can be used for colliding later on (see main Player() class to see it in use)'''
        maxWidth, maxHeight = self.getMaxSize()
        return pygame.Rect(0, 0, maxWidth, maxHeight)


    def anchor(self, anchorPoint=NORTHWEST):
        '''Aligns all the frames based on an anchor point. Its based on the defined constants - NORTH SOUTH SOUTHEAST...'''
        if self.areFramesSameSize(): #If its all the same size, then dont use this at all
            return
        self.clearTransforms()#Clears the transformed images
        maxWidth, maxHeight = self.getMaxSize()
        halfMaxWidth = int(maxWidth / 2)
        halfMaxHeight = int(maxHeight / 2)

        for i in range(len(self._images)):
            # Maps out all the images into one big list...
            # This makes changes to the original images in self._images, not the transformed images in self._transformedImages
            newSurf = pygame.Surface((maxWidth, maxHeight))

            # set the expanded areas to be transparent
            newSurf = newSurf.convert_alpha()
            newSurf.fill((0,0,0,0))

            frameWidth, frameHeight = self._images[i].get_size()
            halfFrameWidth = int(frameWidth / 2)
            halfFrameHeight = int(frameHeight / 2)

            # position the Surface objects to the specified anchor point
            if anchorPoint == NORTHWEST:
                newSurf.blit(self._images[i], (0, 0))
            elif anchorPoint == NORTH:
                newSurf.blit(self._images[i], (halfMaxWidth - halfFrameWidth, 0))
            elif anchorPoint == NORTHEAST:
                newSurf.blit(self._images[i], (maxWidth - frameWidth, 0))
            elif anchorPoint == WEST:
                newSurf.blit(self._images[i], (0, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == CENTER:
                newSurf.blit(self._images[i], (halfMaxWidth - halfFrameWidth, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == EAST:
                newSurf.blit(self._images[i], (maxWidth - frameWidth, halfMaxHeight - halfFrameHeight))
            elif anchorPoint == SOUTHWEST:
                newSurf.blit(self._images[i], (0, maxHeight - frameHeight))
            elif anchorPoint == SOUTH:
                newSurf.blit(self._images[i], (halfMaxWidth - halfFrameWidth, maxHeight - frameHeight))
            elif anchorPoint == SOUTHEAST:
                newSurf.blit(self._images[i], (maxWidth - frameWidth, maxHeight - frameHeight))
            self._images[i] = newSurf


    def nextFrame(self, jump=1):
        '''Function for setting the next frame in the list'''
        self.currentFrameNum += int(jump)


    def prevFrame(self, jump=1):
        '''Function for setting the previous frame in the list'''
        self.currentFrameNum -= int(jump)


    def rewind(self, seconds=None):
        '''Rewinds the elapsed time, so that when standing, it doesnt look weird when you start moving again....'''
        if seconds is None:
            self.elapsed = 0.0
        else:
            self.elapsed -= seconds


    def fastForward(self, seconds=None):
        '''Sets the elapsed time forward, in order to be relative to the actual elapsed time'''
        if seconds is None:
            self.elapsed = self._startTimes[-1] - 0.00002 # done to compensate for rounding errors
        else:
            self.elapsed += seconds

    def _makeTransformedSurfacesIfNeeded(self):
        '''Internal-method. Creates the Surface objects for the _transformedImages list.'''
        if self._transformedImages == []:
            self._transformedImages = [surf.copy() for surf in self._images]


    '''These are all transformation methods, but instead they are applied to all of the frames in the object. Most of these can be found on the pygame.transform documentation.'''
    def flip(self, xbool, ybool):
        '''Allows me to flip images so I can use them interchangebly with direction'''
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = transform.flip(self.getFrame(i), xbool, ybool)


    def scale(self, width_height):
        '''Scales the images'''
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = pygame.transform.scale(self.getFrame(i), width_height)

    def rotate(self, angle):
        '''Rotates the image.'''
        self._makeTransformedSurfacesIfNeeded()
        for i in range(len(self._images)):
            self._transformedImages[i] = pygame.transform.rotate(self.getFrame(i), angle)

    ''' All of these methods are just getting information, and are only used internally in this class...'''
    def _propGetRate(self):
        ''' Gets how fast the prop or animation is playing '''
        return self._rate

    def _propSetRate(self, rate):
        '''Sets the rate the prop is animating at, if its less than 0 itll return an error!'''
        rate = float(rate)
        if rate < 0:
            raise ValueError('rate must be greater than 0.')
        self._rate = rate
    rate = property(_propGetRate, _propSetRate) #Sets the property

    def _propGetLoop(self):
        ''' Gets what stage its looping in'''
        return self._loop

    def _propSetLoop(self, loop):
        ''' Sets where the prop should be when the loop is stopped.'''
        if self.state == PLAYING and self._loop and not loop:
            self._playingStartTime = time.time() - self.elapsed
        self._loop = bool(loop)

    loop = property(_propGetLoop, _propSetLoop)

    def _propGetState(self):
        '''Gets the state: stopped, playing or paused'''
        if self.isFinished():
            self._state = STOPPED # if finished playing, then set state to STOPPED.

        return self._state

    def _propSetState(self, state):
        '''Sets the state!'''
        if state not in (PLAYING, PAUSED, STOPPED):
            raise ValueError('state must be one of pyganim.PLAYING, pyganim.PAUSED, or pyganim.STOPPED')
        if state == PLAYING:
            self.play()
        elif state == PAUSED:
            self.pause()
        elif state == STOPPED:
            self.stop()

    state = property(_propGetState, _propSetState)
    def _propGetVisibility(self):
        '''Gets the visibility'''
        return self._visibility

    def _propSetVisibility(self, visibility):
        '''Sets if the user should be able to see the animated object'''
        self._visibility = bool(visibility)

    visibility = property(_propGetVisibility, _propSetVisibility)


    def _propSetElapsed(self, elapsed):
        '''Sets the elapsed time to a specific value. '''
        elapsed += 0.00001 # done to compensate for rounding errors
        if self._loop:
            elapsed = elapsed % self._startTimes[-1]
        else:
            elapsed = getInBetweenValue(0, elapsed, self._startTimes[-1])

        rightNow = time.time()
        self._playingStartTime = rightNow - (elapsed * self.rate)

        if self.state in (PAUSED, STOPPED):
            self.state = PAUSED # if stopped, then set to paused
            self._pausedStartTime = rightNow


    def _propGetElapsed(self):
        '''Find out how long ago the play()/pause() functions were called.'''
        if self._state == STOPPED:
            # if stopped, then just return 0
            return 0

        if self._state == PLAYING:
            '''if playing, then draw the current frame (based on when the animation started playing).'''
            elapsed = (time.time() - self._playingStartTime) * self.rate
        elif self._state == PAUSED:
            # if paused, then draw the frame that was playing at the time the
            # PygAnimation object was paused
            elapsed = (self._pausedStartTime - self._playingStartTime) * self.rate
        if self._loop:
            elapsed = elapsed % self._startTimes[-1]
        else:
            elapsed = getInBetweenValue(0, elapsed, self._startTimes[-1])
        elapsed += 0.00001 # done to compensate for rounding errors
        return elapsed

    elapsed = property(_propGetElapsed, _propSetElapsed)


    def _propGetCurrentFrameNum(self):
        '''Return the frame number of the frame that will be currently displayed if the animation object were drawn right now.'''
        return findStartTime(self._startTimes, self.elapsed)


    def _propSetCurrentFrameNum(self, frameNum):
        '''Change the elapsed time to the beginning of a specific frame.'''
        if self.loop:
            frameNum = frameNum % len(self._images)
        else:
            frameNum = getInBetweenValue(0, frameNum, len(self._images)-1)
        self.elapsed = self._startTimes[frameNum]

    currentFrameNum = property(_propGetCurrentFrameNum, _propSetCurrentFrameNum)


'''This entire class is the updater for the one above. It has all of the exact SAME methods, so refer to the comments above if unsure about each of the defs here - they should be the same (as its just an updater)'''
class PygConductor(object):
    def __init__(self, *animations):
        self._animations = []
        self.add(*animations)

    def add(self, *animations):
        if type(animations[0]) == dict:
            for k in animations[0].keys():
                self._animations.append(animations[0][k])
        elif type(animations[0]) in (tuple, list):
            for i in range(len(animations[0])):
                self._animations.append(animations[0][i])
        else:
            for i in range(len(animations)):
                self._animations.append(animations[i])

    def _propGetAnimations(self):
        return self._animations

    def _propSetAnimations(self, val):
        self._animations = val

    animations = property(_propGetAnimations, _propSetAnimations)
    def play(self, startTime=None):
        if startTime is None:
            startTime = time.time()

        for animObj in self._animations:
            animObj.play(startTime)

    def pause(self, startTime=None):
        if startTime is None:
            startTime = time.time()

        for animObj in self._animations:
            animObj.pause(startTime)

    def stop(self):
        for animObj in self._animations:
            animObj.stop()

    def reverse(self):
        for animObj in self._animations:
            animObj.reverse()

    def clearTransforms(self):
        for animObj in self._animations:
            animObj.clearTransforms()

    def makeTransformsPermanent(self):
        for animObj in self._animations:
            animObj.makeTransformsPermanent()

    def togglePause(self):
        for animObj in self._animations:
            animObj.togglePause()

    def nextFrame(self, jump=1):
        for animObj in self._animations:
            animObj.nextFrame(jump)

    def prevFrame(self, jump=1):
        for animObj in self._animations:
            animObj.prevFrame(jump)

    def rewind(self, seconds=None):
        for animObj in self._animations:
            animObj.rewind(seconds)

    def fastForward(self, seconds=None):
        for animObj in self._animations:
            animObj.fastForward(seconds)

    def flip(self, xbool, ybool):
        for animObj in self._animations:
            animObj.flip(xbool, ybool)

    def scale(self, width_height):
        for animObj in self._animations:
            animObj.scale(width_height)

    def rotate(self, angle):
        for animObj in self._animations:
            animObj.rotate(angle)





def findStartTime(startTimes, target):
    '''Returns the index of the number in the startimes... '''
    assert startTimes[0] == 0
    lb = 0 # "lb" is lower bound
    ub = len(startTimes) - 1 # "ub" is upper bound

    # handle special cases:
    if len(startTimes) == 0:
        return 0
    if target >= startTimes[-1]:
        return ub - 1

    while True:
        i = int((ub - lb) / 2) + lb

        if startTimes[i] == target or (startTimes[i] < target and startTimes[i+1] > target):
            if i == len(startTimes):
                return i - 1
            else:
                return i

        if startTimes[i] < target:
            lb = i
        elif startTimes[i] > target:
            ub = i



#Defines the blank image that will be used on the main character when moving
blank = image.load('blank.png')
blank = transform.scale(blank,(40,70))
'''The main character class... '''
class Player(pygame.sprite.Sprite):
    '''Defines the initalized characterisitincs of the main player sprite...'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.animObjs = animObjs #Grabs the animation blits
        self.image = front_standing #Sets the image of the character
        self.rect = self.image.get_rect() #Gets the rect used for collision
        self.rect.x = 300 #Defines position
        self.rect.y = 200
        WALKRATE = 2 #Defines speed
        RUNRATE = 5
    ''' Updator for the class... '''
    def update(self):
        if moveUp or moveDown or moveLeft or moveRight:
            # draw the correct walking/running sprite from the animation object
            moveConductor.play() # calling play() while the animation objects are already playing is okay; in that case play() is a no-op
            if running:
                '''Essentially, when there is movement, set the actual image of the character to a blank one, and have an animation play in place of where the character is. I wasnt sure how to make the animation just one Pygame.surface
                so I did it this way... and it works really well!'''
                if direction == UP:
                    self.image = blank
                    self.animObjs['back_run'].blit(screen,(self.rect.x,self.rect.y))
                elif direction == DOWN:
                    self.image = blank
                    self.animObjs['front_run'].blit(screen,(self.rect.x,self.rect.y))
                elif direction == LEFT:
                    self.image = blank
                    self.animObjs['left_run'].blit(screen,(self.rect.x,self.rect.y))
                elif direction == RIGHT:
                    self.image = blank
                    self.animObjs['right_run'].blit(screen,(self.rect.x,self.rect.y))
            else:
                # walking
                if direction == UP:
                    self.image = blank
                    self.animObjs['back_walk'].blit(screen,(self.rect.x,self.rect.y))
                elif direction == DOWN:
                    self.image = blank
                    self.animObjs['front_walk'].blit(screen,(self.rect.x,self.rect.y))
                elif direction == LEFT:
                    self.image = blank
                    self.animObjs['left_walk'].blit(screen,(self.rect.x,self.rect.y))
                elif direction == RIGHT:
                    self.image = blank
                    self.animObjs['right_walk'].blit(screen,(self.rect.x,self.rect.y))
            # actually move the position of the player
            if running:
                rate = RUNRATE
            else:
                rate = WALKRATE
            if moveUp:
                self.rect.y -= rate
            if moveDown:
                self.rect.y += rate
            if moveLeft:
                self.rect.x -= rate
            if moveRight:
                self.rect.x += rate
        else:
            # standing still
            moveConductor.stop() # calling stop() while the animation objects are already stopped is okay; in that case stop() is a no-op
            if direction == UP:
                self.image = back_standing
            elif direction == DOWN:
                self.image = front_standing
            elif direction == LEFT:
                self.image = left_standing
            elif direction == RIGHT:
                self.image = right_standing
        # make sure the player does move off the screen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > width - playerWidth:
            self.rect.x = width - playerWidth
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > height - playerHeight:
            self.rect.y = height - playerHeight

#Defining the various constants that were used in the Player class
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
#Loads the standing images or 'stop' images (when the character is standing
front_standing = image.load('crono_front.gif')
back_standing = image.load('crono_back.gif')
left_standing = image.load('crono_left.gif')
right_standing = transform.flip(left_standing, True, False) #flips the image to get a right standing image
playerWidth, playerHeight = front_standing.get_size() #gets the max height and width, this is used to build the character below

# creating the PygAnimation objects for walking/running in all directions
animTypes = 'back_run back_walk front_run front_walk left_run left_walk'.split()
animObjs = {}
for animType in animTypes:
    imagesAndDurations = [('crono_%s.%s.gif' % (animType, str(num).rjust(3, '0')), 0.1) for num in range(6)]
    animObjs[animType] = PygAnimation(imagesAndDurations)

# create the right-facing sprites by copying and flipping the left-facing sprites
animObjs['right_walk'] = animObjs['left_walk'].getCopy()
animObjs['right_walk'].flip(True, False)
animObjs['right_walk'].makeTransformsPermanent()
animObjs['right_run'] = animObjs['left_run'].getCopy()
animObjs['right_run'].flip(True, False)
animObjs['right_run'].makeTransformsPermanent()
# have the animation objects managed by a conductor.
'''With the conductor, we can call play() and stop() on all the 
animtion objects at the same time, so that way they'll always be in sync with each other.'''

moveConductor = PygConductor(animObjs)

direction = DOWN # player starts off facing down (front)
WALKRATE = 2 #Defines the speed of the walkrate and running rateof the player
RUNRATE = 5
running = moveUp = moveDown = moveLeft = moveRight = False

'''Class for the enemy'''
#Load the image of the enemy
enemy1 = image.load('enemy1.png')
enemy1 = transform.scale(enemy1,(120,120))

'''The actual class of the mob - or enemy'''
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        '''Initiates the basic characteristics and properties of the mob enemies'''
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy1 #set image
        self.rect = self.image.get_rect() #Set the rect
        self.radius  = 20 #Change the collision to a circle with a radius of 20
        #pygame.draw.circle(self.image, BLUE, self.rect.center, self.radius) - Uncomment if you want to see the collision radius of the mobs
        self.rect.x = random.randrange(width - self.rect.width)#Sets coordinates for spawning, will always spawn above the screen in a random area
        self.rect.y = random.randrange(-100,-10)
        self.speedy = random.randrange(2,7)#Sets a random speed
        self.speedx = random.randrange(-2,7)

    def update(self):
        '''Updates the sprites'''
        #Adds the speed values for movement, then updates their position
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        #Respawning, if it goes over a certain threshold then respawn at the top of the screen again
        if self.rect.top > height + 15 or self.rect.left < -100 or self.rect.right > width + 100:
            self.rect.x = random.randrange(width - self.rect.width)
            self.rect.y = random.randrange(-100,-10)
            self.speedy = random.randrange(2,7)
            self.speedx = random.randrange(-2,7)


#Creates a list for all sprites, a list for all enemies, and the player class...
all_sprites = pygame.sprite.Group()
player = Player()
all_enemies = pygame.sprite.Group()
#Game is running there its true...
runningG = True
mainClock = pygame.time.Clock()

def getVal(tup):
    """ getVal returns the (position+1) of the first 1 within a tuple.
        This is used because MOUSEBUTTONDOWN and MOUSEMOTION deal with
        mouse events differently
    """
    for i in range(3):
        if tup[i]==1:
            return i+1
    return 0

def drawWaveScene():
    '''Draws the screen before the actual game. It shows the wave number...'''
    global wave
    for i in range(255):
        s = Surface((1300,750))
        s.fill((i,i,i))
        screen.blit(s, (0,0))
        s.set_alpha(90)
        display.update()
        pygame.time.wait(2)
    if wave == 1:
        screen.blit(waveText1,(390,250))
    if wave == 2:
        screen.blit(waveText2,(390,250))
    if wave == 3:
        screen.blit(waveText3,(390,250))
    if wave == 4:
        screen.blit(waveText4,(390,250))
    if wave == 5:
        screen.blit(waveText5,(390,250))
    display.update()
    pygame.time.wait(1500)


def mainMenuMouseActions(button,mx,my,start,instructions,quit,state):
    '''Defines the main menu mouse actions on the screen'''
    global running
    if state == 'Main Menu':
        if button == 1:
            if start.collidepoint(mx,my):
                state = 'Intermediate wave'
            if instructions.collidepoint(mx,my):
                state = 'Instructions'
            if quit.collidepoint(mx,my):
                pygame.quit()
    return state

def InstructionsMouseActions(button,mx,my,backInstructions,nextPage,state):
    '''Defines the instruction mouse actions'''
    if state == 'Instructions':
        if button == 1:
            if backInstructions.collidepoint(mx,my):
                state = 'Main Menu'
                button = 0
            if nextPage.collidepoint(mx,my):
                state = 'Instructions2'
                button = 0
    return state

def Instructions2MouseActions(button,mx,my,backInstructions,nextPage,previousPage,state):
    '''Defines the instruction mouse actions'''
    if state == 'Instructions2':
        if button == 1:
            if backInstructions.collidepoint(mx,my):
                state = 'Main Menu'
                button = 0
            if nextPage.collidepoint(mx,my):
                state = 'Instructions3'
                button = 0
            if previousPage.collidepoint(mx,my):
                state = 'Instructions'
                button = 0
    return state

def Instructions3MouseActions(button,mx,my,backInstructions,previousPage,state):
    '''Defines the instruction mouse actions'''
    if state == 'Instructions3':
        if button == 1:
            if backInstructions.collidepoint(mx,my):
                state = 'Main Menu'
                button = 0
            if previousPage.collidepoint(mx,my):
                state = 'Instructions2'
                button = 0
    return state

def waveTimer(startTicks):
    '''Defines the stopwatch that is displayed in the game. A new counter is created each wave, and then the inital time between the two are subtraced and divided to get it in seconds'''
    seconds = (pygame.time.get_ticks() - startTicks)/1000
    return seconds

#Intro
mixer.music.load(mainMusic)
mixer.music.play()
screen.blit(introText,(400,350))
screen.blit(logo,(390,150))
display.update()
pygame.time.wait(1700)
# Game Loop
while runningG:
    for evnt in event.get():             # checks all events that happen
        if evnt.type == QUIT:
            running = False
        if evnt.type == MOUSEBUTTONDOWN:
            mx, my = evnt.pos
            button = evnt.button
        if evnt.type == MOUSEMOTION:
            mx, my = evnt.pos
            button = getVal(evnt.buttons)
        elif evnt.type == KEYDOWN:
            if evnt.key in (K_LSHIFT, K_RSHIFT):
                # player has started running
                running = True
            if evnt.key == K_UP:
                moveUp = True
                moveDown = False
                if not moveLeft and not moveRight:
                    # only change the direction to up if the player wasn't moving left/right
                    direction = UP
            elif evnt.key == K_DOWN:
                moveDown = True
                moveUp = False
                if not moveLeft and not moveRight:
                    direction = DOWN
            elif evnt.key == K_LEFT:
                moveLeft = True
                moveRight = False
                if not moveUp and not moveDown:
                    direction = LEFT
            elif evnt.key == K_RIGHT:
                moveRight = True
                moveLeft = False
                if not moveUp and not moveDown:
                    direction = RIGHT

        elif evnt.type == KEYUP:
            if evnt.key in (K_LSHIFT, K_RSHIFT):
                # player has stopped running
                running = False
            if evnt.key == K_UP:
                moveUp = False
                # if the player was moving in a sideways direction before, change the direction the player is facing.
                if moveLeft:
                    direction = LEFT
                if moveRight:
                    direction = RIGHT
            elif evnt.key == K_DOWN:
                moveDown = False
                if moveLeft:
                    direction = LEFT
                if moveRight:
                    direction = RIGHT
            elif evnt.key == K_LEFT:
                moveLeft = False
                if moveUp:
                    direction = UP
                if moveDown:
                    direction = DOWN
            elif evnt.key == K_RIGHT:
                moveRight = False
                if moveUp:
                    direction = UP
                if moveDown:
                    direction = DOWN


    if state == 'Main Menu':
        wave = 1
        screen.blit(titleBackground,(0,0)) #Draws the menu!
        start = screen.blit(startText,Rect(250,120,400,100))
        instructions = screen.blit(instructionsText,Rect(250,270,400,100))
        quit = screen.blit(QuitGameText,Rect(250,420,400,100))
        state = mainMenuMouseActions(button,mx,my,start,instructions,quit,state)

    if state == 'Intermediate wave':
        draw.rect(screen,BLACK,(0,0,1024,576))
        if wave == 1:
            pygame.mixer.music.fadeout(3000) #Fade out the music, draw the wave scene, and then start the timer.
            drawWaveScene()
            startTicks = 0 #Defines the inital timer
            startTicks = pygame.time.get_ticks()
            mixer.music.load(gameMusic)
            mixer.music.play()
            all_sprites.empty() #Empties all possible sprites in the list so when going back in the game there isnt 20000 of them
            all_enemies.empty()
            for i in range(5): #Adds the enemies and player
                enemy = Mob()
                all_enemies.add(enemy)
                all_sprites.add(enemy)
            all_sprites.add(player)
            state = 'GameW1' #Sets the state
        elif wave == 2:
            drawWaveScene() #Defines the inital timer
            startTicks = 0
            startTicks = pygame.time.get_ticks()
            for i in range(2): #Adds more enemies to the game
                enemy = Mob()
                all_enemies.add(enemy)
                all_sprites.add(enemy)
            state = 'GameW2'
        elif wave == 3:
            drawWaveScene() #sets the timer, etc. (same as the last intermediate wave if statements)
            startTicks = 0
            startTicks = pygame.time.get_ticks()
            for i in range(2): #Adds more enemies to the game and the sprite list
                enemy = Mob()
                all_enemies.add(enemy)
                all_sprites.add(enemy)
            state = 'GameW3'
        elif wave == 4:
            drawWaveScene() #sets the timer, etc. (same as the last intermediate wave if statements)
            startTicks = 0
            startTicks = pygame.time.get_ticks()
            for i in range(2):
                enemy = Mob() #Adds more enemies to the game and the sprite list
                all_enemies.add(enemy)
                all_sprites.add(enemy)
            state = 'GameW4'
        elif wave == 5:
            drawWaveScene() #sets the timer, etc. (same as the last intermediate wave if statements)
            startTicks = 0
            startTicks = pygame.time.get_ticks()
            for i in range(3):
                enemy = Mob()
                all_enemies.add(enemy) #Adds more enemies to the game and the sprite list
                all_sprites.add(enemy)
            state = 'GameW5'

    if state == 'GameW1': #Wave 1
        screen.blit(gameBackground, (0,0)) #Draw everything that is required on screen
        all_sprites.update()
        all_sprites.draw(screen)

        death = pygame.sprite.spritecollide(player, all_enemies, False, pygame.sprite.collide_circle) #Defines the loss condition as colliding with a mob class
        if death:
            death = False
            state = 'Dead'

        #Defines the behavior for the clock
        seconds = waveTimer(startTicks)
        waveCountdown = EightBitText.render(str(seconds),1,(255,255,255))
        screen.blit(waveCountdown,(500,25))
        #print(seconds)
        if seconds > 60: #Defines how many seconds are in a wave, and goes to the next wave after it
            wave = 2
            state = 'Intermediate wave'

        if button == 3: #If button three is pressed, fade out the music, and go back to the main menu
            pygame.mixer.music.fadeout(1000)
            all_enemies.remove()
            for i in range(255):
                s = Surface((1300,750))
                s.fill((i,i,i))
                screen.blit(s, (0,0))
                s.set_alpha(90)
                display.update()
                pygame.time.wait(2)
            mixer.music.load(mainMusic)
            mixer.music.play()
            state = 'Main Menu'

    if state == 'GameW2': #Wave 2
        screen.blit(gameBackground, (0,0)) #Draws and updates everything required
        all_sprites.update()
        all_sprites.draw(screen)

        death = pygame.sprite.spritecollide(player, all_enemies, False, pygame.sprite.collide_circle) #Defines the loss condition as colliding with a mob class
        if death:
            death = False
            state = 'Dead'

        #Defines the behavior for the clock
        seconds = waveTimer(startTicks)
        waveCountdown = EightBitText.render(str(seconds),1,(255,255,255))
        screen.blit(waveCountdown,(500,25))
        #print(seconds)
        if seconds > 60: #Number of seconds in the wave
            wave = 3
            state = 'Intermediate wave'

        if button == 3: #If button three is pressed, fade out the music, and go back to the main menu
            pygame.mixer.music.fadeout(1000)
            all_enemies.remove()
            for i in range(255):
                s = Surface((1300,750))
                s.fill((i,i,i))
                screen.blit(s, (0,0))
                s.set_alpha(90)
                display.update()
                pygame.time.wait(2)
            mixer.music.load(mainMusic)
            mixer.music.play()
            state = 'Main Menu'

    if state == 'GameW3': #Wave 3
        screen.blit(gameBackground, (0,0)) #Draws and updates all sprites and the background
        all_sprites.update()
        all_sprites.draw(screen)

        death = pygame.sprite.spritecollide(player, all_enemies, False, pygame.sprite.collide_circle) #Condition for losing (collision with mob)
        if death:
            death = False
            state = 'Dead'

        #Defines the behavior for the clock
        seconds = waveTimer(startTicks)
        waveCountdown = EightBitText.render(str(seconds),1,(255,255,255))
        screen.blit(waveCountdown,(500,25))
        #print(seconds)
        if seconds > 60: #How long the wave lasts
            wave = 4
            state = 'Intermediate wave'

        if button == 3: #If button three is pressed, fade out the music, and go back to the main menu
            pygame.mixer.music.fadeout(1000)
            all_enemies.remove()
            for i in range(255):
                s = Surface((1300,750))
                s.fill((i,i,i))
                screen.blit(s, (0,0))
                s.set_alpha(90)
                display.update()
                pygame.time.wait(2)
            mixer.music.load(mainMusic)
            mixer.music.play()
            state = 'Main Menu'

    if state == 'GameW4': #Wave 4
        screen.blit(gameBackground, (0,0)) #Create and update every sprite and the background
        all_sprites.update()
        all_sprites.draw(screen)

        death = pygame.sprite.spritecollide(player, all_enemies, False, pygame.sprite.collide_circle) #Condition for losing (collision with mob)
        if death:
            death = False
            state = 'Dead'

        #Defines the behavior for the clock
        seconds = waveTimer(startTicks)
        waveCountdown = EightBitText.render(str(seconds),1,(255,255,255))
        screen.blit(waveCountdown,(500,25))
        #print(seconds)
        if seconds > 60:
            wave = 5
            state = 'Intermediate wave'

        if button == 3: #If button three is pressed, fade out the music, and go back to the main menu
            pygame.mixer.music.fadeout(1000)
            all_enemies.remove()
            for i in range(255):
                s = Surface((1300,750))
                s.fill((i,i,i))
                screen.blit(s, (0,0))
                s.set_alpha(90)
                display.update()
                pygame.time.wait(2)
            mixer.music.load(mainMusic)
            mixer.music.play()
            state = 'Main Menu'

    if state == 'GameW5':
        screen.blit(gameBackground, (0,0)) #Draws everything on screen
        all_sprites.update()
        all_sprites.draw(screen)

        death = pygame.sprite.spritecollide(player, all_enemies, False, pygame.sprite.collide_circle) #Condition for losing (collision)
        if death:
            death = False
            state = 'Dead'

        #Defines the behavior for the clock
        seconds = waveTimer(startTicks)
        waveCountdown = EightBitText.render(str(seconds),1,(255,255,255))
        screen.blit(waveCountdown,(500,25))
        #print(seconds)
        if seconds > 60: #Amount of time left in the wave, go to the win screen if the player survives
            state = 'Win'

        if button == 3: #If button three is pressed, fade out the music, and go back to the main menu
            pygame.mixer.music.fadeout(1000)
            all_enemies.remove()
            for i in range(255):
                s = Surface((1300,750))
                s.fill((i,i,i))
                screen.blit(s, (0,0))
                s.set_alpha(90)
                display.update()
                pygame.time.wait(2)
            mixer.music.load(mainMusic)
            mixer.music.play()
            state = 'Main Menu'

    if state == 'Win': #Draws the win screen with some music :)
        screen.blit(winBackground,(0,0))
        mixer.music.load(winMusic)
        mixer.music.play()
        display.update()
        pygame.time.wait(18000)
        mixer.music.load(mainMusic)
        mixer.music.play()
        state = 'Main Menu'

    if state == 'Dead': #Draws the win screen with some music :(
        screen.blit(diedBackground,(0,0))
        mixer.music.load(deadMusic)
        mixer.music.play()
        display.update()
        pygame.time.wait(7000)
        mixer.music.load(mainMusic)
        mixer.music.play()
        state = 'Main Menu'

    if state == 'Instructions': #Draws the 1st page of the instructions
        screen.blit(instructions1,(0,0))
        backInstructions = screen.blit(backText,Rect(390,500,50,50))
        nextPage = screen.blit(nextInstructionsText, Rect(790,500,50,50))
        state = InstructionsMouseActions(button,mx,my,backInstructions,nextPage,state)
        button = 0
    if state == 'Instructions2': #Draws the 2nd page of the instructions
        screen.blit(instructions2,(0,0))
        backInstructions2 = screen.blit(backText,Rect(390,500,50,50))
        nextPage2 = screen.blit(nextInstructionsText, Rect(790,500,50,50))
        previousPage2 = screen.blit(previousInstructionsText, Rect(40,500,50,50))
        state = Instructions2MouseActions(button,mx,my,backInstructions2,nextPage2,previousPage2,state)
        button = 0
    if state == 'Instructions3': #Draws the 3rd page of the instructions
        screen.blit(instructions3,(0,0))
        backInstructions3= screen.blit(backText,Rect(390,500,50,50))
        previousPage3 = screen.blit(previousInstructionsText, Rect(40,500,50,50))
        state =  Instructions3MouseActions(button,mx,my,backInstructions3,previousPage3,state)
        button = 0
    display.flip()
    mainClock.tick(60)                     # waits long enough to have 60 fps
