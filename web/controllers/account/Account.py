from flask import Blueprint,request,redirect,jsonify

from application import db
from common.libs.Helper import ops_render,getCurrentDate
from common.models.User import User
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService


router_account = Blueprint("account_page",__name__)

@router_account.route('/index')
def index():
    resp_data = {}
    list = User.query.all()
    resp_data['list'] = list
    return ops_render('account/index.html',resp_data)

@router_account.route('/info')
def info():
    resp_data = {}
    req = request.args
    uid = int(req.get('id',0))
    reback_url =UrlManager.buildUrl('/account/index')
    if uid < 1:
        return redirect(reback_url)
    info = User.query.filter_by(uid=uid).first()

    if not info:
        return redirect(reback_url)

    resp_data['info'] = info
    return ops_render('account/info.html',resp_data)

@router_account.route('/set',methods=['GET','POST'])
def set():
    if request.method == 'GET':
        resp_data = {}
        req = request.args
        uid = int(req.get('id',0))
        info = None
        if uid :
            info = User.query.filter_by(uid=uid).first()
        resp_data['info'] = info
        return ops_render('account/set.html',resp_data)
    # POST
    resp = {
        'code':200,
        'msg':'操作成功！',
        'data':{}
    }

    # ajax 发送的数据
    req = request.values
    id = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''
    mobile = req['mobile'] if 'mobile' in req else ''
    email = req['email'] if 'email' in req else ''
    login_name = req['login_name'] if 'login_name' in req else ''
    login_pwd = req['login_pwd'] if 'login_pwd' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的用户名'
        return jsonify(resp)
    
    if mobile is None or len(mobile) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的手机号'
        return jsonify(resp)
    
    if email is None or len(email) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的邮箱'
        return jsonify(resp)
    
    if login_name is None or len(login_name) < 1:
        resp['code'] = -1
        resp['msg'] = '请输入正确的登录账号'
        return jsonify(resp)
    
    if login_pwd is None or len(login_pwd) < 6:
        resp['code'] = -1
        resp['msg'] = '请输入正确的密码长度'
        return jsonify(resp)
    
    is_exsits = User.query.filter(User.login_name == login_name).first()
    if is_exsits:
        resp['code'] = -1
        resp['msg'] = '该登录名已存在!'
        return jsonify(resp)

    user_info = User.query.filter_by(uid = id).first()
    if user_info:
        model_user = user_info
    else:
        model_user = User()
        model_user.created_time = getCurrentDate()
        model_user.login_salt = UserService.generateSalt()
    model_user.nickname = nickname
    model_user.mobile = mobile
    model_user.email = email
    model_user.login_name = login_name
    model_user.login_pwd = login_pwd


    aa = User.query.all()[-1]
    uid = aa.uid + 1
    model_user.avatar = 1
    model_user.uid = uid

    model_user.updated_time = getCurrentDate()
    db.session.add(model_user)
    db.session.commit()

    return jsonify(resp)