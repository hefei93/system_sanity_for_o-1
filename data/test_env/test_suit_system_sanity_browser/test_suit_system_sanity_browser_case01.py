# coding=utf-8
'''
@author: hu_ch
for android o
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from test_suit_system_sanity_browser import *
from urlparse import clear_cache
import os

class test_suit_system_sanity_browser_case01(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch browser
    Step2:open baidu
    Step3:clear browser history
    Verification: 
    ER1:history can clear successfully
    
    '''
    
    def test_case_main(self, case_results):
        global case_flag , TAG, recoreName,p     
        case_flag = False
        recordName=''.join(__name__.split('_')[-2:])      
        TAG = 'clear browser history '
        log_test_framework(TAG, self.name + " -Start")
        


        start_activity("com.android.browser", "org.chromium.chrome.browser.ChromeTabbedActivity")
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 15):
            phone.permission_allow()
        if wait_for_fun(lambda:search_view_by_id('terms_accept'), True, 15):            
            click_button_by_id('terms_accept')
            if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                click_button_by_id('next_button')
                if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                    click_button_by_id('next_button')
                    if wait_for_fun(lambda:search_view_by_id('next_button'), True, 5):
                        click_button_by_id('next_button')  
        self.openUrl('www.baidu.com','百度一下')
        case_flag=self.clear_browser_history()  
        if search_text('has stopped',searchFlag=TEXT_CONTAINS):
            log_test_framework("system_sanity_browser_case1:", "Popup has stopped")
            take_screenshot()
            click_textview_by_text('OK')
            sleep(2)      
            case_flag=False 
        
        for temp in range(4):
            send_key(KEY_BACK)
            if search_text('QUIT',searchFlag=TEXT_MATCHES,isScrollable=0):
                click_textview_by_text('QUIT')
                sleep(2)
            sleep(1)
        
        send_key(KEY_HOME)
        sleep(1) 
          
        if case_flag:
            qsst_log_case_status(STATUS_SUCCESS, "" , SEVERITY_HIGH)
        else:
            qsst_log_case_status(STATUS_FAILED, "", SEVERITY_HIGH)
        
        case_results.append((self.case_config_map[fs_wrapper.CASE_NAME_ATTR], case_flag))            
    
    def test_case_end(self):
        '''
        record the case result
        '''
        '''
        @attention: modify by min.sheng
        '''
        log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : end')
        if can_continue() and case_flag == True:
            # shutdown()
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ': case pass')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tpass')
        else:
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], TAG + ' : case fail')
            print_report_line(self.case_config_map[fs_wrapper.CASE_NAME_ATTR] + TAG + ' : \tfail')
            save_fail_log()
        p.terminate()
            
    def clear_browser_history(self):
        send_key(KEY_MENU)
        sleep(1)
        click_textview_by_text('History')
        sleep(3)
        x=getDisplayWidth()
        y=getDisplayHeight()
        click(int(x)/2, int(y)-80)
        sleep(5)
        click_textview_by_id('spinner')
        wait_for_fun(lambda:search_text('beginning of time'), True, 5)
        click_textview_by_text('beginning of time')
        click_textview_by_id("button_preference")
        sleep(4)
        if wait_for_fun(lambda:search_text('CLEAR',searchFlag=TEXT_MATCHES,isScrollable=0),True,3):
            click_textview_by_text('CLEAR')
            sleep(4)
        if not wait_for_fun(lambda:search_text('Search history',searchFlag=TEXT_MATCHES), True, 3):
            log_test_framework("system_sanity_browser_case1:", "Clear browser history pass")
            return True
        else:
            log_test_framework("system_sanity_browser_case1:", "Clear browser history fail")
            take_screenshot()
            return False

        
    def openUrl(self,httpurl='www.baidu.com',searchId='id/toolbar_shadow'):
        if search_view_by_id('url'):
            click_textview_by_id('url')
            sleep(3)
            send_key(KEY_DEL)
           # entertext_edittext_by_id('url','http://%s'%httpurl)
            os.system('adb shell input text http://%s'%httpurl)
            print 'adb shell input text http://%s'%httpurl
        elif search_view_by_id('url_bar'):
            click_textview_by_id('url_bar')
            sleep(3)
            send_key(KEY_DEL)
            #entertext_edittext_by_id('url_bar','http://%s'%httpurl)
            os.system('adb shell input text http://%s'%httpurl)
        sleep(5)
        send_key(KEY_ENTER)
        sleep(3)
        if wait_for_fun(lambda:search_view_by_id(searchId),True, 60) or wait_for_fun(lambda:search_text(searchId,isScrollable=0),True,60):
            log_test_framework(self.name, "OPen website pass")
            return True
        else:
            take_screenshot()
            return False
        
    
    