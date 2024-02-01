import os


if __name__ == "__main__":
    '''
    用户运行init.bat，init.bat调用init_bat.py，init_bat.py获取主文件的绝对路径，并使用msedge打开
    '''
    # 获取当前脚本所在的目录
    current_directory = os.path.dirname(__file__)
    # 指定文件的相对路径
    file_relative_path = '../template/home.html'
    # 将文件相对路径与当前目录拼接，得到文件的绝对路径
    absolute_path = os.path.abspath(os.path.join(current_directory, file_relative_path))
    # 创建一个批处理脚本
    bat_script = f'''
    @REM pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    @echo off
    start  "" msedge {absolute_path}
    python app.py
    ''' 
    # 将批处理脚本写入文件
    with open('startup.bat', 'w') as file:
        file.write(bat_script)
