from flask import Flask, render_template
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

links = {'active': [], 'inactive': []}

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('url')
parser.add_argument('status')

@app.route('/')
def home():
    return render_template('index.html')

class all_links(Resource):
	def get(self):
		return links
	
	def post(self):
		args = parser.parse_args()
		if not args['url']:
			return 'Missing url argument!'
		if not args['title']:
			return 'Missing title argument!'

		links['active'].append({'title': args['title'], 'url': args['url']})

		return links['active'], 201

class all_links_by_status(Resource):
    def get(self):
        args = parser.parse_args()
        if not args['status']:
            return 'Missing status argument!'
        if args['status'] not in links:
            return 'Invalid status argument!'
        return links[args['status']]

api.add_resource(all_links,'/all_links')
api.add_resource(all_links_by_status,'/all_links_by_status')


if __name__ == '__main__':
    app.run(debug=True)
