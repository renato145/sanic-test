import app_model
from sanic import Sanic
from sanic.response import text, json
from sanic.exceptions import NotFound, ServerError

model = None
app = Sanic(__name__)


def load_model():
    global model
    model = app_model.load_model()

@app.route('/')
async def app_root(request):
    return text('This is chewbacca.')

@app.route('/name/<name:string>')
async def name(request, name):
    return text('Hello %s' % name)

@app.route('/post', methods=['POST'])
async def post_handler(request):
    return text('POST request - %s' % request.json)

@app.route('/get')
async def get_handler(request, methods=['GET']):
    return text('GET request - %s' % request.args)

@app.route('/body', methods=['POST'])
async def test_body(request):
    return text('%s' % request.body)

@app.route('/files', methods=['POST'])
async def post_json(request):
    test_file = request.files.get('image')

    file_parameters = {
        'name': test_file.name,
        'type': test_file.type,
    }

    return json({ "received": True, "file_names": request.files.keys(), "test_file_parameters": file_parameters })

@app.route('/killme')
async def i_am_ready_to_die(request):
    raise ServerError("Something bad happened :C", status_code=500)

@app.route('/get-label')
async def get_labels_from_url(request):
    global model
    if 'url' not in request.args.keys():
        return json('No url parameter.')

    src = request.args['url'][0]
    out = app_model.get_pred(src, model, 'url')

    return json(out)

@app.route('/get-label', methods=['POST'])
async def get_labels_from_file(request):
    global model
    img_file = request.files.get('image')
    if img_file is None:
        return json('No image file found.')

    out = app_model.get_pred(img_file.body, model, 'file')

    return json(out)

@app.exception(NotFound)
async def ignore_404s(request, exception):
    return text("Yep, I totally found the page: %s" % request.url)

app.run(host='0.0.0.0', port=8000, before_start=load_model(), debug=True)
# app.run(host='0.0.0.0', port=8000, debug=True)


# curl -X POST -F image=@t.jpg 'http://localhost:8000/get-label' ; echo ""
# curl http://localhost:8000/get-label?url=http://www.freephotosbank.com/photographers/photos1/60/med_556d65fb50a408d93f7141963b542250.jpg; echo""