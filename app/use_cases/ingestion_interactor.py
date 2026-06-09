from typing import List, Any
import os
from app.domain.interfaces.vector_store import VectorStoreInterface
from app.domain.interfaces.multimodal_llm import MultimodalLLMInterface

class IngestionInteractor:

    def __init__(
        self, 
        vector_store: VectorStoreInterface, 
        llm_service: MultimodalLLMInterface
    ):
        self.vector_store = vector_store
        self.llm_service = llm_service


    async def ingest_file(self, file_name: str, file_bytes: bytes, modality: str) -> dict[str, Any]:
   
        # AWS Lambda only allows writing to /tmp
        is_lambda = os.environ.get("AWS_LAMBDA_FUNCTION_NAME") is not None
        temp_dir = "/tmp/downloads" if is_lambda else "./downloads"
        
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, file_name)

        # Save the uploaded bytes to a temporary local file so PyPDFLoader can read it
        with open(temp_path, "wb") as f:
            f.write(file_bytes)

        if modality.lower() == "pdf":

            texts = self.llm_service.load_and_extract_text_from_pdf(temp_path)
    
            text_summaries, _ = await self.llm_service.generate_text_summaries(
                texts=texts, 
                tables=[], 
                summarize_texts=True
            )
            
            self.vector_store.add_summaries_and_docs(
                doc_summaries=text_summaries,
                doc_contents=texts
            )
            
            os.remove(temp_path)
            
            return {"status": "success", "message": f"Ingested {len(texts)} pages from PDF."}
        else:
            return {"status": "error", "message": f"Modality {modality} not supported yet."}
