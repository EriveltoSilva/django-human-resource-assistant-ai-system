"""  consumers for chat analysis """
import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .utils import CVAnalyzer
from .models import Vacancy, Candidate

def deb(obj):
    print("#"*100)
    print(obj)
    print("#"*100)

class CandidateAnalysisConsumer(AsyncWebsocketConsumer):
    """Consumer for chat analysis"""
    async def connect(self):
        """ AsyncWebsocketConsumer method to connect """
        self.vacancy_id = self.scope['url_route']['kwargs']['vid']
        self.num_docs = self.scope['url_route']['kwargs']['num_documents']
        self.username = "Anonymous"
        self.room_group_name = f'chat_{self.vacancy_id}'

        self.vacancy = await self.get_vacancy_instance()
        self.job_description = await self.get_job_description()

        # Inicialize chatbot class
        self.chatbot = CVAnalyzer()
        
        # Create docs from pdf in database
        docs = await self.chatbot.create_docs(await self.get_candidacies(), self.scope['cookies']['sessionid'])
        
        #Create embeddings instance
        embeddings = await self.chatbot.create_embeddings_load_data()

        #Create vectorstore
        self.vectorstore =  await self.chatbot.get_vectorstore(docs, embeddings)

        print("CONEXÃO ACEITA!")
        #Join room
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    #Receive message from web socket
    async def receive(self, text_data=None):
        data = json.loads(text_data)
        message = data['message']
        #Send message to room group
        await self.channel_layer.group_send(self.room_group_name,{'type':'chat_message','message': message})


    #Send message to chat group
    async def chat_message(self, event):
        if event['message'] == 'data':
            deb(f"received message {event['message']}")
            
            # Get the docs pdf
            relevant_docs = await self.chatbot.similar_docs(self.job_description, self.num_docs, self.vectorstore, self.scope['cookies']['sessionid'])
            response = await self.get_response_formatted(relevant_docs)
            deb(f"SENDING RESPONSE TO FRONT...")
            deb(response)
            await self.send(text_data=json.dumps({
                'type': 'response',
                'message': "Estes são os candidatos que melhor se adequam a vaga!",
                'data':response
            }))    

    # ************************************** My Custom methods  **********************************
    @sync_to_async
    def get_vacancy_instance(self):
        """ get vacancy instance that candidates applied """
        return Vacancy.objects.get(vid=self.vacancy_id)

    @sync_to_async
    def get_job_description(self) -> str:
        """ get all string text description """
        return self.vacancy.get_job_description()
    
    @sync_to_async
    def get_candidacies(self):
        """ get all candidacies"""
        candidates = Candidate.objects.filter(vacancy=self.vacancy)
        candidacy_list = [candidate for candidate in candidates]
        return candidacy_list
    
    async def get_response_formatted(self, relevant_docs):
        items = []
        for item in range(len(relevant_docs)):
            items.append({
                'header': f"👉 {str(item+1)}",
                'filename': str(relevant_docs[item][0].metadata['name']),
                'compatibility': f"{round(float(relevant_docs[item][1])*100, 2)}%",
                'summary': await self.chatbot.get_summary([relevant_docs[item][0]])
            })
        return items
