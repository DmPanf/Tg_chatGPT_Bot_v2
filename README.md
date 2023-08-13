# Telegram chatGPT Bot v.2

- The Bot with chatGPT represents a feature-rich Telegram bot which can understand both text and voice inputs and can reply in either text or synthesized voice, backed by GPT-3 for generating responses.

## Purpose:
- The code implements a Telegram bot which communicates with users.
- The bot has integrated **OpenAI's GPT-3** to process text queries, and Yandex's SpeechKit to recognize and synthesize voice messages.


![image](https://github.com/DmPanf/TgBot_chatGPT/assets/99917230/6e468c5a-c06a-47e2-9756-18b94da4c53d)


## Description:

- Imports and Setup: The code starts by importing necessary libraries and loading environment variables. It initializes OpenAI with a secret key and establishes a Yandex SpeechKit session.

- User Access: The user_allowed decorator is defined to restrict certain bot commands to a list of allowed users.

- Voice and Text Mode: Users can switch between voice and text modes. The bot can reply either in text or synthesized voice, and can also recognize voice messages to convert them to text. The available voice characters for synthesis are Alena, Filipp, Jane, and Madirus.

- Commands:
 - /start: Greets the user and prompts them to ask any question.
 - /help: Provides information on how the bot can be interacted with.
 - /voice: Lets the user change settings for voice characters and the mode of interaction (voice or text).

- Voice Recognition: If the bot is in voice mode and the user sends a voice message, the code uses Yandex SpeechKit to convert the voice message to text. This text is then processed further.

- GPT Integration: The bot sends the received text (either typed by the user or converted from voice) to GPT-3, gets a response, and either:
 - Sends the response back in text form.
 - Or synthesizes a voice message using the chosen character and sends it back to the user.

- Main Loop: In the main() function, the bot's handlers are added to the application and the bot starts listening for incoming messages and commands.
