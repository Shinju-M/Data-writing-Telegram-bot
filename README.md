  <h3 align="center">Data-writing-Telegram-bot</h3>

  <p align="center">
    Telegram bot that stores the chat log in a MySQL database
  </p>


<!-- ABOUT THE PROJECT -->
## About The Project

The project contains the code for the Telegram bot that stores the curator chat log in a MySQL database and performs several operations on data such as counting messages that vere not replyed, calculation of the general average reply time and average reply time for each curator.


### Files
 The project contains several files:
<br>
1. Bot.py contains the code that performs Telegram polling;
2. handlers.py contains message handlers;
3. filters.py contains filters filters for message handlers;
4. db.py is resposible for connection to MySql and also contains functions for database and tables creation and data selsction.
</br>



<!-- USAGE EXAMPLES -->
## Usage
<br>
In order to start the Bot you firs need to insert your bot token to the code in Bot.py file:

![изображение](https://user-images.githubusercontent.com/120586885/232023683-df691cde-6002-42ad-ae89-d5c48de3b7b0.png)

After running the bot you need to insert the hostname of your MySQL, username and password for your MySQL host.
 </br>
 <br>
After that you can add your bot in a Telegram chat and start it by "/start" command. By this command the bot automatcally creates a database for the chat that contains tables "Members", "Messages" and "Replies". Bot can be added to several chats, in this case different log for each chat will be written.
Table "Members" contains user id of each active member of the chat and the status of each member (whether member is curator or not). Every member of the chat except the member who used the "/start" command initially is treated as a student. In order to change the status to curator the member that wants to change status needs to use the command "/curator" in the chat.
</br>
 <br>
After the "/start" bot will store every message from any student in "Messages" table and every reply in "Replys" table (commands and messages from bot will not be stored in the log).
### Commands
You can use the following commands in order to get information performed on the chat database directly from the bot:
<br>
1. /reply_stats - sends the information on the number of messages that were and were not replied;
![изображение](https://user-images.githubusercontent.com/120586885/232029686-a1cf3934-adca-4ece-a55f-9d97c119b0e7.png)
2. /non_replied - sends the texts of messages that were not replied;
<br>![изображение](https://user-images.githubusercontent.com/120586885/232030408-bc5cb4b1-55f3-4d8d-b05a-9fee7983eb16.png)</br>
3. /time - shows an average reply time for all of the chat curators;
![изображение](https://user-images.githubusercontent.com/120586885/232031454-c5a918e0-3690-4e79-acfa-dce7ef1a7540.png)
4. /time_curator - sends an average reply time for each chat curator.
![изображение](https://user-images.githubusercontent.com/120586885/232031814-05e5a271-8e51-40a0-8a7d-5e3c3b29be1b.png)


</br>
