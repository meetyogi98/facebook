import os
import pandas as pd
from flask import Flask, render_template, Response, request, redirect, url_for
fb = pd.read_csv('fb_data.csv')

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/get_Post', methods=['GET','POST'])
def get_post():
    
    # show the form, it wasn't submitted
    return render_template('get_post.html')

@app.route("/get_post", methods=['POST'])
def get_post_fb():
	account = request.form.get('account')
	pages = request.form.get('pages')
	pages = int(pages)
	filename = request.form.get('filename')
	print(account,pages,filename)
	from facebook_scraper import get_posts
	post1 = get_posts(account,pages=pages, extra_info = True)
	fb = pd.DataFrame(post1)
	fb.to_csv(filename+'.csv')
	fb = pd.read_csv( filename +'.csv')
	print(fb)
	return render_template( 'get_post_output.html',tables=[fb.to_html()], titles=fb.columns.values);
 

@app.route('/specificdate', methods=['GET','POST'])
def specificDate():
    
    # show the form, it wasn't submitted
    return render_template('specificDate.html')

@app.route("/specificDate", methods=['POST'])
def get_post_of_specificDate():
	date1 = request.form.get('Date')
	#print('User input date is: ',date1)
	#print(type(date1))
	fb = pd.read_csv('fb_data.csv')
	x = fb[fb['Date'] == date1]
	#print(x)
	return render_template( 'specificDate.html',tables=[fb.to_html()], titles=fb.columns.values);

@app.route('/rangedate', methods=['GET','POST'])
def rangeDate():
    
    # show the form, it wasn't submitted
    return render_template('rangeDate.html')

@app.route("/rangeDate", methods=['POST'])
def get_post_from_to_date():
	start = request.form.get('Date1')
	end = request.form.get('Date2')
	print(start,end)
	fb = pd.read_csv('fb_data.csv')
	start = start.split('-')
	end = end.split('-')
	print(start,end)
	x = start[0]
	print(type(x))
	print(x)
	x = int(x)
	y = int(end[0])
	z = y+1
	print(x,y,z)
	b = pd.DataFrame()
	for y in range(x, z):
		y = str(y)
		date = y+'-'+start[1]+'-'+start[2]
		a = fb[fb['Date'] == date]
		b = b.append(a)
	return render_template( 'rangeDate.html',tables=[fb.to_html()], titles=fb.columns.values);

@app.route('/rangetime', methods=['GET','POST'])
def rangeTime():
    
    # show the form, it wasn't submitted
    return render_template('rangeTime.html')

@app.route("/rangeTime", methods=['POST'])
def get_post_from_to_time():
    t_start = request.form.get('Time1')
    t_end = request.form.get('Time2')
    date = request.form.get('Date')
    t_start = t_start.split(':')
    t_end = t_end.split(':')
    a = int(t_start[0])
    b = int(t_end[0]) + 1
    c = pd.DataFrame()
    for y in range(a,b):
        y = str(y)
        for x in range(0,60):
            if x<10:
                x = str(x)
                for z in range(0,60):
                    if z<10:    
                        z = str(z)
                        #print(y,':','0',x,':','0',x)
                        time = y+':'+'0'+x+':'+'0'+z
                        d = fb[(fb['Time'] == time) & (fb['Date'] == date)]
                        c = c.append(d)
                        #print(time)
                        #b = df[df['Time'] == y+':'+'x' & df['Date'] == 'date']
                    else:
                        x = str(x)
                        z = str(z)
                        #print(y,':',x,':',x)
                        time = y+':'+'0'+x+':'+z
                        d = fb[(fb['Time'] == time) & (fb['Date'] == date)]
                        c = c.append(d)
                        #print(time)
                        #b = df[df['Time'] == y+':'+'x' & df['Date'] == 'date']
            else:
                for z in range(0,60):
                    if z<10: 
                        x = str(x)
                        z = str(z)
                        #print(y,':','0',x,':','0',x)
                        time = y+':'+x+':'+'0'+z
                        d = fb[(fb['Time'] == time) & (fb['Date'] == date)]
                        c = c.append(d)
                        #print(time)
                        #b = df[df['Time'] == y+':'+'x' & df['Date'] == 'date']
                    else:
                        x = str(x)
                        z = str(z)
                        #print(y,':',x,':',x)
                        time = y+':'+x+':'+z
                        d = fb[(fb['Time'] == time) & (fb['Date'] == date)]
                        c = c.append(d)
                        #print(time)
                        #b = df[df['Time'] == y+':'+'x' & df['Date'] == 'date']
    return render_template( 'rangeTime.html',tables=[fb.to_html()], titles=fb.columns.values);

if __name__ == "__main__":
    app.run()
    
