from flask import Blueprint, render_template, request, current_app, flash
from flask.helpers import url_for
from flask.wrappers import Request
from prompt_toolkit import HTML
from werkzeug.utils import redirect 
from flask_login import login_required, current_user
from datetime import date, datetime, timedelta
from ..models import User, OAuth, Events
from .. import db 
from werkzeug.utils import secure_filename
from google.cloud import storage
from dateutil.relativedelta import relativedelta
from ..tbconfig import tb, channel_id
import calendar
import uuid as uuid
import os
import time


calendar = Blueprint('calendar', __name__, template_folder='templates', static_folder='static')

##################GOOGLE CLOUD BUCKET#####################
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "em-coursecalendar.json"
storage_client = storage.Client()
bucket = storage_client.get_bucket('emcc_date_bucket')

@calendar.route('/')
def index():
    date_times = datetime.now().strftime("%d/%m/%Y")
    current_month = str(datetime.now().month -1)
    event_standby = Events.query.all()

    timeframe = date.today() + timedelta(days=365)

    def splitter(link):
        name, extension = os.path.splitext(str(link))
        link=extension
        return link

    try:
      username = current_user.username   
    except:
      username = None


    return render_template('index.html',
    username = username,
    event_standby=event_standby,
    date_times = date_times,
    splitter=splitter,
    nav_index = True,
    current_month=current_month
    )


#################### FORM ROUTES #########################


@calendar.route('/addevent', methods=['GET','POST'])
@login_required
def addevent():

    def remove_breaks(s):
        return s.replace('\r', '').replace('\n', '<br>').replace("'", '"')

    def dateform(y):
        y = datetime.strptime(y, "%d/%m/%Y")
        y = y.strftime("%Y-%m-%d")
        return y

    id = request.form['eventupdate-index']
    name = remove_breaks(request.form['eventupdate-name'])
    location = remove_breaks(request.form['eventupdate-location'])
    startDate = dateform(request.form['eventupdate-start-date'])
    endDate = dateform(request.form['eventupdate-end-date'])
    description = remove_breaks(request.form['eventupdate-description'])
    link = request.form['eventupdate-link']
    linktype = request.form['eventupdate-linktype']
    public= bool(request.form.get('eventupdate-public'))
    file1_desc = request.form['eventupdate-description1']
    file2_desc = request.form['eventupdate-description2']
    uploaded_file1 = request.files['file1']
    uploaded_file2 = request.files['file2']

    user = current_user.id

    filename1 = str(uuid.uuid1()) + "." + secure_filename(os.path.splitext(uploaded_file1.filename)[1])
    filename2 = str(uuid.uuid1()) + "." + secure_filename(os.path.splitext(uploaded_file2.filename)[1])
    

    if request.method == 'POST':

        ################  data in database ##############
        if id != '':
            update_events = Events.query.get(id)
            if update_events.file1_id == '':
                if filename1 != '':
                    file1_ext = os.path.splitext(filename1)[1]
                    if file1_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                        flash('Only upload jpg, png or pdf files', 'danger')
                        return redirect(request.referrer)
                    elif file1_ext == '':
                        flash('Please upload appropriate file to File/image 1', 'danger')
                        return redirect(request.referrer)
                    else:
                        new_file1_id = filename1
                        blob1 = bucket.blob(filename1)
                        if os.path.splitext(filename1)[1] == '.pdf':
                            blob1.upload_from_string(uploaded_file1.read(), content_type='application/pdf')
                        else:
                            blob1.upload_from_string(uploaded_file1.read())
                        update_events.file1_desc = file1_desc
                        update_events.file1_id = new_file1_id

                else:
                    file1_desc = None
                    file1_id = None
            else:
                if file1_desc != '':
                    if filename1 != '':
                        file1_ext = os.path.splitext(filename1)[1]
                        if file1_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                            flash('Only upload jpg, png or pdf files', 'danger')
                            return redirect(request.referrer)
                        elif file1_ext == '':
                            flash('Please upload appropriate file to File/image 1', 'danger')
                            return redirect(request.referrer)
                        else:
                            try:
                                blob1 = bucket.blob(update_events.file1_id)
                                blob1.delete()
                            except:
                                pass
                            new_file1_id = filename1
                            blob1 = bucket.blob(filename1)
                            if os.path.splitext(filename1)[1] == '.pdf':
                                blob1.upload_from_string(uploaded_file1.read(), content_type='application/pdf')
                            else:
                                blob1.upload_from_string(uploaded_file1.read())
                            update_events.file1_desc = file1_desc
                            update_events.file1_id = new_file1_id
                    else:
                        file1_desc = None
                        file1_id = None
                else:
                    pass

            update_events.name = name
            update_events.location = location
            update_events.startDate = startDate
            update_events.endDate = endDate
            update_events.description = description
            update_events.link = link
            update_events.linktype = linktype
            update_events.public = public
            
           
            db.session.commit()
            return redirect(request.referrer)

        ########### data empty #################
        else:
            if filename1 != '' and file1_desc != '':
                file1_ext = os.path.splitext(filename1)[1]
                if file1_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    #abort(400)
                    flash('Only upload jpg, png or pdf files', 'danger')
                    return redirect(request.referrer)
                elif file1_ext == '':
                    flash('Please upload appropriate file to File/image 1', 'danger')
                    return redirect(request.referrer)

                else:
                    blob1 = bucket.blob(filename1)
                    if os.path.splitext(filename1)[1] == '.pdf':
                        blob1.upload_from_string(uploaded_file1.read(), content_type='application/pdf')
                    else:
                        blob1.upload_from_string(uploaded_file1.read())
                    file1_id = filename1

            else:
                file1_desc = None
                file1_id = None


            if filename2 != '' and file2_desc != '':
                file2_ext = os.path.splitext(filename2)[1]
                if file2_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    #abort(400)
                    flash('Only upload jpg, png or pdf files', 'danger')
                    return redirect(request.referrer)
                elif file2_ext == '':
                    flash('Please upload appropriate file to File/image 2', 'danger')
                    return redirect(request.referrer)

                else:
                    blob2 = bucket.blob(filename2)
                    if os.path.splitext(filename2)[1] == '.pdf':
                        blob2.upload_from_string(uploaded_file2.read(), content_type='application/pdf')
                    else:
                        blob2.upload_from_string(uploaded_file2.read())
                    file2_id = filename2
                
            else:  
                file2_desc = None
                file2_id = None

            new_event = Events(user_id=user, name=name, location = location, startDate = startDate, 
                endDate = endDate,description=description, created_by=current_user.username,
                link=link, linktype=linktype, public=public,
                file1_desc=file1_desc, file2_desc=file2_desc,
                file1_id=file1_id, file2_id=file2_id
                )

        user= User.query.get(current_user.id)
        user.bookmarks.append(new_event)
        db.session.add(new_event)
        db.session.commit()

        return redirect(request.referrer)


@calendar.route('/delete', methods = ['POST'])
def delete():

    delete_form = int(request.form['eventdelete-index'])
    delete_id = Events.query.get(delete_form)
    file1_path = delete_id.file1_id
    file2_path = delete_id.file2_id

    if request.method == 'POST':
        db.session.delete(delete_id)
        try:
            blob1 = bucket.blob(file1_path)
            blob1.delete()
        except:
            pass
        try:
            blob2 = bucket.blob(file2_path)
            blob2.delete()
        except:
            pass
        db.session.commit()
        return redirect(request.referrer)

'''
@calendar.route('/test')
def test():
    user = User.query.get(current_user.id)
    event = Events.query.get(2)
    print(user.bookmarks)
    #db.session.commit()
    return 'test'

'''