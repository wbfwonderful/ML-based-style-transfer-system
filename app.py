import shutil
import subprocess
from flask import Flask, render_template, send_from_directory, redirect, url_for, flash, session, request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import Length
from flask_wtf.file import FileRequired, FileAllowed
import os
import config
import re
app = Flask(__name__)
app.config.from_object(config)


# 定义用户上传表单
class UploaderFrom(FlaskForm):
    file = FileField('Upload images!', validators=[FileRequired(), FileAllowed(['jpg'])])
    style = StringField('style images')
    submit = SubmitField('Upload!')


# 首页
@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route('/style', methods=['GET', 'POST'])
def style_upload():
    # 新建表单
    form = UploaderFrom()
    # 如果有表单传入
    if form.validate_on_submit():
        # 获取表单中的数据
        f = form.file.data
        content_img = f.filename
        style_img = form.style.data

        # 保存上传的图片 这里保存到了IEContraAST/input/content/下
        f.save(os.path.join(os.path.join(os.getcwd(), 'IEContraAST', 'input', 'content'), content_img))

        # 将图片复制到 static文件夹下,便于显示
        shutil.copy(os.path.join(os.path.join(os.getcwd(), 'IEContraAST', 'input', 'content'), content_img),
                    os.path.join(os.path.join(os.getcwd(), 'static'), content_img))
        # redirect 重定向到 style 函数,也就是下面的路由函数
        return redirect(url_for('style', content_img=content_img, style_img=style_img))
    return render_template("style_upload.html", form=form)
    # 更改操作目录


# 接收文件名为参数
@app.route('/style/<path:content_img>')
def style(content_img):
    # 获取请求中的参数
    style_img = request.args.get("style_img")

    # 进入到模型的工作目录
    current_path = os.getcwd()
    os.chdir(os.path.join(current_path, "IEContraAST"))

    print(os.getcwd())
    # 这是调用模型的 python 命令,注意换行时要在每行的字符串末尾保留一个空格
    style_command = f"python Eval.py --content input/content/{content_img} " \
                    f"--style input/style/chinesepainting/{style_img} " \
                    f"--vgg model/chinesepainting/vgg_normalised.pth " \
                    f"--decoder model/chinesepainting/decoder_iter_160000.pth " \
                    f"--transform model/chinesepainting/transformer_iter_160000.pth " \
                    f"--output ../static"


    # 执行命令
    res = subprocess.getstatusoutput(style_command)
    # 这里是获取上面命令的输出并打印出来
    print(res.__str__())
    # 正则获取文件名
    c = re.findall('^(.*?).jpg', content_img)
    s = re.findall('^(.*?).jpg', style_img)

    stylized_filename = c[0] + "_stylized_" + s[0] + ".jpg"

    # 为 stylized_result 页面设置路径,
    url1 = url_for("static", filename=stylized_filename)
    url2 = url_for("static", filename=content_img)
    return render_template("result.html", url1=url1, url2=url2)


#
#
# @app.route('/destyle', methods=['GET', 'POST'])
# def destyle_upload():
#
#         return redirect(url_for('destyle', content_img=content_img, style_img=style_img))
#     return render_template("destyle_upload.html", form=form)
#     # 更改操作目录
#
# @app.route('/destyle/<path:content_img>')
# def destyle(content_img):
#
#     return render_template("result.html", url1=url1, url2=url2)
#

if __name__ == '__main__':
    app.run()



