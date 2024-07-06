# Leyline Technical Challenge

## Instructions
-  `docker-compose build --no-cache`
-  `docker-compose up -d`
-  on your browser go to: `http://127.0.0.1:5001/`
-  choose a file by clicking `browse`
-  press the `upload`
-  wait for progress bar to fill
-  observe video to appear on webpage

## Solution:
- One of the big challenges was providing a solution on the form submission and how to pass the data from the backend back to the front. Usually, with a form submission, it requries a redirect. I subverted the redirect by adding a event listener to the submit event.
- After that, I needed to pass the data back still. I piggybacked off a query parameter that goes back to the index page. 
- Back to my listener method, I make a ajax call in conjunction with server sent events to listen to the progress.
- Once completion is observed, I attach the finished video to an iframe, so that subsequent processing won't affect the playback of the first video.

- I made the front end check for existing in progress jobs, and resumes the progress bar

## Limitations and areas of improvement:

- There is a slight visual issue with the progress bar when there are multiple jobs queued, but it does not affect the queue or the progress.
- The docker image uses the development server, this would be replaced by nginx, caddy or other production server
- Right now, the queue is relying on redis/rq solely. If this was to be deployed in production, I would most likely add a database component on top for robustness
- Data being passed from backend to frontend after the queue is started is not how I would implement it regularly, but is sufficient for the purposes of this demo. If there is a login component, I would associate the jobs with the user, or if there isn't then maybe some session cookie to persist the job information.
- In prod, the dynamic video would be streamed instead of loading a static video