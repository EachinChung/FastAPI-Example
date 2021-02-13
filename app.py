import uvicorn

from callback.main import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run('app:app', host='0.0.0.0', reload=True, debug=True)
