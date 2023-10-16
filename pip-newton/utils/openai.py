
import openai

class openai_llm():

    def gpt_complation(prompt, verbose=False):
        """
        Function to build the prompt.
        
        Parameters
        ----------
        prompt : string
            A prompt to be provided to the model to get the text complation. It contains the infomation for generating the response.

        verbose : bool
            A boolean flag that determines whether to print the prompt generated

        Returns
        -------
        generated_text : string
            The text generated by the model following the instructions in the prompt.
        
        """

        generated_text = ""
        
        try:
            #Make your OpenAI API request here
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.7,
                max_tokens=399,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            
            generated_text = response.choices[0].text.replace("\n", "")

        except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
            print(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.error.APIConnectionError as e:
        #Handle connection error here
            print(f"Failed to connect to OpenAI API: {e}")
            pass
        except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
            print(f"OpenAI API request exceeded rate limit: {e}")
            pass

        if(verbose):
            print(generated_text)

        return generated_text