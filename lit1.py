import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import sys
import re
import os
from openai import AzureOpenAI
import faiss
from jinja2 import Environment, FileSystemLoader

from utils.index import FAISSIndex
from utils.oai import OAIEmbedding, render_with_token_limit
from utils.logging import log
import random
import urllib.request

from rag_components import display_faq
from rag_components import display_movies
from rag_components import generic_plot
from rag_components import get_match

#### load OpenAI models ####
client = AzureOpenAI(
  api_version = "2024-02-01",
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  azure_endpoint = os.getenv("OPENAI_API_BASE")  
)

#### load index #####
index_path='.index/movies.index_256_64'
index = FAISSIndex(index=faiss.IndexFlatL2(1536), embedding=OAIEmbedding())
index.load(path=index_path)

#### load posters ####
import csv
with open('assets/posters.csv', mode='r') as infile:
    reader = csv.reader(infile,delimiter='|')
    mydict = {rows[0]:rows[1] for rows in reader}

#################################
####### MAIN HEADER + TABS ######
#################################
st.set_page_config(layout="wide")
st.header("CineMatch")
st.subheader("A movie for every occasion...",divider='gray')
tab1, tab2, tab3, tab4, tab5 = st.tabs(["FAQ","MATCH", "CHAT", "Weather", "Local"])

######################
### 1. BASIC MATCH ###
######################
with tab1:
  display_faq()

######################
### 2. BASIC MATCH ###
######################

with tab2: 
  c1, c2, c3, c4, c5= st.columns(5)
  with c1: submitted = st.button("GO",key='match')
  with c2: movie = st.text_input("Input imdbId", "tt0209144",help="Movie IDs begin with 'tt' and can be found at imdb.com")
  with c4: neighbors = st.selectbox('Number of matches', (1,2,3,4,5),index=4,help="The number of nearest matches displayed.")

  if submitted:
    ########################################
    ### get movie plot & make generic ######
    ########################################
    plotfile = "assets/plots.out"
    plots=[]
    with open(plotfile) as f:
      for line in f:
        if movie in line: plots.append(line)

    title = re.sub(r"^.*Title:","",re.sub(r"Plot:.*$","",plots[0]))
    plot = re.sub(r"^.*Plot:","",re.sub(r"imdbID:.*$", "", plots[0]))

    response=generic_plot(plot)

    #############################################
    ### display the user movie & generic plot ###
    #############################################
    col1, col2,= st.columns(2)
    with col1:
      st.write("**Title**: ",title)
      st.write("**Plot**: ",plot)
      st.write("**Generic Plot**: ",response.choices[0].message.content)

    with col2:
      try:
        imgURL = mydict[movie]
        urllib.request.urlretrieve(imgURL, "movie1.jpg")
        st.image("movie1.jpg" )
      except:
        st.image("default.jpg" )
        pass

    ##########################################
    ### search the index and show matches ####
    ##########################################
    snippets = index.query(response.choices[0].message.content, top_k=neighbors)
    sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]

    display_movies(snippets,mydict)

######################
### 2. CHATBOT    ####
######################
with tab3: 
  vibe = st.text_input("Movie vibe", "sports team underdog inspiring with romance",help="enter potential plot components")
  options = st.text_input("Additional filters", "not too scary",help="use this to refine and filter the matches further")
  verbose = st.checkbox("Show all matches",value=False)
  submitted = st.button("GO",key='chat')

  if submitted:
    #################################
    ### create & show generic plot ##
    #################################
    response=generic_plot(vibe)
    st.write("**Generic Plot**: ",response.choices[0].message.content)

    ##########################################
    ### search the index and show matches ####
    ##########################################
    snippets = index.query(response.choices[0].message.content, top_k=neighbors)
    sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
    if verbose: display_movies(snippets,mydict)

    #######################################
    ### build context and run final LLM ###
    #######################################
    get_match(snippets,mydict,vibe,options)
