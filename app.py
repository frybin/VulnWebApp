from webapp import app

if __name__ == '__main__':
    app.run(host=app.config['IP'], port=int(app.config['PORT']))

application = app