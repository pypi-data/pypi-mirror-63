from sanic import Sanic
from sanic.response import json
from function_helper import function_deps

app = Sanic()
@app.route('/')
@function_deps([
    {
        'name': 'name',
        'source': 'query'
    }
])
async def test(name):
    return json({'hello': name})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)


