from ticketselling import create_app_wsgi
from dotenv import load_dotenv

load_dotenv()
app = application = create_app_wsgi()  # noqa
