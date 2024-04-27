import io
import random
import string
import subprocess
from contextlib import redirect_stdout

from pywebio import start_server
from pywebio.output import *
from pywebio.session import *


def get_code_output(height=None):
    """创建一个代码输出区，返回输出到该区域的回调函数"""
    rand_id = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    html = '<pre><code id="%s"></code></pre>' % rand_id
    style(put_html(html), 'height:%spx' % height if height else '')
    return lambda text: run_js('$("#%s").append(text)' % rand_id, text=str(text))

def main():
    put = get_code_output()
    put('Décodeur SARSAT\n')

    put = get_code_output(height=400)

    class WebIO(io.IOBase):
        def write(self, bytes):
            put(bytes)

    #with redirect_stdout(WebIO()):
        #print('test')

    # 支持脚本输出重定向
    process = subprocess.Popen("/root/Orangepi_Sarsat/406/scan406.pl 433.95M 433.95M", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            put('.')
            #break
        if output:
            put(output.decode('utf8'))

        #with use_scope('scrollable'):
        #    put_scrollable(output)
        #output.append(put_text('text\n' * 40))
        # hack: to scroll bottom
        #run_js('window.scrollTo(0,document.body.scrollHeight);')
        #run_js('$("#%s").scrollTo(0,document.body.scrollHeight);')

start_server(main, port=8080, debug=True)
