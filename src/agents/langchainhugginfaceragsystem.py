from langchain_community.document_loaders import UnstructuredURLLoader
#pip install unstructured
#pip install "unstructured[html]"
#pip install chromadb
#pip install -U langchain-huggingface
#pip install langchain_chroma


from langchain_text_splitters  import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline

from langchain_core.output_parsers import StrOutputParser
import torch
from transformers import AutoModelForCausalLM ,AutoTokenizer
from langchain import hub
from typing_extensions import List,TypedDict
from langgraph.graph import StateGraph,START


urls = ["https://langchain-ai.github.io/langgraph/tutorials/introduction/"]

loader=UnstructuredURLLoader(urls=urls)
doc=loader.load()

print(doc[0].page_content[:500])  # preview first 500 chars


#print(doc)

text_splitter=RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=10)

all_split=text_splitter.split_documents(doc)

print(len(all_split))

embeding=HuggingFaceEmbeddings()

vector=embeding.embed_query("hello world");

vector[:5]


# storing the database locally 

#vectorstore=Chroma.from_documents(documents=all_split,embedding=HuggingFaceEmbeddings(),persist_directory="./chroma.db") here embedding model would be store

vectorstore=Chroma.from_documents(documents=all_split,embedding=HuggingFaceEmbeddings())


# vectorstore=Chroma(
#  persist_directory="./chroma.db",
#  embedding_function=HuggingFaceEmbeddings()) #here loading data from embedding model

model_id="tiiuae/falcon-7b"


text_generation_pipeline = pipeline(
    "text-generation",   # ✅ correct
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    max_new_tokens=200,   # ✅ also use plural
    device=-1,            # use 0 if you have CUDA
    temperature=0.7,
    top_k=50
)

llm=HuggingFacePipeline(pipeline=text_generation_pipeline)

template="hello i am do not nothing"

prompt=PromptTemplate.from_template(template)

prompthub=hub.pull("rlm/rag_prompt")


class State(TypedDict):
     question:str
     context:List(Document)
     answer:str
def retrive(state:State):
    retrive_doc= vectorstore.similarity_search(state["question"],k=1)
    return {"context":retrive_doc}


def generate(state:State):
    doc_content = "\n\n".join(doc.page_content for doc in state["context"])

    message = prompt.invoke({"question": state["question"], "context": doc_content})
    response=llm.invoke(message)
    return {"answer":response}


state_graph=StateGraph(State).add_sequence([retrive,generate])

state_graph.add_edge(START,"retrive")

graph=state_graph.compile()

response=graph.invoke({"question":"what is langgraph"})

print(response["answer"])