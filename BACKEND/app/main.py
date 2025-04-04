import uvicorn
from fastapi import FastAPI
from routers import include_routers

app = FastAPI(title='JSB API', version='0.1')

include_routers(app)

@app.get('/')
async def root():
    return {'message': 'API H'}

if __name__ == '__main__':
    uvicorn.run("app.main:app", host='0.0.0.0', port=8000, reload=True)
