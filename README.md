# aanchal_ai

A new Flutter project.

## Getting Started

The frontend of the project is in flutter.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

# aanchal_ai_webapp_backend

**Pre-requisites**

You will need to run the Llama3 and Whisper service somewhere to support this app.
Currently, we are running it at http://10.222.76.205:8000.
In case you want to run it on your local system, download weights and use `android/llama3_service/llama3_hindi_whisper_service.py` to run this server.
*All required packages to be installed at your end. Check environment.yml for details.*

LLAMA3_SERVICE environment variable must be set accordingly.

### Docker run.

1. Copy all the codes to the server. Let <app_path> be the application path. `cd <app_path>`
2. Build the Docker image. `docker build -t aanchal-android .`
3. Run the service using following command.
```
docker run -d -p <host_port>:6000 -e LLAMA3_SERVICE=http://10.222.76.205:8000 -v <app_path>:/app aanchal-android
```

