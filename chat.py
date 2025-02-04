from ollama import AsyncClient

def generateMessage(messageData, defaultMessage):
    populatedMessage = defaultMessage.format(**messageData)
    return populatedMessage

def generateMessageBody(messageData, defaultMessage):
    
    message = generateMessage(messageData=messageData, defaultMessage=defaultMessage)
    request = [
        {
            'role': 'user',
            'content': 'formalize the following message in html format',
        },
        {
            'role': 'user',
            'content': message,
        }
    ]
    hostStr = str(messageData.get('host'))
    modelStr = str(messageData.get('model'))
    client = AsyncClient(
        host = hostStr
        )
    try:
       response = client.chat(model=modelStr, stream=False, messages=request)
       print(response.message.content)
       return response.message.content

    except Exception as exception:
       print(f'Error occurred while chatting with Ollama: {exception}')
       return message
