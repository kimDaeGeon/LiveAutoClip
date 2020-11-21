import requests
import json
import sys
import os

import numpy as np
import pandas as pd


# Twitch Request Class
class ChatRequest:
    chat_index = 0

    def __init__(self, client_id, video_id):
        self.client_id = client_id
        self.video_id = video_id
        self.chat_log = pd.DataFrame(columns=["Time", "User", "Chat"])

    def getRequest(self):
        chat_index = 0
        while True:
            if chat_index == 0:
                url = "https://api.twitch.tv/v5/videos/" + self.video_id + "/comments?content_offset_seconds=0"
                chat_index += 1
            else:
                url = "https://api.twitch.tv/v5/videos/" + self.video_id + "/comments?cursor="
                url += next_cursor

            params = dict({"client_id": self.client_id})
            response = requests.get(url=url, params=params)
            data = json.loads(response.text)

            # Make Series
            for idx in range(len(data["comments"])):
                Time = data["comments"][idx]["created_at"][11:19]
                User = data["comments"][idx]["commenter"]["display_name"]
                Chat = data["comments"][idx]["message"]["body"]
                
                # Append in DataFrame
                log = pd.Series({"Time":Time, "User":User, "Chat":Chat})
                self.chat_log = self.chat_log.append(log, ignore_index=True)

            if "_next" not in data.keys():
                break
            next_cursor = data["_next"]

    def saveChatLog(self, file_name="chat_log.csv"):
        # save as *.csv
        self.chat_log.to_csv(file_name, index=False, encoding="utf-8-sig")

        # save as *.txt
        with open(file_name, mode="w", encoding="utf-8-sig") as file_handler:
            chat_content = ""
            for idx, chat in enumerate(self.chat_log["Chat"]):
                chat_content += chat + '\n'
            file_handler.writelines(chat_content)


# Chat Analysis Class
class ChatAnalyze:
    def __init__(self, file_name="chat_log.csv"):
        if os.path.isfile(file_name):
            self.chat_log = pd.read_csv(file_name, encoding="utf-8-sig")
            
            self.file_handler = open(file_name[0:-3]+".txt", mode="r", encoding="utf-8").read
            self.chat_str = self.file_handler.readlines()
    
    def __del__(self):
        self.filehandler.close()



