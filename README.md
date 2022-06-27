# Telegram Crawler
Application crawls channels in user telegram chat. It iterates over messages inside channel and find possible invitation link to other channels.
## setup
First of all user should get api_id and api_hash from his telegram account. User should login using [this telegram website](https://my.telegram.org/auth). After that click on API Development tools and after register new tool if its not registered yet. Api_id and api_hash should be inserted into correspondind field in config.json file.

User can run program using make command. Pipvenv is required for makefile. Using ```make setup``` user is able to install dependencies. Next virtual should be created using ```make run_venv``` and after that ```make run_py``` runs application. dependecies using ```make update``` and delete virtual env. using ```make delete``` command. 

In case of two factor authorization user will be required to enter mobile number to ensure his autentity. 
![running](https://user-images.githubusercontent.com/66804919/175908792-5d8d2f19-ca96-4442-9aba-e889a6caca1a.gif)
After that new session for user will be created. 
