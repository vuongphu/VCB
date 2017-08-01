import requests
import os
import re
from cookielib import LWPCookieJar
import lxml.html
from captcha2upload import CaptchaUpload
import shutil
import json
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}
url_vcb = 'https://www.vietcombank.com.vn'
url_login = 'https://www.vietcombank.com.vn/IBanking2015/'
path_checknamein = '/ChuyenTien/TaiKhoan/CheckSoTaiKhoan'
path_detail_exchange = '/ThongTinTaiKhoan/TaiKhoan/ChiTietGiaoDich'
path_detail_info = '/ThongTinTaiKhoan/TaiKhoan/GetThongTinChiTiet'
path_send_money_step1 = '/ChuyenTien/TaiKhoan/Step1'
path_send_money_step2 = '/ChuyenTien/TaiKhoan/Step2'
path_send_money_step3 = '/ChuyenTien/TaiKhoan/Step3'
path_send_money = '/chuyentien/taikhoan/chuyentientronghethong'




class vbc_task():

    def __init__(self,user,password,name,api2captcha):

        self.s = requests.Session()
        self.s.headers.update(headers)
        self.user=user
        self.password=password
        self.name=name
        self.s.cookies = LWPCookieJar('cookiejar')
        self.captcha = CaptchaUpload((api2captcha))
        self.hash_session = ''
        self.RequestVerificationToken = ''
        self.TokenData = ''
        self.TaiKhoanTrichNo = ''
        self.MaLoaiTaiKhoanEncrypt = ''
        self.SoDuHienTai = ''
        self.LoaiTaiKhoan = ''
        self.LoaiTienTe = ''
        self.AID = ''
        self.HinhThucChuyenTien = ''
        self.SoDuTaiKhoanNguon = ''
        self.LINK_DETAIL = ''
        self.otpValidType = ''
        self.captcha_guid1 = ''
        self.RequestVerificationData = ''

    def vcb_login(self):
        try:
            r = self.s.get(url_login)

            if r.status_code == 200:
              
                content = r.text
                doc = lxml.html.fromstring(content)
                img_capchat = doc.xpath(
                    "//div[@class='img-captcha']/img/@src")[0]
                response = self.s.get(url_vcb + img_capchat, stream=True)
                with open('captcha.png', 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                captcha_id = doc.xpath(
                    "//input[@name='captcha-guid1']/@value")[0]
                captcha_sm = self.captcha.solve(out_file.name)
                data = {
                    'source': '',
                    'username': str(self.user),
                    'pass': str(self.password),
                    'captcha': str(captcha_sm),
                    'captcha-guid1': str(captcha_id),
                }
                r = self.s.post(r.url, data=data, allow_redirects=True)
                if r.status_code == 200:

                    
                    doc = lxml.html.fromstring(r.text)
                    self.hash_session = doc.xpath(
                        "//li[@class='home']/a/@href")[0]
                    self.RequestVerificationToken = doc.xpath(
                        "//input[@name='__RequestVerificationToken']/@value")[0]
                    self.LINK_DETAIL = doc.xpath(
                        "//a[@class='linkDetails icon-right']/@href")[0]
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def check_login(self):
        try:
            r = self.s.get(url_login)
            if r.status_code == 200:
                doc = lxml.html.fromstring(r.text)
                check = doc.xpath(
                    "//div[@class='dieuhuong dieuhuong-home']/span/span/text()")[0]
                self.hash_session = doc.xpath("//li[@class='home']/a/@href")[0]
                self.RequestVerificationToken = doc.xpath(
                    "//input[@name='__RequestVerificationToken']/@value")[0]
                self.LINK_DETAIL = doc.xpath(
                    "//a[@class='linkDetails icon-right']/@href")[0]
            else:
                return False
        except:
            return False
        if check == self.name:
            return True
        return False

    def data_detal(self, startdate, enddate):
        data = {
            'TokenData': str(self.TokenData),
            '__RequestVerificationToken': str(self.RequestVerificationToken),
            'TaiKhoanTrichNo': str(self.TaiKhoanTrichNo),
            'MaLoaiTaiKhoanEncrypt': str(self.MaLoaiTaiKhoanEncrypt),
            'SoDuHienTai': str(self.SoDuHienTai),
            'LoaiTaiKhoan': str(self.LoaiTaiKhoan),
            'LoaiTienTe': str(self.LoaiTienTe),
            'AID': str(self.AID),
            'NgayBatDauText': str(startdate),
            'NgayKetThucText': str(enddate),
        }
        return data

    def get_data_infor(self):
        try:
            r = self.s.get(url_vcb + self.LINK_DETAIL)
            if r.status_code == 200:
                doc = lxml.html.fromstring(r.text)
                self.RequestVerificationToken = doc.xpath(
                    "//input[@name='__RequestVerificationToken']/@value")[0]
                newstr = doc.xpath(
                    "//select[@id='TaiKhoanTrichNo']/option/@value")[0]
                self.TaiKhoanTrichNo = newstr
                self.MaLoaiTaiKhoanEncrypt = newstr.split('|')[1]
                self.AID = doc.xpath(
                    "//input[@name='AID']/@value")[0]
                data = self.data_detal('', '')
                # print data
                # sau khi lay data lan moi duoc lay tokendata
                # self.hash_session = doc.xpath("//li[@class='home']/a/@href")[0]

                r = self.s.post(url_vcb + self.hash_session.replace("ibanking2015", "IBanking2015") +
                           path_detail_info, data=data, allow_redirects=False)
                post_response = json.loads(r.text)
                # print post_response
                # print post_response['DanhSachTaiKhoan']
                self.SoDuHienTai = int(
                    post_response['DanhSachTaiKhoan'][0]['SoDuKhaDung'])
                self.LoaiTaiKhoan = post_response[
                    'DanhSachTaiKhoan'][0]['MaLoaiTaiKhoan']
                self.LoaiTienTe = post_response[
                    'DanhSachTaiKhoan'][0]['LoaiTienTe']
                self.TokenData = post_response['TokenData']
                return True
            else:
                return False
        except:
            return False

    def detail_exchange(self, startdate, enddate):
        if self.get_data_infor() == False:
            return False
        data = self.data_detal(startdate, enddate)
        try:
            r = self.s.post(url_vcb + self.hash_session + path_detail_exchange,
                       data=data, allow_redirects=False)
            if r.status_code == 200:
                post_response = json.loads(r.text)
                return post_response['ChiTietGiaoDich']
            else:
                return False
        except:
            return False

    def check_namein(self, accountnb):
        # dict_cookies= requests.utils.dict_from_cookiejar(s.cookies)
        # for d in dict_cookies :
        #     if regex.search(d):
        #         self.RequestVerificationToken=dict_cookies.get(d)
        data = {
            'SoTaiKhoan': str(accountnb),
            '__RequestVerificationToken': str(self.RequestVerificationToken),

        }
        try:
            r = self.s.post(url_vcb + self.hash_session +
                       path_checknamein, data=data, allow_redirects=False)
            if r.status_code == 200:
                post_response = json.loads(r.text)
                return post_response['TenChuKhoan']
            else:
                return False
        except:
            return False

    def data_send_money_step1(self, name_receiver, nb_receiver, amount, memo):
        data = {
            '__RequestVerificationToken': str(self.RequestVerificationToken),
            'HinhThucChuyenTien': str(self.HinhThucChuyenTien),
            'TaiKhoanTrichNo': str(self.TaiKhoanTrichNo.split('|')[0]),
            'SoDuTaiKhoanNguon': str(self.SoDuHienTai),
            'LoaiTienTaiKhoanNguon': str(self.LoaiTienTe),
            'SoTaiKhoanNguoiHuong': str(nb_receiver),
            'TenNguoiHuong': str(name_receiver),
            'LuuThongTinNguoiHuong': 'false',
            'TenGoiNho': '',
            'SoTien': str(amount),
            'LoaiTienChuyenKhoan': str(self.LoaiTienTe),
            'NoiDungThanhToan': str(memo),
            'ThuPhiNguoiChuyen': str(self.ThuPhiNguoiChuyen),
        }
        return data

    def send_money_step1(self, amount, nb_receiver, memo):
        try:
            self.HinhThucChuyenTien = 1
            self.ThuPhiNguoiChuyen = 2
            name_receiver = self.check_namein(nb_receiver)
            self.get_data_infor()
            data = self.data_send_money_step1(
                name_receiver, nb_receiver, amount, memo)
            r = self.s.post(url_vcb + self.hash_session.replace("ibanking2015",
                                                           "IBanking2015") + path_send_money_step1, data=data, allow_redirects=True)
            if r.status_code == 200:
                post_response = json.loads(r.text)
                if post_response['Status']['Error'] == False:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def data_send_money_step2(self, captcha_sm):
        data = {
            '__RequestVerificationToken': str(self.RequestVerificationToken),
            'otpValidType': str(self.otpValidType),
            'captcha-guid1': str(self.captcha_guid1),
            'otpCaptcha': str(captcha_sm),
        }

        return data

    def send_money_step2(self):
        try:
            self.otpValidType = 3
            r = self.s.get(url_vcb + self.hash_session +
                      path_send_money)
            doc = lxml.html.fromstring(r.text)
            self.captcha_guid1 = doc.xpath(
                "//input[@name='captcha-guid1']/@value")[0]
            img_capchat = doc.xpath("//img[@id='captchaImage']/@src")[0]
            response = self.s.get(url_vcb + img_capchat, stream=True)
            with open('captcha.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            captcha_sm = captcha.solve(out_file.name)
            data = self.data_send_money_step2(captcha_sm)
            r = self.s.post(url_vcb + self.hash_session.replace("ibanking2015", "IBanking2015") + path_send_money_step2,
                       data=data, allow_redirects=True)
            if r.status_code == 200:
                post_response = json.loads(r.text)
                if post_response['Status']['Error'] == False:
                    self.RequestVerificationData = post_response[
                        'Status']['ExtraData']
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def data_send_money_step3(self, MaGiaoDich):
        data = {
            '__RequestVerificationToken': str(self.RequestVerificationToken),
            '_RequestVerificationData': str(self.RequestVerificationData),
            'MaGiaoDich': str(MaGiaoDich),

        }

        return data

    def send_money_step3(self):
        #
        try:
            count = 0
            while True or count == 5:
                f = open("text.txt", "r")
                check = f.read()
                if check != '':
                    MaGiaoDich = check
                    break
                time.sleep(6)
                count = count + 1
            #   lay ma giao dich tu database
            data = self.data_send_money_step3(MaGiaoDich)
            r = self.s.post(url_vcb + self.hash_session.replace("ibanking2015", "IBanking2015") +
                       path_send_money_step3, data=data, allow_redirects=True)
            if r.status_code == 200:

                post_response = json.loads(r.text)
                if post_response['Error'] == False:
                    return True
                else:
                    return False
            else:
                return False
        except:
            return False

    def send_money(self, amount, nb_receiver, memo):
        if self.send_money_step1(amount, nb_receiver, memo) == True:
            print "Done Step 1"
            if self.send_money_step2() == True:
                print "Done Step 2"
                if self.send_money_step3() == True:
                    print "Done Step 3"
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def main(self):
        if not os.path.exists('cookiejar'):
            self.s.cookies.save()
        else:
            self.s.cookies.load(ignore_discard=True)
        if self.check_login() != True:
            print "New Login"
            if self.vcb_login() != True:
                print "Login Fail"
                return False
        self.s.cookies.save(ignore_discard=True)
        return True
