# Usage

## Getting a Token

Cena supports long-live api tokens in the user frontend. See [user settings page](../users-groups/user-settings.md)


## Key Components

### Exploring Your Local API
On your local installation you can access interactive API documentation that provides `curl` examples and expected results. This allows you to easily test and interact with your API to identify places to include your own functionality. You can visit the documentation at `http://cena.yourdomain.com/docs` or see the example at the [Demo Site](https://cena-demo.aindoria.dev/docs)

### Recipe Extras
Recipes extras are a key feature of the Cena API. They allow you to create custom json key/value pairs within a recipe to reference from 3rd part applications. You can use these keys to contain information to trigger automation or custom messages to relay to your desired device. 

For example you could add `{"message": "Remember to thaw the chicken"}` to a recipe and use the webhooks built into cena to send that message payload to a destination to be processed.

