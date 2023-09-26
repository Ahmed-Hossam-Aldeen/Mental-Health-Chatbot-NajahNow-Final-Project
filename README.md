# Mental Health Chatbot Project

## Overview

The Rasa NLU (Natural Language Understanding) Project is a comprehensive solution for building conversational AI applications with a focus on understanding and processing natural language text in Arabic. This project leverages the power of Rasa, an open-source framework for building conversational AI, to enable chatbots and virtual assistants to interact seamlessly with users in Arabic.

**Project Goals:**

1. **Arabic Language Support:** The primary goal of this project is to provide robust support for the Arabic language in conversational AI applications. Arabic is one of the most widely spoken languages globally, and it's essential to ensure that chatbots and virtual assistants can understand and respond to users in Arabic effectively.

2. **Mental Health Support:** A key focus of this project is on providing assistance and resources related to mental health. The project includes intents and responses that address questions and concerns about mental health, coping skills, seeking professional help, and expressing concern for others.

**Key Features:**

- **Intent Recognition:** The project includes a range of intents specifically designed to understand and respond to user queries related to mental health. These intents cover a wide spectrum of questions and concerns users may have.

- **Response Generation:** The responses provided by the chatbot are carefully crafted to offer information, support, and guidance. Users can receive information about mental health, coping strategies, and where to find professional help.

- **Customization:** This Rasa project is highly customizable, allowing developers to adapt it to different use cases and industries. You can easily extend the intents, responses, and the conversation flow to suit your application's requirements.


## Installation
```pip install -r requirements.txt```

# Training the Model
```rasa train``` 

# Usage (Locally)
```rasa run actions```

```rasa shell```

# Usage (web server)
```rasa run --cors "*"  ```

```rasa run actions```

``` python -m http.server ```
