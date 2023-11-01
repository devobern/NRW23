from app import app

if __name__ == '__main__':
    # todo: Remove after testing: 
    app.run(host='0.0.0.0', port=5000, ssl_context=('/home/nicolin/Projects/local_certs/localhost+2.pem', '/home/nicolin/Projects/local_certs/localhost+2-key.pem'))
    #app.run()
