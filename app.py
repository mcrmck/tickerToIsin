import csv
from flask import Flask, render_template, request, send_file, send_from_directory
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
from io import TextIOWrapper
import os

ticker_row = 0
country_row = 1
UPLOAD_FOLDER = 'uploads/'



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))




    with open('uploads/' + filename) as infile, open('static/master.csv') as masterfile:
        reader = csv.reader(infile)
        master = csv.reader(masterfile)
        checked = {}
        type =''
        for row in reader:
            print(row[ticker_row])
            if row[ticker_row] not in checked:
                print('here')
                if row[country_row] == '' or row[country_row] == 'Country':
                    country = ''
                else:
                    country = row[country_row]
                checked[row[ticker_row]] = ("",country)


        print(checked)
        for row in master:
            if row[1] in checked:
                if checked[row[1]][1] == row[5] or checked[row[1]][1] == '':
                    checked[row[1]] = row[2]

        for key, value in checked.items():
            if isinstance(value, tuple):
                checked[key] = ''



    with open('uploads/' + filename) as infile,open('converted_isin.csv', 'w') as outfile:
        outfile.truncate()
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            output_row = row
            output_row.append(checked.get(row[ticker_row]))
            writer.writerow(output_row)

    return send_file('converted_isin.csv', as_attachment=True)


if __name__ == '__main__':
    app.run()
