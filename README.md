# Beatrix Kiddo

On almost every project that customers only want an "app", a "web" or a "webapp", then it makes you do the loop-task of developing again and again a backend service (an API) that coud serve to any device web or app ... or you simply copy/paste the past project and modify some parameters, but the code could'nt be so clean like it would by creating a new project.


## Mission
The main goal of this project called Beatrix Kiddo (actually the idea came to me at the moment I remembered Kill Bill, I'll rename it then), is to automate the cyclic task to build an API and put the main effort of developers in UI/UX part (make beautiful WebDesign or good looking UI for an App), that's it. Because, from my point of view, UI/UX dev is the artistic part where a developer could add *art* to his/her/their product.

## Yeah..yeah... but ... How it works? (still improving)

The script works with an .json file as an input and it will be read all the fields needed to create the models, then the correspond endpoints.

### 1. Create your own json file
```json
{
    "app_name": "notetaking",
    "models": [
        { "Notes":	["message(TextField[max_length=300])",
                    "time_created(DateTimeField[auto_now=True])"]},
        { "Users": 	["fullname(CharField[max_length=300])",
                    "nickname(CharField[max_length=300])"]}
    ]
}
```
### 2. Run the script
`python scratch.py path/to/json.file`

### 3. See your new project created
By now, the project will be created alonside the scratch.py script.

### NOTE
By now only it works to produce Django projects, building API Rests in Django (with Django REST API Framework), the goal of this project is to support more frameworks (Flask - Python, Iris - Golang, Express.js - Node), for more details see in [What's Next?]

Currently the models values described in the json file sample as showed above is according [Django Models documentation]. Then it'll be changed to a more general rule to support several frameworks.

[What's Next?]: http://www.reddit.com
[Django Models documentation]: https://docs.djangoproject.com/en/1.11/topics/db/models/#


## What's Next?

Actually there is a too looo...oong TO-DO LIST, here I mention some features will be developed in the next days.

* Extend the features in models relation between models (currently it's working with default django db engine: mysql  )
* Add database types: not only SQL but also No-SQL, like MongoDB at first
* Customize the endpoints that will be described in another field into the json file
* Replace the `.json` file with a `.be` file with own syntaxis (pretending to be similar to TOML)
* Extend the support for more framework, next framework: iris - Golang