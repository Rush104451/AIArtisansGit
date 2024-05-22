import os
import time
import json
from openai import AzureOpenAI
import sys
from pathlib import Path

# Get the path to the cloned repository from command-line arguments
repo_paths = sys.argv[1]


def check(inp):
    client = AzureOpenAI(
        azure_endpoint="https://ai-artisans-inst.openai.azure.com/", 
        api_key="50191a226a76405288d363378c927895",  
        api_version="2024-02-15-preview"
    )

    message_text = [{"role":"system","content":"You are a technical architect who has the knowledge and expertise in coding according to coding standards. You will receive many codes from now and you have to check if the standards are followed or not. Here is the code:\n" + inp}]
    try:
        completion = client.chat.completions.create(
            model="gpt-4-32k",
            messages=message_text,
            temperature=0.34,
            stop=None
        )
        choice = completion.choices[0]
        # Get the ChatCompletionMessage object  
        message = choice.message  
        # Get the content value  
        content = message.content  
        return content
    except Exception as err:
        raise err.with_traceback(err.__traceback__)

# Store generated comments in a list
comments = []
extensions = ['.txt','.java','.css','.py','.js','.jsx']
# Process each file in the repository paths

for root, dirs, files in os.walk(repo_paths):
    for file in files:
        file_path = os.path.join(root, file)
        # Perform processing on the file (e.g., read its content, analyze code, etc.)
        print("Processing file:", file_path)
        with open(file_path, 'r') as f:
            file_name, file_extension = os.path.splitext(file_path)
            print(file_extension + file_name)
            if(file_extension in extensions):
                content = f.read()
                comment = check(content)
                comments.append("Processing file:"+ file_path)
                comments.append(comment)
                comments.append("---------------------------------------------------------------------------------------------------------")
                print("Comment for file:", file_path)
                print(comment)

# Write generated comments to comment.txt file
with open("comment.txt", "w") as comment_file:
    for comment in comments:
        comment_file.write(comment + "\n")
