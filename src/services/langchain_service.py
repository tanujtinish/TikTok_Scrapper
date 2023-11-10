import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from src.configs.pinecone_config import langchain_pinecone_index
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


class Langchain_service:
  def __init__(self):
    load_dotenv()
    self.OPENAI_API_KEY = os.getenv("API_KEY")
    self.model_name = 'text-embedding-ada-002'
    self.index_name = 'langchain-pinecone-index'
    self.embed = OpenAIEmbeddings(
        model=self.model_name,
        openai_api_key=self.OPENAI_API_KEY
    )
    self.text_field = "text"
    self.index = langchain_pinecone_index
    self.vectorstore = Pinecone(
        self.index, self.embed.embed_query, self.text_field
    )
    self.llm_gpt_3_5 = ChatOpenAI(
      openai_api_key=self.OPENAI_API_KEY,
      model_name = "gpt-3.5-turbo",
      temperature=0.0
    )
    self.llm_gpt_4 = ChatOpenAI(
      openai_api_key=self.OPENAI_API_KEY,
      model_name = "gpt-4-0613",
      temperature=0.0
    )
    self.llm = OpenAI(
      openai_api_key=self.OPENAI_API_KEY,
      temperature=0.0
    )
    self.retriever_multi_query = MultiQueryRetriever.from_llm(
      retriever=self.vectorstore.as_retriever(),
      llm=self.llm,
    )
    self.prompt_template_self_only = os.getenv("PROMPT_TEMPLATE_SELF_ONLY")
    self.prompt_with_self_only = PromptTemplate(template = self.prompt_template_self_only, input_variables=["context", "question"])
    self.prompt_template_all_sources = os.getenv("PROMPT_TEMPLATE_ALL_SOURCE")
    self.prompt_with_all_sources = PromptTemplate(template = self.prompt_template_all_sources, input_variables=["context", "question"])
  
  def embed_text_openai(self, text):
    return self.embed.embed_query(text)
  
  def get_relative_docs(self, text, k):
    relevant_docs = self.retriever_multi_query.get_relevant_documents(query=text,k=k)
    return relevant_docs
  
  def ask_question_from_all_sources(self, text, k):
    relevant_docs = self.retriever_multi_query.get_relevant_documents(query=text,k=k)
    chain = load_qa_chain(self.llm_gpt_4,chain_type="stuff",verbose=True,prompt=self.prompt_with_all_sources)
    res = chain.run(input_documents=relevant_docs, question=text)
    return res
  
  def ask_question_from_relative_docs(self,text,k):
    relevant_docs = self.retriever_multi_query.get_relevant_documents(query=text,k=k)
    chain = load_qa_chain(self.llm_gpt_3_5,chain_type="stuff",verbose=True,prompt=self.prompt_with_self_only)
    res = chain.run(input_documents=relevant_docs, question=text)
    return res
    
  
langchain_service = Langchain_service()
