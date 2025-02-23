import requests
import secrets
from urllib.parse import urlencode

from flask import redirect, url_for, session, current_app, request, abort, flash
from flask_app import app, User, user_repo

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("success: You've been logged out.")
    return redirect('/')

@app.route('/authorize/<provider>')
def oauth2_authorize(provider):
    if session.get('user_id'):
        print(f"User already logged in by id: { session.get('user_id') }. Redirecting to home page.")
        return redirect('/')

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        print(f"Provider '{provider}' not found.")
        abort(404)

    session['oauth2_state'] = secrets.token_urlsafe(16)
    print(f"Generated oauth2 state: {session['oauth2_state']}")

    qs = urlencode({
        'client_id': provider_data['client_id'],
        'redirect_uri': url_for('oauth2_callback', provider=provider, _external=True),
        'response_type': 'code',
        'scope': ' '.join(provider_data['scopes']),
        'state': session['oauth2_state'],
    })

    print(f"Redirecting to provider's authorize URL: {provider_data['authorize_url']}?{qs}")
    return redirect(provider_data['authorize_url'] + '?' + qs)

@app.route('/callback/<provider>')
def oauth2_callback(provider):
    if session.get('user_id'):
        print(f"User already logged in with id: {session.get('user_id')}. Redirecting to home page.")
        return redirect('/')

    provider_data = current_app.config['OAUTH2_PROVIDERS'].get(provider)
    if provider_data is None:
        print(f"Provider '{provider}' not found.")
        abort(404)

    if 'error' in request.args:
        for k, v in request.args.items():
            if k.startswith('error'):
                flash(f'{k}: {v}')
                print(f"Error received from provider: {k}: {v}")
        return redirect('/')

    # Проверяем, если состояние существует в сессии
    if 'oauth2_state' not in session:
        print("Session state not found. Redirecting to authorize again.")
        return redirect(url_for('oauth2_authorize', provider=provider))

    # Сравниваем состояния
    if request.args.get('state') != session['oauth2_state']:
        print(f"State mismatch: received state '{request.args.get('state')}' does not match session state '{session['oauth2_state']}'.")
        # В данном случае вы можете либо повторно вызвать авторизацию, либо вывести ошибку
        return redirect(url_for('oauth2_authorize', provider=provider))

    # Удаляем состояние из сессии после успешной проверки
    session.pop('oauth2_state')

    if 'code' not in request.args:
        print("Authorization code not found in request.")
        abort(401)

    print(f"Exchanging authorization code for access token.")
    response = requests.post(provider_data['token_url'], data={
        'client_id': provider_data['client_id'],
        'client_secret': provider_data['client_secret'],
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': url_for('oauth2_callback', provider=provider, _external=True),
    }, headers={'Accept': 'application/json'})

    if response.status_code != 200:
        print(f"Failed to obtain access token. Status code: {response.status_code}, Response: {response.text}")
        abort(401)

    oauth2_token = response.json().get('access_token')
    print(f"Access token obtained: {oauth2_token}")

    if not oauth2_token:
        print("Access token is missing in the response.")
        abort(401)

    print(f"Fetching user information using the access token.")
    response = requests.get(provider_data['userinfo']['url'], headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    
    if response.status_code != 200:
        print(f"Failed to fetch user information. Status code: {response.status_code}, Response: {response.text}")
        abort(401)

    email = provider_data['userinfo']['email'](response.json())
    print(f"User email obtained: {email}")

    user = user_repo.get_user_by_email(email)
    if user is None:
        print(f"No user found. Creating a new user with email: {email}")
        new_user = User(username=email.split('@')[0], email=email, password="without_password")
        user_id = user_repo.save(new_user)
    else:
        user_id = user.id
        print(f"User found. User ID: {user_id}")

    session['user_id'] = user_id
    print(f"User ID {user_id} has been stored in session.")
    return redirect('/')