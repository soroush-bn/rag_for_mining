from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rag_router import router as rag_router

def create_app() -> FastAPI:
    """
    Factory function to assemble the FastAPI application, 
    configure CORS, middleware, and include routers.
    """
    app = FastAPI(
        title="Multimodal RAG API",
        description="Clean Architecture setup for Multimodal RAG Q&A",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

    app.include_router(rag_router)

    return app

app = create_app()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
