'''
@author: hu_ch
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from qrd_shared.mms.Mms import *
from test_suit_system_sanity_music import *


class test_suit_system_sanity_music_case01(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch music
    Step2:switch music in status bar
    Verification: 
    ER1:can control music in status bar"
    
    '''
    
    
    def test_case_main(self, case_results):
        global case_flag , TAG    ,recoreName,p 
        recordName=''.join(__name__.split('_')[-2:])    
        case_flag = False
        TAG = "Dev-ci cases: Music "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """

        
        
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity('com.android.music','com.android.music.MusicBrowserActivity')
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
            phone.permission_allow()             
        if wait_for_fun(lambda:search_view_by_id('search'), True, 5):
            log_test_framework("gp_sanity_music_case2:", "Launch music pass")  
        click_songtab('Albums') 
        click_songtab('Songs')         
        click_button_by_id('play_indicator')
        sleep(2)
        click_textview_by_text('Play')
        sleep(3)
        if search_text("recordings", searchFlag=TEXT_CONTAINS):
            log_test_framework("gp_sanity_music_case2:", "Play music pass")            
            case_flag = True                        
        elif search_text('has stopped'):
            log_test_framework("gp_sanity_music_case2:", "Popup has stopped")
            take_screenshot()
            click_textview_by_text('OK')
            sleep(2)         
        else:
            log_test_framework("gp_sanity_music_case2:", "Play music fail")
            take_screenshot()
        send_key(KEY_BACK)
        sleep(1)
        send_key(KEY_BACK)
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
  
