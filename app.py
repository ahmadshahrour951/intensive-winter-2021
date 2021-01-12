import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Prepare env variables for database
load_dotenv()
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
MONGODB_DBNAME = 'dev'

app = Flask(__name__)

# Start db connections
app.config["MONGO_URI"] = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@cluster0.l6db0.mongodb.net/{MONGODB_DBNAME}?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route('/')
def base_redirect():
    return redirect(url_for('aspirations_render'))

# Aspirations routes
@app.route('/aspirations', methods=['GET'])
def aspirations_render():
   # Fetch all the aspirations documents
    main_data = list(mongo.db.aspirations.find({})) or []

    for data in main_data:
      data['_id'] = str(data['_id'])

    return render_template('base.jinja2', page="aspirations", main_data=main_data)

@app.route('/aspirations', methods=['POST', 'PATCH'])
def aspirations_post():
  aspirations = mongo.db.aspirations

  #hidden input method placed in the form to help differentiate the two methods
  http_method = request.form.get('_method')

  if  http_method == 'post':
    aspirations.insert_one({
        "name": request.form.get('name'),
        "description": request.form.get('description')
    })
  elif http_method == 'patch':
    aspirations.update_one({'_id': ObjectId(request.form.get('_id'))},
    {
        '$set': {
            'name': request.form.get('name'),
            'description': request.form.get('description')
        }
    })
  
  return redirect(url_for('aspirations_render'))

@app.route('/aspirations/<id>', methods=['DELETE'])
def aspirations_delete(id):
  # this route acts like an api
  aspirations = mongo.db.aspirations
  aspirations.delete_one({'_id': ObjectId(id)})
  return jsonify(success=True)

# Actions routes
@app.route('/actions', methods=['GET'])
def actions_render():
  #fetch all documents for actions
  main_data = list(mongo.db.actions.find({})) or []

  for data in main_data:
      data['_id'] = str(data['_id'])
  
  return render_template('base.jinja2', page="actions", main_data=main_data, is_detail=False)


@app.route('/actions/<id>', methods=['GET'])
def actions_detail_render(id):
  main_data = list(mongo.db.actions.find({})) or []

  for data in main_data:
      data['_id'] = str(data['_id'])

  #provide an extra variable for template disection
  detail_data = mongo.db.actions.find_one({'_id': ObjectId(id)})

  return render_template('base.jinja2', page="actions", main_data=main_data, detail_data=detail_data, is_detail=True)

@app.route('/actions', methods=['POST', 'PATCH'])
def actions_post():
  actions = mongo.db.actions

  # this uses the same way as the aspirations route
  http_method = request.form.get('_method')

  if http_method == 'post':
    actions.insert_one({
        "name": request.form.get('name'),
        "description": request.form.get('description')
    })
  elif http_method == 'patch':
    actions.update_one({'_id': ObjectId(request.form.get('_id'))},
                           {
        '$set': {
            'name': request.form.get('name'),
            'description': request.form.get('description')
        }
    })

  return redirect(url_for('actions_render'))

@app.route('/actions/<id>', methods=['DELETE'])
def actions_delete(id):
  # this uses the same way as aspirations route
  actions = mongo.db.actions
  actions.delete_one({'_id': ObjectId(id)})
  return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
