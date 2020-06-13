# TVTime Flask API - WIP

This is a proof of concept of an API using TVTime service and not exploiting its own API system. This repository aims to provide at least the possibility of retrieving information about your own TV series that you are tracking on [TVTime](https://tvtime.com).

## The idea
The way the API works is by providing some rest endpoints with Flask. When a request for the endpoint arrives, python `requests` takes care of forwarding the request to TVTime. TVTime cookies are handled internally by the Flask API.
```
    User───>JSON request───>Flask API───>request───>TVTime.com──┐
                                                                │
    User<─────JSON reply<─────Flask scraping<──────response<────┘
```

The response returned by TVTime generally holds 2 cookies, which are stored internally in Flask: Flask generates a session cookie that the user will use to perform the requests.

The response returns the HTML page as well, which will be scraped with BeautifulSoup for useful information. The data will be rearragend and put inside a JSON file, that will be returned to the user.

## Requirements
Not many, except for a TVTime account. But if you are here, you probably already have one.

`requirements.txt` takes care of installing, through `pip` what is needed to run the API.

## Usage

**Before using this API, please make sure that the backend on which you are running this Flask API can be accessed over secure http requests. Since you are sending login information containing your ID and password, you should NEVER send them on unsecure connections.**

### APIs
*The following API is a working in progress*

|**URL**|**Method**|**Data**|**Response**|
|---|---|---|---|
|/login   |POST   |username + password (in request body)   |session cookie   |
|/shows   |GET   | session cookie (in request header)   | List of series you are tracking   |
|/show/\<id\>   |GET   |session cookie (in request header)   |List of seasons + episodes for show `id`   |
