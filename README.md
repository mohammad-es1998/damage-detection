## Damage Detection Project

This project aims to detect damage using a machine learning model. It provides a backend service for damage detection and integrates with a frontend application for a user-friendly interface.

### Getting Started

To run the backend service, follow these steps:

```bash
docker build --network host -t damage-detection:dev .
docker run -d --network host damage-detection:dev
```

After running the backend service, you can access the Swagger documentation for the API at http://127.0.0.1:5002/apidocs.

### Frontend Repository
For the frontend application, you can find the repository at https://github.com/mohammad-es1998/damage-detection-front. Follow the instructions in that repository to set up and run the frontend.

### Running Locally
If you want to run the project on your own computer, you can use the provided Dockerfile. Follow the instructions above to build and run the Docker container.

