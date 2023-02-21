<div align="center">
 <h1>SteamAutoJoin</h1>
 <p>Python script that automatically joins Steam groups for you with cool/rare clan tags.</p>
</div>

<br/>

<p align="center">
 <a href="#about">About this project</a> •
 <a href="#configuration">How to configure</a> •
 <a href="#usage">How to use</a>
</p>

<br/>

## About
SAJ (SteamAutoJoin) is a Python script which logs into your Steam account and searches for groups with cool/rare clan tags. If found, SAJ will join them. Script is easy-to-use and configurable.

<br/>

## Configuration
- **username** - Account's username.
> Example: ```"anonymous"```
- **password** - Account's password.
> Example: ```"anonymous"```
- **start_id** - ID from which SAJ will start searching for groups.
> Default: ```1```
- **only_words** - If enabled, SAJ will join groups only when clan tag is in a [list containing 479 000 English words](https://github.com/dwyl/english-words).
> Default: ```"false"```. Set to ```"true"```, if you want to enable it.
