# Canvas LMS assignments to Microsoft To-Do tasks sync
Synchronizes assignments in canvas to a task list in Microsoft To-Do.

## Prerequisites:
1. API key and url for Canvas LMS
2. App registration in Azure AD. See https://github.com/inbalboa/pymstodo/blob/master/GET_KEY.md
3. A little patience and knowledge of APIs. This is a very early alpha and requires tinkering to get working for you.
    

Shout out to inbalboa who made the pymstodo module.

https://github.com/inbalboa/pymstodo

And the University of Central Florida for making the canvasapi module.

https://github.com/ucfopen/canvasapi


PS.
This was only tested on MS To-Do business version. You might be able to get it working on the consumer version by manually editing the app registration manifest to allow personal accounts (in Azure AD).