# Welcome to random-facts python module !
A powerfull , flexible and modern python module to retrieve random useless facts from the mighty web , special thanks to [Joseph Paul](https://jsph.pl) for the api !
# Getting started
* Install the module with pip : `pip install random-facts`
* Import it : `import random-facts as r`
* You're set ! Consult the [docs](#api-docs) and get going
# Api docs
The docs <a href="#api-docs">section</a>

## 1- random_fact(format='json' , language='en')
### 1-1 Description
A function that generates a random useless fact
### 1-2 Params
`format` : __string__ : Can be one of **'html'** , **'md'** , **'txt'** or **'json'** . Default is **'json'**
`language` : __string__ : Can be one of **'de' (Dutch)** or **'en'** . Default is **'en'**
### 1-3 Returns
Returns an **object** similar to :
```py
{'status_code': 200, 'response': {'id': 'id of the fact , can be used in the get_fact() function to get its info', 'text': 'the fact itself', 'source': 'the source', 'source_url': 'the source url', 'language': 'its language', 'permalink': 'a link that lets you view the fact anytime anyplace'}}
```


## 2- daily_fact(format='json' , language='en')
### 2-1 Description
A function that gets today's fact , updated every 24 hours
### 2-2 Params
`format` : __string__  : Can be one of **'html'** , **'md'** , **'txt'** or **'json'** . Default is **'json'**
`language` : __string__  : Can be one of **'de' (Dutch)** or **'en'** . Default is **'en'**
### 2-3 Returns
Returns an **object** similar to :
```py
{'status_code': 200, 'response': {'id': 'id of the fact , can be used in the get_fact() function to get its info', 'text': 'the fact itself', 'source': 'the source', 'source_url': 'the source url', 'language': 'its language', 'permalink': 'a link that lets you view the fact anytime anyplace'}}
```

## 3- get_fact(id='json' , format='json')
### 3-1 Description
A function that gets a fact's info by its ID 
### 3-2 Params
`format` : __string__  : Can be one of **'html'** , **'md'** , **'txt'** or **'json'** . Default is **'json'**
`id` : __string__ : a 36 of length string containing both numbers and characters . You **must** provide it or an exception will be raised 
### 3-3 Returns
Returns an **object** similar to :
```py
{'status_code': 200, 'response': {'id': 'id of the fact , can be used in the get_fact() function to get its info', 'text': 'the fact itself', 'source': 'the source', 'source_url': 'the source url', 'language': 'its language', 'permalink': 'a link that lets you view the fact anytime anyplace'}}
```
# Support
Join my discord [server](https://discord.gg/9fhkSZH) for support
