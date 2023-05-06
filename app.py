from flask import Flask, request, send_file, render_template
from io import BytesIO
from youtube import *
import uuid
import os


app = Flask("__main__")

yt = YouTube()

last_vid = ""


#@app.route("/download",methods=["GET","POST"])
def down(url:str):
    global last_vid
    print("last vid : "+last_vid)
    ###url = request.args["url"]
    try:
        os.remove(last_vid)
    except Exception as e:
        print(e)
    print(url)
    url=url.split("?")[0]
    #url = f"https://www.youtube.com/{url}"
    myuuid = str(uuid.uuid4())
    result,title = yt.download_video(url,myuuid)
    thumbnail = yt.get_thumbnail(url)
    last_vid = result
    print("result:::")
    print(result)
    if result:
        last_img = result
        return (result,title,thumbnail)
    else:
        return (None , None, None)
    
    
@app.route("/download",methods=["GET","POST"])
def download():
    print(request.values)
    print(request.form["inputUrl"])
    keyword = request.form["inputUrl"]
    if keyword:
        try:
            result,vid_id = down(keyword)
            return send_file(
                result,
                as_attachment=True,
                attachment_filename=f"{vid_id}.mp4",
                mimetype="video/mp4",
            )
        except Exception as e:
            print(e)
            return "Error"

    
@app.route("/home",methods=["GET","POST"])
def home():
    
    if request.method == 'POST':
        print(request.values)
        keyword = request.form["inputUrl"]
        print(keyword)
        if keyword:
            try:
                result,title,thumb = down(str(keyword))
                return render_template("index.html",video=[result,title,thumb])
                
            except Exception as e:
                print(e)
                return "Error"
    else:
        return render_template("index.html")
    return "Error2"
    


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4000,debug=True)