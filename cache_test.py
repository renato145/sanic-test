import asyncio
import aioredis
from time import time
from sanic import Sanic
from sanic.response import text

app = Sanic(__name__)
loop = None
redis = None

async def init(sanic, _loop):
    global loop
    global redis
    loop = _loop
    redis = await aioredis.create_redis(('localhost', 6379), loop=loop)

@app.route('/')
async def app_root(request):
    i = await redis.incr('my-key')
    return text('This is chewbacca #%d.\n' % i)

@app.route('/save/<name:string>')
async def save_x(request, name):
    await redis.rpush('names', name)
    return text('Saved: %s\n' % name)

@app.route('/remove/<name:string>')
async def remove_x(request, name):
    return text('Removed: %s\n' % name)

app.run(host='0.0.0.0', port=8000, before_start=init, workers=4)#, debug=True)


# curl -X POST -F image=@t.jpg 'http://localhost:8000/get-label' ; echo ""
# curl http://localhost:8000/get-label?url=http://www.freephotosbank.com/photographers/photos1/60/med_556d65fb50a408d93f7141963b542250.jpg; echo""