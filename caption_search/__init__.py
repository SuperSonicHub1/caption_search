from flask import Flask
import os.path

def create_app(test_config=None):

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		DATABASE=os.path.join(app.instance_path, 'caption_search.sqlite'),
	)

	if test_config is None:
        # load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# load the test config if passed in
		app.config.from_mapping(test_config)

	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass

	@app.template_filter('repr')
	def repr_filter(o: object) -> str:
		return repr(o)

	from flask import render_template, request, abort
	from . import database, sql
	database.init_app(app)

	@app.route('/')
	def index():
		return render_template("index.html")

	@app.route('/search')
	def search():
		query = request.args.get("q")
		if not query:
			abort(400)

		db = database.get_db()

		results = db.execute(sql.search, [query]).fetchall()

		results_graph = {}
		for result in results:
			video_id, title = result["video_id"], result["title"]
			if video_id in results_graph:
				results_graph[video_id]["items"].append(result)
			else:
				results_graph[video_id] = {
					"title": title,
					"items": [result]
				}

		return render_template("search.html", query=query, results=results_graph,)

	return app
