# aanchal_ai_frontend

A new Flutter project.

## Getting Started

The frontend of the project is in flutter.

A few resources to get you started if this is your first Flutter project:

- [Lab: Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Cookbook: Useful Flutter samples](https://docs.flutter.dev/cookbook)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

# FRONTEND
 
The frontend of the app is built in flutter. 

## Building the APK file

After cloning the files into a local system, the APK file can be built using the following steps-
1. Install Flutter by using th eofficial instructions (https://docs.flutter.dev/get-started/install)
2. Install Android Studio and Android SDK
3. Add Flutter and Dart extensions to VS Code
4. Open VS Code and navigate to the project directory
5. Ensure that you are in the Flutter project root directory
6. In the terminal, run the following command- flutter pub get
   This will install all the necessary dependencies.
7. Run the following command to build the APK- flutter build apk

The APK file can be found in the following location - build/app/outputs/flutter-apk/

## Changing the IP address

Whenever the IP address needs to be changed, changes have to be made in the following files -
1. home.dart on line 51
2. loading_page.dart on line 41
3. prediction.dart on lines 29, 95, 194 and 242
4. conv.dart on line 57

The ports and the routes will remain the same.



# BACKEND

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

