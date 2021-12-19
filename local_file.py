import os
import shutil

base_path = os.getcwd()
datapath = os.path.join(base_path, 'data')


def get_files():
    for root, dirs, files in os.walk(datapath):
        # print(root)
        # print(dirs)
        # print(files)
        pass
    return files
    # for file in files:
    #     # 获取文件所属目录
    #     # print(root)
    #     # 获取文件路径
    #     print(os.path.join(root, file))


def send_file(file):
    pass


def del_file(file):
    file = os.path.join(datapath, file)
    if os.path.exists(file):  # 如果文件存在
        # 删除文件，可使用以下两种方法。
        os.remove(file)  # 则删除
        # os.unlink(my_file)
        return True
    else:
        print('no such file:%s' % file)
        return False


if __name__ == '__main__':
    print(get_files())
