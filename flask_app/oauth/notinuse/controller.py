#app, session, redirect, url_for, current_app, urlencode, user_repo, User, response, requests, request, secrets

from entity_serch import app, User, user_repo
from flask import redirect, url_for, session, current_app, request, abort, flash
import requests
import secrets
from urllib.parse import urlencode

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("success: You've been logged out.")
    return redirect(url_for('prediction_page'))


@app.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if 'user_id' in session:
        return redirect(url_for('prediction_page'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    session['oauth2_state'] = secrets.token_urlsafe(16)

    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    return redirect(provider_data['authorize_url'] + '?' + qs)


@app.route('/callback/<provider>')
def oauth2_callback(provider):
    if 'user_id' in session:
        return redirect(url_for('prediction_page'))

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        abort(404)

    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
        return redirect(url_for('prediction_page'))

    if request.args['state'] != session.get('oauth2_state'):
        abort(401)

    if 'code' not in request.args:
        abort(401)

    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider, _external=True),
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        abort(401)

    oauth2_token = response.json().get('access_token')
    if not oauth2_token:
        abort(401)

    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    if response.status_code != 200:
        abort(401)

    email = provider_data['userinfo']['email'](response.json())

    user = user_repo.get_user_by_email(email)
    if user is None:
        new_user = User(username=email.split('@')[0], email=email, password="without_password")
        user_id = user_repo.save(new_user)
    else:
        user_id = user.id

    session['user_id'] = user_id
    return redirect(url_for('prediction_page'))