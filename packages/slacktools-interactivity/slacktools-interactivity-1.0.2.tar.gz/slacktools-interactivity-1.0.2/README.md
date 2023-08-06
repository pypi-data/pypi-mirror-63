# slacktools-interactivity
A simple framework for working with Slack interactivity (https://api.slack.com/interactivity).
 
### Install

`pip install slacktools-interactivity`

## Commands
Register your `CommandHandler` class with the `ComandFactory` and when you receive a 
command request from Slack simply grab the command instance from the factory and execute it.

### Basic Usage

Define your command:
```python
from interactivity import CommandFactory, CommandHandler, CommandValidationError

from myproject import get_status, post_status


@CommandFactory.register("/status")
class StatusCommand(CommandHandler):
    def _validate(self):
        if not get_status(id=self.payload.text):
            raise CommandValidationError("Not a valid id.")
        
    def _execute(self):
        post_status(id=self.payload.text)

``` 

Handle the Slack command request:
```python
from rest_framework.views import APIView
from rest_framework.response import Response

from interactivity import CommandFactory

class CommandsView(APIView):
    def post(self, request):
        handler = CommandFactory.make_handler(request.data)
        handler.execute()
        return Response()
```

### Action Commands
Action commands allow you execute many different actions from a single Slack command. The text following
the command is used to determine which action should be performed. The text is split by spaces, the first character
set determines the action and the remain character sets are passed to the action as options/parameters.

#### Example
The below class definitions will handle the following command: `/status service api`
```python
from interactivity import (
    ActionCommandHandler, 
    CommandAction, 
    CommandValidationError,
    CommandFactory
)

from myproject import post_status_msg


class ServiceStatus(CommandAction):
    def validate(self):
        if len(self.options) == 0:
            CommandValidationError(self.payload, "Missing service name")
    
    def execute(self):
        post_status_msg(self.options[0])


@CommandFactory.register("/status")
class StatusCommand(ActionCommandHandler):
    ACTIONS = {
        "service": ServiceStatus
    }
```

## Views
To document

## Actions
To document
