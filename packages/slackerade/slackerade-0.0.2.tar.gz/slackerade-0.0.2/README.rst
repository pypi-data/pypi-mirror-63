slackerade
==========

Masquerade yourself as fictitious user on slack

Usage
-----

::

    ./slackerade.py https://hooks.slack.com/services/CHANNEL/URL/HASH
    USERNAME MSG EMOJI_NAME
    
Note: to have access to the channel *Webhook Url* you must first activate slack *Incoming Webhook* feature as explained `here <https://api.slack.com/messaging/webhooks#posting_with_webhooks>`_.

Example
-------

``./slackerade.py https://hooks.slack.com/services/<censured> "The Joker"  "That's the joke" ":thats_the_joke:"``

gives :

.. figure:: https://github.com/Kraymer/public/raw/master/slackerade/slackerade_demo.png
   :alt:
