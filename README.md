# CineMatch
> An example of **GenAI-powered personalization** in retail - illustrated using movies.

The (ficticious) retailer **CineMatch** is a movie subscription service. 
The success of CineMatch depends on keeping their customers engaged so they do not cancel their subscriptions.
CineMatch uses segmentation and recommendation engines, but would like to explore the use of GenAI for dynamic personalization.

The solution is a slight variation on the basic RAG format. About 35,000 movie plots were embedded and stored in a FAISS database.
Based on a signal from the user (which can be direct or indirect) an LLM creates a generic scenario and then looks for semantically similar movie plots. A second LLM compares the ranked results with the user's original signal to personalize the suggestion.  A chat window captures direct input from the user (called "the vibe"). A user can also provide additional context (e.g. "not too scary"). External signals include scenarios based on weather forecast, local events, and social media topics and trends. 

## System Requirements
- Open AI key and active LLM & Embedding deployments
- Weather API key for the external signal source
- FAISS as vector storage and retrieval
- Streamlit runs the app

## Installation
create environment
> XXX

install requirements
> YYY

copy the env.example file and fill in your endpoints and API key
> ZZZ

run the application
> AAA

## Limitations / Improvements
1. Evaluation framework
2. Feedback loop
3. Search Quality
4. Reviews vs Descriptions

## Responsible AI Considerations
Possible Harm
User 
