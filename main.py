import re
import praw
from urllib.parse import quote
import time
from codecs import unicode_escape_decode
import os, sys
from dotenv import load_dotenv

# sys.stdout = open('out.log', 'w')
# sys.stderr = sys.stdout

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir,'.env'))

user_agent=os.environ.get('PRAW_USER_AGENT')
client_id=os.environ.get('PRAW_CLIENT_ID')
client_secret=os.environ.get('PRAW_CLIENT_SECRET')
username=os.environ.get('PRAW_USERNAME')
password=os.environ.get('PRAW_PASSWORD')
url=os.environ.get('URL')
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
    for comment in subreddit.stream.comments():
        print(comment.body)
        if hasattr(comment,"body"):
            replied=False
            comment.refresh()
            for reply in comment.replies:
                if hasattr(reply,"author"):
                    print(reply.author)
                    if reply.author == username:
                        break
            else:
                print("hi", comment.body)
                if (hasattr(comment,"author")):
                    print("hi")
                    if (comment.author != username):
                        process_comment(comment)

def process_comment(comment):
    print("#"+comment.body)
    found = re.findall(re.compile(r"\$\$.*?\$\$"),comment.body)
    if found:
        for i in range(len(found)):
            found[i] = quote(found[i].replace('\\\\', '\\'), safe='/')
        l=[f"[{i}](http://{url}/mathjax/{s})" for i, s in enumerate(found, 1)]
        s="I've rendered your latex: "+' '.join(l)
        comment.reply(s)
        print(comment.author)
        print(comment.body)
        print(s)
        print("###################", flush=True)
        time.sleep(120)
        

if __name__ == "__main__":
    main()