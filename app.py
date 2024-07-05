from flask import Flask, redirect, url_for, request, render_template, Response, flash, session, jsonify, make_response
from time import sleep

from rq import Queue
from rq.job import Job
from rq import get_current_job
from rq.registry import StartedJobRegistry

from redis import Redis

import time
import json
import os

r = Redis(os.environ.get('REDIS_URL','localhost'))
q = Queue(connection=r)


def ai_simulator(data):
    job = get_current_job()
    
    n=0
    top = 30
    while n < top: 
        job.meta['progress'] = n/top*100
        job.save_meta()
        time.sleep(1)
        n=n+1
    
    data = data.upper()
    return 'Processed %s' % (data,)

app = Flask(__name__, template_folder='.')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload():
    print('in upload')
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            value = uploaded_file.filename
            job = q.enqueue(ai_simulator, value)
    return redirect(url_for('index')+'?job_id='+job.id)

@app.route('/overview/')
def overview():
    registry = StartedJobRegistry('default', connection=r)

    running_job_ids = registry.get_job_ids()  # Jobs which are exactly running. 
    response_data = jsonify({'data': running_job_ids})
    resp = make_response(response_data, 201)
    return resp



@app.route('/progress/<string:job_id>')
def progress(job_id):
    def get_status():
        job = Job.fetch(job_id, connection=r)
        status = job.get_status()
        
        while status != 'finished':

            status = job.get_status()
            job.refresh()

            d = {'status': status}

            if 'progress' in job.meta:
                d['value'] = job.meta['progress']
            else:
                d['value'] = 0
                
            # IF there's a result, add this to the stream
            if job.result:
                d['result'] = job.result

            json_data = json.dumps(d)
            yield f"data:{json_data}\n\n"
            time.sleep(1)


    return Response(get_status(), mimetype='text/event-stream')