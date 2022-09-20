from email import message
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#         await self.channel_layer.group_send(
#              self.room_group_name,
#              {
#                 'type':'tester_message',
#                 'tester':'haii Akkiii'
#              }
#         )

#     async def tester_message(self, event):
#         tester =event['tester']

#         await self.send(text_data=json.dumps({
#             'tester':tester,
#         }))


#     async def disconnect(self, close_code):
#      await self.channel_layer.group_discard(
#         self.room_group_name,
#         self.channel_name

#      )  

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']    

#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type':'chat_message',
#                 'message':message,
#             }
#         )  

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_group_name = 'test'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()


        # self.send(text_data=json.dumps({
        # 'type':'connection_established',
        # 'message':'You are connected'
        #   }))


    def receive(self,text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':'chat_message',
                'message':message
            }
        )

        # print('Message:',message)

        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message':message
        # }))
           
       
    def chat_message(self,event):
        message = event['message']

        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message    
        }))       
       
    
      


