from flask import Blueprint,request
from flask_mail import Message
import os
import json
from models import FormModel
from models import EmailModel
from exts import db,mail
import re
import string
import random
from datetime import datetime


bp = Blueprint('user', __name__, url_prefix='/User')

@bp.route('/login')
def login():
    return '登录界面'

@bp.route('/SavePic',methods=["POST"])
def SavePic():
    pic_obj = request.files['file']
    file_path = os.path.join(r"./static", "{}".format(pic_obj.filename))
    pic_obj.save(file_path)
    return pic_obj.filename

@bp.route('/SaveFile',methods=["POST"])
def SaveFile():
    file_obj = request.files['file']
    file_path = os.path.join(r"./static","{}".format(file_obj.filename))
    file_obj.save(file_path)
    return file_obj.filename
    
@bp.route('/FormSubmit',methods=["POST"])
def FormSubmit():
    ruleForm = request.json.get('ruleForm')
    date = " ".join((re.findall(r'(.*)T(.*)\.(.*)', ruleForm['date1'])[0][0],
                    re.findall(r'(.*)T(.*)\.(.*)', ruleForm['date2'])[0][1]))
    captcha_model = EmailModel.query.filter_by(email=ruleForm['email']).first()
    if ruleForm['captcha'] == captcha_model.captcha.lower() or ruleForm['captcha'] == captcha_model.captcha:  
        new_Form = FormModel(name = ruleForm['name'],
                             region = ruleForm['region'],
                             date = date,
                             delivery = ruleForm['delivery'],
                             type = ','.join(ruleForm['type']),
                             resource = ruleForm['resource'],
                             desc = ruleForm['desc'],
                             imageName = ','.join(ruleForm['imageName']),
                             fileName = ','.join(ruleForm['fileName']),
                             email = ruleForm['email'],
                             captcha = ruleForm['captcha']
                             # imageName = ','.join([list(i.keys())[0] for i in ruleForm['image']]),
                             # imageUrl = ','.join([list(i.values())[0] for i in ruleForm['image']]).encode(),
                             # fileName = ','.join([list(i.keys())[0] for i in ruleForm['file']]),
                             # fileUrl = ','.join([list(i.values())[0] for i in ruleForm['file']]).encode()
                             # image = str(ruleForm['image']),
                             # file = str(['file'])
                             )
        print(new_Form)
        db.session.add(new_Form)
        db.session.commit()
        return json.dumps({"code":200,"msg":'注册成功'}, ensure_ascii=False)
    else:
        return json.dumps({"code":404,"msg":'验证码输入错误'}, ensure_ascii=False)

@bp.route('/SelectForms',methods=["GET"])
def SelectForms():
    forms = FormModel.query.all()
    
    forms_data = [{'id':form.id,
                  'name': form.name,
                  'region': form.region,
                  'date': form.date,
                  'delivery':str(form.delivery) ,
                  'type': form.type.split(','),
                  'resource': form.resource,
                  'desc': form.desc,
                  'imageName':form.imageName.split(','),
                  'fileName':form.fileName.split(','),
                  'email':form.email,
                   # 'imageName': form.imageName.split(','),
                   # 'imageUrl': form.imageUrl.split(','),
                   # 'fileName': form.fileName.split(','),
                   # 'fileUrl': form.fileUrl.split(',')
                  # 'image':re.findall(r'\[(.*)\]',form.image)[0].split(','),
                  # 'file':re.findall(r'\[(.*)\]',form.file)[0].split(',')
                  } for form in forms]
    print(forms_data)
    return json.dumps(forms_data, ensure_ascii=False)

@bp.route('/DeleteForm',methods=["POST"])
def DeleteForm():
    delete_id = request.json.get('delete_id')
    delete_form = FormModel.query.filter_by(id=delete_id).first()
    db.session.delete(delete_form)
    db.session.commit()
    return json.dumps({"code":200}, ensure_ascii=False)
    
@bp.route('/SendEmail',methods=["POST"])
def SendEmail():
    email = request.json.get('email')
    letters = string.ascii_letters + string.digits
    captcha = ''.join(random.sample(letters,6))
    body_content = '【活动提交验证码】验证码：{}。尊敬的用户，您正在办理活动注册提交，我们不会向您索要此验证码，切勿告知他人。'.format(captcha)
    if email:  
        message = Message(subject='活动提交验证码',
                          recipients=[email],
                          body = body_content)
        mail.send(message)
        email_model = EmailModel.query.filter_by(email = email).first()
        if email_model:
            email_model.captcha = captcha
            email_model.create_time = datetime.now()
            db.session.commit()
        else:
            new_email_model = EmailModel(email = email,
                                          captcha = captcha)
            db.session.add(new_email_model)
            db.session.commit()
        return json.dumps({"code":200,'msg':'邮箱发送成功！'}, ensure_ascii=False)
    else:
        return json.dumps({"code":404,'msg':'邮箱发送失败！'}, ensure_ascii=False)
    
# @bp.route('/SendEmail',methods=["POST"])
# def SendEmail():
#     email = request.json.get('email')
#     letters = string.ascii_letters + string.digits
#     captcha = ''.join(random.sample(letters,6))
#     print(captcha)
#     body_content = '【活动提交验证码】验证码：{} 。尊敬的用户，您正在办理活动注册提交，我们不会向您索要此验证码，切勿告知他人。'.format(captcha)
#     if email:  
#         message = Message(subject='活动提交验证码',
#                           recipients=[email],
#                           body = body_content)
#         mail.send(message)
#         return json.dumps({"code":200,'captcha':str(captcha),'msg':'邮箱发送成功！'}, ensure_ascii=False)
#     else:
#         return json.dumps({"code":404,'msg':'邮箱发送失败！'}, ensure_ascii=False)