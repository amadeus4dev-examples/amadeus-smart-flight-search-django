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

For authentication add your API key/secret in your .bash_profile.

```sh
export API_KEY=YOUR_API_KEY
export API_SECRET=YOUR_API_SECRET
```

Finally, run the Django server.
```sh
python manage.py runserver
```