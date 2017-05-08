'''
@author: hu_ch
'''

import fs_wrapper
import settings.common as SC
from case_utility import *
from logging_wrapper import log_test_case, save_fail_log, print_report_line
from test_case_base import TestCaseBase
from qrd_shared.case import *



class test_suit_system_sanity_contact_case14(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    """
    "Procedure:
    Step1:Launch contacts
    Step2:delete all contacts
    Verification: 
    ER1:contacts can be deleted successfully
    """
    '''
    
    
    def test_case_main(self, case_results):
        global case_flag , TAG,recoreName,p
        recordName=''.join(__name__.split('_')[-2:])     
        case_flag = False
        TAG = "delete all contacts: Contact "
        log_test_framework(TAG, self.name + " -Start")
        
        """
        cases contnets you need to add
        
        """
        settings.check_after_resetphone()
        p=subprocess.Popen('adb shell screenrecord /sdcard/%s.mp4'%recordName,shell=True)
        start_activity("com.android.contacts", "com.android.contacts.activities.PeopleActivity")
        sleep(10)
        phone.permission_allow()
        if search_text("All contacts") or search_text("ADD NEW ACCOUNT")or search_text("Contacts", searchFlag=TEXT_CONTAINS):
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Enter contact successfully")
            sleep(3)
        if contact.checkHasContact():
            log_test_framework(self.name, 'contact has contacts')
        else:
            contact.add_contact_to_phone("deall","123")
        contact.del_all_contact()              
        if search_text("deall")==False:
            log_test_case("concatct30", "Delete all contacts successfully")
            case_flag = True
        elif search_text("No contacts"):            
            log_test_case("concatct30", "Delete all contacts successfully")
            case_flag = True                  
        elif search_text("Unfortunately"):
            if search_text("OK"):
                click_button_by_text("OK")
            take_screenshot()
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs Crash")
            
        elif search_text("isn't responding"):
            if search_text("OK"):
                click_button_by_text("OK")
            take_screenshot()
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "Occurs ANR")
            
        else:
            take_screenshot()
            log_test_case(self.case_config_map[fs_wrapper.CASE_NAME_ATTR], "case fail")
        
        send_key(KEY_BACK)
        sleep(3)
        send_key(KEY_BACK)
        sleep(3)
        send_key(KEY_HOME)
        sleep(3)
        
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
