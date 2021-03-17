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
