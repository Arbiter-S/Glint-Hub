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
   
2. **Environment Variables**
The following environment variables are required to run the application:  

- `API_KEY` - API key to use for a third party service to fetch gold price. Check [this](https://www.navasan.tech/api/) for more info. (Optional: Default values for gold price have been implemented.) 
- `SETTINGS` - The mode to run the project in. You can either set "DEV" or "PRO" which changes the settings file to use. (Optional: Development settings are used by default.)
- `SECRET_KEY` - The secret key for Django
- `DB_NAME` - The name of the database 
- `DB_USER` - The database username
- `DB_PASSWORD` - The database password

    Make sure to define these variables in a `.env` file or your environment before running the application.

3. **Run with Docker Compose:**
   Ensure Docker and Docker Compose are installed afterwards run the following command:
   ```bash
   docker-compose up --build
   ```

4. **Access the API:**
GlintHub provides comprehensive API documentation:

- **Swagger UI**: An interactive interface for exploring and testing the API is available at:  
  `http://localhost/api/docs/ui/`

- **OpenAPI Schema**: For the full API schema in YAML format, visit:  
  `http://localhost/api/docs/`



## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

