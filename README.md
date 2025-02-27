# GlintHub  

GlintHub is a feature-rich backend API built for an e-commerce platform specializing in gold products.
Developed with Django and Django REST Framework (DRF), it integrates essential functionalities such as real-time gold
price updates, user account verification through email, and secure payment processing using the Zarinpal gateway. 
With Nginx serving as a reverse proxy, GlintHub is optimized for performance, reliability, and scalability—making it
a robust solution for modern e-commerce needs.


## Running the project
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Arbiter-S/Glint-Hub.git
   cd Glint-Hub 
   ```
2. **Configure environment variables**
    
    GlintHub has two main modes in which you can run the project. One is development and the other is production.
    How the mode is selected depends on your environment variables and which docker compose file you run. Development mode allows
    you to use all the local features of your IDE while not having to wait for docker to build your containers for each small change,
    while production mode gives you a production-like environment and scalability. Before you can start the project you need
    to create a .env file inside the Docker directory. After that you need to have the following variables defined within 
    your .env file:

- `API_KEY` - API key to use for a third party service to fetch gold price. Check [this](https://www.navasan.tech/api/) for more info. (Optional: Default values for gold price have been implemented.) 
- `SETTINGS` - This variable determines what setting module is being used by django. set 'DEV' for development and 'PRO'
for production. This variable must match the docker compose file you run. For instance if you run docker-compose.development.yml
you should set this variable to 'DEV' otherwise the app won't function properly. (Optional: Development settings are used by default.) 
- `SECRET_KEY` - The secret key for Django. This value is not required if you are in development mode.
- `DB_NAME` - The name of the database 
- `DB_USER` - The database username
- `DB_PASSWORD` - The database password

    Make sure to define these variables in a `.env` file or your environment before running the application.

3. **Install the packages**

    This project supports package management via both pip and poetry. To install the required dependencies run the following commands
    ```bash
    # Create a virtual environment
    python -m venv venv
    
    # Activate the virtual environment
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    
    # Install dependencies using pip
    pip install -r requirements.txt
    
    # Alternatively, install dependencies using Poetry. Read more about poetry https://python-poetry.org/docs/
    poetry install
    ```

4. **Run with Docker Compose**

    Ensure Docker and Docker Compose are installed. Run the following command
    for production mode:
    ```bash
    docker-compose --file Docker\docker-compose.production.yml up
    ```
    Run the following commands for development mode in two different terminal tabs
    ```bash
    python manage.py runserver 80
    docker-compose --file Docker\docker-compose.development.yml up
    ```

5. **Access the API:**
GlintHub provides comprehensive API documentation:

- **Swagger UI**: An interactive interface for exploring and testing the API is available at:  
  `http://localhost/api/docs/ui/`

- **OpenAPI Schema**: For the full API schema in YAML format, visit:  
  `http://localhost/api/docs/`


## Testing
To run the tests run the following commands

- For **Windows**:
  
  Run the following command in powershell in project's root:
    ```powershell
    docker-compose --file Docker\docker-compose.development.yml up -d; pytest -vv; docker-compose --file Docker\docker-compose.development.yml down
    ```

- For **Linux(Bash or Zsh)**:

    Run the following command in the terminal in project's root:
    ```bash
    docker-compose --file Docker/docker-compose.development.yml up -d &&  pytest -vv && docker-compose --file Docker/docker-compose.development.yml down
    ```

These commands will start the containers, execute the tests on your local machine, and then shut down the
containers when the tests are complete.
## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

