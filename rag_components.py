import streamlit as st 
import re
import os
import urllib.request
from prompts import system_conv
from prompts import system_generic
from prompts import system_recommend

from dotenv import load_dotenv
load_dotenv()
from openai import AzureOpenAI

#### load OpenAI models ####
client = AzureOpenAI(
  api_version = "2024-02-01",
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),
  azure_endpoint = os.getenv("OPENAI_API_BASE")
)


def display_faq():
  st.subheader("What is the goal?",divider="gray")
  col1, col2,= st.columns(2)
  with col1: st.write('''A common retail goal is to present items to users in a way that engages additional consumption. Traditional methods include customer segmentation and recommnedation engines. These methods are effective but remain distanced from the user. This system attempts further customization by dynamically presenting items the user. ''')
  with col2: st.image("images/Light-bulb.png")

  st.subheader("How does it match?",divider="gray")
  col1, col2,= st.columns(2)
  with col1: st.image("images/search.png")
  with col2: st.write('''The system translates a user signal into an intent with an LLM that re-writes it in the style of the product descriptions (i.e. movie plots). The descriptions from all products are embedded and stored in a vector database. Searching based on the user's generic intent, products with the most similar descriptions are retrieved. Another LLM selects the most compatible match based on the original input and delivers it to the user.  ''')

  st.subheader("How can use signals?",divider="gray")
  col1, col2,= st.columns(2)
  with col1: st.write('''In addition to direct user input via chatbot, the system attempts to leverage external signals that do not require user input. Examples include weather, local sports, social media, etc. Content could be peridically collected and then sent to an LLM for translation. For example, if a user's followers are talking about traveling to an exotic beach, maybe the user would be looking for plots that include similar scenery with a relaxing vibe.  ''')
  with col2: st.image("images/weather-icon-png-2.png")


def generic_plot(plot):
  conversation=[]
  conversation.append(system_generic)
  conversation.append({"role": "user", "content": plot})

  ### rewrite the plot as a generic description ###
  response = client.chat.completions.create(
    model="gpt-4o", # model = "deployment_name".
    messages=conversation
    )

  return response
  

def display_movies(snippets,mydict):
    st.subheader("Similar Movies",help="Ranked by vector similarity to the generic plot of movie submitted.",divider="gray")
    for doc in snippets:
      col1, col2,= st.columns(2)
      matchID = re.sub(r"^.*imdbID: ", "", doc.text).strip()
      matchTitle = re.sub(r"^.*Title:","",re.sub(r"Plot:.*$","",doc.text))
      matchPlot = re.sub(r"^.*Plot:","",re.sub(r"imdbID:.*$", "", doc.text))
      imdburl = 'https://www.imdb.com/title/'+matchID
      with col1:
        st.write("**Title**: ",matchTitle)
        st.write("**imdbId**: [%s](%s)" % (matchID,imdburl))
        st.write("**Similarity**: ",doc.score)
        st.write("**Plot**: ",matchPlot)
        selected = st.feedback("thumbs",key=matchID,disabled=True)
      with col2:
        try:
          imgURL = mydict[matchID]
          urllib.request.urlretrieve(imgURL, "movie2.jpg")
          st.image("movie2.jpg")
        except:
          st.image("images/default.jpg")
          pass

def get_match(snippets,mydict,vibe,options):
    st.subheader("Your Matching Movie",help="Hand-picked from movies with relevant plots.",divider="gray")
    conversation=[]
    conversation.append(system_recommend)
    conversation.append({"role": "user", "content": vibe+" "+options})
    context=""
    for doc in snippets:
      context=context+doc.text
    conversation.append({"role":"assistant","content": context})
    response = client.chat.completions.create( model="gpt-4o", messages=conversation)

    col1, col2,= st.columns(2)
    with col1:
      st.write(response.choices[0].message.content)

    found = re.search(r"tt[0-9]+",response.choices[0].message.content)
    if found:
      with col2:
        try:
          imgURL = mydict[found[0]]
          urllib.request.urlretrieve(imgURL, "movie2.jpg")
          st.image("movie2.jpg")
          imdburl = 'https://www.imdb.com/title/'+found[0]
          st.write("[%s](%s)" % (found[0],imdburl))
        except:
          st.image("images/default.jpg")
          pass

