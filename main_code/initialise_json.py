import json

details = {
    "jane123": {"name": "Jane Doe",
                "hashed_password": b'$2b$12$Rg1AfE9GqoGU5fs6biZmf.IWf188pRLVFr40tKqGXwIJzTrIoM1GW'.decode("utf-8"),
                # asdf
                "signed_in": False,
                "question_queue":[],
                "unsigned binary to decimal": {"correct": [12,9,10,2], "incorrect": [12,5,12,13]},
                "decimal to unsigned binary": {"correct": [1], "incorrect": [9]},
                "sign and magnitude binary to decimal": {"correct": [7], "incorrect": [6]},
                "decimal to sign and magnitude binary": {"correct": [0], "incorrect": [0]},
                "hexadecimal to decimal": {"correct": [0], "incorrect": [0]},
                "decimal to hexadecimal": {"correct": [0], "incorrect": [0]}
                },
    "lolly123": {"name": "Lolly Leitch",
                 "hashed_password": b'$2b$12$BBOVggTcLnHxeX.oesD64.Dxy/iDlS1esifdv.sHlUtYkq3Gi3j/m'.decode("utf-8"),
                 # qwerty
                 "signed_in": False,
                 "question_queue":[],
                 "unsigned binary to decimal": {"correct": [7,7], "incorrect": [3,5]},
                 "decimal to unsigned binary": {"correct": [0], "incorrect": [0]},
                 "sign and magnitude binary to decimal": {"correct": [0], "incorrect": [0]},
                 "decimal to sign and magnitude binary": {"correct": [0], "incorrect": [0]},
                 "hexadecimal to decimal": {"correct": [0], "incorrect": [0]},
                 "decimal to hexadecimal": {"correct": [0], "incorrect": [0]}
                 }
}
# #json doesnt allow inline comments or trailing commas
# #needs strings not bytes data type
with open("details.json", mode="w", encoding="utf-8") as write_file:
    json.dump(details, write_file, indent=4)
