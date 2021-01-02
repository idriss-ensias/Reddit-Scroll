# Reddit-Scroll
# To use this app you need your reddit credentials (client_id, client_secret, user_agent, username, password) and add them to the "redo" function in models.py line 9
## 1. Go to https://www.reddit.com/prefs/apps for client_id and client_secret
## 2. user_agent is "weirdjango:v1.0.0 (by u/{{ your username }})" with {{ your username }} your reddit username
## 3. username and password are your reddit account username and password
  
  
  
A simple website i built that displays reddit images, videos and other media types on a 4 columns interface.  
You choose the subreddits from where to fetch the media content and you can "update" to fetch more content.  
You may encounter some bugs while using the website, as i'm not an experienced developper and this repository mainly serves as a proof of concept.  
I will submit a much better version using different front end frameworks and improved backend  
Many features in the website were added as i was working on it  
  
    
    
![alt text](https://github.com/idriss-ensias/Reddit-Scroll/blob/main/cleancurve.PNG)  
  
  
## Requirements
To start you need :  
### PRAW : interact with the reddit API
### BeautifulSoup : process html from PRAW submissions
### Django-Rest-Framework : I use rest for some features of the website  
This project also uses Native javascript, Bootstrap and django 
## Media 
You can like, delete, view details or enlarge a media element  
on the detai page you can go to the actual reddit post, you can also view comments (you can't see second or more level replies to comments)
## Home page
On the home page you have a 4 panel scrollable feed (when you reach the bottom of the page you can click on the "more" button to load more content)  
A simple algorithm is used to choose the elements to display, it takes into account only two factors number of elements and number of local likes for a subreddit  
Each element is displayed with like, details, enlarge , delete buttons on the right and redditor, Subreddit button on the left  
When you click on one of the buttons on the left, you are redirected to a new page displaying only the elements of the subreddit or redditor you clicked ordered by number of reddit upvotes (again when you reach the bottom of the page you can click on the "more" and load more content)  
## Subreddit page
The subreddit page shows all the subreddits registered and a form to add new subreddit to fetch content from  
## Redditors page
Same as Subreddit page  
## Update page
this the page where you fetch more content, there are two buttons  
an update all button to fetch content from all the registered subreddits and an update button to fetch content from the checked subreddits on the dropdown list  
## Search  
You can search content by title of each element  
## My objective is learning, so i would appreciate feedback at idriss.el.moussaouiti@gmail.com  
# Idriss El Moussaouiti





