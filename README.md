## How to run the project locally

Clone the repository.
```sh
git clone https://github.com/amadeus4dev/flight-search-demo.git
cd flight-search-demo
```
Next create a virtual environment and install the dependencies.

```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Finally, run the Django server.
```sh
python manage.py runserver
```