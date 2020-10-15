from hbdeal.app import main, initialize_app
from hbdeal.services.deal_service import update_last_deals, User
from hbdeal.core.hb_api import HBOauthApi

app = initialize_app()

app.run()
