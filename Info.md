## Custom Component
In Rasa the filestructure is very important to make any changes in it  default config or add something new. That's why it is very important to checkout the virtual environment's lib where the "rasa/" module is saved. Checkout the below article to get an idea of the structure:

https://towardsdatascience.com/multi-lingual-chatbot-using-rasa-and-custom-tokenizer-7aeb2346e36b

checkout "everything" in "rasa/" directory which will make it easier for the developer to build the bot.
#### Add Custom Component to default component file
Add the custom component to default_components.py file in dir "rasa/engine/recipes" or search with the keyword "default" in "rasa/" dir, you will get default_components.py file.


## CommandLine Interface
Using an UI is important for checking the chatbot converation as the terminal or commandline doesn't support bangla font correctly. No fix has been found or not likely to be found.