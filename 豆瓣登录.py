import time, random
from PIL import Image
import requests, json, base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.request import urlretrieve
from selenium.webdriver.common.action_chains import ActionChains


class Douban():

    def __init__(self):
        self.url = "https://www.douban.com/"
        # 这里配置驱动参数，如增加代理和UA信息
        opt = webdriver.ChromeOptions()
        # 增加代理和UA信息
        # opt.add_argument('--proxy-server=http://223.96.90.216:8085')
        opt.add_argument(
            '--user-agent=' + "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
        # 创建webdriver实例
        self.driver = webdriver.Chrome()
        self._headers = {
            'Content-Type': 'application/json'
        }

    def base64_api(self, img, img2):
        time.sleep(2)
        # 图鉴官方提供的接口，这里稍微修改了下，因为自己使用就直接把账号密码放进去了
        with open(img, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64Bg = base64_data.decode()
        with open(img2, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64Slid = base64_data.decode()

        data = {"token": 'xRlc1FzftqaWOW4t-w-fA_IGcB3bfEeH_MHufK2Dos8', "type": 20111, "background_image": b64Bg, 'slide_image': b64Slid}
        resp = requests.post("http://api.jfbym.com/api/YmServer/customApi",  headers=self._headers, data=json.dumps(data))
        print(resp.text)
        # print(resp.json()['data']['data'])
        if resp.json()['code'] == 10000:
            return resp.json()['data']['data']
        else:
            return self.base64_api(img, img2)


    def input_username_password(self):
        # 实现访问主页，并输入用户名和密码
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.save_screenshot("reimgs/0.jpg")
        iframe = self.driver.find_element(By.TAG_NAME, 'iframe')  # 主代码在iframe里面，要先切进去
        self.driver.switch_to.frame(iframe)  # 切到内层
        time.sleep(0.5)
        self.driver.find_element(By.CLASS_NAME, 'account-tab-account').click()  # 模拟鼠标点击
        time.sleep(0.2)
        self.driver.find_element(By.ID, 'username').send_keys('15521168615')  # 模拟键盘输入
        time.sleep(0.1)
        self.driver.find_element(By.ID, 'password').send_keys('amsuperl123')  # 模拟键盘输入
        time.sleep(0.2)
        self.driver.find_element(By.CSS_SELECTOR, '.btn-account').click()

    def get_img(self):
        """
        获取验证码原图,并获得偏移量和偏移
        :return:
        """
        time.sleep(6)
        iframe = self.driver.find_element(By.TAG_NAME, 'iframe')  # 验证码仍然代码在iframe里面，要先切进去
        self.driver.switch_to.frame(iframe)  # 切到内层
        time.sleep(2)
        # 获取验证码图片
        style_slip = self.driver.find_element(By.XPATH, '//*[@id="tcOperation"]/div[8]').get_attribute('style')
        style_bg = self.driver.find_element(By.ID, 'slideBg').get_attribute('style')
        # 获取样式字符串，将该字符串转化为字典
        style_dict_bg = {i.split(':')[0]: i.split(':')[-1] for i in style_bg.split('; ')}
        style_dict_slip = {i.split(':')[0]: i.split(':')[-1] for i in style_slip.split('; ')}
        # 组装图片地址
        # src = "https://t.captcha.qq.com" + style_dict['background-image'][6:-2]
        src_bg = "https:" + style_dict_bg['background-image']
        src_slip = "https:" + style_dict_slip['background-image']
        print(src_bg)
        # 将图片下载到本地
        urlretrieve(src_bg, 'reimgs/douban_img1.png')
        urlretrieve(src_slip, 'reimgs/douban_img_slip.png')
        # 返回网页图片的宽和高
        print(style_dict_slip['background-size'][1:8])
        print(style_dict_slip['background-size'][11:18])
        return (eval(style_dict_bg['width'][1:-2]), eval(style_dict_bg['height'][1:-3]) - 35, eval(style_dict_slip['background-size'][1:8]), eval(style_dict_slip['background-size'][11:18]))

    def get_distance(self, a, b, c, d):
        # 实现图片缩放
        captcha = Image.open('reimgs/douban_img1.png')
        # x_scale = captcha.size[0] / a
        # y_scale = captcha.size[1] / b
        scale = 0.64
        (x, y) = captcha.size
        # x_resize = int(x / x_scale)
        # y_resize = int(y / y_scale)
        x_resize = int(x * scale)
        y_resize = int(y * scale)
        """
        Image.NEAREST ：低质量
        Image.BILINEAR：双线性
        Image.BICUBIC ：三次样条插值
        Image.ANTIALIAS：高质量
        """
        img = captcha.resize((x_resize, y_resize), Image.ANTIALIAS)
        img.save('reimgs/douban_img2.png')

        captcha = Image.open('reimgs/douban_img_slip.png')
        # x_scale = captcha.size[0] / c
        # y_scale = captcha.size[1] / d
        scale = 0.42
        (x, y) = captcha.size
        # x_resize = int(x / x_scale)
        # y_resize = int(y / y_scale)
        x_resize = int(x * scale)
        y_resize = int(y * scale)
        """
        Image.NEAREST ：低质量
        Image.BILINEAR：双线性
        Image.BICUBIC ：三次样条插值
        Image.ANTIALIAS：高质量
        """
        img = captcha.resize((x_resize, y_resize), Image.ANTIALIAS)
        img.save('reimgs/douban_img_slip2.png')


        time.sleep(0.5)
        # 使用云打码获取x轴偏移量
        distance = self.base64_api(img='reimgs/douban_img2.png', img2='reimgs/douban_img_slip2.png')
        return distance

    def get_track(self, distance):
        """
        计算滑块的移动轨迹
        """
        print(distance)
        # 通过观察发现滑块并不是从0开始移动，有一个初始值20.6845
        a = int((eval(distance) - 20.6845)/4)
        # a = int((eval(distance))/4)
        # 构造每次的滑动参数
        # 注意这里的负数作用：1.为了模拟人手，2.以上计算很多取了约数，最终结果存在误差，但误差往往在一定范围内，可以使用这些数值简单调整。
        track = [a, -2.1, a, -1.8, a, -1.5, a]
        return track

    def shake_mouse(self):
        """
        模拟人手释放鼠标抖动
        """
        ActionChains(self.driver).move_by_offset(xoffset=-0.4, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=0.6, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=-1.1, yoffset=0).perform()
        ActionChains(self.driver).move_by_offset(xoffset=0.9, yoffset=0).perform()

    def operate_slider(self, track):
        # 定位到拖动按钮
        slider_bt = self.driver.find_element(By.CLASS_NAME, 'tc-slider-normal')
        # 点击拖动按钮不放
        ActionChains(self.driver).click_and_hold(slider_bt).perform()
        # 按正向轨迹移动
        # move_by_offset函数是会延续上一步的结束的地方开始移动
        for i in track:
            ActionChains(self.driver).move_by_offset(xoffset=i, yoffset=0).perform()
            self.shake_mouse()  # 模拟人手抖动
            time.sleep(random.random() / 100)  # 每移动一次随机停顿0-1/100秒之间骗过了极验，通过率很高
        time.sleep(random.random())
        # 松开滑块按钮
        ActionChains(self.driver).release().perform()
        time.sleep(4)

    def login(self):
        """
        实现主要的登陆逻辑
        :param account:账号
        :param password: 密码
        :return:
        """
        self.input_username_password()
        time.sleep(0.5)
        # 下载图片，并获取网页图片的宽高
        a, b, c, d = self.get_img()
        print(a)
        print(b)
        print(c)
        print(d)
        # 计算滑块的移动轨迹,开始拖动滑块移动
        self.operate_slider(self.get_track(self.get_distance(a, b, c, d)))
        # 输出登陆之后的cookies
        print(self.driver.get_cookies())
        time.sleep(0.5)
        self.driver.save_screenshot("reimgs/douban.jpg")

    def __del__(self):
        """
        调用内建的稀构方法，在程序退出的时候自动调用
        类似的还可以在文件打开的时候调用close，数据库链接的断开
        """
        self.driver.quit()


if __name__ == "__main__":
    douban = Douban()  # 实例化
    douban.login()  # 之后调用登陆方法