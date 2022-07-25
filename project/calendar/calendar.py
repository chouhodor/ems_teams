from fileinput import filename
from flask import Blueprint, render_template, request, current_app, flash
from flask.helpers import url_for
from flask.wrappers import Request
from prompt_toolkit import HTML
from werkzeug.utils import redirect 
from flask_login import login_required, current_user
from datetime import date, datetime, timedelta
from ..models import Logs, User, OAuth, Events
from .. import db 
from werkzeug.utils import secure_filename
from google.cloud import storage
from dateutil.relativedelta import relativedelta
import calendar
import uuid as uuid
import os
import time


calendar = Blueprint('calendar', __name__, template_folder='templates', static_folder='static')

##################GOOGLE CLOUD BUCKET#####################
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ems-teams.json"
storage_client = storage.Client()
bucket = storage_client.get_bucket('event-file')

def remove_breaks(s):
    return s.replace('\r', '').replace('\n', '<br>').replace("'", '"')

def dateform(y):
    y = datetime.strptime(y, "%d/%m/%Y")
    y = y.strftime("%Y-%m-%d")
    return y

def insert_breaks(s):
    return s.replace('<br>', '\n')

@calendar.route('/')
@login_required
def index():
    date_times = datetime.now().strftime("%d/%m/%Y")
    current_month = str(datetime.now().month -1)
    event_standby = Events.query.order_by(Events.tarikh).filter(Events.status == 'aktif').all()
    user_role = User.query.all()

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
    current_month=current_month,
    user_role=user_role,
    insert_breaks=insert_breaks,
    remember=True
    )

@calendar.route('/selesai')
@login_required
def selesai():
    date_times = datetime.now().strftime("%d/%m/%Y")
    current_month = str(datetime.now().month -1)
    event_standby = Events.query.order_by(Events.tarikh).filter(Events.status == 'selesai').all()
    user_role = User.query.all()

    timeframe = date.today() + timedelta(days=365)

    def splitter(link):
        name, extension = os.path.splitext(str(link))
        link=extension
        return link

    try:
      username = current_user.username   
    except:
      username = None


    return render_template('selesai.html',
    username = username,
    event_standby=event_standby,
    date_times = date_times,
    splitter=splitter,
    nav_index = True,
    current_month=current_month,
    user_role=user_role
    )

@calendar.route('/logs')
@login_required
def logs():
    date_times = datetime.now().strftime("%d/%m/%Y")
    current_month = str(datetime.now().month -1)
    event_logs = Logs.query.order_by(Logs.tarikhmasa_log).all()
    user_role = User.query.all()

    timeframe = date.today() + timedelta(days=365)

    def splitter(link):
        name, extension = os.path.splitext(str(link))
        link=extension
        return link

    try:
      username = current_user.username   
    except:
      username = None


    return render_template('logs.html',
    username = username,
    event_logs=reversed(event_logs),
    date_times = date_times,
    splitter=splitter,
    nav_index = True,
    current_month=current_month,
    user_role=user_role
    )

#################### FORM ROUTES #########################


@calendar.route('/addevent', methods=['GET','POST'])
@login_required
def addevent():

    id = request.form['eventupdate-index']
    program = remove_breaks(request.form['program'])
    tarikh = dateform(request.form['tarikh'])
    masa = remove_breaks(request.form['masa'])
    tempat = remove_breaks(request.form['tempat'])
    vvip = remove_breaks(request.form['vvip'])
    ephysician = remove_breaks(request.form['ephysician'])
    med_officer = remove_breaks(request.form['med_officer'])
    med_assistant = remove_breaks(request.form['med_assistant'])
    snurse = remove_breaks(request.form['snurse'])
    driver = remove_breaks(request.form['driver'])
    nota = remove_breaks(request.form['nota'])
    uploaded_file1 = request.files['file1']

    user = current_user.id
    print(uploaded_file1.filename)
    if uploaded_file1.filename != '':
        filename1 = str(uuid.uuid1()) + "." + secure_filename(os.path.splitext(uploaded_file1.filename)[1])    
    else:
        filename1 = ''

    if request.method == 'POST':
        if filename1 != '':
            file1_ext = os.path.splitext(filename1)[1]
            if file1_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                #abort(400)
                flash('Only upload jpg, png or pdf files', 'danger')
                print(filename1)
                return redirect(request.referrer)
            elif file1_ext == '':
                flash('Please upload appropriate file to File/image', 'danger')
                return redirect(request.referrer)

            else:
                blob1 = bucket.blob(filename1)
                if os.path.splitext(filename1)[1] == '.pdf':
                    blob1.upload_from_string(uploaded_file1.read(), content_type='application/pdf')
                else:
                    blob1.upload_from_string(uploaded_file1.read())
                file1_id = filename1

        else:
            file1_id = None



        new_event = Events(user_id=user, program=program.upper(), tarikh=tarikh, masa=masa, tempat=tempat, vvip=vvip, ephysician = ephysician, 
        med_officer=med_officer, med_assistant=med_assistant, snurse=snurse, driver=driver,
            nota=nota, created_by=current_user.username,
            file1_id=file1_id
            )
        
        new_log = Logs(program_log=program.upper(), tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, event_change='Program baru')
        db.session.add(new_log)

        db.session.add(new_event)
        db.session.commit()



        return redirect(request.referrer)

@calendar.route('/updateevent_admin', methods=['GET','POST'])
@login_required
def updateevent_admin():

    id = request.form['eventupdate-index']
    program = remove_breaks(request.form['program'])
    tarikh = dateform(request.form['tarikh'])
    masa = remove_breaks(request.form['masa'])
    tempat = remove_breaks(request.form['tempat'])
    vvip = remove_breaks(request.form['vvip'])
    ephysician = remove_breaks(request.form['ephysician'])
    med_officer = remove_breaks(request.form['med_officer'])
    med_assistant = remove_breaks(request.form['med_assistant'])
    snurse = remove_breaks(request.form['snurse'])
    driver = remove_breaks(request.form['driver'])
    nota = remove_breaks(request.form['nota'])
    uploaded_file1 = request.files['file1']

    user = current_user.id
    '''
    if uploaded_file1.filename != '':
        filename1 = str(uuid.uuid1()) + "." + secure_filename(os.path.splitext(uploaded_file1.filename)[1])    
    else:
        filename1 = ''
    '''
    if request.method == 'POST':
        update_events = Events.query.get(id)
        if uploaded_file1.filename != '':
            filename1 = str(uuid.uuid1()) + "." + secure_filename(os.path.splitext(uploaded_file1.filename)[1]) 
            file1_ext = os.path.splitext(filename1)[1]
            if file1_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                flash('Only upload jpg, png or pdf files', 'danger')
                print('error1')
                return redirect(request.referrer)
            elif file1_ext == '':
                flash('Please upload appropriate file to File/image', 'danger')
                print('error2')
                return redirect(request.referrer)
            else:
                new_file1_id = filename1
                blob1 = bucket.blob(filename1)
                if os.path.splitext(filename1)[1] == '.pdf':
                    blob1.upload_from_string(uploaded_file1.read(), content_type='application/pdf')
                else:
                    blob1.upload_from_string(uploaded_file1.read())
                update_events.file1_id = new_file1_id

        else:
            pass

        update_events.program = program
        update_events.tarikh = tarikh
        update_events.masa = masa
        update_events.tempat = tempat
        update_events.vvip = vvip
        update_events.ephysician = ephysician
        update_events.med_officer = med_officer
        update_events.med_assistant = med_assistant
        update_events.snurse = snurse
        update_events.driver = driver
        update_events.nota = nota

        new_log = Logs(program_log=program.upper(), tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, 
                        event_change='Program dikemaskini oleh admin')
        db.session.add(new_log)
           
        db.session.commit()
        return redirect(request.referrer)
'''
@calendar.route('/updateevent_manager', methods=['GET','POST'])
@login_required
def updateevent_manager():

    id = request.form['eventupdate-index']
    ephysician = remove_breaks(request.form['ephysician'])
    med_officer = remove_breaks(request.form['med_officer'])
    med_assistant = remove_breaks(request.form['med_assistant'])
    snurse = remove_breaks(request.form['snurse'])
    driver = remove_breaks(request.form['driver'])
    nota = remove_breaks(request.form['nota'])
    uploaded_file1 = request.files['file1']

    user = current_user.id


    filename1 = str(uuid.uuid1()) + "." + secure_filename(os.path.splitext(uploaded_file1.filename)[1])    

    if request.method == 'POST':
        update_events = Events.query.get(id)
        if update_events.file1_id == '':
            if filename1 != '':
                file1_ext = os.path.splitext(filename1)[1]
                if file1_ext not in current_app.config['UPLOAD_EXTENSIONS']:
                    flash('Only upload jpg, png or pdf files', 'danger')
                    return redirect(request.referrer)
                elif file1_ext == '':
                    flash('Please upload appropriate file to File/image', 'danger')
                    return redirect(request.referrer)
                else:
                    new_file1_id = filename1
                    blob1 = bucket.blob(filename1)
                    if os.path.splitext(filename1)[1] == '.pdf':
                        blob1.upload_from_string(uploaded_file1.read(), content_type='application/pdf')
                    else:
                        blob1.upload_from_string(uploaded_file1.read())
                    update_events.file1_id = new_file1_id

            else:
                file1_id = None



        update_events.ephysician = ephysician
        update_events.med_officer = med_officer
        update_events.med_assistant = med_assistant
        update_events.snurse = snurse
        update_events.driver = driver
        update_events.nota = nota

        
            
           
        db.session.commit()
        return redirect(request.referrer)

'''
@calendar.route("/ephysician_form",methods=["POST"])
def ephysician_form():
    if request.method == "POST":
        id = request.form['index_ephysician']
        ephysician = request.form.get("ephysician")
        update_events = Events.query.get(id)
        update_events.ephysician = ephysician
        user = current_user.id

        new_log = Logs(program_log=update_events.program, tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, 
                        event_change='EP dikemaskini: '+ ephysician)
        db.session.add(new_log)

        db.session.commit()     

    return redirect(request.referrer)

@calendar.route("/med_officer_form",methods=["POST"])
def med_officer_form():
    if request.method == "POST":
        id = request.form['index_med_officer']
        med_officer = request.form.get("med_officer")
        update_events = Events.query.get(id)
        update_events.med_officer = med_officer
        user = current_user.id

        new_log = Logs(program_log=update_events.program, tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, 
                        event_change='MO dikemaskini: '+ med_officer)
        db.session.add(new_log)
        db.session.commit()     

    return redirect(request.referrer)

@calendar.route("/med_assistant_form",methods=["POST"])
def med_assistant_form():
    if request.method == "POST":
        id = request.form['index_med_assistant']
        med_assistant = request.form.get("med_assistant")
        update_events = Events.query.get(id)
        update_events.med_assistant = med_assistant
        user = current_user.id

        new_log = Logs(program_log=update_events.program, tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, 
                        event_change='PPP dikemaskini: '+ med_assistant)
        db.session.add(new_log)
        db.session.commit()     

    return redirect(request.referrer)

@calendar.route("/snurse_form",methods=["POST"])
def snurse_form():
    if request.method == "POST":
        id = request.form['index_snurse']
        snurse = request.form.get("snurse")
        update_events = Events.query.get(id)
        update_events.snurse = snurse
        user = current_user.id

        new_log = Logs(program_log=update_events.program, tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, 
                        event_change='SN dikemaskini: '+ snurse)
        db.session.add(new_log)
        db.session.commit()     

    return redirect(request.referrer)

@calendar.route("/driver_form",methods=["POST"])
def driver_form():
    if request.method == "POST":
        id = request.form['index_driver']
        driver = request.form.get("driver")
        update_events = Events.query.get(id)
        update_events.driver = driver
        user = current_user.id

        new_log = Logs(program_log=update_events.program, tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, 
                        event_change='PKB dikemaskini: '+ driver)
        db.session.add(new_log)
        db.session.commit()     

    return redirect(request.referrer)

@calendar.route('/padam_form', methods = ['POST'])
def padam_form():
    
    padam_id = Events.query.get(int(request.form['padam-index']))
    file1_path = padam_id.file1_id
    user = current_user.id

    if request.method == 'POST':
        db.session.delete(padam_id)
        try:
            blob1 = bucket.blob(file1_path)
            blob1.delete()
        except:
            pass

        new_log = Logs(program_log=padam_id.program, tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, 
                        event_change='Program dipadam')
        db.session.add(new_log)
        db.session.commit()
        return redirect(request.referrer)

@calendar.route('/selesai_form', methods = ['POST'])
def selesai_form():
    selesai_id = Events.query.get(int(request.form['selesai-index']))

    if request.method == 'POST':
        selesai_id.status = 'selesai'
        user = current_user.id
        new_log = Logs(program_log=selesai_id.program, tarikhmasa_log = datetime.now().strftime('%Y-%m-%d %H:%M:%S'), changer=current_user.username, user_id=user, 
                event_change='Status program: Selesai')
        db.session.add(new_log)
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