# TVTime Flask API [![codecov](https://codecov.io/gh/Kwbmm/scraped-tvtime-api/branch/master/graph/badge.svg?token=CWB4FE67O1)](https://codecov.io/gh/Kwbmm/scraped-tvtime-api) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=tvtime-api&metric=alert_status)](https://sonarcloud.io/dashboard?id=tvtime-api)

This is a proof of concept of an API using TVTime service and not exploiting its own API system. This repository aims to provide at least the possibility of retrieving information about your own TV series that you are tracking on [TVTime](https://tvtime.com).

## The story (or reasons why this exists)
The existing [TVTime API](https://api.tvtime.com/doc) has 2 main drawbacks in my opinion:

  1. Requires the developer to send an email to TvTime for "approval". This greatly limits the possibility of creating new projects. If the project is not deemed worthy of the approval, you won't get any API key.
  2. The API cannot be used for personal usage.

Back in the days when I was using Plex, I had planned to create a plugin to automatically mark as 'watched' the episodes I was watching through Plex. A Plex plugin already existed, but it was unmantained and I had issues with it. I did ask TVtime for an API key. No response received. I put the project aside and moved on with my life.

Today, I am looking into learning Flask and so I thought about creating a free version of the API. Given what I have said, the API is limited to returning information on current followed shows and can be used to mark episodes as watched/unwatched. I don't expect to add more.

Regarding the second drawback: I don't really see why I am not allowed to access the data of the shows that I am watching and do whatever I like with it (privately or not), without asking for permission to a third-party (TvTime).

Finally, this "API" is nothing more than an automated way to log into your account.

## The future
My plan is to give a base from which people can start developing. It would be great seeing plugins for Plex, Emby and Jellyfin coming up.

## The idea
The way the API works is by providing some rest endpoints with Flask. When a request for the endpoint arrives, python `requests` takes care of forwarding the request to TVTime. TVTime cookies are handled internally by the Flask API.
```
    User──────>JSON request──────>Flask API──────>request───>TVTime.com──┐
                                                                         │
    User<─────JSON reply<─────Beautiful Soup scraping<──────response<────┘
```

The response returned by TVTime generally holds 2 cookies, which are stored internally in Flask: Flask generates a session cookie that the user will use to perform the requests.

The response returns the HTML page as well, which will be scraped with BeautifulSoup for useful information. The data will be rearragend and put inside a JSON file, that will be returned to the user.

## Requirements
Not many, except for a TVTime account. But if you are here, you probably already have one.

`requirements.txt` takes care of installing, through `pip` what is needed to run the API.


## Development

This codebase is written in Python 3 and requires `pip`.

`pip` and requirements are installed by running `make install`

## Testing and debugging
Tests can be run with `make test`. This will run the tests through `coverage` library to generate a coverage report.

If you wish, for debugging purposes, to run a single test, you can do so by running `python -m unittest discover -k test_name` (e.g. `python -m unittest discover -k test_when_unfollowing_show_should_ok`)

### Remote debugging
The project can be run inside a docker container, thus remote debugging is a possibility. Remote debugging allows the user to send actual requests through third-party clients (like Postman or from Chrome/Firefox built-in network tab) to this API.

**1) Prereqs:**
  - A python container on which you've already run the setup (i.e. `make install`)
  - VSCode with the python plugin installed

**2) Inside the container**

  - Run `FLASK_APP=<path_to_main.py>`
  - Run `make debug_remote`

A flask webserver should be started and waiting for new requests.

**3) In your VSCode**

You should have setup a `launch.json` inside `.vscode` folder. The file can be easily setup through VSCode remote debugging configuration wizard. Main points to highlights are:

  - The container runs the debug server on port 5678, so the port should be opened on container and the VSCode configuration should point to that port
  - The flask API runs on port 5000 inside the container. That port must be opened as well.
  - The VSCode config will contain a `pathMappings` object that needs to be setup properly. Specifically, `remoteRoot` should point to the folder containing this project inside the container, while `localRoot` should point to the folder on your local env (laptop).

Here's an example of my config:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Remote Attach",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "127.0.0.1",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/src/scraped-tvtime-api/"
                }
            ]
        }
    ]
}
```
If the `launch.json` is correctly setup, you should be able to attach to the remote debugger. If you place breakpoints in the code and try to hit the endpoints, VSCode should stop execution at the breakpoints.

## Usage

**Before using this API, please make sure that the backend on which you are running this Flask API can be accessed over secure http requests. Since you are sending login information containing your ID and password, you should NEVER send them on unsecure connections.**

### APIs
*The following API is a work in progress*

|**URL**|**Method**|**Data**|**Response**|
|---|---|---|---|
|/login   |POST   |username + password (in request body)   |session cookie   |
|/shows   |GET   | session cookie (in request header)   | List of series you are tracking   |
|/show/\<id\>   |GET   |session cookie (in request header)   |List of seasons + episodes for show `id`   |
|/show/\<id\>/follow   |PUT   |session cookie (in request header)   |Start following the show corresponding to `id`   |
|/show/\<id\>/follow   |DELETE   |session cookie (in request header)   |Stop following the show corresponding to `id`   |
|/episode/\<id\>/watched   |PUT   |session cookie (in request header)   |Mark episode `id` as watched   |
|/episode/\<id\>/watched   |DELETE   |session cookie (in request header)   |Mark episode `id` as not watched   |
