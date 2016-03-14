# code_401_wk2_http
Code 401 week 2 HTTP server project

Step 1:
  - open listening socket using socket library
  - server loop to take incoming requests and send them back
  - client loop to receive requests and return them to console


Step 2:
  - response_ok function to send HTTP 200 code response
  - response_error function to send HTTP 500 server error response


Step 3:
  - added request validation
  - added error codes for bad requests
  - extract URI from valid response.
  - return appropriate HTTP response to client


Step Final:
  - added gevent to support server concurrency
  - modified tests to be OS independent (in parallel with step 3)
