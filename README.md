# SDRTrunk Uploader
This is an middleware for SDRTrunk to upload to Rdio-Scanner's API. This middleware runs on Flask and accepts connections from SDRTrunk by mimicing the Broadcastify Calls API. For more information about the Broadcastify Calls API, please visit [their wiki](https://wiki.radioreference.com/index.php/Broadcastify-Calls-API)

## Setup
This guide assumes you have both [SDRTrunk](https://github.com/DSheirer/sdrtrunk) and [Rdio-Scanner](https://github.com/chuot/rdio-scanner/) installed and configure. On Rdio-Scanner, you need to a system and an API Key defined. This middleware assumes that Rdio-Scanner has the `/api` endpoint accessible. 

### Install and Run
You can run this locally (Gunicorn) or via Docker. 
#### Variables
You can use the .env.example file to create a .env file if you are running locally, or utilize the docker environmental variables for setting the container arguments.<br>
<br>
The configurable variables are
```
MIDDLEWARE_URL= (default http://127.0.0.1:8080) - the URL that the middleware is publicly accessible. This is used as a return URL for SDRTrunk.
LISTENING_PORT - (default 8080) port that the middleware is listening on
LISTENING_ADDRESS - (default 0.0.0.0) the IP address that Flask binds to
RDIO_SCANNER_URL - (default http://127.0.0.1:3000) the URL for the Rdio-Scanner instance
CAPTURE_DIR - (default /var/tmp) the directory the JSON metadata is sent to
WORKERS - (default 2) the number of workers for Flask (should be no more than 2n+1 where n is the number of CPU cores)
```

#### Gunicorn
Gunicorn is a WSGI for Flask. You can run it in the background. You need to clone repository, then install the Python requirements.
```
git clone https://github.com/rml596/sdrtrunk-uploader.git
cd sdrtrunk-uploader.git 
pip3 install -r requirements.txt
```
Once you have the requirments installed, you can run Gunicorn via
```
gunicorn server:app --config gunicorn.py
```

You can run Gunicorn as a systemd process, but that is out of scope. Follow [this guide](https://www.edmondchuc.com/blog/deploying-python-flask-with-gunicorn-nginx-and-systemd) for more information.
#### Docker
To run via docker, you must have docker installed. Run the following to bring up the container.

```
docker run -d \
-p 8080:8080 \
-e MIDDLEWARE_URL=http://127.0.0.1 \
-e RDIO_SCANNER_URL=http://host.docker.internal:3000 \
robertlynch3/sdrtrunk-uploader:latest
```
Use the [docker-compose.yml](docker-compose.yml) file for reference. You can run this as a stand-alone container or incorporate it into an existing Rdio-Scanner docker-compose. In either instance, make sure that the `RDIO_SCANNER_URL` variable has the correct URL. 


### Configure
#### SDRTrunk Configuration
This middleware mimics the Broadcastify Calls API. To configure SDRTrunk, you should create a new Streaming configuration as documented in [SDRTrunk's wik](https://github.com/DSheirer/sdrtrunk/wiki/Playlist-Editor#how-to-setup-broadcastify-calls). Use the `System ID` and `API Key` from Rdio-Scanner and the `Broadcastify URL` should match the `MIDDLEWARE_URL` variable.

## Broadcastify Flow
[Broadcastify Calls API](https://wiki.radioreference.com/index.php/Broadcastify-Calls-API) has a flow has two steps. First, the SDR software `POSTS` the metadata (systemId, talkgroup, unit id, etc) to the Calls API, Broadcastify process that data and will send back a message to either send the audio or to skip it. If the API returns a `0`, indicating that Broadcastify has accepted the call. In this return message, Broadcastify also sends back a unique URL to upload the call to. The SDR then will `PUT` the file to that unique URL.


# Issues
Please report any issues via [GitHub issues](https://github.com/rml596/sdrtrunk-uploader/issues).