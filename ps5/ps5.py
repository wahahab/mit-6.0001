# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

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

class NewsStory():
    def __init__(self, guid, title, description, link, pubdate):
        self._guid = guid
        self._title = title
        self._description = description
        self._link = link
        self._pubdate = pubdate
    def get_guid(self):
        return self._guid
    def get_title(self):
        return self._title
    def get_description(self):
        return self._description
    def get_link(self):
        return self._link
    def get_pubdate(self):
        return self._pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self._words = tuple(phrase.lower().split(' '))
    def evaluate_text(self, text):
        text = text.lower()
        # Replace all punctuation with space.
        for p in string.punctuation:
            text = text.replace(p, ' ')
        words = [w for w in text.split(' ') if w]
        for i, w in enumerate(words):
            if w == self._words[0]:
                return tuple(words[i: i + len(self._words)]) == self._words
        return False
# Problem 3

class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.evaluate_text(story.get_title())

# Problem 4

class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.evaluate_text(story.get_description())

# TIME TRIGGERS

# Problem 5
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self, time_string):
        self._time = datetime.strptime(time_string, '%d %b %Y %H:%M:%S')
        self._time = self._time.replace(tzinfo=pytz.UTC)

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        pubtime = story.get_pubdate()
        pubtime = pubtime.replace(tzinfo=pytz.UTC)
        return pubtime < self._time
        
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pubtime = story.get_pubdate()
        pubtime = pubtime.replace(tzinfo=pytz.UTC)
        return pubtime >= self._time

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self._trigger = trigger
    def evaluate(self, story):
        return not self._trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, left_trigger, right_trigger):
        self._left_trigger = left_trigger
        self._right_trigger = right_trigger
    def evaluate(self, story):
        return self._left_trigger.evaluate(story) \
            and self._right_trigger.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, left_trigger, right_trigger):
        self._left_trigger = left_trigger
        self._right_trigger = right_trigger
    def evaluate(self, story):
        return self._left_trigger.evaluate(story) \
            or self._right_trigger.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    return [s for s in stories
            if any([t.evaluate(s) for t in triggerlist])]



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
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    triggers = {}
    trigger_class_map = {
        'TITLE': TitleTrigger,        
        'DESCRIPTION': DescriptionTrigger,        
        'AFTER': AfterTrigger,
        'BEFORE': BeforeTrigger,
        'NOT': NotTrigger,
        'AND': AndTrigger,
        'OR': OrTrigger,
    }
    two_params_trigger = set([
        'AND', 'OR',    
    ])
    triggerlist = []
    def get_trigger(inputs):
        trigger_class = trigger_class_map[inputs[0]]
        if inputs[0] in two_params_trigger:
            return trigger_class(triggers[inputs[1]],
                triggers[inputs[2]])
        return trigger_class(inputs[1])

    for i, line in enumerate(lines):
        inputs = line.split(',')
        if inputs[0] == 'ADD':
            triggerlist.extend([triggers[n] for n in inputs[1:]])
            continue
        triggers[inputs[0]] = get_trigger(inputs[1:])
    return triggerlist


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        t5 = DescriptionTrigger("car")
        triggerlist = [t1, t4, t5]

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
        import traceback
        traceback.print_exc()
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

