
from flask import Flask, request,make_response
from flask_cors import CORS
import json
#from flask_sqlalchemy import SQLAlchemy

#initialize frame
app = Flask(__name__)
#browser security protocal
CORS(app, supports_credentials=True)

teachers=[{'id':1,'name':'admin','password':'1234'}]
teachers_id=0
#initialize database
#mysql=SQLAlchemy(app)
#database type+drive type://username:password@database address:API/database used
#app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:12345678@localhost:3306/project'
#app.config['SQLALCHEMY_ECHO'] = True
#mysql.init_app(app)

@app.after_request
def after_request(resp):
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.before_request
def before_request():
    if request.path=='/login' or request.path== '/':
        return None
    if request.cookies.get('id') is None:
        return response(999,'please re-login')
    return None

@app.route('/teacher_lists',methods=['Get'] )
def teacher_lists():
    #teachers_list=[]
    #sql='select * from teachers'
    #rets=query(sql)
    #if len(rets)>0:
     #   for idx, row in enumerate(rets):
      #      teachers_list.append({'id':row['id'],'name':row['name']})
    return response(0,'ok',teachers)
@app.route('/teacher_add',methods=['POST'] )
def teacher_add():
    global teachers_id,teachers
    if str(request.data)=='':
        return response(1,'index error')
    tea={"id":0,"name":"","password":''}

    data=json.loads(request.data)

    if 'name' in data:
        tea["name"]=data["name"]
    else:
        return response(1,'enter name')
    if 'password' in data:
        tea["password"]=data["password"]
    else:
        return response(1,'enter password')

    teachers_id=teachers_id+1
    tea['id']=teachers_id
    teachers.append(tea)
    return response(0,'ok')

@app.route('/teacher_delete',methods=['POST'] )
def teacher_delete():
    global teachers_id,teachers
    if str(request.data)=='':
        return response(1,'index error')
    param=json.loads(request.data)
    if 'id' not in param:
        return response(1,'index error')
    deletedata(teachers,param['id'])
    return response(0,'Deleted')
@app.route('/teacher_edit',methods=['POST'] )
def teacher_edit():
    global teachers_id, teachers
    if str(request.data)=='':
        return response(1,'index error')
    param=json.loads(request.data)
    if 'id' not in param:
        return response(1,'index error')
    if 'name' in param and 'name' =='':
        return response(1,'name cannot be empty')
    if 'password' in param and 'password' =='':
        return response(1,'password cannot be empty')

    tea=searchdata(teachers,param['id'])
    if tea is None:
        return response(1,'teacher not found')
    if 'name' in param:
        if param['name'] == '':
            return response(1,'enter name')
        tea['name']=param['name']
    if 'password' in param:
        if param['password'] == '':
            return response(1,'enter password')
        tea['password']=param['password']
    editdata(teachers,param['id'],tea)
    return response(0,'updated')



students=[]
student_id=0
def searchdata(list,id):
    for i in range(len(list)):
        if list[i]['id'] == id:
            return list[i]
    return None
def editdata(list,id,data):
    for i in range(len(list)):
        if list[i]['id'] == id:
            list[i] = data
            return
    return

def deletedata(list,id):
    for i in range(len(list)):
        if list[i]['id'] == id:
            del list[i]
            return
    return

#def query(sql,param=None):
 #   ress=mysql.session.execute(sql,param)
  #  data=[dict(zip(result.keys(),result)) for result in ress]
   # return data

@app.route('/login',methods=['POST'] )
def login():

    param=json.loads(request.data)
    if 'name' not in param:
        return response(1000,'enter your name')
    if 'password' not in param:
        return response(1001,'enter your password')
    #sql="SELECT * FROM teachers WHERE name=:name"
    #ret=query(sql,{'name':param['name']})
    #print(ret)
    #if len(ret)>0 and ret[0]['password']==param['password']:
     #   resp = response(0, 'ok', {'id':ret[0]['id'], 'name': ret[0]['name']})
      #  resp.set_cookie('id',str(ret[0]['id']), max_age=3600)
       # return resp
    for i in range(len(teachers)):
       if teachers[i]['name'] == param['name'] and teachers[i]['password'] == param['password']:
            resp=response(0,'ok',{'id':teachers[i]['id'],'name':teachers[i]['name']})
            resp.set_cookie('id',str(teachers[i]['id']),max_age=3600)
            return resp
    return response(2000,'unauthorized')

@app.route('/logout',methods=['POST'] )
def logout():
    resp=response(0,'logged out')
    resp.delete_cookie('id')
    return resp

def response(code,message,data:any=None):
    res={'code':code,'message':message,'data':{}}
    if data is not None:
        if hasattr(data,'__dict__'):
            res['data']=data.__dict__
        else:
            res['data']=data
    return make_response(json.dumps(res,sort_keys=True,ensure_ascii=False),200)


@app.route('/student_lists',methods=['Get'] )
def student_lists():

    return response(0,'ok',students)


@app.route('/student_add',methods=['POST'] )
def student_add():
    global students, student_id
    if str(request.data)=='':
        return response(1,'index error')
    stu={"id":0,"name":"","math":0,"english":0,"physics":0}

    data=json.loads(request.data)
    if 'name' in data:
        stu["name"]=data["name"]
    else:
        return response(1,'enter name')
    if 'math' in data:
        stu["math"]=data["math"]
    if 'english' in data:
        stu["english"]=data["english"]
    if 'physics' in data:
        stu["physics"]=data["physics"]
    student_id=student_id+1
    stu['id']=student_id
    students.append(stu)
    return response(0,'ok')

@app.route('/student_delete',methods=['POST'] )
def student_delete():
    global students, student_id
    if str(request.data)=='':
        return response(1,'index error')
    param=json.loads(request.data)
    if 'id' not in param:
        return response(1,'index error')
    deletedata(students,param['id'])
    return response(0,'Deleted')

@app.route('/student_edit',methods=['POST'] )
def student_edit():
    global students
    if str(request.data)=='':
        return response(1,'index error')
    param=json.loads(request.data)
    if 'id' not in param:
        return response(1,'index error')
    if 'name' not in param:
        return response(1,'name cannot be empty')
    stu=searchdata(students,param['id'])
    if stu is None:
        return response(1,'student not found')
    if 'name' in param:
        stu['name']=param['name']
    if 'math' in param:
        stu['math']=param['math']
    if 'english' in param:
        stu['english']=param['english']
    if 'physics' in param:
        stu['physics']=param['physics']
    editdata(students,param['id'],stu)
    return response(0,'updated')

if __name__ == '__main__':
    app.run(port=9000)