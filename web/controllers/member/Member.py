# from flask import Blueprint,request,redirect,jsonify
# from common.libs.Helper import ops_render


# router_member = Blueprint("member_page",__name__)

# @router_member.route("/index")
# def index():
#     return ops_render("member/index.html")


from flask import Blueprint,request,redirect,jsonify

from application import db,app
from sqlalchemy import or_

from common.libs.Helper import ops_render,getCurrentDate,iPagination
from common.libs.UrlManager import UrlManager
from common.libs.user.UserService import UserService
from common.models.member.Member import Member

router_member = Blueprint("member_page",__name__)

@router_member.route('/index')
def index():
    resp_data = {}
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1
    query = Member.query
    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Member.status == int(req['status']))

    if 'mix_kw' in req:
        rule = or_(Member.nickname.ilike('%{0}%'.format(req['mix_kw'])),Member.mobile.ilike('%{0}%'.format(req['mix_kw'])))
        query = query.filter(rule)

    params = {
        'total':query.count(),
        'page':page,
        'page_size':1,
        # 'page_size':app.config['PAGE_SIZE'],可以用它来代替1
        'url':request.full_path.replace('&p={}'.format(page),'')
    }
    # 分页的三大关键字
    pages = iPagination(params)
    offset = (page-1)*1
    limit = 1*page


    list = query.all()[offset:limit]
    resp_data['list'] = list 
    resp_data['status'] = {
        '1':'正常',
        '0':'删除'
    }

    resp_data['pages'] = pages
    return ops_render('member/index.html',resp_data)

@router_member.route('/info')
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id",0))
    reback_url = UrlManager.buildUrl("/member/index")
    if id < 1:
        return redirect(reback_url)
    
    info = Member.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)
    
    resp_data['info'] = info
    return ops_render('member/info.html',resp_data)

@router_member.route('/set',methods=['GET','POST'])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int(req.get("id",0))
        info = None
        if id:
            info = Member.query.filter_by(id=id).first()
        resp_data['info'] = info
        return ops_render('member/set.html',resp_data)
    # POST  更新数据库
    resp = {
        'code':200,
        'msg':"操作成功",
        'data':{}
    }
    # ajax 发送的数据
    req = request.values
    ids = req['id'] if 'id' in req else 0
    nickname = req['nickname'] if 'nickname' in req else ''


    if nickname is None or len(nickname) < 1:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的昵称"
        return jsonify(resp)
   

    
    Member_info = Member.query.filter_by(id = ids).first()
    if Member_info:
        model_Member = Member_info
    else:
        model_Member = Member()
        model_Member.created_time = getCurrentDate()
        model_Member.login_salt = UserService.generateSalt()

    model_Member.nickname = nickname

    model_Member.id = 4
    model_Member.avatar = 1
    # if Member_info and Member_info.id == 1:
    #     resp['code'] = -1
    #     resp['msg'] = "该用户为Dws，不允许修改"
    #     return jsonify(resp)
    # model_Member.login_pwd = UserService.generatePwd(login_pwd,model_Member.login_salt)
    model_Member.updated_time = getCurrentDate()
    
    db.session.add(model_Member)
    db.session.commit()
    return jsonify(resp)



@router_member.route('removeOrRecover',methods=['GET','POST'])
def removeOrRecover():
    resp = {
        'code':200,
        'msg':'操作成功',
        'data':{}
    }
    
    req = request.values
    ids = req['id'] if 'id' in req else 0
    acts = req['acts'] if 'acts' in req else ''

    if acts not in ['remove','recover']:
        resp['code'] = -1
        resp['msg'] = '操作有误'
        return jsonify(resp)

    if id:
        Member_info = Member.query.filter_by(id=ids).first()
        if not Member_info:
            resp['code'] = -1
            resp['msg'] = '指定的账号不存在'
            return jsonify(resp)
        # if Member_info and Member_info.id == 1:
        #     resp['code'] = -1
        #     resp['msg'] = '该用户是大神，不能动'
        #     return jsonify(resp)

        if acts == 'remove':
            Member_info.status = 0
        elif acts == 'recover':
            Member_info.status = 1
        
        # user_info.status = 0
        Member_info.updated_time = getCurrentDate()
        db.session.add(Member_info)
        db.session.commit()
    return jsonify(resp)


