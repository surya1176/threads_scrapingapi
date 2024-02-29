from metathreads import MetaThreads
from metathreads import config
import pandas as pd
import numpy as np
def main():
    # ?config.PROXY = {"http":"127.0.0.1","https":"127.0.0.1"}
    columns = ['postid', 'likestopost','post_text','politician_username', 'userid','commentid','comment','commentor_username','replies_to_comment','likes_to_comment']
    df = pd.DataFrame(columns=columns)
    config.TIMEOUT = 100
    threads = MetaThreads()
    username = None
    password = None
    if not all([username, password]):
        username = str(input("Enter Your Username or Email :"))
        password = str(input("Enter Your Password :"))
    threads.login(username, password)
    
   #  #print(myarray)
   #  myarray= []
    
   #  all_posts=[]
   #  post_cursor=None
    count=0
   #  while True : 
   #     post_res= threads.get_user_threads("potus",cursor=post_cursor)
   #     posts= post_res.get('data',[])
   #     if not posts : 
   #         break
   #     all_posts.extend(posts)
   #     post_cursor = post_res.get('cursor_endpoint')
   #     print(post_cursor)
   #     if not post_cursor:
   #      break
           
   #  for post in all_posts : 
   #     res= post['threads']
   #     for sub_post in res : 
   #        if 'thread_items' in sub_post and len(sub_post['thread_items']) > 0:
   #            post_info = sub_post['thread_items'][0].get("post", {})
   #            postid= post_info['pk']
   #            text_post_app_info = post_info.get('text_post_app_info', {})
   #            if text_post_app_info:
   #               post_preview_caption = text_post_app_info.get('post_preview_caption', '')
                 
   #            like_count = post_info.get('like_count', 0)
   #            myarray.append({'postid' : postid, 'likestopost': like_count , 'post_text':post_preview_caption })

 
   
   #  np.save('temp.npy', np.array(myarray))
   #  print(len(myarray))
    myarray = np.load('temp.npy',allow_pickle=True)
    cursor = None
    for item in myarray :
     count+=1
     print("hi") 
     likes= item['likestopost']
     id=item['postid']
     post_text=item['post_text']
     all_comments = []
     #print(threads.get_thread(id))
     while True:
      response = threads.get_thread_replies(id, cursor=cursor)
      #print(response.keys())
      comments = response.get('data', [])
      if not comments:
         break
    
      all_comments.extend(comments)
      #print(len(all_comments))
      #print(response.get('has_next_page'))
      cursor = response.get('cursor_endpoint')
      print(cursor)
      if not cursor:
         break
    

     print(f"Total Comments: {len(all_comments[0]['reply_threads'])}")
     for comment in all_comments: 
        
         res= comment['reply_threads']
         for subcomment in res: 
          if 'thread_items' in subcomment and len(subcomment['thread_items']) > 0:
             post_info = subcomment['thread_items'][0].get("post", {})
    
             text_post_app_info = post_info.get('text_post_app_info', {})
          if text_post_app_info:
            post_preview_caption = text_post_app_info.get('post_preview_caption', '')
            reply_to_author = text_post_app_info.get('reply_to_author', {})
            direct_reply_count = text_post_app_info.get('direct_reply_count', 0)
         
            caption = post_info.get('caption')
            if caption:
             user_info = caption.get('user', {})
             commentor_username = user_info.get('username', '')
            
             like_count = post_info.get('like_count', 0)
            
            # Now you have all the required values
             new_data = {
                'postid': id,
                'politician_username': reply_to_author.get('username', ''),
                'post_text' : post_text,
                'userid': reply_to_author.get('pk', ''),
                'commentid': post_info.get('pk', ''),
                'comment': post_preview_caption,
                'commentor_username': commentor_username,
                'replies_to_comment': direct_reply_count,
                'likestopost' : likes,
                'likes_to_comment': like_count
             }
          print(count)  
          df = df.append(new_data, ignore_index=True)
             
       


          
           
    print(len(df))      
    file_path = './metathreads/data.csv'
    

    df.to_csv(file_path, index=False)
   #  res=  threads.get_thread_replies("https://www.threads.net/@potus/post/C1VRCZgrTq_")
   #  print(res.keys())
   #  print(len(res['data'][0]['reply_threads']))
    
   #  print(threads.get_thread("https://www.threads.net/@potus/post/C1VRB7bLJRi")['reply_threads'][2]['thread_items'][0].keys())
   #  threads.get_thread("thread_id or thread_url")
    """
    Here is an example
    thread_url > https://www.threads.net/t/CuP48CiS5sx
    thread_id > 3138977881796614961

    It works with both id and url.
    thread.get_thread(3138977881796614961)
    

    YOU CAN ALSO THROW IN MULTIPLE INPUTS AT A SINGLE TIME (WORKS WITH EVERY METHOD i.e. liking, posting, deleting , extracting data - all functions), IT SUPPORTS ASYNC/AWAIT (CONCURRENT REQUESTS.)
    Just make sure you don't hit the API rate limits.

    So getting multiple threads is as easy as passing a list.

    threads.get_thread([3138977881796614961,3140525365550562013])
    """

    # # like a thread
    # threads.like_thread(3138977881796614961)

    # # repost a thread
    # threads.repost_thread([3138977881796614961, 3140525365550562013])

    # # post a thread
    # threads.post_thread(thread_caption="My First Thread..")

    # CHECK DOCUMENTATION FOR FULL FUNCTIONALITY.


if __name__ == "__main__":
    main()
