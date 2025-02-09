import json, os
from openai import OpenAI


class Character():

    def __init__(self, *args, **kwargs):

        self.name = kwargs.get("name", None)

        if self.name:
            self.retrieve_saved_character()
        
        self.load_character(**kwargs) #override any fields 
    
    def load_character(self, *args, **kwargs):

        self.name = kwargs.get("name", getattr(self, "name", ""))
        self.full_name = kwargs.get("full_name", getattr(self, "full_name", ""))
        self.backstory = kwargs.get("backstory", getattr(self, "backstory", ""))
        self.nickname = kwargs.get("nickname", getattr(self, "nickname", ""))
        self.conversation = kwargs.get("conversation", getattr(self, "conversation", self.starter_prompt))

    def save(self):
        
        with open(f"characters/profiles/{self.name}.json", "w") as outfile:

            outobj = dict(
                name = self.name,
                backstory = self.backstory,
                full_name = self.full_name,
                conversation=self.conversation
            )

            outfile.write(json.dumps(outobj, indent=4))

    def retrieve_saved_character(self):

        if not self.name:
            return None
        
        try:
            profile = json.loads(open(f"characters/profiles/{self.name}.json", "r").read())
        except FileNotFoundError:
            profile = dict()
        
        self.load_character(**profile)
    
    @property
    def system_prompt(self):

        return f"""You are an actor playing character in a murder mystery. 
        You embody your character.
        Keep your conversation short and natural. 
        Only respond with what you say. Do not describe your movements. 
        Give the user space to keep asking you questions.
        This is the first round, and the user will be meeting you and all the other characters. 
        You may share anything from your backstory. 
        
        Your Backstory:
        Your name is {self.full_name}. {self.backstory}
        """
    
    @property
    def starter_prompt(self):
        return [dict(
            role="system",
            content=self.system_prompt
        )]
    
    def chat(self, message):

        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )

        self.conversation.append(dict(
            role="user",
            content=message
        ))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.conversation
        ).choices[0].message.content

        self.conversation.append(dict(
            role="assistant",
            content=response
        ))

        self.save()

        return response
    
    def clear_convo(self):
        delattr(self, "conversation")
        self.save()