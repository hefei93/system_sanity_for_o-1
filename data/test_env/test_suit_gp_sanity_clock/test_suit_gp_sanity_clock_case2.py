'''
@author: wei,xiang
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from qrd_shared.mms.Mms import *



class test_suit_gp_sanity_clock_case2(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch clock
    Step2:New a clock and delete
    Verification: 
    ER1:phone number would display as URI
    ER2:DUT would go into Dialer"
    
    '''
    
    
    def test_case_main(self, case_results):
        
        global case_flag , TAG
        case_flag = False
        TAG = "Dev-ci cases: CLOCK "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """
        start_activity('com.android.deskclock','com.android.deskclock.DeskClock')
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
            phone.permission_allow()        
        if search_view_by_desc('Alarm'):
            click_imageview_by_desc('Alarm')
            sleep(3)
            click_button_by_id('fab')
            sleep(3)
            if search_text('OK'):
                click_textview_by_text('OK')
                sleep(5)
                if search_view_by_id('delete'):
                    log_test_framework("gp_sanity_clock_case2:", "New clock pass")
                    click_button_by_id('delete')
                    sleep(5)
                    if search_text('Alarm deleted') == True or search_view_by_id('delete') == False:
                        log_test_framework("gp_sanity_clock_case2:", "Delete clock pass")
                        case_flag = True
        if search_text('has stopped'):
            log_test_framework("gp_sanity_clock_case2:", "Popup has stopped")
            take_screenshot()
            click_textview_by_text('OK')
            sleep(2)        
        else:
            log_test_framework("gp_sanity_bt_case1:", "Launch bt fail")        
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
            
  
