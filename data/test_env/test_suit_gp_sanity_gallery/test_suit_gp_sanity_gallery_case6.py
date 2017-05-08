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



class test_suit_gp_sanity_gallery_case6(TestCaseBase):
    '''

    @see: L{TestCaseBase <TestCaseBase>}
    '''
    '''
    "Procedure:
    Step1:Launch camera
    Step2:check if the gallery can show the pics and videos correctly
    Verification: 
    ER1:phone number would display as URI
    ER2:DUT would go into Dialer"
    
    '''
    
    
    def test_case_main(self, case_results):
        global case_flag , TAG        
        case_flag = False
        TAG = "Dev-ci cases: Gallery "
        log_test_framework(TAG, self.name+" -Start")
        
        """
        
        cases contents you need to add
        
        
        """

        
        start_activity('org.codeaurora.snapcam','com.android.camera.CameraLauncher')
        if wait_for_fun(lambda:search_view_by_id('permission_allow_button'), True, 5):
            phone.permission_allow()
        if wait_for_fun(lambda:search_text('Yes'), True, 5):           
            click_textview_by_text('Yes')
        if wait_for_fun(lambda:search_text('OK'), True, 5):           
            click_textview_by_text('OK')        
        camera.take_panorama_picture()
        if wait_for_fun(lambda:search_view_by_id("preview_thumb"), True, 8):
            click_imageview_by_id("preview_thumb")
        if wait_for_fun(lambda:search_view_by_id("photopage_bottom_control_edit"), True, 5):
            click(1005, 84)
            if wait_for_fun(lambda:search_text("Details"), True, 5):
                click_textview_by_text("Details")
                if wait_for_fun(lambda:search_text("QCOM-AA", searchFlag=TEXT_CONTAINS), True, 5):
                    log_test_framework("gp_sanity_gallery_case6:", "maker information display QCOM-AA")
                    case_flag = True       
        elif search_text('has stopped'):
            log_test_framework("gp_sanity_gallery_case6:", "Popup has stopped")
            take_screenshot()
            click_textview_by_text('OK')
            sleep(2)
        elif search_text("isn't responding"):                
                take_screenshot()
                sleep(5)
                click_textview_by_text("OK")
                log_test_framework("gp_sanity_gallery_case6:", "ANR")
        else:
            log_test_framework("gp_sanity_gallery_case6:", "case fail")
        
        send_key(KEY_BACK)
        sleep(2)
        send_key(KEY_BACK)
        sleep(2)
        if wait_for_fun(lambda:search_view_by_id("shutter_button"), True, 5):
            click_imageview_by_id('camera_switcher')
            if wait_for_fun(lambda:search_view_by_desc("Switch to photo"), True, 5):
                click_imageview_by_desc('Switch to photo')
                sleep(2)        
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
            
  
