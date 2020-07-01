from flask import Flask, render_template, url_for, redirect, request, session
from students_arrangement import final_classroom

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'ul!H(QLNP=kr("VFL,)~'

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/studentslist', methods = ['GET', 'POST'])
def studentslist():
    if request.method == 'POST':
        studentslist = request.form['studentslist']
        if len(studentslist) == 0:
            return render_template('studentslist.html')
        for i in range(20): #I couldn´t find another solution to clean the form
            studentslist = studentslist.replace("\r\n\r\n", "\r\n")
        studentslist = studentslist.replace("\r","").split('\n')
        session['studentslist'] = studentslist
        st_dict = {}
        for k, v in enumerate(studentslist):
            st_dict[int(k)] = v
        session['st_dict'] = st_dict
        return redirect(url_for('studentspositioning'))

    return render_template('studentslist.html')


@app.route('/studentspositioning', methods = ['GET', 'POST'])
def studentspositioning():
    students_list_file = request.remote_addr + "_st.txt"
    studentslist = session.get('studentslist', None)
    st_front = []
    st_back = []

    if request.method == 'POST':
        for i in range(len(studentslist)):
            if request.form['seat'+str(i)] == "front":
                st_front.append(i)
            elif request.form['seat'+str(i)] == "back":
                st_back.append(i)
        session['st_front'] = st_front
        session['st_back'] = st_back
        return redirect(url_for('studentsgroups'))

    else:
        return render_template('studentspositioning.html', studentslist=studentslist)



@app.route('/studentsgroups', methods = ['GET', 'POST'])
def studentsgroups():
    studentslist = session.get('studentslist', None)
    st_enemies = []

    if request.method == 'POST':
        for i in range(1,11):
            _listtemp = []
            for st in request.form.getlist('Grupo'+str(i)):
                if (len(st)) > 2:
                    _listtemp.append(int(st[1:-1])) #receiving as '[0]', we just want 0.
            if len(_listtemp) > 0:
                st_enemies.append(_listtemp)
        session['st_enemies'] = st_enemies
        return redirect(url_for('classroom'))

    else:
        return render_template('studentsgroups.html', studentslist=studentslist)




@app.route('/classroom', methods = ['GET', 'POST'])
def classroom():
    studentslist = session.get('studentslist', None)
    if request.method == 'POST':
        classroom_x = request.form['classroomx']
        classroom_y = request.form['classroomy']
        if classroom_x.isdigit() == False or classroom_y.isdigit() == False:
            return render_template('classroom.html', alert="ERRO! Preencha X e Y com números")
        #check size of class
        if len(studentslist) > int(classroom_x) * int(classroom_y):
                return render_template('classroom.html', alert="ERRO! Há mais alunos do que lugares disponíveis!")
        session['room_cols'] = classroom_x
        session['room_rows'] = classroom_y

        return redirect(url_for('espelhodeclasse'))
    else:
        return render_template('classroom.html')

@app.route('/espelhodeclasse')
def espelhodeclasse():
    st_dict = session.get('st_dict', None)
    st_front = session.get('st_front', None)
    st_back = session.get('st_back', None)
    st_enemies = session.get('st_enemies', None)
    classroom_x = session.get('room_cols', None)
    classroom_y = session.get('room_rows', None)

    _to_list = final_classroom(st_dict, st_front, st_back, st_enemies, int(classroom_x), int(classroom_y))[0]
    warning = final_classroom(st_dict, st_front, st_back, st_enemies, int(classroom_x), int(classroom_y))[1]
    if warning == 'failed':
        return render_template('espelhodeclasse.html', classroom_x=int(classroom_x), classroom_y=int(classroom_y),_to_list=_to_list, warning=warning)
    else:
        return render_template('espelhodeclasse.html', classroom_x=int(classroom_x), classroom_y=int(classroom_y),
                               _to_list=_to_list)


@app.route('/classroomfinal')
def classroomfinal():
    st_dict = session.get('st_dict', None)
    st_front = session.get('st_front', None)
    st_back = session.get('st_back', None)
    st_enemies = session.get('st_enemies', None)
    classroom_x = session.get('room_cols', None)
    classroom_y = session.get('room_rows', None)

    _to_list = final_classroom(st_dict, st_front, st_back, st_enemies, int(classroom_x), int(classroom_y))[0]
    warning = final_classroom(st_dict, st_front, st_back, st_enemies, int(classroom_x), int(classroom_y))[1]
    if warning == 'failed':
        return render_template('classroomfinal.html', classroom_x=int(classroom_x), classroom_y=int(classroom_y),
                               _to_list=_to_list, warning=warning)
    else:
        return render_template('classroomfinal.html', classroom_x=int(classroom_x), classroom_y=int(classroom_y),
                               _to_list=_to_list)


if __name__ == '__main__':
    app.run(debug=True)

