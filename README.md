# intensive-winter-2021

The project is called FinestSelf. The objective is to allow a user to store and create aspirations and actions on a daily basis.

Language: Python 3.8.5
Framework: Flask 1.1.12
Templating: Jinja2 2.11.2

So two pages were created '/aspirations' and '/actions'. Each will have its own collection in mongodb.

The aspirations page will handle display data via cards and manipulating data via modals, since the priority is to allow the user to see as many aspirations as possible in this route. While in the actions page, the priority lies in have space and a bit more freedom to write your daily actions, so space was priorized over the number of actions to display.

This product is meant to help me measure market appetite for journalling and habits. The pandemic I feel has made me and many others palpable and woke? This is a movement to create your own philosophy for living.

## Aspirations
Here you'll find that there are 3 routes. I use modals to help perform crud operations 

aspirations/ GET route:
This will fetch all documents from the aspirations collection, then it will be presented as cards that link to their own modals for editing.

aspirations/ POST & PATCH route:
There is a variable called '_method' that I attach to the input:hidden feature in the form. Both will execute different code depending on the method, however both will redirect the user to the main page.

aspirations/<id> DELETE route
This route acts like a restful API and once the delete execution is complete, the user will receive a confirmation and the page is redirected.

## Actions
Here you'll also find very similar routes to aspirations except with an additional GET request for detail data. Also, the method of templating different here since I chose to display the console card instead of using a modal.

actions/ GET route 
This will fetch all documents from the actions collection, then it will be presented as cards that link to their own detail route

actions/<id> GET route
This fetches the detail page which contains a form for the user to edit the specific action .

actions/ POST & PATCH route
This acts the same way as the aspirations API does. based on a form variable it will determine the effects and produce the same redirect for the user to the main page.

actions/<id> DELETE route
Acts as a restful api and deletes the resource in interest and returning a successful response. 
## Future Features
- Creating a relationship between actions and aspirations
- Recording timestamps of each document created
- Timeline feature showing main action KPIs and graphs of progress
- Share feature to phycologst?
