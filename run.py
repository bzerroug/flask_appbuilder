from app import app

#app.config['RECAPTCHA_USE_SSL'] = False
#app.config['RECAPTCHA_PUBLIC_KEY'] = 'public'

app.run(host='0.0.0.0', port=8080, debug=True)

