from app import app
import os

if os.getenv('DEBUG'):
    app.run(port=5000, debug=True)
else:
    app.run()
