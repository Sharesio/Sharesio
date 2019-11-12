#!/usr/bin/env bash
echo 'Get authtoken from https://dashboard.ngrok.com/auth:'
read authtoken
ngrok authtoken $authtoken
ngrok http 5000
