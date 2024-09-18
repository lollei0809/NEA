import json

questions = {"convert 00001001 to denery": 9,
             "convert 12 to binary": 1100}
json.dumps(questions)#converts to json formatting eg True=true.
# converting back to python might give wrong dta type as both int and float are json numbers
with open ("json_question_prototype.json", mode="w", encoding="utf-8") as file:
    json.dump(questions,file)