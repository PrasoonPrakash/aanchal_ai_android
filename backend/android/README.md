# aanchal_ai_webapp

**Pre-requisites**

You will need to run the Llama3 and Whisper service somewhere to support this app.
Currently, we are running it at http://10.222.76.205:8000.
In case you want to run it on your local system, download weights and use `llama3_service/llama3_hindi_whisper_service.py` to run this server.
*All required packages to be installed at your end. Check environment.yml for details.*

LLAMA3_SERVICE environment variable must be set accordingly.

### Docker run.

1. Copy all the codes to the server. Let <app_path> be the application path. `cd <app_path>`
2. Build the Docker image. `docker build -t aanchal-android .`
3. Run the service using following command.
```
docker run -d -p <host_port>:6000 -e LLAMA3_SERVICE=http://10.222.76.205:8000 -v <app_path>:/app aanchal-android
```