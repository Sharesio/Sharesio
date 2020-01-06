#!/usr/bin/env bash

curl -X POST -H "Content-Type: application/json" -d '{
    "get_started": {
        "payload": "POSTBACK_CREATE_ACCOUNT"
    },
    "greeting": [
        {
            "locale": "default",
            "text": "Hello {{user_first_name}}, welcome to Sharesio!"
        }
    ],
    "persistent_menu": [
      {
        "locale": "default",
        "composer_input_disabled": false,
        "call_to_actions": [
          {
            "type": "postback",
            "title": "Delete account",
            "payload": "POSTBACK_DELETE_ACCOUNT"
          }
        ]
      }
    ]
}' "https://graph.facebook.com/v5.0/me/messenger_profile?access_token=$1"
