# Experimentation and Evaluation

This folder contains the experiments and evaluation of the OpenAI Prompt that are performed using the [Azure ML PromptFlow](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/overview-what-is-prompt-flow?view=azureml-api-2).

This contains the following folders:

- [Data](./data/): Contains the ground truth data that is used for experiments and bulk evaluation.
- [Evaluation](./evaluation/Results.ipynb): Contains the evaluation results of the OpenAI Prompt, which contains three Out of the Box evaluations provided by the PromptFlow.
    - F1 Score: Standard F1 score calculated in the basis of the ground truth data and the result given by the OpenAI Prompt.
    - GPT Similarity: GPT Similarity is a metric that measures the similarity between the ground truth data and the result given by the OpenAI Prompt.
    - GPT Relevance: GPT Relevance is a metric that is used when getting ground truth data is difficult. It measures the relevance of the result given by the OpenAI Prompt. For example the OpenAI Prompt is given a Weather context and and a question related to weather, then the score is calculated based on the relevance of the answer given by the OpenAI Prompt and the context given.
