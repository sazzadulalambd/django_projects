import openai

openai.api_key = 'api-key'

def generate_completion():
    try:
        # Create completion request
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="what is chat gpt?",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Retrieve generated text
        completion_text = response.choices[0].text.strip()

        return completion_text

    except openai.error.OpenAIError as e:
        # Handle API errors
        print(f"OpenAI API error: {e}")

    except Exception as e:
        # Handle other errors
        print(f"An error occurred: {e}")

# Generate completion and print the result
completion_text = generate_completion()
print(completion_text)


# import os
# import openai

# openai.api_key= os.getenv("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")
# completion = openai.Completion.create(engine="gpt-3.5-turbo", prompt="what google?")
# print(completion.choices[0]['text'])


# openai.api_key = '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'

# response = openai.Completion.create(
#     engine='text-davinci-003',
#     prompt='Once upon a time',
#     max_tokens=50
# )

# print(response.choices[0].text.strip())

# sk-jwSM1jx47gWP6NrvW9KHT3BlbkFJH0Bph30dYmW1Ig56rQ3tv