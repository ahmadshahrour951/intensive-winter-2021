import requests
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/finestSelfDev"
mongo = PyMongo(app)



@app.route('/')
def base_redirect():
    return redirect(url_for('aspirations_render'))


@app.route('/aspirations', methods=['GET'])
def aspirations_render():
    main_data = list(mongo.db.aspirations.find({}))  or []

    for data in main_data:
      data['_id'] = str(data['_id'])

    return render_template('base.jinja2', page="aspirations", main_data=main_data)

@app.route('/aspirations', methods=['POST', 'PATCH'])
def aspirations_post():
  aspirations = mongo.db.aspirations
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
  aspirations = mongo.db.aspirations
  aspirations.delete_one({'_id': ObjectId(id)})
  return jsonify(success=True)


@app.route('/actions/<id>', methods=['GET'])
def actions_detail_render(id):
  main_data = list(mongo.db.actions.find({})) or []

  for data in main_data:
      data['_id'] = str(data['_id'])

  detail_data = mongo.db.actions.find_one({'_id': ObjectId(id)})

  return render_template('base.jinja2', page="actions", main_data=main_data, detail_data=detail_data, is_detail=True)

@app.route('/actions', methods=['GET'])
def actions_render():
  main_data = list(mongo.db.actions.find({})) or []

  for data in main_data:
      data['_id'] = str(data['_id'])
  
  return render_template('base.jinja2', page="actions", main_data=main_data, is_detail=False)


@app.route('/actions', methods=['POST', 'PATCH'])
def actions_post():
  actions = mongo.db.actions
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
  actions = mongo.db.actions
  actions.delete_one({'_id': ObjectId(id)})
  return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
