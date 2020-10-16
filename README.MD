# Hubspot Deals Project

## Run project
Run project on local env with docker:

Set the `env_file` with your preferred configs (you can user the `env_file.demo` file as reference)
```
docker-compose build
docker-compose up
```

Now you can try on: http://localhost:5000/user/

## Testing
Run unit tests

```
pip install -r requirements-dev.txt
pytest tests
```

## Use

### Users

- User list `/user/`
- User add `/user/add`
- User detail/update `/user/edit/<user_id>`

### Deals
 
- User Deals list `/deals/<user_id>`
- User Deals update `/deals/<user_id>`


To start using this app you need at least one user with the Hubspot client_id and client_secret credentials.
You can get user Deals clicking on `Update deals` button on **User Deals list** view.
If the user has not token, then it will be redirected to Hubspot App page to start the OAuth flow to get API the token.
You can see user credentials data on **User detail** view.
You cna force to user api refresh token if you set the `Token expiration date` lower than the current date on the User Detail view.

To finalize the entire Hubspot OAuth flow your app should be available on a public domain using https... or you can change the domain of the redirected url after the redirection fails (http://localhost:5000/user/hb-oauth?code=XXXXX-XXXXX-XXXX&stage=YYYYYYYYYYY)