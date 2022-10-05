# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Jordan Gallivan

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    
    
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initializes a NewsStory Object
        a NewsStory Object has the following attributes:
            self.guid (string, globally unique identifier, determined by the input)
            self.title (string, title of the news story, determined by the input)
            self.description (string, description of the news story, determined by the input)
            self.link (string, link to the news story, determined by the input) 
            self.pubdate(datetime, publication date of news story, , determined by the input)
        '''
        
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        Assumes story is of class NewsStory (guid, title, description, link, pubdate)
        
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
        Initializes a PhraseTrigger Object
        a Phrase Trigger Object has the following attributes:
            self.story (string, inherited from Trigger)
            self.phrase (string, phrase to be compared)
        '''
        
        self.phrase=phrase
        
    def is_phrase_in(self, comparison):
        
        final_phrase=self.phrase.lower()
        comparison=comparison.lower() # make the comparison lower case
        final_phrase=final_phrase+' '     # add terminal ' '
         
        # removes all punctuation
        for i in string.punctuation:
        
            comparison=comparison.replace(i,' ')
        
        final_comp=' '.join(comparison.split()) # remove extra ' 's
        final_comp += ' '   # add terminal ' '
            
        if final_phrase not in final_comp:
            return False
        else:
            return True

# Problem 3
class TitleTrigger(PhraseTrigger):

    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())    

                      
# Problem 4
# TODO: DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    
    def evaluate(self,story):
        return self.is_phrase_in(story.get_description())



# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, str_time):
        '''
        initializes TimeTrigger with the following attributes:
            input: str_time (string, must be in EST and in the format of "%d %b %Y %H:%M:%S".)
            self.time (datetime, str_time converted to a datetime attribute)
        '''
        
        time = datetime.strptime(str_time, "%d %b %Y %H:%M:%S")
        

            # time = time.replace(tzinfo=pytz.timezone("EST"))

        
        self.time=time
         

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    
    def evaluate(self, story):
        
        try:
            condition= story.get_pubdate() < self.time
        except:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
            condition= story.get_pubdate() < self.time
            
        return condition
    
class AfterTrigger(TimeTrigger):
    
    def evaluate(self,story):
        try:
            condition= story.get_pubdate() > self.time
        except:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))
            condition= story.get_pubdate() > self.time
        
        return condition


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trig):
        self.trig=trig
    
    def evaluate(self, story):
        return not self.trig.evaluate(story)

# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1=trig1
        self.trig2=trig2
        
    def evaluate(self,story):
        condtrig1=self.trig1.evaluate(story)
        condtrig2=self.trig2.evaluate(story)
        
        if condtrig1 and condtrig2:
            return True
        else:
            return False 

# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trig1, trig2):
        self.trig1=trig1
        self.trig2=trig2
        
    def evaluate(self,story):
        condtrig1=self.trig1.evaluate(story)
        condtrig2=self.trig2.evaluate(story)
        
        if condtrig1 or condtrig2:
            return True
        else:
            return False 


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    
    filteredstories=[]
    
    for story in stories:
        for trig in triggerlist:
            if trig.evaluate(story):
                filteredstories.append(story)
    
    return filteredstories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []  #list where each element is the line data ignoring comments and blanks
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    # ['t1,TITLE,COVID', 't2,DESCRIPTION,Russia', 't3,DESCRIPTION,Supreme', 't4,AFTER,3 Oct 2016 17:00:10', 't5,AND,t2,t3', 't6,AND,t1,t4', 'ADD,t5,t6']

##########################################################################
    #make a trigger map and creat a trigger list based on classes above
    trig_dict={'TITLE': TitleTrigger,
               'DESCRIPTION': DescriptionTrigger,
               'AFTER': AfterTrigger,
               'BEFORE': BeforeTrigger,
               'NOT': NotTrigger,
               'AND': AndTrigger,
               'OR': OrTrigger}
                #dictionary of trigger types with their associated CLASS call
    
    triggers={}     #dictionary of the trigger numbers with their associated trigger Class call
                    #{t#:TriggerClass(phrase)}
    adds=[]         #list of the trigger numbers to be added to the call function
    
    for linedata in lines:  
        #linedata= one line of data in the following format 't#,TYPE,'PHRASE' or AND/OR/NOT Call or ADD
        datalist=linedata.split(',')    #list of items in each line [t# , TYPE, PHRASE]
        
        if 'ADD' not in linedata.upper():   #verify line isn't ADD
            #verify not an Add condition    
            if datalist[1].upper() != 'AND' and datalist[1].upper() != 'OR' and datalist[1].upper() != 'NOT':    
                #verify NOT AND OR are not in line (via datalist)

                triggers[datalist[0]] = trig_dict[datalist[1]](datalist[2])
            
            elif 'NOT' in linedata.upper():
                #NOT Case
                triggers[datalist[0]] = NotTrigger(triggers[datalist[2]])
            #   triggers key value t# = NotTrigger(   previous trigger  )
            else:
                #AND and OR Cases
                triggers[datalist[0]] = trig_dict[datalist[1]](triggers[datalist[2]], triggers[datalist[3]])
                #triggers key value t# = AND or OR Class call (      trigger 1      ,      trigger 2       )
        else:
            #the add condition trigger names
            for addtrig in datalist[1:]:
                adds.append(addtrig)

    output_trig=[]
    for i in adds:
        #add the triggers to a final output list
        output_trig.append(triggers[i])

    return output_trig
    


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("COVID")
        # t2 = DescriptionTrigger("Russia")
        # t3 = DescriptionTrigger("Ukraine")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

