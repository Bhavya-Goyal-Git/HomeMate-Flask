from . import celery
from celery.schedules import crontab
from .mailing import format_message,send_email
from ..models import db
from ..models.tables import ServiceRequest, Professional, Customer
from sqlalchemy.sql import func
from sqlalchemy import and_
import datetime
from dateutil.relativedelta import relativedelta
from .csvexport import export_to_csv
from flask_sse import sse
import time

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender,**kwargs):
    sender.add_periodic_task(crontab(hour=17,minute=0),mail_pending_serviceReq.s(),name="Professional's pending service requests Mailing")
    sender.add_periodic_task(crontab(hour=17,minute=0),mail_tomorrow_requests.s(),name="Professional Tomorrow service requests Mailing")
    sender.add_periodic_task(crontab(hour=7,minute=0,day_of_month=1),mail_customer_reports.s(),name="Customer Monthly reports")

@celery.task(bind=True)
def ServiceRequestTableExport(self):
    sdata = ServiceRequest.query.all()
    time.sleep(6)
    r = export_to_csv(sdata)
    if r[0]:
        sse.publish({"status":"success","filename":r[1]},type="message",channel=self.request.id)
    else:
        sse.publish({"status":"fail"},type="message",channel=self.request.id)

@celery.task()
def mail_pending_serviceReq():
    pending = pending = db.session.query(Professional,func.count(ServiceRequest.id)).join(ServiceRequest.professional).group_by(Professional.id).filter(ServiceRequest.status=="booked").all()
    for prof,count in pending:
        if count!=0:
            d = {"name":prof.name, "email_address":prof.user_data.email_address, "pending":count}
            send_service_email.delay(d)

@celery.task()
def mail_tomorrow_requests():
    tomoro =  datetime.date.today() + datetime.timedelta(days=1)
    p = db.session.query(ServiceRequest,Customer,Professional).join(ServiceRequest.customer).join(ServiceRequest.professional).filter(ServiceRequest.dateofcompletion==tomoro).filter(ServiceRequest.status=="accepted").all()
    d= {}
    for srq,cus,prof in p:
        try:
            d[f"PID{prof.id}"]["requests"].append({
                "service_id":f"SID{srq.id}",
                "customer_name":cus.name,
                "customer_base_address":cus.base_address,
                "customer_city":cus.city,
                "customer_pincode":cus.pincode,
                "customer_state":cus.state
            })
        except:
            d[f"PID{prof.id}"] = {
                "email_address":prof.user_data.email_address,
                "pname":prof.name,
                "tomorrow_date":tomoro.strftime('%d-%m-%Y'),
                "requests":[{
                "service_id":f"SID{srq.id}",
                "customer_name":cus.name,
                "customer_base_address":cus.base_address,
                "customer_city":cus.city,
                "customer_pincode":cus.pincode,
                "customer_state":cus.state
            }]
            }
    for pid in d:
        send_tomorrow_email.delay(d[pid])
    
@celery.task()
def mail_customer_reports():
    prev_month_first = (datetime.date.today().replace(day=1) - relativedelta(months=1)).replace(day=1)
    cdata = Customer.query.all()
    for cust in cdata:
        sreqs = ServiceRequest.query.filter(and_(ServiceRequest.customer_id==cust.id,ServiceRequest.dateofrequest>=prev_month_first)).order_by(ServiceRequest.dateofrequest).all()
        d={"email_address":cust.user_data.email_address,"cname":cust.name,"requests":[]}
        for sreq in sreqs:
            d["requests"].append({"service_id":f"SID{sreq.id}",
                                "service":sreq.professional.service_type.title,
                                "professional":sreq.professional.name,
                                "dateofrequest":sreq.dateofrequest.strftime('%d-%m-%Y'),
                                "dateofcompletion":sreq.dateofcompletion.strftime('%d-%m-%Y'),
                                "status":sreq.status,
                                "bill":sreq.total_bill if sreq.total_bill else 0
                                })
        if len(d["requests"])>0:
            d["month"] = prev_month_first.strftime('%B')
            d["total_services"] = len(d["requests"])
            d["statuses"] = {}
            d["total_spend"] = 0
            for s in d["requests"]:
                d["statuses"][s["status"]] = d["statuses"].get(s["status"],0)+1
                d["total_spend"]+=s["bill"]
            send_customer_report.delay(d)

@celery.task()
def send_service_email(data):
    #data must have data to render in jinja template as well as email_adress to use here
    message = format_message("pending_request.html",data) #fill a template here
    send_email(data["email_address"],subject="Pending Service Requests!",message=message) #fill the subject here

@celery.task()
def send_tomorrow_email(data):
    message = format_message("tomorrow_request.html",data)
    send_email(data["email_address"],subject="Service Requests for Tomorrow!",message=message)

@celery.task()
def send_customer_report(data):
    message = format_message("customer_report.html",data)
    send_email(data["email_address"],subject="Customer Monthly Report!",message=message)