import logging
from flask import Flask, render_template, request, redirect, session, url_for
import math
from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color

app = Flask(__name__, static_url_path='', static_folder="./static")
app.template_folder = 'templates'
app.secret_key = 'your-secret-key'
app.config['TEMPLATES_AUTO_RELOAD'] = True  # 自动重新加载模板

# 配置日志
logging.basicConfig(filename='app.log', level=logging.DEBUG)

# 首页
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/end2', methods=['GET', 'POST'])
def end2():
    return render_template('caculate.html')


def lab_to_rgb(l, a, b):
    # 创建LabColor对象
    lab_color = LabColor(l, a, b)
    # 转换Lab到RGB
    rgb_color = convert_color(lab_color, sRGBColor)
    # 返回RGB元组
    return int(rgb_color.rgb_r * 255), int(rgb_color.rgb_g * 255), int(rgb_color.rgb_b * 255)


@app.route('/cacu', methods=['GET', 'POST'])
def cacu():
    if request.method == 'POST':
        # 获取表单数据
        P1 = float(request.form['P1'])
        P2 = float(request.form['P2'])
        G = float(request.form['G'])
        S = float(request.form['S'])

        #原色
        rgb_color0 = lab_to_rgb(P2, G, S)

        # 根据公式计算 白板的lab 值
        L1 = 0.97 + 1.19 * P1 + 0.83 * P2 - 0.05 * G - 0.04 * S
        a1 = 3.81 - 0.37 * P1 + 0.01 * P2 + 0.87 * G + 0.06 * S
        b1 = 11.40 - 0.40 * P1 + 0.02 * P2 + 0.11 * G + 0.90 * S

        rgb_color = lab_to_rgb(L1, a1, b1)

        # 根据公式计算 黑板板的lab 值
        L2 = 21.12 - 0.95 * P1 + 0.70 * P2 - 0.05 * G - 0.03 * S
        a2 = 1.08 - 0.84 * P1 + 0.01 * P2 + 0.76 * G + 0.03 * S
        b2 = 10.23 - 0.16 * P1 - 0.07 * P2 - 0.14 * G + 0.81 * S
        rgb_color2 = lab_to_rgb(L2, a2, b2)

        # 设置 Lab 值1 是否计算完成的标志
        lab_values_calculated = True

        return render_template('caculate.html', rgb_color0=rgb_color0, rgb_color=rgb_color, rgb_color2=rgb_color2, L1=L1, a1=a1, b1=b1, L2=L2,
                               a2=a2, b2=b2, lab_values_calculated=lab_values_calculated)


if __name__ == '__main__':
    app.run(debug=True)
