# Telegram Crawler
Application crawls channels in user telegram chat. It iterates over messages inside channel and find possible invitation link to other channels.
## Setup
First of all user should get api_id and api_hash from his telegram account. User should login using [this telegram website](https://my.telegram.org/auth). After that click on API Development tools and after register new tool if its not registered yet. Api_id and api_hash should be inserted into correspondind field in config.json file.

User can run program using make command. Pipvenv is required for makefile. Using ```make setup``` user is able to install dependencies. Next virtual env. should be created using ```make run_venv``` and after that ```make run_py``` runs application. User is able to uninstall dependecies using ```make clean```,  update dependecies using ```make update``` and delete virtual env. using ```make delete``` command. 

## First Initialization
In case of two factor authorization user will be required to enter mobile number to ensure his autentity. 
</br>![running](https://user-images.githubusercontent.com/66804919/175908792-5d8d2f19-ca96-4442-9aba-e889a6caca1a.gif)</br>
After that new session for user will be created and first initial crawling will be started. Aplication will crawl user's groups and gather invitation links. The cache file called ```crawlerCache``` will be created automatically after first initialization. ```crawlerCache``` contains all crowled groups, so application is not required to crawl each time user run application after first initialization. It can takes up to 5 min from my experience to crawl initial groups. User can choose from 4 given options after initialization finished. All founded groups will be printed in list above options. 
</br>![firstcrawling](https://user-images.githubusercontent.com/66804919/175912425-04226705-680d-4e64-b4fe-9d0e08371564.gif)</br>
## Application Commands
Oprions are:
- Crawl - execute new crawl on founded groups/channels
- List information - list information about crawled groups/channels and some meta information including (id, name, to_process_count, edges_count, parent_group)
- Join one group - User will join one group. Telegram limits requests to join to channel approximately up to 25 for one hour.
- Exit - quit application and diskoccent from current session
</br>To execute corresponding command user should enter number (1,2,3 or 4) to command promt.
</br>**Notes: user can be banned for some time (up to 5 mins) due flooding, that's why joining groups and crawling should be not overused**
