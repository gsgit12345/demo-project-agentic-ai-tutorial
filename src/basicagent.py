import os

class BasicAgent:

    def percept(self,percept):
        if percept=="obstacle":

            return "turn right"
        else:

            return "turn left"


agent=BasicAgent()

data=agent.percept('obstacle')

print(data)

print(os.getcwd())