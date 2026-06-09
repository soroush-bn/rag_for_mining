from typing import List, Tuple, Optional
import vertexai
from app.common.constants import CHAT_MODEL_NAME, PROJECT_ID, REGION
from app.domain.interfaces.multimodal_llm import MultimodalLLMInterface
from app.domain.models import Document
from langchain_google_vertexai import ChatVertexAI, VertexAI, VertexAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document as LangchainDocument

def split_image_text_types(docs):
    """Split base64-encoded images and texts"""
    texts = []
    for doc in docs:
        if isinstance(doc, LangchainDocument) or hasattr(doc, 'page_content'):
            texts.append(doc.page_content)
        elif isinstance(doc, str):
            texts.append(doc)
    return texts

def img_prompt_func(data_dict):
    """Join the context into a single string"""
    formatted_texts = "\n".join(data_dict["context"])
    messages = []

    text_message = {
        "type": "text",
        "text": (
            "You are a mine safety expert tasked with providing safety advice.\n"
            "You will be given a mix of text and tables.\n"
            "Use this information to provide safety advice related to the user question.\n"
            f"User-provided question: {data_dict['question']}\n\n"
            "Text and / or tables:\n"
            f"{formatted_texts}"
        ),
    }
    messages.append(text_message)
    return [HumanMessage(content=messages)]


class GeminiMultimodalLLMImpl(MultimodalLLMInterface):

    def __init__(self):
        # Initialize Vertex AI with project ID and region from constants
        vertexai.init(project=PROJECT_ID, location=REGION)
        
        self.chat_model = ChatVertexAI(
            temperature=0, 
            model_name=CHAT_MODEL_NAME,
            max_output_tokens=1024
        )
        self.embeddings = VertexAIEmbeddings(model_name="gemini-embedding-001", project=PROJECT_ID, location=REGION)

    async def generate_answer(self, query: str, context: List[Document], image_url: Optional[str] = None) -> str:
        pass

    async def generate_embedding(self, text: str) -> List[float]:
        return self.embeddings.embed_query(text)

    async def extract_image_features(self, image_bytes: bytes) -> List[float]:
        pass
    
    def multi_modal_rag_chain(self, retriever):
        """Multi-modal RAG chain initialized with the Vector DB retriever"""
        chain = (
            {
                "context": retriever | RunnableLambda(split_image_text_types),
                "question": RunnablePassthrough(),
            }
            | RunnableLambda(img_prompt_func)
            | self.chat_model
            | StrOutputParser()
        )
        return chain

    def load_and_extract_text_from_pdf(self, pdf_path: str) -> List[str]:
        """Loads a PDF and extracts its text per page."""
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        return [doc.page_content for doc in documents]
    
    async def generate_text_summaries(self, texts: List[str], tables: List[str], summarize_texts: bool=False) -> Tuple[List[str], List[str]]:
        
        prompt_text = """You are an assistant tasked with summarizing tables and text for retrieval. \
        These summaries will be embedded and used to retrieve the raw text or table elements. \
        Give a concise summary of the table or text that is well optimized for retrieval. Table or text: {element} """
        prompt = PromptTemplate.from_template(prompt_text)
        
        empty_response = RunnableLambda(
            lambda x: AIMessage(content="Error processing document")
        )
        
        # Use standard VertexAI for summarization
        model = VertexAI(
            temperature=0, 
            model_name=CHAT_MODEL_NAME, 
            max_output_tokens=1024
        ).with_fallbacks([empty_response])
        
        summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

        text_summaries = []
        table_summaries = []

        if texts and summarize_texts:
            text_summaries = summarize_chain.batch(texts, {"max_concurrency": 1})
        elif texts:
            text_summaries = texts

        if tables:
            table_summaries = summarize_chain.batch(tables, {"max_concurrency": 1})

        return text_summaries, table_summaries