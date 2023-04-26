import requests
import os
import subprocess
import time


class ControlNano:
    def __init__(self, nano_name, url):
        self._nano_name = nano_name
        self._url = url
        self._what_url = self._url + 'api/nano/' + self._nano_name
        self._show_dashboard_url = self._url + self._nano_name + '/show_dashboard'
        self._cmd_old = ''
        self._terminal_url = url + 'api/nano/' + nano_name + '/terminal'
        self._show_dashboard_url = url + 'api/nano/' + nano_name + '/show_dashboard'

    def what(self):
        return requests.get(self._what_url).json().get('what')

    def custom_cmd(self):
        _cmd = requests.get(self._terminal_url).json().get('custom_cmd')
        _old_cmd = ''
        if _cmd != _old_cmd and _cmd != None:
            os.system(_cmd)
            _suc_cmd = subprocess.run(_cmd, stdout=subprocess.PIPE, shell=True).stdout.decode()
            _err_cmd = subprocess.run(_cmd, stderr=subprocess.PIPE, shell=True).stderr.decode()
            result = _suc_cmd if _suc_cmd != '' else _err_cmd
            payload = {'custom_cmd_output': result, 'custom_cmd': _cmd}
            _old_cmd = _cmd
            requests.post(self._terminal_url, data=payload)

    def screenshot(self):
        _name = 'screenshot.png'
        _command = f'gnome-screenshot --file="{_name}"'
        subprocess.call(_command, shell=True)
        with open(_name, 'rb') as f:
            _image_data = f.read()
            _image = {'screenshot': _image_data}
            requests.post(self._what_url, files=_image)

    def show_dashboard(self):
        _dashboard_link = requests.get(self._show_dashboard_url).json().get('dashboard_link')
        with open('./Desktop/pageweb_redemarrage.sh', 'r') as test:
            lines = test.readlines()
        lines[lines.index('firefox\n') + 1] = _dashboard_link + '\n'
        with open('./Desktop/pageweb_redemarrage.sh', 'w') as test:
            test.writelines(lines)

        data = {'what': ''}
        requests.post(self._what_url, data)

    def reboot(self):
        requests.post(self._what_url, data={'what': ''})
        _reboot_cmd = 'sudo reboot'
        subprocess.run(_reboot_cmd, stdout=subprocess.PIPE, shell=True).stdout.decode()

    def show_video(self):
        print('show the video')
        data = {'what': ''}
        requests.post(self._what_url, data)

    def controls(self):
        while True:
            try:
                what = self.what()
                if what == 'show_video':
                    self.show_video()

                elif what == 'show_dashboard':
                    self.show_dashboard()

                elif what == 'reboot':
                    self.reboot()

                elif what == 'screenshot':
                    self.screenshot()

                elif what == 'custom_cmd':
                    self.custom_cmd()

                time.sleep(2)
            except:
                print('no')
                time.sleep(2)


























