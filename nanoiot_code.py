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
        self._upgrade_url = url + 'api/nano/' + nano_name + '/upgrade'
        self._feedback = url + 'api/nano/' + nano_name + '/feedback'

    def what(self):
        try:
            what = requests.get(self._what_url, timeout=5).json().get('what')
            print('\n-----------------------success : waiting for action-----------------------\n')
            return what
        except requests.exceptions.ConnectionError:
            print("\n-----------------------couldn't get action-----------------------\n")

    def custom_cmd(self):
        _cmd = requests.get(self._terminal_url, timeout=5).json().get('custom_cmd')
        if _cmd is not None:
            try:
                print('A')
                process = subprocess.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                try:
                    stdout, stderr = process.communicate(timeout=5)
                    result = stdout.decode() if stdout.decode() != '' else stderr.decode()
                    result = result.replace('\n', '<br>')
                    payload = {'custom_cmd_output': result, 'custom_cmd': _cmd}
                except subprocess.TimeoutExpired:
                    process.kill()
                    payload = {'custom_cmd_output': 'Time out', 'custom_cmd': _cmd}
                    print('c')
            except Exception as e:
                print('D')
                payload = {'custom_cmd_output': 'Error: ' + str(e), 'custom_cmd': _cmd}
            requests.post(self._terminal_url, data=payload)
        else:
            print("Same command won't be executed")

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
        with open('/home/dm/Desktop/pageweb_redemarrage.sh', 'r') as test:
            lines = test.readlines()
        lines[lines.index('firefox\n') + 1] = _dashboard_link + '\n'
        with open('/home/dm/Desktop/pageweb_redemarrage.sh', 'w') as test:
            test.writelines(lines)
        print(f'dashboard: {_dashboard_link} will be shown after reboot')
        time_formated = time.ctime(time.time())
        requests.post(self._feedback,
                      data={'feedback': 'Shown dashboard is: ' + _dashboard_link, 'time': time_formated})
        data = {'what': ''}
        requests.post(self._what_url, data)

    def reboot(self):
        requests.post(self._what_url, data={'what': ''})
        _reboot_cmd = 'sudo reboot'
        time_formated = time.ctime(time.time())
        requests.post(self._feedback, data={'feedback': 'Reboot OK', 'time': time_formated})
        subprocess.run(_reboot_cmd, stdout=subprocess.PIPE, shell=True).stdout.decode()

    def show_video(self):
        data = {'what': ''}
        requests.post(self._what_url, data)
        command = f'firefox --kiosk {self._url}control/nano/uploaded-video/{self._nano_name}'
        terminal_cmd = ["gnome-terminal", "--", "bash", "-c", command]
        time_formated = time.ctime(time.time())
        requests.post(self._feedback, data={'feedback': 'Video is shown on NanoIoT', 'time': time_formated})
        subprocess.run(terminal_cmd)

    def change_resolution(self):
        _resolution = requests.get(self._change_resolution_url, timeout=5).json().get('resolution')
        _change_resolution_command = 'xrandr -s ' + _resolution
        subprocess.run(_change_resolution_command, stdout=subprocess.PIPE, shell=True).stdout.decode()
        print(_resolution)
        time_formated = time.ctime(time.time())
        data = {'what': ''}
        requests.post(self._feedback, data={'feedback': 'Resolution changed to: ' + _resolution, 'time': time_formated})
        requests.post(self._what_url, data)

    def upgrade(self):
        data = {'what': ''}
        requests.post(self._what_url, data)
        code = requests.get(self._upgrade_url, timeout=5).json().get('code')
        with open('/home/dm/Desktop/NanoIotController.py', "w+") as f:
            f.write(code)
        subprocess.call(['python3', '/home/dm/Desktop/nanoiot_control.py'])
        time_formated = time.ctime(time.time())
        requests.post(self._feedback, data={'feedback': 'Upgrade OK', 'time': time_formated})
        exit()

    def check(self):
        data = {'what': ''}
        time_formated = time.ctime(time.time())
        requests.post(self._feedback, data={'feedback': 'Checked', 'time': time_formated})
        requests.post(self._what_url, data)

    def controls(self):
        try:
            while True:
                what = self.what()
                if what == 'check':
                    print('check')
                    self.check()
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

                elif what == 'upgrade':
                    print('\ncommand: upgrade\n')
                    self.upgrade()

                elif what == '' or what is None:
                    print()
                else:
                    print('\n----unkown action----\n')

                time.sleep(2)
        except:
            time.sleep(7)
            data = {'what': ''}
            requests.post(self._what_url, data)
            subprocess.call(['python3', '/home/dm/Desktop/nanoiot_control.py'])

# updated-1
