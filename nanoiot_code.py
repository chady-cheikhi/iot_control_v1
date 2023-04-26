import requests
import os
import subprocess
import time

""" '/' important at the end of the link"""

nano_name = 'test'
what_url = 'http://192.168.56.1:8000/api/nano/' + nano_name
show_dashboard_url = 'http://192.168.56.1:8000/api/nano/' + nano_name + '/show_dashboard'
# status_url=
cmd_old = ''


def screenshot(name):
    command = f'gnome-screenshot --file="{name}"'
    subprocess.call(command, shell=True)
    with open(name, 'rb') as f:
        image_data = f.read()
        image = {'screenshot': image_data}
        # requests.post(what_url, data ={'status': 'done'})
    return image


def reboot():
    reboot_cmd = 'sudo reboot'
    suc_cmd = subprocess.run(reboot_cmd, stdout=subprocess.PIPE, shell=True).stdout.decode()


# requests.post(what_url, data ={'status': 'done'})


def custom_cmd(cmd):
    test = os.system(cmd)
    suc_cmd = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True).stdout.decode()
    err_cmd = subprocess.run(cmd, stderr=subprocess.PIPE, shell=True).stderr.decode()
    result = suc_cmd if suc_cmd != '' else err_cmd
    print(result)
    payload = {'custom_cmd_output': result, 'custom_cmd': cmd}
    return payload


def show_dashboard(link):
    print(link)
    with open('./Desktop/pageweb_redemarrage.sh', 'r') as test:
        lines = test.readlines()
    lines[lines.index('firefox\n') + 1] = link + '\n'
    with open('./Desktop/pageweb_redemarrage.sh', 'w') as test:
        test.writelines(lines)

    data = {'what': ''}
    requests.post(what_url, data)


def show_video():
    pass


while True:
    what = requests.get(what_url).json().get('what')
    print(what)
    if what == 'screenshot':
        screenshot_name = 'screenshot.png'
        image = screenshot(screenshot_name)
        requests.post(what_url, files=image)

    elif what == 'reboot':
        requests.post(what_url, data={'what': ''})
        reboot()
    elif what == 'custom_cmd':
        URL = 'http://192.168.56.1:8000/api/nano/' + nano_name + '/terminal'
        cmd = requests.get(URL).json().get('custom_cmd')
        print(cmd)
        if cmd != cmd_old and cmd != None:
            response = custom_cmd(cmd)
            print(response)
            cmd_old = cmd
            requests.post(URL, data=response)
        print('commmand not executed')

    elif what == 'show_dashboard':
        dashboard_link = requests.get(show_dashboard_url).json().get('dashboard_link')
        show_dashboard(dashboard_link)
    elif what == 'show_video':
        show_video()
        data = {'what': ''}
        requests.post(what_url, data)

    else:
        print('None of the above "whats"')
    time.sleep(2)










