import uvicorn
from fastapi import FastAPI
from routers import auth, tickets

app = FastAPI(title='JSB API', version='0.1')

app.include_router(auth.router)
app.include_router(tickets.router)

@app.get('/')
async def root():
    return {'message': 'API H'}

if __name__ == '__main__':
    uvicorn.run("bot.main:app", host='0.0.0.0', port=8000, reload=True)
