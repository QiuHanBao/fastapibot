import os
import telebot
from telebot import types
import ast
import qrcode
from aligo import Aligo, Auth
from telethon import TelegramClient

from setting import base_path, datapath
from aliyunpan import blfile, dowlodfile
from local_file import get_files, del_file

TOKEN = "1725389645:AAFtB1HfUVaHV-knttR58Xc8nA4RcIVnB7k"
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)


def login(message):
    def show(qr_link: str):
        """自定义显示二维码"""
        # 1.将二维码链接转为图片
        qr_img = qrcode.make(qr_link)
        savepath = os.path.join(datapath, 'login.png')
        print("登录二维码在:", savepath)
        qr_img.save(savepath)
        with open(file=savepath, mode='rb') as f:
            bot.send_photo(chat_id=message.chat.id, photo=f, caption='扫描登录二维码', )

    auth = Auth(name='秋海星星', show=show)
    ali = Aligo(auth=auth)
    return ali


# 最简单的语法书写
@bot.message_handler(commands=["help", 'start'])
def help(message):
    bot.send_message(message.chat.id, "这是电报机器人,此机器人没有任何作用,也没有帮助")


@bot.message_handler(commands=["about"])
def about(message):
    bot.send_message(message.chat.id, "这个机器人是个测试机器人")


@bot.message_handler(commands=["file"])
def getfiles(message):
    bot.send_message(chat_id=message.chat.id, text='已下载文件列表', reply_markup=makeFilesKeyboard())


@bot.message_handler(commands=["driver"])
def get_drvier_files(message):
    global ali
    ali = login(message)
    bot.send_message(chat_id=message.chat.id, text='云盘文件', reply_markup=makeKeyboard())


def stock_request(message):
    '''
    运行函数,函数返回True,会继续执行主函数
    返回False终止执行,不返回数据
    '''
    request = len(message.text)
    if request > 7:
        return False
    else:
        return True


@bot.message_handler(func=stock_request)
def chat_message(message):
    print(message.content_type)
    print(message.text)
    if message.text == '音频':
        bot.send_message(message.chat.id, text='返回音频')
    elif message.text == '视频':
        bot.send_message(message.chat.id, text='返回视频')
        # vide = r'D:\project\herokuflaskweb\data\大理寺日志.S01E02.mp4'
        # vide_dir, vide_name = os.path.split(vide)
        # with open(vide, 'rb') as fp:
        #     bot.send_video(chat_id=message.chat.id, data=fp, caption=vide_name)
    elif message.text == '键盘' or message.text == 'jp':
        markup = types.ReplyKeyboardMarkup(row_width=3)
        itembtn1 = types.KeyboardButton('键盘')
        itembtn2 = types.KeyboardButton('取消键盘')
        itembtn3 = types.KeyboardButton('d')
        itembtn4 = types.KeyboardButton('keyboard')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        bot.send_message(chat_id=message.chat.id, text='已发送键盘', reply_markup=markup)
    elif message.text == '取消键盘':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(chat_id=message.chat.id, text='已经取消键盘', reply_markup=markup)
    else:
        # bot.send_message(chat_id=message.chat.id, text=',谢谢')
        bot.send_message(message.chat.id, message.text)


stringList = {"Name": "John", "Language": "Python", "API": "pyTelegramBotAPI"}
# pid, stringList = blfile()

delIcon = u"\u274C"
crossIcon = "下载"


# v[name,size,type,url,pid,fid]

def makeFilesKeyboard():
    markup = types.InlineKeyboardMarkup()
    file_list = get_files()
    for fname in file_list:
        markup.add(types.InlineKeyboardButton(text=fname, callback_data='fname'),
                   types.InlineKeyboardButton(text=delIcon, callback_data="del-" + fname))
    markup.add(types.InlineKeyboardButton(text='关闭', callback_data="close"))
    return markup


def makeKeyboard(id='root'):
    markup = types.InlineKeyboardMarkup()
    pid, stringList = blfile(ali, id)
    for k, v in stringList.items():
        markup.add(types.InlineKeyboardButton(text=v[0], callback_data="['v', '" + k + "']"),
                   types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + k + "']"))
    markup.add(types.InlineKeyboardButton(text='关闭', callback_data="close"),
               types.InlineKeyboardButton(text='返回上级', callback_data="['v', '" + pid + "']"))
    # markup.add(types.InlineKeyboardButton(text='返回上级', callback_data="['v', '" + pid + "']"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if (call.data.startswith("['v'")):
        print(f"call.data : {call.data} , type : {type(call.data)}")
        print(f"ast.literal_eval: {ast.literal_eval(call.data)} , type : {type(ast.literal_eval(call.data))}")
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[-1]
        # bot.answer_callback_query(callback_query_id=call.id,
        #                           show_alert=True,
        #                           text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="文件目录",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(keyFromCallBack),
                              parse_mode='HTML')
    if (call.data.startswith("['key'")):
        fname = dowlodfile(ali, ast.literal_eval(call.data)[-1])
        sendfile = os.path.join(datapath, fname)
        with open(sendfile, 'rb')as fp:
            bot.send_video(chat_id=call.message.chat.id, data=fp, caption=fname)
        bot.send_message(chat_id=call.message.chat.id, text=fname)
    if (call.data.startswith("close")):
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if (call.data.startswith("del")):
        del_fname = call.data.split('-')[-1]
        del_fname = os.path.join(datapath, del_fname)
        del_file(del_fname)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="已下载文件列表",
                              message_id=call.message.message_id,
                              reply_markup=makeFilesKeyboard(),
                              parse_mode='HTML')




if __name__ == "__main__":
    # server.run(host="0.0.0.0", port=8000)
    server.run(host="127.0.0.1", port=8000, debug=True)
