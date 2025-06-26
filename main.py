from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from data_ingestion.ingestion_pipeline import DataIngestion
from data_models.models import QuestionRequest, AgentState
from agent.workflow import GraphBuilder
from langchain_core.messages import HumanMessage

app = FastAPI()

# Initialize DataIngestion and GraphBuilder
data_ingestion = DataIngestion()

# Build the graph
graph_builder = GraphBuilder()
graph = graph_builder.build()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        return data_ingestion.ingest_data(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chatbot/")
async def chatbot_endpoint(request: QuestionRequest):
    try:
        state = AgentState(messages=[HumanMessage(content=request.question)])
        response = graph.invoke(state)
        ai_response = response['messages'][-1].content
        return JSONResponse(content={"response": ai_response})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))