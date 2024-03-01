## Comprehensive Django Deployment Guide: From Local Development to Live Site on a Remote Server

### On Remote Server:

1. Connect to the remote server via SSH:

    ```bash
    ssh -p 1522 ygbl@155.133.26.105
    ```

    Enter your password when prompted.

2. Create project folders:

    ```bash
    mkdir project
    cd project
    mkdir versity_info
    ```

    To get the project path:

    ```bash
    pwd
    ```

    Note the path (e.g., `/home/ygbl/project/versity_info`).

    Exit from the remote server:

    ```bash
    exit
    ```

### On Local Machine:

3. Go to the project folder:

    ```bash
    cd /path/to/your/local/project
    ```

4. Activate your virtual environment:

    ```bash
    source path/to/your/virtualenv/bin/activate
    ```

5. Save the requirements to a text file:

    ```bash
    pip3 freeze > requirements.txt
    ```

6. Deactivate the virtual environment:

    ```bash
    deactivate
    ```

7. Zip the project folder:

    versity_info.zip

8. Copy the zip file to the remote server:

    ```bash
    scp -P 1522 versity_info.zip ygbl@155.133.26.105:/home/ygbl/project/versity_info
    ```

    Enter your server password when prompted.

### On Remote Server:

9. Connect to the remote server again:

    ```bash
    ssh -p 1522 ygbl@155.133.26.105
    ```

    Enter your password.

10. Navigate to the project folder and unzip the file:

    ```bash
    cd project/versity_info
    unzip versity_info.zip
    ```

11. Create and activate a virtual environment:

    ```bash
    python -m venv ygblvenv
    source ygblvenv/bin/activate
    ```

12. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

13. Move to the source directory:

    ```bash
    cd src
    ```

14. Start the Django development server in a detached screen session:

    ```bash
    screen -S "run"
    python manage.py runserver 0.0.0.0:9000
    ctrl + A + D
    ```
    
15. Your site is now live on [http://155.133.26.105:9000](http://155.133.26.105:9000). You can reattach to the screen session later if needed:

    ```bash
    screen -r "run"
    ```

Remember to replace placeholders like `/path/to/your/local/project` with your actual local project path. Let me know if you have any questions or need further clarification!
