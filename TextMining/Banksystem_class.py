import datetime
import oracledb

def get_db_connection():
    try:
        conn = oracledb.connect(
            user="system",
            password="Manager1",
            dsn="localhost:1521/FREE"
        )
        return conn
    except oracledb.DatabaseError as e:
        print(f"Database connection error: {e}")
        return None

# [데이터 구조] 계좌 클래스
class Account:
    def __init__(self, acc_num, bank, balance, alias, owner_name):
        self.acc_num = acc_num
        self.bank = bank
        self.balance = balance
        self.alias = alias
        self.owner_name = owner_name # 요구사항: 계좌주명 포함
        self.history = []
        self.add_history(f"개설 입금: {balance}원")

    def add_history(self, detail):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.history.append(f"[{now}] {detail}")

# [데이터 구조] 유저 클래스
class User:
    def __init__(self, uid, upw, name, is_admin=False):
        self.uid = uid
        self.upw = upw
        self.name = name
        self.is_admin = is_admin
        self.accounts = []

# [메인 로직] 시스템 매니저
class BankSystem:
    def __init__(self):
        # 기본 관리자 계정 생성
        self.users = {'admin': User('admin', 'admin123', '관리자', True)}
        self.current_user = None

    def run(self):
        while True:
            if not self.current_user:
                print("\n=== 메인 메뉴 ===")
                print("1. 회원가입  2. 로그인  3. 종료")
                menu = input("선택: ")
                if menu == '1': self.register()
                elif menu == '2': self.login()
                elif menu == '3': break
            else:
                if self.current_user.is_admin:
                    self.admin_menu()
                else:
                    self.bank_menu()

    # --- 인증 기능 ---
    def register(self):
        uid = input("아이디: ")
        if uid in self.사용자: return print("이미 존재하는 아이디입니다.")
        upw = input("비밀번호: ")
        name = input("이름: ")
        self.사용자[uid] = User(uid, upw, name)
        print(f"{name}님, 회원가입을 축하합니다!")

    def login(self):
        uid = input("아이디: ")
        upw = input("비밀번호: ")
        if uid in self.사용자 및 self.사용자[uid].upw == upw:
            self.current_user = self.사용자[uid]
            print(f"로그인 성공! {self.current_user.name}님 환영합니다.")
        else:
            print("아이디 또는 비밀번호가 틀렸습니다.")

    # --- 일반 유저 메뉴 ---
    def bank_menu(self):
        print(f"\n=== 은행 메뉴 [{self.current_user.name}] ===")
        print("1. 계좌생성  2. 계좌조회  3. 입금/출금  4. 계좌이체")
        print("5. 정보수정/삭제  6. 검색  7. 거래내역  8. 로그아웃")
        menu = input("선택: ")

        if menu == '1': self.create_account()
        elif menu == '2': self.show_accounts()
        elif menu == '3': self.handle_money()
        elif menu == '4': self.transfer()
        elif menu == '5': self.manage_account()
        elif menu == '6': self.search_accounts()
        elif menu == '7': self.show_history()
        elif menu == '8': self.current_user = None

    # --- 계좌 기본 기능 ---
    def create_account(self):
        banks = ["하나은행", "우리은행", "국민은행", "신한은행", "기업은행"]
        print(f"지원 은행: {banks}")
        bank = input("은행명: ")
        if bank not in banks: return print("지원하지 않는 은행입니다.")
        
        acc_num = input("계좌번호: ")
        alias = input("계좌 별칭: ")
        try:
            money = int(input("최초 입금액(1000원 이상): "))
            if money < 1000: return print("최초 입금액은 1000원 이상이어야 합니다.")
        except ValueError: return print("숫자만 입력 가능합니다.")

        new_acc = Account(acc_num, bank, money, alias, self.current_user.name)
        self.current_user.accounts.append(new_acc)
        print(f"[{bank}] 계좌가 정상 등록되었습니다.")

    def show_accounts(self, target_list=None):
        accs = target_list if target_list is not None else self.current_user.accounts
        if not accs:
            print("해당하는 계좌가 없습니다.")
            return False
        for i, acc in enumerate(accs):
            print(f"{i+1}. [{acc.bank}] {acc.acc_num} | 별칭: {acc.alias} | 잔액: {acc.balance}원")
        return True

    def handle_money(self):
        if not self.show_accounts(): return
        try:
            idx = int(input("작업할 계좌 번호 선택: ")) - 1
            acc = self.current_user.accounts[idx]
            action = input("1. 입금  2. 출금: ")
            amount = int(input("금액: "))
            
            if amount <= 0: return print("0원 초과 금액만 가능합니다.")

            if action == '1':
                acc.balance += amount
                acc.add_history(f"입금: {amount}원")
                print("입금 완료.")
            elif action == '2':
                if acc.balance < amount: return print("잔액이 부족합니다.")
                acc.balance -= amount
                acc.add_history(f"출금: {amount}원")
                print("출금 완료.")
        except (ValueError, IndexError): print("잘못된 입력입니다.")

    def transfer(self):
        if not self.show_accounts(): return
        try:
            idx = int(input("출금할 내 계좌 선택: ")) - 1
            from_acc = self.current_user.accounts[idx]
            
            target_uid = input("이체할 상대방 ID: ")
            if target_uid not in self.사용자: return print("존재하지 않는 사용자입니다.")
            
            target_user = self.사용자[target_uid]
            print(f"--- {target_user.name}님의 계좌 목록 ---")
            for i, acc in enumerate(target_user.accounts):
                print(f"{i+1}. {acc.bank} ({acc.acc_num})")
            
            t_idx = int(input("이체받을 계좌 선택: ")) - 1
            to_acc = target_user.accounts[t_idx]
            
            amount = int(input("이체 금액: "))
            if amount <= 0: return print("0원 초과 금액만 이체 가능합니다.")
            if from_acc.balance < amount: return print("잔액 부족으로 이체가 취소됩니다.")

            # 원자적 처리 (출금 후 입금)
            from_acc.balance -= amount
            to_acc.balance += amount
            from_acc.add_history(f"이체 출금({to_acc.acc_num}): {amount}원")
            to_acc.add_history(f"이체 입금({from_acc.acc_num}): {amount}원")
            print("이체가 성공적으로 완료되었습니다.")
        except (ValueError, IndexError): print("이체 중 오류가 발생했습니다.")

    # --- 계좌 관리 (수정/삭제/검색) ---
    def manage_account(self):
        self.show_accounts()
        try:
            idx = int(input("수정/삭제할 계좌 선택: ")) - 1
            acc = self.current_user.accounts[idx]
            mode = input("1. 별칭 수정  2. 계좌 삭제: ")
            
            if mode == '1':
                new_alias = input("새 별칭: ")
                if any(a.alias == new_alias for a in self.current_user.accounts):
                    return print("이미 사용 중인 별칭입니다.")
                acc.alias = new_alias
                print("별칭이 수정되었습니다.")
            elif mode == '2':
                self.current_user.accounts.pop(idx)
                print("계좌가 삭제되었습니다.")
        except: print("잘못된 접근입니다.")

    def search_accounts(self):
        print("1. 별칭 검색  2. 계좌번호 검색  3. 은행별 검색")
        choice = input("선택: ")
        keyword = input("검색어 입력: ")
        
        results = []
        for acc in self.current_user.accounts:
            if choice == '1' 및 keyword in acc.alias: results.append(acc)
            elif choice == '2' 및 keyword in acc.acc_num: results.append(acc)
            elif choice == '3' 및 keyword in acc.bank: results.append(acc)
        
        self.show_accounts(results)

    def show_history(self):
        if not self.show_accounts(): return
        idx = int(input("조회할 계좌 선택: ")) - 1
        for h in self.current_user.accounts[idx].history:
            print(h)

# --- 관리자 기능 (수정/보완 버전) ---
    def admin_menu(self):
        print("\n" + "="*10 + " 관리자 모드 " + "="*10)
        print("1. 전체 사용자 목록 조회")
        print("2. 사용자 정보 수정 (이름/비밀번호)")
        print("3. 사용자 삭제")
        print("4. 로그아웃")
        menu = input("선택: ")

        if menu == '1':
            print("\n[전체 사용자 리스트]")
            if len(self.사용자) <= 1: # 관리자 본인 제외
                print("가입된 일반 사용자가 없습니다.")
            for uid, user in self.사용자.items():
                admin_tag = "[관리자]" if user.is_admin else "[일반]"
                print(f"{admin_tag} ID: {uid} | 이름: {user.name} | 비밀번호: {user.upw} | 계좌: {len(user.accounts)}개")

        elif menu == '2':
            uid = input("수정할 사용자 ID: ")
            if uid in self.사용자:
                target = self.사용자[uid]
                print(f"현재 정보 - 이름: {target.name}, 비밀번호: {target.upw}")
                new_name = input("새 이름 (변경 없으면 엔터): ")
                new_pw = input("새 비밀번호 (변경 없으면 엔터): ")
                
                if new_name: target.name = new_name
                if new_pw: target.upw = new_pw
                print(f"[{uid}] 사용자의 정보가 수정되었습니다.")
            else:
                print("존재하지 않는 사용자입니다.")

        elif menu == '3':
            uid = input("삭제할 사용자 ID: ")
            if uid == 'admin':
                print("관리자 계정은 삭제할 수 없습니다.")
            elif uid in self.사용자:
                del self.사용자[uid]
                print(f"[{uid}] 사용자가 시스템에서 삭제되었습니다.")
            else:
                print("존재하지 않는 사용자입니다.")

        elif menu == '4':
            self.current_user = None
            print("관리자 모드 종료.")
if __name__ == "__main__":

    BankSystem().run()
