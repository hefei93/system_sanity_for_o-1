# coding=utf-8
'''

@author: hu_ch
for android N
@version:

'''
from utility_wrapper import *
import fs_wrapper
from test_suit_base import TestSuitBase
from case_utility import *
import re, datetime, shlex
from qrd_shared.case import *


CASE_PLUG_IN_FUNCTION_NAME = 'case_plug_in'
test_suit_config_map = {}
global_suit_config_map = {}
BOOL_STK_WIFI_CHECK = False
BOOL_STK_MOBILE_NETWORK_CHECK = False

laucher = Launcher()


class test_suit_system_sanity_browser(TestSuitBase):
    '''
    test_suit_ui_message is a class for browser suit.

    @see: L{TestSuitBase <TestSuitBase>}
    '''
    pass

URL_TITLE = {'百度':('www.baidu.com','百度一下'),
              '新浪':('sina.cn','手机新浪网'),
              '豌豆荚':('www.wandoujia.com','安卓手机娱乐第一入口-豌豆荚'),
              '百度视频':('m.video.baidu.com','精选_百度视频'),
              '百度音乐':('music.baidu.com','百度音乐-移动版'),
              '优酷':('www.youku.com','优酷-中国领先')}

def init_and_open_wifi(wifi_name='CIENET_3F', wifi_password= "cienet@aug2014"):
    '''
        @author: huchen
    '''
    start_activity("com.android.settings", ".Settings")
        # remove for UI change in AndroidL.
        #settings.whether_open_mobile_data(False)
    settings.enable_wifi(wifi_name, wifi_password) 
'''
    @attention: modify by min,sheng
    @see: init_and_open_wifi(wifi_name, wifi_password):
def init_and_open_wifi():
        start_activity("com.android.settings", ".Settings")
        # remove for UI change in AndroidL.
        #settings.whether_open_mobile_data(False)
        WIFI_NAME = 'Hydra'
        #WIFI_PASSWORD_SEQUENCE = ['k','num_sign','5','num_sign','x','num_sign','4','8','num_sign','caps','v','caps','z','num_sign','3']
        WIFI_PASSWORD_SEQUENCE = ['caps','k','num_sign','5','num_sign','x','num_sign','4','8','num_sign','caps','v','z','num_sign','3'] # this is for 8994, screen is 1600*2416
        settings.enable_wifi(WIFI_NAME, WIFI_PASSWORD_SEQUENCE)
'''
def stop_page():
    try:
        scroll_to_top()
        click_imageview_by_id('stop',isScrollable=0)
    except:pass
    
def exit_browser():
    sleep(2)
    
    close_other_tabs(left=0)    
    
def close_other_tabs(left=1):
    sleep(1)
    
    windowNum = get_view_text_by_id(VIEW_TEXT_VIEW, 'tab_switcher_text')
    windowNum = int(windowNum)
    
    if windowNum>left:
        click_imageview_by_id('tab_switcher')
        for i in range(windowNum-left):
            click_imageview_by_id('closetab')
        if left>0:click_imageview_by_id('tab_view') # now should be just 1 window in browser  
        
def clear_current_app():
    '''
    @author: add by min.sheng
    clear current application
    '''
    laucher.back_to_launcher()
    send_key(KEY_MENU)
    if is_view_enabled_by_id(VIEW_BUTTON, "recents_clear"):
        click_button_by_id("recents_clear",1,0)
    send_key(KEY_BACK)
    
def openUrl(httpurl='www.baidu.com',searchId='id/toolbar_shadow'):
    if search_view_by_id('url'):
        click_textview_by_id('url')
        sleep(3)
        send_key(KEY_DEL)
        #entertext_edittext_by_id('url','http://%s'%httpurl)
        os.system('adb shell input text http://%s'%httpurl)
    elif search_view_by_id('url_bar'):
        click_textview_by_id('url_bar')
        sleep(3)
        send_key(KEY_DEL)
        os.system('adb shell input text http://%s'%httpurl)
        #entertext_edittext_by_id('url_bar','http://%s'%httpurl)
    sleep(5)
    send_key(KEY_ENTER)
    sleep(3)
    if wait_for_fun(lambda:search_view_by_id(searchId),True, 60) or wait_for_fun(lambda:search_text(searchId,isScrollable=0),True,60):
        log_test_framework("system_sanity_browser_case2:", "OPen website pass")
        return True
    else:
        take_screenshot()
        return False
    
def openNotification():
    x=getDisplayWidth()
    y=getDisplayHeight()
    os.system('adb shell input swipe %s 0 %s %s 500'%((int(x)/2),(int(x)/2),(int(y)/2)))
    