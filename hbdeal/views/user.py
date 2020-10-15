from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from mongoengine.errors import NotUniqueError

from hbdeal.services import deal_service
from hbdeal.core.models.deal import User

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/', methods=('GET',))
def user_list():
    users = deal_service.get_user_list()
    return render_template('user_list.html', users=users)

@bp.route('/add', methods=('GET', 'POST'))
@bp.route('/edit/<user_id>', methods=('GET', 'POST'))
def user_add_or_edit(user_id=None):
    errors = []
    success = []

    if user_id:
        user = deal_service.get_user(user_id)
    else:
        user = User()
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.hb_client_id = request.form['hb_client_id']
        user.hb_client_secret = request.form['hb_client_secret']
        try:
            user.save()
            if user_id is None:
                return redirect('/user/edit/{}?added=success'.format(user.id))
            success = ['User has been updated']
        except NotUniqueError:
            errors = ['User name is duplicated']
    else:
        if request.args.get('added') == 'success':
            success = ['User has been added']


    return render_template('user_edit.html', user=user, errors=errors, success=success)
