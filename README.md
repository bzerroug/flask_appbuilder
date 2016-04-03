Meteo for dataware
==================

- Requirements:

    To use the sdk Splunk, create a file

    # Splunk host (default: localhost)
    host=localhost
    # Splunk admin port (default: 8089)
    port=8089
    # Splunk username
    username=admin
    # Splunk password
    password=changeme
    # Access scheme (default: https)
    scheme=https
    # Your version of Splunk (default: 5.0)
    version=5.0
    
    Save the file as .splunkrc in the current user's home directory.
    
    For example on OS X, save the file as:

    ~/.splunkrc
    
    On Windows, save the file as:

    C:\Users\currentusername\.splunkrc
    
    For more informations https://github.com/splunk/splunk-sdk-python
   

- Installation:

    ```bash
    # Create and enter in a virtualenv
    virtualenv /tmp/venv
    source /tmp/venv/bin/activate

    git clone https://github.com/bzerroug/flask_appbuilder
    cd flask_appbuilder
    pip install -e .
    ```

- Run:

    ```bash
    # Assuming you're in the venv
    dataware-meteo
    ```
