# Title: Use Ollama with Python
#
# Description:
# This script demonstrates how to interact with local Large Language Models (LLMs)
# using the Ollama Python library. It covers basic chat, streaming responses,
# and simple text generation.
#
# Installation:
# Before running this code, ensure you have Ollama installed on your system
# (from https://ollama.com/) and the Python library installed.
#
# Command to install the library:
# pip install ollama==0.2.1

import ollama  # Import the official Ollama library

# --- Example 1: Basic Chat ---
# This method mimics a conversation format where you provide a list of messages.
# It is useful for maintaining context or chat history.

# response = ollama.chat(
#     model='llama3.1',  # Specify the model you want to use (ensure you have pulled it via 'ollama pull llama3.1')
#     messages=[
#         {
#             'role': 'user',    # The role can be 'user', 'assistant', or 'system'
#             'content': 'Why is the sky blue?',  # The actual prompt or question
#         },
#     ]
# )
# # The response is a dictionary containing metadata and the message
# print(response)
# # To get just the answer text, we access ['message']['content']
# # print(response['message']['content'])


# --- Example 2: Streaming Chat ---
# Streaming allows you to receive and display the response piece by piece
# as it is being generated, rather than waiting for the entire answer.
# This creates a "typewriter" effect similar to ChatGPT.

# stream = ollama.chat(
#     model='llama3.1',
#     messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],
#     stream=True,  # Enable streaming mode
# )
#
# # Iterate through the stream generator
# for chunk in stream:
#   # Print each piece of content immediately.
#   # end='' prevents printing a new line after each chunk.
#   # flush=True ensures the output appears immediately on the screen.
#   print(chunk['message']['content'], end='', flush=True)


# --- Example 3: Simple Generation (Active Code) ---
# The .generate() method is a simpler way to get a completion for a single prompt
# without setting up the message history structure.

response = ollama.generate(
    model='llama3.1',             # Specify the model
    prompt='Why is the sky blue?' # Provide the prompt directly
)

# The result is a dictionary. We access the 'response' key to get the text.
print(response['response'])
