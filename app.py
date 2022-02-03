from aiohttp import web
import aiohttp_jinja2, jinja2
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client.test_database

MAX_LENGTH = 100


async def get_event(request):
    map_shape = await db.shape.find_one({}, {'_id': 0})
    coordinates = await db.coordinates.find({}, {'_id': 0}).to_list(length=MAX_LENGTH)
    return web.json_response(data={'shape': map_shape, 'coordinates': coordinates})


async def record_event(request):
    event = await request.json()
    event = dict(event)
    map_shape = await db.shape.find_one({}, {'_id': 0})

    if event['x'] >= map_shape['x'] or event['y'] >= map_shape['y']:
        return web.Response(status=400)

    event_type = event.pop('type')
    if event_type == 'start':
        await db.coordinates.insert_one(event)
    else:
        await db.coordinates.delete_many(event)
    return web.Response()


async def change(request):
    x_coord = int(request.query.get('x'))
    y_coord = int(request.query.get('y'))
    await db.shape.delete_many({})
    await db.shape.insert_one({'x': x_coord, 'y': y_coord})
    return web.Response()


@aiohttp_jinja2.template('index.html')
async def index(request):
    pass


app = web.Application()
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader('templates'))

app.add_routes([web.get('/api/v1/event/', get_event),
                web.post('/api/v1/event/', record_event),
                web.get('/api/v1/reshape/', change),
                web.get('/', index)])

if __name__ == '__main__':
    web.run_app(app)
