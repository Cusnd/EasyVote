from flask import Flask, request, render_template_string, redirect
import json
import os

app = Flask(__name__)

# HTML 模板
survey_template = '''
<!doctype html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>问卷调查</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 20px;
            width: 400px;
            position: relative;
        }
        h2 {
            text-align: center;
        }
        input[type="submit"] {
            width: 100%;
            padding: 10px;
            background: #4caf50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background: #45a049;
        }
        .copyright {
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 12px;
            color: #888;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="copyright">Designed and Created By Liu Tong (Cusnd)</div>
        <h2>问卷调查</h2>
        <form method="POST" action="/submit">
            <label>1. 认为国家安全对个人的重要性：</label><br>
            <input type="radio" name="question1" value="A"> 十分重要<br>
            <input type="radio" name="question1" value="B"> 一般重要<br>
            <input type="radio" name="question1" value="C"> 不重要<br>
            <input type="radio" name="question1" value="D"> 与我无关<br><br>

            <label>2. 是否认为当前国家安全教育对增强公民的安全意识有帮助：</label><br>
            <input type="radio" name="question2" value="A"> 非常有帮助<br>
            <input type="radio" name="question2" value="B"> 有一定帮助<br>
            <input type="radio" name="question2" value="C"> 作用不大<br>
            <input type="radio" name="question2" value="D"> 与我无关<br><br>

            <label>3. 对国家安全形势的总体看法：</label><br>
            <input type="radio" name="question3" value="A"> 非常乐观<br>
            <input type="radio" name="question3" value="B"> 较为乐观<br>
            <input type="radio" name="question3" value="C"> 一般<br>
            <input type="radio" name="question3" value="D"> 较为担忧<br><br>

            <label>4. 认为普通公民在维护国家安全中应发挥什么作用：</label><br>
            <input type="checkbox" name="question4" value="A"> 主动参与国家安全宣传<br>
            <input type="checkbox" name="question4" value="B"> 及时举报可疑行为<br>
            <input type="checkbox" name="question4" value="C"> 提高自身安全意识<br>
            <input type="checkbox" name="question4" value="D"> 遵守法律法规<br>
            <input type="checkbox" name="question4" value="E"> 其他<br><br>

            <input type="submit" value="提交">
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(survey_template)

@app.route('/submit', methods=['POST'])
def submit():
    # 收集问卷结果
    result = {
        'question1': request.form.get('question1'),
        'question2': request.form.get('question2'),
        'question3': request.form.get('question3'),
        'question4': request.form.getlist('question4')
    }

    # 读取现有的结果
    try:
        with open('survey_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        results = {
            'question1': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
            'question2': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
            'question3': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
            'question4': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
        }

    # 更新结果统计
    if result['question1'] in results['question1']:
        results['question1'][result['question1']] += 1
    if result['question2'] in results['question2']:
        results['question2'][result['question2']] += 1
    if result['question3'] in results['question3']:
        results['question3'][result['question3']] += 1
    for answer in result['question4']:
        if answer in results['question4']:
            results['question4'][answer] += 1

    # 保存结果
    with open('survey_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    return redirect('/results')

@app.route('/results')
def results():
    # 读取存储的结果
    try:
        with open('survey_results.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        results = {
            'question1': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
            'question2': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
            'question3': {'A': 0, 'B': 0, 'C': 0, 'D': 0},
            'question4': {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0}
        }

    # 将结果显示在页面上
    return render_template_string('''
    <!doctype html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <title>投票结果</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f0f0f0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: rgba(255, 255, 255, 0.8);
                border-radius: 15px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                padding: 20px;
                width: 600px;
                position: relative;
            }
            h2, h3 {
                text-align: center;
            }
            p {
                font-size: 16px;
                margin: 10px 0;
            }
            a {
                display: block;
                text-align: center;
                margin-top: 20px;
                text-decoration: none;
                color: #4caf50;
                font-weight: bold;
            }
            a:hover {
                color: #388e3c;
            }
            .copyright {
                position: absolute;
                top: 10px;
                right: 10px;
                font-size: 12px;
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="copyright">Designed and Created By Liu Tong (Cusnd)</div>
            <h2>投票结果</h2>
            <h3>1. 认为国家安全对个人的重要性</h3>
            <p>A: {{ results['question1']['A'] }} 票</p>
            <p>B: {{ results['question1']['B'] }} 票</p>
            <p>C: {{ results['question1']['C'] }} 票</p>
            <p>D: {{ results['question1']['D'] }} 票</p>

            <h3>2. 当前国家安全教育对增强公民安全意识的帮助程度</h3>
            <p>A: {{ results['question2']['A'] }} 票</p>
            <p>B: {{ results['question2']['B'] }} 票</p>
            <p>C: {{ results['question2']['C'] }} 票</p>
            <p>D: {{ results['question2']['D'] }} 票</p>

            <h3>3. 对国家安全形势的总体看法</h3>
            <p>A: {{ results['question3']['A'] }} 票</p>
            <p>B: {{ results['question3']['B'] }} 票</p>
            <p>C: {{ results['question3']['C'] }} 票</p>
            <p>D: {{ results['question3']['D'] }} 票</p>

            <h3>4. 普通公民在维护国家安全中应发挥的作用</h3>
            <p>A: {{ results['question4']['A'] }} 票</p>
            <p>B: {{ results['question4']['B'] }} 票</p>
            <p>C: {{ results['question4']['C'] }} 票</p>
            <p>D: {{ results['question4']['D'] }} 票</p>
            <p>E: {{ results['question4']['E'] }} 票</p>

            <a href="/">返回问卷页面</a>
        </div>
    </body>
    </html>
    ''', results=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
