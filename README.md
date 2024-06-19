# june-20-tech-talk
 
# Overview
This is a 101 for starting out with Large Language Models (LLMs)! While LLMs have been out for a while, they have gotten really popular in the last two years. This tech talk shows you how to setup a local LLM, expose it via API, and then interface via Streamlit and Gradio! 

# Network diagram

![plot](./imgs/network-diagram.svg)

# Intro
Before we get into it, there are some terms we need to know. 

First off we have __large language model__. "Large language models largely represent a class of deep learning architectures called transformer networks. A transformer model is a neural network that learns context and meaning by tracking relationships in sequential data, like the words in this sentence...A transformer is made up of multiple transformer blocks, also known as layers. " [Nvidia, 2024](https://www.nvidia.com/en-us/glossary/large-language-models/)

__Quantized__: "Quantization is a technique to reduce the computational and memory costs of running inference by representing the weights and activations with low-precision data types like 8-bit integer (int8) instead of the usual 32-bit floating point (float32)...Reducing the number of bits means the resulting model requires less memory storage, consumes less energy (in theory), and operations like matrix multiplication can be performed much faster with integer arithmetic. It also allows to run models on embedded devices, which sometimes only support integer data types." [HuggingFace, 2024](https://huggingface.co/docs/optimum/en/concept_guides/quantization)

__Tokens__: "the atomic unit that the model is training on and making predictions on. A token is typically one of the following:

* a _word_—for example, the phrase "dogs like cats" consists of three word tokens: "dogs", "like", and "cats".
* a _character_—for example, the phrase "bike fish" consists of nine character tokens. (Note that the blank space counts as o`ne of the tokens.)
* _subwords_—in which a single word can be a single token or multiple tokens. A subword consists of a root word, a prefix, or a suffix. For example, a language model that uses subwords as tokens might view the word "dogs" as two tokens (the root word "dog" and the plural suffix "s"). That same language model might view the single word "taller" as two subwords (the root word "tall" and the suffix "er")." [Google Developers, 2024](https://developers.google.com/machine-learning/glossary#token)

__Temperature__: "A hyperparameter that controls the degree of randomness of a model's output. Higher temperatures result in more random output, while lower temperatures result in less random output... Choosing the best temperature depends on the specific application and the preferred properties of the model's output. For example, you would probably raise the temperature when creating an application that generates creative output. Conversely, you would probably lower the temperature when building a model that classifies images or text in order to improve the model's accuracy and consistency." [Google Developers, 2024](https://developers.google.com/machine-learning/glossary#token)

# Setup
First download [LM Studio](https://lmstudio.ai/). We are using LM Studio because it is a free and open source way to host LLMs. This application makes it easy to find compatible LLMs, interface with them, and start a server with them. 

Once it is downloaded, search for `llama 3`. The full name should look something like `
lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf`. You can find the model card for this on [HuggingFace](https://huggingface.co/lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF).

*You may have noticed I chose the Q4 version and that is because I don't think my laptop could run VS Code, LM Studio, Outlook, and share my screen on Teams all at the same time!*

Once that is done downloading, we can check out the model in the __AI Chat__ tab. This is a great way to talk to your LLM locally, or test the LLM before deploying it on a server. 

The __Playground__ tab is another great one to compare the performance of different LLMs. 

# Starting the server
Switching over to the __Local Server__ tab, there is a lot of information on the page. You can set the parameters on the right, get Python code for how to interact with it in the middle, and start the server on the left. The bottom shows the logs for the LLM. Don't forget to load your model at the top before you try to start the server!