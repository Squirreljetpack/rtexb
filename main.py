import re
import praw
from urllib.parse import quote
import time
from codecs import unicode_escape_decode
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

user_agent=os.environ.get('PRAW_USER_AGENT'),
client_id=os.environ.get('PRAW_CLIENT_ID'),
client_secret=os.environ.get('PRAW_CLIENT_SECRET'),
username=os.environ.get('PRAW_USERNAME'),
password=os.environ.get('PRAW_PASSWORD'),
url=os.environ.get('URL'),
subreddits=os.environ.get('PRAW_SUBREDDITS')


def main():
    reddit = praw.Reddit(
        user_agent=user_agent,
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
    )

    subreddit = reddit.subreddit(subreddits)
    for submission in subreddit.stream.submissions():
        for comment in submission.comments:
            if hasattr(comment,"body"):
                process_comment(comment)


def process_comment(comment):
    if hasattr(reply,"author"):
        if reply.author == username:
            return
    found = re.findall(re.compile(r"\$\$.*?\$\$"),comment.body)
    if found:
        for i in range(len(found)):
            found[i] = quote(found[i].replace('\\', ''), safe='/')
        l=[f"[{i}](http://{url}/mathjax/{s})" for i, s in enumerate(found, 1)]
        s="I've rendered your latex: "+' '.join(l)
        comment.reply(s)
        time.sleep(60)
    for reply in comment.replies:
        process_comment(reply)
        
        

if __name__ == "__main__":
    main()