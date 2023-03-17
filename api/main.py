import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prompt = ""
    split_length = ""
    file_data = []

    if request.method == "POST":
        prompt = request.form["prompt"]
        split_length = int(request.form["split_length"])

        file_data = split_text(prompt, split_length)

    return render_template("index.html", prompt=prompt, split_length=split_length, file_data=file_data)
            
def split_text(text, split_length):
    num_parts = -(-len(text) // split_length)
    file_data = []

    for i in range(num_parts):
        start = i * split_length
        end = min((i + 1) * split_length, len(text))

        if i == num_parts - 1:
            content = f'[START PART {i + 1}/{num_parts}]\n' + text[start:end] + f'\n[END PART {i + 1}/{num_parts}]'
            content += '\nALL PARTS SENT. Now you can continue processing the request.'
        else:
            content = f'Do not answer yet. This is just another part of the text I want to send you. Just receive and acknowledge as "Part {i + 1}/{num_parts} received" and wait for the next part.\n[START PART {i + 1}/{num_parts}]\n' + text[start:end] + f'\n[END PART {i + 1}/{num_parts}]'
            content += f'\nRemember not answering yet. Just acknowledge you received this part with the message "Part {i + 1}/{num_parts} received" and wait for the next part.'

        file_data.append({
            'name': f'split_{str(i + 1).zfill(3)}_of_{str(num_parts).zfill(3)}.txt',
            'content': content
        })

    return file_data