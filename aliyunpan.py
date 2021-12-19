from aligo import Aligo, Auth
import qrcode
import os
from loguru import logger
import tempfile
from setting import datapath


def show(qr_link: str):
    """自定义显示二维码"""
    # 1.将二维码链接转为图片
    qr_img = qrcode.make(qr_link)
    savepath = os.path.join(datapath, 'login.png')
    print("登录二维码在:", savepath)
    qr_img.save(savepath)


def blfile(ali, fileid='root'):
    dic = {}
    pid = ali.get_file(fileid).parent_file_id
    if not pid:
        pid = 'root'
    flist = ali.get_file_list(fileid)
    for f in flist:
        dic[f.file_id] = [f.name, f.size, f.type, f.download_url, f.parent_file_id, f.file_id]
    return pid, dic


@logger.catch()
def dowlodfile(ali, fid):
    f = ali.get_file(fid)
    ali.download_file(local_folder=datapath, file_id=fid)
    logger.debug('下载完成')
    return f.name

# auth = Auth(name='秋海星星', show=show, level=logging.ERROR)
# auth = Auth(name='秋海星星', show=show)
# ali = Aligo(auth=auth)

# # blfile()
# # os.makedirs(os.path.dirname(filename), exist_ok=True)
# flist = ali.get_file_list()
# for f in flist:
#     print(f.name, f.file_id)
#     if f.name == '特别篇3-09.mp4':
#         dowlodfile(ali, fid=f.file_id)
# #         print('下载位置：',datapath)
# ali.download_file(local_folder=datapath, file_id='')
