'''
@author: li,yazhou
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *
from test_suit_gp_sanity_contact import *

class test_suit_gp_sanity_contact_case17(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    
    def test_case_main(self, case_results):
        global case_flag , TAG
        case_flag = False        
        TAG = "Dev-ci cases: Contact "
        log_test_framework(self.name, " -Start")
        
        
        """
        cases contnets you need to add
        """
        
        def execute():  
            start_activity("com.android.contacts", "com.android.contacts.activities.PeopleActivity")
            if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 8):
                phone.permission_allow()
            if search_text("Next"):
                send_key(KEY_BACK)
                sleep(3)
            if wait_for_fun(lambda:search_text("All contacts"), True, 5) or search_text("ADD NEW ACCOUNT")or search_text("Contacts", searchFlag=TEXT_CONTAINS):
                log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Enter contact successfully")    			                     
                send_key(KEY_BACK)
                send_key(KEY_BACK)
                send_key(KEY_HOME)            
                if wait_for_fun(lambda:search_view_by_desc("Apps list"), True, 3):
                    log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Back to home successfully")
                    case_flag=True           
            elif search_text("Unfortunately"):                    
                take_screenshot()
                if search_text("OK"):
                    click_button_by_text("OK")
                    sleep(2)
                if search_text("Close"):
                    click_button_by_text("Close")
                    sleep(2)
                log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs Crash")
                
            elif search_text("isn't responding"):
                take_screenshot()
                if search_text("OK"):
                    click_button_by_text("OK")
                    sleep(2)
                if search_text("Close"):
                    click_button_by_text("Close")
                    sleep(2)
                log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR")
                
            else:
                take_screenshot()
                log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "case fail")

            return case_flag
        
        case_flag = repeat_cmcc_devci(execute)
        
        
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
    
