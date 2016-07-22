# ImitationBot

A HipChat bot that will imitate anyone! Powered by [markovify](https://github.com/jsvine/markovify).

## Requirements

* [HipChat](https://hipchat.com), obviously.
* A HipChat room with a sufficient history to make some great messages.
* A free [Heroku](https://www.heroku.com) account
* A [user token](https://www.hipchat.com/account/api). Best just to make it have all rights.
* If you want the ImitationBot to send from a seperate account, you'll need a Room Token.
* A MongoDB instance (easily provisioned from Heroku)
* A Redis instance (also easily provisioned from Heroku)

## Installation

1. Set up a HipChat outgoing web hook at https://www.hipchat.com/docs/apiv2/method/create_webhook. Make sure to pick a trigger word, such as `/imitate`. 

2. Clone this repo, set up a Heroku app with Redis and Mongo, and deploy ImitationBot there. Make sure to set up the config variables in your Heroku app's settings screen.

## Config Variables

* `ROOM_ID`: The hipchat room where this is going to be deployed.
* `USER_KEY`: The user token you setup for yourself
* `IMITATIONBOT_KEY`: The room token to send ImitationBot from
* `MONGODB_URI`: The MongoDB URI for the database you are using
* `REDIS_URL`: Your redis instance

## Usage

*Note, I'm assuming your webhook is `/imitate`*
* The first time your run ImitationBot, type `/imitate update` to build the corpus of messages
* Then, its just `/imitate @user` to run
* Anytime you want to update the corpus, just send `/imitate corpus`
* This code might not work... I've not written tests, and I've only run it on one HipChat server so far.

MIT License

Copyright (c) 2016 James Judd

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.