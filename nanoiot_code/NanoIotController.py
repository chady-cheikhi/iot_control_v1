import requests
import os
import subprocess
import time


class NanoIot:
    def __init__(self, nano_name, url):
        self._nano_name = nano_name
        self._url = url
        self._what_url = self._url + 'api/nano/' + self._nano_name
        self._show_dashboard_url = self._url + self._nano_name + '/show_dashboard'
        self._cmd_old = ''
        self._terminal_url = url + 'api/nano/' + nano_name + '/terminal'
        self._show_dashboard_url = url + 'api/nano/' + nano_name + '/show_dashboard'
        self._old_cmd = ''
        self._change_resolution_url = url + 'api/nano/' + nano_name + '/change_resolution'

    def what(self):
        try:
            what = requests.get(self._what_url, timeout=5).json().get('what')
            print('\n-----------------------success : waiting for action-----------------------\n')
            return what
        except requests.exceptions.ConnectionError:
            print("\n-----------------------couldn't get action-----------------------\n")

    def custom_cmd(self):
        _cmd = requests.get(self._terminal_url, timeout=5).json().get('custom_cmd')
        if _cmd != self._old_cmd and _cmd is not None:
            self._old_cmd = _cmd
            os.system(_cmd)
            _suc_cmd = subprocess.run(_cmd, stdout=subprocess.PIPE, shell=True).stdout.decode()
            _err_cmd = subprocess.run(_cmd, stderr=subprocess.PIPE, shell=True).stderr.decode()
            result = _suc_cmd if _suc_cmd != '' else _err_cmd
            result = result.replace('\n', '<br>')
            payload = {'custom_cmd_output': result, 'custom_cmd': _cmd}
            requests.post(self._terminal_url, data=payload)
        else:
            print("same command wouldn't be executed")

    def screenshot(self):
        _name = f'screenshot_{self._nano_name}.png'
        _command = f'gnome-screenshot --file={_name}'
        subprocess.call(_command, shell=True)
        with open(_name, 'rb') as f:
            _image_data = f.read()
            _image = {'screenshot': _image_data}
            _image_name = {'image_name': self._nano_name}
            requests.post(self._what_url, files=_image, data=_image_name)

    def show_dashboard(self):
        _dashboard_link = requests.get(self._show_dashboard_url, timeout=5).json().get('dashboard_link')
        with open('./Desktop/pageweb_redemarrage.sh', 'r') as test:
            lines = test.readlines()
        lines[lines.index('firefox\n') + 1] = _dashboard_link + '\n'
        with open('./Desktop/pageweb_redemarrage.sh', 'w') as test:
            test.writelines(lines)
        print(f'dashboard: {_dashboard_link} will be shown after reboot')
        data = {'what': ''}
        requests.post(self._what_url, data)

    def reboot(self):
        requests.post(self._what_url, data={'what': ''})
        _reboot_cmd = 'sudo reboot'
        subprocess.run(_reboot_cmd, stdout=subprocess.PIPE, shell=True).stdout.decode()

    def show_video(self):
        data = {'what': ''}
        requests.post(self._what_url, data)

    def change_resolution(self):
        _resolution = requests.get(self._change_resolution_url, timeout=5).json().get('resolution')
        _change_resolution_command = 'xrandr -s ' + _resolution
        subprocess.run(_change_resolution_command, stdout=subprocess.PIPE, shell=True).stdout.decode()
        print(_change_resolution_command)
        data = {'what': ''}
        requests.post(self._what_url, data)

    def controls(self):
        while True:
            what = self.what()
            if what == 'show_video':
                print('\ncommand: show_video\n')
                self.show_video()

            elif what == 'show_dashboard':
                print('\ncommand: show_dashboard\n')
                self.show_dashboard()

            elif what == 'reboot':
                print('\ncommand: reboot\n')
                self.reboot()

            elif what == 'screenshot':
                print('\ncommand: screenshot\n')
                self.screenshot()

            elif what == 'custom_cmd':
                print('\ncommand: custom_cmd\n')
                self.custom_cmd()

            elif what == 'change_resolution':
                print('\nchange resolution\n')
                self.change_resolution()

            elif what == '' or what is None:
                print()
            else:
                print('\n----unkown action----\n')

            time.sleep(2)





























