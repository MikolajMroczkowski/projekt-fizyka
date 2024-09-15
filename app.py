from flask import Flask, render_template, request

import electrical
import przemiana_izobaryczna
import magnetic


app = Flask(__name__, static_folder='assets',static_url_path='/assets')


@app.route('/')
def home():  # put application's code here
    return render_template('index.html')

@app.route('/poleMagnetyczne')
def calc_third():  # put application's code here
    return render_template('poleMagnetyczne.html', error='')


@app.route('/poleMagnetyczne/compute')
def calc_third_compute():  # put application's code here
    m = request.args.get('m')
    v = request.args.get('v')
    q = request.args.get('q')
    B = request.args.get('B')
    if m == '' or v == '' or q == '' or B == '':
        return render_template('poleMagnetyczne.html', error='Podaj wszystkie wartości')
    r, img = magnetic.compute(float(m), float(v), float(q), float(B))
    return render_template('poleMagnetyczneRes.html', error='', res=r, res_img=img)



@app.route('/obwodElektryczny')
def calc_second():  # put application's code here
    schema = electrical.schema_uri()
    return render_template('obwodElektryczny.html', error='', schema_uri=schema)


@app.route('/obwodElektryczny/compute')
def calc_second_compute():  # put application's code here

    e1 = request.args.get('e1')
    r1 = request.args.get('r1')
    e2 = request.args.get('e2')
    r2 = request.args.get('r2')
    R1 = request.args.get('R1')
    R2 = request.args.get('R2')
    if e1 == '' or r1 == '' or e2 == '' or r2 == '' or R1 == '' or R2 == '':
        schema = electrical.schema_uri()
        return render_template('obwodElektryczny.html', error='Podaj wszystkie wartości', schema_uri='')
    I, V = electrical.calculate(float(e1), float(r1), float(e2), float(r2), float(R1), float(R2))
    schema = electrical.schema_uri(e1, r1, e2, r2, R1, R2, round(I, 4), round(V, 4))
    return render_template('obwodElektrycznyRes.html', error='', schema_uri=schema, resA=round(I,4), resV=round(V,4))

@app.route('/przemianaIzobaryczna')
def calc_first():  # put application's code here
    return render_template('przemianaIzobaryczna.html', error='')


@app.route('/przemianaIzobaryczna/compute')
def calc_first_compute():  # put application's code here
    v_mode = request.args.get('vType')
    v2 = -1
    p = request.args.get('p')
    if v_mode == '0':
        v1_raw = request.args.get('v1')
        v2_raw = request.args.get('v2')
        v1_raw_multiplier = request.args.get('v1-multiple')
        v2_raw_multiplier = request.args.get('v2-multiple')
        if v1_raw == '' or v2_raw == '':
            return render_template('przemianaIzobaryczna.html', error='Podaj wartości V1 i V2')
        if v1_raw_multiplier == '' or v2_raw_multiplier == '':
            return render_template('przemianaIzobaryczna.html', error='Podaj wartości mnożnika V1 i V2')
        v1 = float(v1_raw) * float(v1_raw_multiplier)
        v2 = float(v2_raw) * float(v2_raw_multiplier)
    elif v_mode == '1':
        v_raw = request.args.get('v-connected')
        v_raw_multiplier = request.args.get('v-connected-multiple')
        if v_raw == '':
            return render_template('przemianaIzobaryczna.html', error='Podaj wartość V')
        if v_raw_multiplier == '':
            return render_template('przemianaIzobaryczna.html', error='Podaj wartość mnożnika V')
        v1 = float(v_raw) * float(v_raw_multiplier)
    else:
        return render_template('przemianaIzobaryczna.html', error='Wybierz sposób podania wartości V')
    if p == '':
        return render_template('przemianaIzobaryczna.html', error='Podaj wartość P')
    p_multiplier = request.args.get('p-multiple')
    if p_multiplier == '':
        return render_template('przemianaIzobaryczna.html', error='Podaj wartość mnożnika P')
    p = float(p) * float(p_multiplier)
    plot = False
    if v2==-1:
        res = przemiana_izobaryczna.calc(p, v=v1)
    else:
        res = przemiana_izobaryczna.calc(p, v1, v2)
        plot = przemiana_izobaryczna.plot_uri(p, v1, v2, p_multiplier=float(p_multiplier), v1_multiplier=float(request.args.get('v1-multiple')), v2_multiplier=float(request.args.get('v2-multiple')))
    return render_template('przemianaIzobarycznaRes.html', error='', res=res, plot_uri=plot)


#custom error page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

if __name__ == '__main__':
    app.run()

