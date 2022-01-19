from FlaskBlogApp import app

if __name__== "__main__": # είναι main όταν το τρέχουμε εμείς.
    app.run(debug=True,host="0.0.0.0", port=8080)