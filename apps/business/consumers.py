"""  consumers for chat analysis """
import json
# import random
# from uuid import uuid4

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .utils import ChatPDFLangchain
# from .models import Chat, ChatMessage
# from apps.legalcases.models import Document
# from .models import Message, Room, ArquivoPDF

def deb(obj):
    print("#"*100)
    print(obj)
    print("#"*100)


class ChatPDFConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Inicialize chatbot class
        self.chatbot = ChatPDFLangchain()
        
        # Create docs from pdf in database
        docs = await self.chatbot.create_docs([await self.get_pdf()], self.scope['cookies']['sessionid'])
        # print(docs)
        
        # split docs int chunks
        chunks =  await self.chatbot.split_docs(docs)

        # embeddings
        embeddings = await self.chatbot.get_embeddings()

        # create vectorstore
        self.chat_db = await self.chatbot.get_vectorstore(chunks, embeddings)

        # create conversation chain
        self.chain = await self.chatbot.get_chain()

        #Join room
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()



    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    #Receive message from web socket
    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_message(self.scope['user'], message)
        response = await self.response_message(message)

        #Send message to room group
        await self.channel_layer.group_send(self.room_group_name,{'type':'chat_message','chatbot_response': response,'username':username})


    #Receive message from web socket
    async def chat_message(self, event):
        #Send message to Websockets
        await self.send(text_data=json.dumps({
            'type':'response',
            'message': event['chatbot_response'],
            'username': self.scope.get('user').__str__()
        }))
    
    async def response_message(self,message)-> str:
        print("---------------------------------------------->response", self.room_name, message)        
        relevant_docs = await self.chatbot.get_similar_docs(db=self.chat_db, query=message, k=1)
        response = await self.chatbot.get_answer(chain=self.chain,query=message, relevant_docs=relevant_docs)
        await self.save_message(sender=None, message=response)
        return response
    
    @sync_to_async
    def save_message(self,sender=None,message=""):
        print("---------------------------------------------->save_message", self.room_name, message)
        Message.objects.create(room=Room.objects.get(name=self.room_name), sender=sender,content=message)
        
    
    @sync_to_async
    def get_pdf(self):
        return ArquivoPDF.objects.get(title=self.room_name)



class CandidateAnalysisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.username = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'chat_%s' % self.chat_id

        # Inicialize chatbot class
        self.chatbot = ChatPDFLangchain()
        
        # Create docs from pdf in database
        #docs = await self.chatbot.create_docs([await self.get_pdf()], self.scope['cookies']['sessionid'])
        # print(docs)

        # split docs int chunks
        #chunks =  await self.chatbot.split_docs(docs)

        # embeddings
        #embeddings = await self.chatbot.get_embeddings()

        # create vectorstore
        #self.chat_db = await self.chatbot.get_vectorstore(chunks, embeddings)

        # create conversation chain
        #self.chain = await self.chatbot.get_chain()

        #Join room
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    #Receive message from web socket
    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']

        await self.save_message(self.scope['user'], message)
        response = await self.response_message(message)

        #Send message to room group
        await self.channel_layer.group_send(self.room_group_name,{'type':'chat_message','chatbot_response': response,'username':username})


    #Receive message from web socket
    async def chat_message(self, event):
        #Send message to Websockets
        await self.send(text_data=json.dumps({
            'type':'response',
            'message': event['chatbot_response'],
            'username': self.scope.get('user').__str__()
        }))
    
    async def response_message(self,message)-> str:
        #print("---------------------------------------------->response", self.chat_id, message)        
        #relevant_docs = await self.chatbot.get_similar_docs(db=self.chat_db, query=message, k=1)
        #response = await self.chatbot.get_answer(chain=self.chain,query=message, relevant_docs=relevant_docs)
        #await self.save_message(sender=None, message=response)
        # return response
        return ""
    
    @sync_to_async
    def save_message(self,sender=None,message=""):
        ...
    #     print("---------------------------------------------->save_message", self.chat_id, message)
    #     ChatMessage.objects.create(chat=self.chat, user=sender,content=message)
        
    
    @sync_to_async
    def get_pdf(self):
        ...
    #     self.chat = Chat.objects.get(id=self.chat_id)
    #     return Document.objects.get(id=self.chat.file.id)
