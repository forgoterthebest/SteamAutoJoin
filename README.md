<div align="center">
 <h1>SteamAutoJoin</h1>
 <p>Python script that automatically joins Steam groups with cool/rare clan tags.</p>
</div>

## About
SAJ (SteamAutoJoin) is a Python script which logs into your Steam account and searches for groups with cool/rare clan tags. If found, SAJ will join them. Script is easy-to-use and configurable.

## Requirements
- [Google Chrome](https://www.google.com/chrome/)
- Python 3.x
- Python modules:

  ```
  art
  colorama
  requests
  selenium
  ```

## How to use?
1. Install Python modules using ```pip install -r requirements.txt``` or ```pip install art colorama requests selenium```.
2. Configure [config.json](./config.json).
3. Run ```main.py``` using ```python main.py```. If login details are correct, you should see the script doing its job without any problems.

## Configuration
Every option below is stored in ```config.json```.
- **username** - Account's username.
> Example: ```"anonymous"```
- **password** - Account's password.
> Example: ```"anonymous"```
- **start_id** - ID from which SAJ will start searching for groups.
> Default: ```1```
- **only_words** - If enabled, SAJ will join groups only when clan tag is in a [list containing ~479k English words](https://github.com/dwyl/english-words).
> Default: ```"false"```. Set to ```"true"```, if you want to enable it.
