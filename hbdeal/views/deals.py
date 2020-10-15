from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from hbdeal.services import deal_service
from hbdeal.core.models.deal import User


bp = Blueprint('deals', __name__, url_prefix='/deals')


@bp.route('/<user_id>', methods=('GET',))
def user_deal_list(user_id):
    user = deal_service.get_user(user_id)
    deals = deal_service.get_user_deals(user)

    return render_template('deals_list.html', user=user, deals=deals)


@bp.route('/<user_id>/update', methods=('GET',))
def user_deal_list(user_id):
    user = deal_service.get_user(user_id)
    deals = deal_service.get_user_deals(user)

    return render_template('deals_list.html', user=user, deals=deals)