import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# ==========================================
# 1. 이메일 발송 설정
# ==========================================
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465 # SSL 포트

# 발신자 이메일 주소와 구글 앱 비밀번호를 입력하세요.
SENDER_EMAIL = 'npos1191004@gmail.com' 
SENDER_PASSWORD = 'wrnsscxxuuyjgqoj' # 구글 계정에서 발급받은 16자리 앱 비밀번호 (띄어쓰기 없이)

# 수신자 이메일 주소 목록 (여러 명일 경우 쉼표로 구분하여 추가)
RECEIVERS = [
    'yuntown203@naver.com',
]

# 이메일 제목
EMAIL_SUBJECT = '[뉴스레터] 오늘의 하남 지역 뉴스입니다.'

# 본문으로 사용할 HTML 파일 경로 (같은 폴더에 있다고 가정)
HTML_FILE_PATH = '하남지역뉴스_20260731.html'

def send_email():
    # 1. HTML 파일 읽기
    try:
        # 스크립트와 동일한 폴더에 있는 파일을 읽어옵니다.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, HTML_FILE_PATH)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ 오류: '{HTML_FILE_PATH}' 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return

    # 2. SMTP 서버 연결 및 로그인 (SSL 방식)
    print("⏳ 구글 이메일 서버에 연결 중...")
    try:
        smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("✅ 구글 서버 로그인 성공!")
    except Exception as e:
        print(f"❌ 로그인 실패 (이메일 주소나 앱 비밀번호를 확인하세요):\n{e}")
        return

    # 3. 각 수신자에게 메일 발송
    print("-" * 30)
    for receiver in RECEIVERS:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver

        # HTML 본문 추가
        part_html = MIMEText(html_content, 'html')
        msg.attach(part_html)

        try:
            smtp.sendmail(SENDER_EMAIL, receiver, msg.as_string())
            print(f"전송 성공 ➡️ {receiver}")
        except Exception as e:
            print(f"전송 실패 ❌ {receiver} (원인: {e})")

    # 4. 연결 종료
    smtp.quit()
    print("-" * 30)
    print("🎉 모든 메일 발송 작업이 완료되었습니다.")

if __name__ == '__main__':
    send_email()
