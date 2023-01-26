import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def verificationCode(email):
    try:
        my_mail = "beomwon@naver.com" # 나의 이메일 (보내는 사람 이메일 주소) ***
        pwd = "dlqjadnjs"  # 위의 이메일 계정 비밀번호 ***
        to_mail = email  # 받는 사람 이메일 주소 ***

        # 메일 제목/ 받는 사람/ 보내는 사람 정보
        msg = MIMEMultipart()
        msg['Subject'] = "(주)비바라비다 오슐랭 회원가입 인증번호"  # 이메일 제목 ***
        msg['From'] = my_mail
        msg['To'] = to_mail

        # 인증번호 생성
        code = ""
        for i in range(6):
            code += str(random.randint(0,9))

        # 본문 내용
        text = MIMEText(code) # 이메일 본문 ***
        msg.attach(text)

        # 이메일 전송
        smtp = smtplib.SMTP("smtp.naver.com", 587)
        smtp.starttls()
        smtp.login(user=my_mail, password=pwd)
        smtp.sendmail(my_mail, to_mail, msg.as_string())
        smtp.close()

        return code

    except:

        return 'error'

if __name__ == '__main__':
    # test
    code = verificationCode('de')
    print(code)