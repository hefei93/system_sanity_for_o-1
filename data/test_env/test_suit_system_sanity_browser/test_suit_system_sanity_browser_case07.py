# coding=utf-8
'''
@author: c_wwan
for android O
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

class test_suit_system_sanity_browser_case07(TestCaseBase):
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
        TAG = 'Browser zoom in/out '
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
        openUrl('m.sohu.com')            
        sleep(5)
        enableForceenablezoom()

        zoom_by_param(ZOOM_DOWN)
        sleep(5)
        zoom_by_param(ZOOM_UP)
        case_flag=True
        
        enableForceenablezoom()
          
        if search_text('has stopped',searchFlag=TEXT_CONTAINS, isScrollable=0):
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
                    

    
    
