from apiclient import errors
import json
# ...

def getFirstMessage(service, user):
  try:
    response = service.users().messages().list(userId=user).execute()
    messageID = response['messages'][0]["id"]
    message = service.users().messages().get(userId=user, id=messageID).execute()
    return json.dumps(message)

  except errors.HttpError, error:
    print 'An error occurred: %s' % error
    if error.resp.status == 401:
      # Credentials have been revoked.
      # TODO: Redirect the user to the authorization URL.
      raise NotImplementedError()