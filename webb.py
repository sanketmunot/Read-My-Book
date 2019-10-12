import os
from flask import Flask,request, render_template, send_file
app = Flask(__name__)
@app.route('/action' , methods = ['GET','POST'])
def action():
    if request.method == 'POST':
        file=request.files['pic']
        email=request.form['email']
        filename=file.filename
        file.save(filename)
        import cv2
        import numpy as np

        img = cv2.imread(filename)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        cv2.imwrite("alpha.png", img);
        # ocr
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

        result = pytesseract.image_to_string(img)
        print(result)

        from gtts import gTTS
        myobj = gTTS(text=result, lang='en', slow=False)
        myobj.save("Book Audio.mp3")

        import yagmail

        yag = yagmail.SMTP('readmybook95@gmail.com', '********')  # (email,password)

        subject = '''Here's your audio'''
        body = ["Book Audio.mp3"]
        yag.send(to=email, subject=subject, contents=body)

        return render_template('home.html')

@app.route("/action2", methods = ['GET','POST'])
def action2():
    if request.method == 'POST':
        file=request.files['pic']

        filename=file.filename
        file.save(filename)
        import cv2
        import numpy as np

        img = cv2.imread(filename)
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)
        cv2.imwrite("alpha.png", img);


        # ocr
        import pytesseract
        pytesseract.pytesseract.tesseract_cmd = r"Tesseract-OCR\tesseract.exe"

        result = pytesseract.image_to_string(img)
        print(result)

        from gtts import gTTS
        myobj = gTTS(text=result, lang='en', slow=False)
        myobj.save("Book Audio.mp3")

        return send_file("Book Audio.mp3", mimetype='audio/mpeg')


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/contact/")
def contact():
    return render_template('contact.html')

@app.route("/contact/feedback" , methods = ['GET','POST'])
def feedback():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    city = request.form['city']
    subject = request.form['subject']
    body = [firstname,lastname,city,subject]
    import yagmail

    yag = yagmail.SMTP('readmybook95@gmail.com', 'read_1010')  # (email,password)

    yag.send(to='readmybook95@gmail.com', subject='feedack', contents=body)

    return render_template('home.html')



if __name__ == '__main__':
    app.run(host = '192.168.0.107',port=5005)
