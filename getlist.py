"""Get a list of Messages from the user's mailbox.
"""
import base64
import email
from apiclient import errors

class GetList(object):
    def __init__(self):
        """This is to get the list """

        self.query = 'from:shreyabhargava12@gmail.com'
        self.mital_modha = 'from:mital.modha@hotmail.com'



    def ListMessagesMatchingQuery(self,service, user_id):
      """List all Messages of the user's mailbox matching the query.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

      Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
      """
      try:
        query = self.mital_modha
        response = service.users().messages().list(userId=user_id,q=query).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])

        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = service.users().messages().list(userId=user_id, q=query,
                                             pageToken=page_token).execute()
          messages.extend(response['messages'])

        return messages
      except errors.HttpError:
        print ('An error occurred')


    def ListMessagesWithLabels(self,service, user_id, label_ids=[]):
      """List all Messages of the user's mailbox with label_ids applied.

      Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.

      Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
      """
      try:
        response = service.users().messages().list(userId=user_id,
                                                   labelIds=label_ids).execute()
        messages = []
        if 'messages' in response:
          messages.extend(response['messages'])

        while 'nextPageToken' in response:
          page_token = response['nextPageToken']
          response = service.users().messages().list(userId=user_id,
                                                     labelIds=label_ids,
                                                     pageToken=page_token).execute()
          messages.extend(response['messages'])

        return messages
      except errors.HttpError:
        print('An error occurred:')

    def GetMessage(self, service, user_id, msg_id):
          """Get a Message with given ID.

          Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: The ID of the Message required.

          Returns:
            A Message.
          """
          try:
            message = service.users().messages().get(userId=user_id, id=msg_id).execute()

            # print 'Message snippet: %s' % message['snippet']

            return message
          except errors.HttpError:
            print ('An error occurred')
