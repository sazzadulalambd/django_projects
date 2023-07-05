from bardapi import Bard
import os
os.environ["_BARD_API_KEY"] = "XAiRHVlinXCObYxgloKra1HvID5shPCC1yc6UQQzxH-lRn_hes5yGobZFhjl1Q--AJgKYg."

message = input("Enter your prompt:")

print(Bard().get_answer(str(message)))