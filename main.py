from flask import Flask, render_template, request, jsonify
import xml.etree.ElementTree as ET
import os
import time
from flask_wtf.csrf import CSRFProtect

import aiml

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
csrf = CSRFProtect(app)

global k
k = aiml.Kernel()
k.learn("manzai_aiml.xml")

time.sleep(1)

@app.route("/")
def chat():
	# global k
	# k = aiml.Kernel()
	# k.learn("manzai_aiml.xml")
	return render_template('chat.html')

@app.route("/ask", methods=['POST'])
def ask():
	# メッセージを取得
	global k
	message = str(request.form['messageText'])

	while True:
		if message == "quit":
			exit()

		else:
			bot_response = k.respond(' '.join(list(message)))
			# チャットボットの返答を返す
			return jsonify({'status':'OK','answer':bot_response})

@app.route("/generator", methods=['POST'])
def generator():
	global k
	# メッセージを取得
	requestText = str(request.form['requestText'])
	responseText = str(request.form['responseText'])

	tree_ = ET.ElementTree(file="manzai_aiml.xml")
	root = tree_.getroot()

	category = ET.SubElement(root, 'category')
	pattern = ET.SubElement(category,'pattern')

	pattern.text = ' '.join(list(requestText))
	template=ET.SubElement(category,'template')

	template.text = responseText
	tree_.write("manzai_aiml.xml", encoding='utf-8', xml_declaration=True)

	time.sleep(1)

	k = aiml.Kernel()    
	k.learn("manzai_aiml.xml")

	return jsonify({'status':'OK','result':'言葉を覚えたよ。\nページを更新してね。\nOkay. AIML learned the language.\nPlease reload the page.'})

if __name__ == "__main__":
    #port = int(os.getenv("PORT"))
    app.run(host='0.0.0.0', port=5000, debug=True)
